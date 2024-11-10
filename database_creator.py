"""Module to create all the tables in the database."""

import multiprocessing
import json
import sqlite3
import pathlib

import pandas as pd


GANA_DICT = {
    1: "भ्वादिगण",
    2: "अदादिगण",
    3: "जुहोत्यादिगण",
    4: "दिवादिगण",
    5: "स्वादिगण",
    6: "तुदादिगण",
    7: "रुधादिगण",
    8: "तनादिगण",
    9: "क्र्यादिगण",
    10: "चुरादिगण",
}

LAKARA_DICT = {
    "lat": "लट्",
    "lit": "लिट्",
    "lut": "लुट्",
    "lrut": "लृट्",
    "lot": "लोट्",
    "lang": "लङ्",
    "vidhiling": "विधिलिङ्",
    "let": "लेट्",
    "ashirling": "आशीर्लिङ्",
    "lung": "लुङ्",
    "lrung": "लृङ्",
}

PRATYAYA_DICT = {
    "yangluk": "यङ्लुक्",
    "san": "सन्",
    "yang": "यङ्",
    "nich": "णिच्",
    "yak": "यक्",
    "-": "-",
}

PURUSHA_DICT = {
    "१": "प्रथमपुरुष",
    "२": "मध्यमपुरुष",
    "३": "उत्तमपुरुष",
}

VACHANA_DICT = {
    "१": "एकवचन",
    "२": "द्विवचन",
    "३": "बहुवचन",
}

PADA_DICT = {"a": "आत्मनेपदम्", "p": "परस्मैपदम्"}


def initiate_database() -> sqlite3.Connection:
    """Create the database and all the tables."""
    # Create the database
    conn = sqlite3.connect("database.db")

    return conn


def create_dhatu_table(conn: sqlite3.Connection):
    """Create the dhatu table."""

    json_file = pathlib.Path("dhatu/data.txt")

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)["data"]

    df = pd.DataFrame(data)

    # This is a complex column, we will handle it later
    df = df.drop(columns=["upasargas"])

    df.to_sql("dhatu", conn, if_exists="replace", index=False)


def create_dhaturupa(filename: pathlib.Path):
    """Create the dhaturupa table."""

    print(f"Creating table for {filename}")

    conn = sqlite3.connect("database.db")

    with filename.open(encoding="utf-8") as f:
        data: dict[str, dict] = json.load(f)

    basic_lakaras = list(data["01.0001"].keys())
    basic_lakaras = [lakara[1:] for lakara in basic_lakaras]

    lakaras = ["a" + lakara for lakara in basic_lakaras]
    lakaras += ["p" + lakara for lakara in basic_lakaras]

    for lakara in lakaras:
        table_name = filename.stem + "_" + lakara
        create_dhaturupa_table(data, conn, table_name, lakara)

    conn.close()


def create_dhaturupa_table(
    data: dict, conn: sqlite3.Connection, table_name: str, lakara: str
):
    """Create the dhaturupa table."""

    df = pd.DataFrame(
        columns=[
            "baseindex",
            "१.१",
            "१.२",
            "१.३",
            "२.१",
            "२.२",
            "२.३",
            "३.१",
            "३.२",
            "३.३",
        ]
    )
    for key, value in data.items():

        if lakara not in value:
            continue

        forms = value[lakara]

        if not forms:
            continue

        rupas = forms.split(";")

        if len(rupas) != 9:
            raise ValueError(
                f"Error in {key}: {forms}, len: {len(rupas)}, content: {rupas}"
            )

        row = {
            "baseindex": key,
            "१.१": rupas[0],
            "१.२": rupas[1],
            "१.३": rupas[2],
            "२.१": rupas[3],
            "२.२": rupas[4],
            "२.३": rupas[5],
            "३.१": rupas[6],
            "३.२": rupas[7],
            "३.३": rupas[8],
        }

        df.loc[len(df)] = row

    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Created table {table_name}")


def create_all_dhatu_related_tables():
    """Create all the tables related to dhatu."""

    conn = initiate_database()
    create_dhatu_table(conn)
    conn.close()

    files = pathlib.Path("dhatu").glob("*.txt")
    files = [
        file
        for file in files
        if file.name not in ["data.txt", "dhatuforms_krut.txt", "dhatuprayogas.txt"]
        and "vidyut" not in file.name
    ]

    with multiprocessing.Pool() as pool:
        pool.starmap(create_dhaturupa, [(file,) for file in files])


def add_verbs_to_database(
    row: dict[str, str], table: str, column_name: str, cursor: sqlite3.Cursor
):
    """Add the verbs to the database."""

    for word in row[column_name].split(","):

        purusha, vachana = column_name.split(".")

        parts = table.split("_")

        lakara = parts[-1]
        pada = lakara[0]
        lakara = lakara[1:]

        if len(parts) == 3:
            pratyaya = parts[1]
        else:
            pratyaya = "-"

        cursor.execute(
            "INSERT INTO verbs VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                word,
                row["baseindex"],
                LAKARA_DICT[lakara],
                PADA_DICT[pada],
                PRATYAYA_DICT[pratyaya],
                PURUSHA_DICT[purusha],
                VACHANA_DICT[vachana],
            ),
        )


def collect_all_verbs():
    """Collect all the verbs from the dhaturupa tables."""

    conn = sqlite3.connect("database.db")

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'dhatu_%'"
    ).fetchall()

    tables = [table[0] for table in tables]

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS verbs")

    cursor.execute(
        "CREATE TABLE verbs (verb TEXT, baseindex TEXT, lakara TEXT, pada TEXT, pratyaya TEXT, purusha TEXT, vachana TEXT)"  # pylint: disable=line-too-long
    )

    for table in tables:

        df = pd.read_sql(f"SELECT * FROM {table}", conn)

        for _, row in df.iterrows():
            for column in df.columns[1:]:
                if row[column]:
                    add_verbs_to_database(row, table, column, cursor)

    conn.commit()

    num_verbs = conn.execute("SELECT COUNT(*) FROM verbs").fetchone()[0]

    print(f"Finished collecting {num_verbs} verbs")

    conn.close()


def query_verb(verb: str):
    """Query the verb from the database."""

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM verbs WHERE verb = ?", (verb,))

    rows = cursor.fetchall()

    if not rows:
        print(f"Verb {verb} not found")
        return

    for row in rows:

        cursor.execute("SELECT * FROM dhatu WHERE baseindex = ?", (row[1],))
        dhatu = cursor.fetchone()
        gana = GANA_DICT[int(dhatu[1].split(".")[0])]

        string = f"{row[0]} इति धातुपाठस्य {dhatu[3]} {dhatu[8]} इति पाठात् {dhatu[2]} इति {gana}स्य धातोः "  # pylint: disable=line-too-long

        if row[4] == "-":
            string += "कर्तरि प्रयोगे "
        elif row[4] == "यक्":
            string += "भावकर्म्मणि प्रयोगे "
        else:
            string += f"{row[4]} प्रत्यये परे "

        string += f"{row[2]}-लकार-{row[5]}-{row[6]}-{row[3]} रूपम् ॥"

        print(string)

        print(row)
        print(dhatu)

    conn.close()


def parse_vachaspatyam():
    """Parse the vachaspatyam file."""

    filename = pathlib.Path("kosha").joinpath("vcp.json")

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS vachaspatyam")

    cursor.execute("CREATE TABLE vachaspatyam (word TEXT, gender TEXT, meaning TEXT)")

    # print(len(data["data"]["words"]))

    raw_words = data["data"]["words"]

    for word, refs in raw_words.items():
        for ref in refs.split(","):
            # print(word, ref)

            text = data["data"]["text"][ref]
            classification = text[0].split(" ")[1]

            if classification[-1] == "०":

                if classification == "पु०":
                    genders = ["पुंलिङ्गम्"]
                elif classification == "स्त्री०":
                    genders = ["स्त्रीलिङ्गम्"]
                elif classification == "न०":
                    genders = ["नपुंसकलिङ्गम्"]
                elif classification == "अव्य०":
                    genders = ["अव्ययम्"]
                elif classification == "त्रि०":
                    genders = ["पुंलिङ्गम्", "स्त्रीलिङ्गम्", "नपुंसकलिङ्गम्"]
                elif classification in ["पुंन", "अस्त्री"]:
                    genders = ["पुंलिङ्गम्", "नपुंसकलिङ्गम्"]
                else:
                    continue

                for gender in genders:

                    cursor.execute(
                        "INSERT INTO vachaspatyam VALUES (?, ?, ?)",
                        (word, gender, text[0]),
                    )

    conn.commit()

    conn.close()


def main():
    """Main function to create all the tables in the database."""
    # create_all_dhatu_related_tables()
    # collect_all_verbs()
    # query_verb("अस्मि")

    parse_vachaspatyam()


if __name__ == "__main__":
    main()
