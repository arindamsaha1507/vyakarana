"""Module to create all the tables in the database."""

import json
import sqlite3
import pathlib

import pandas as pd


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
    print(df.columns)

    # This is a complex column, we will handle it later
    df = df.drop(columns=["upasargas"])

    df.to_sql("dhatu", conn, if_exists="replace", index=False)


def create_dhaturupa(conn: sqlite3.Connection):
    """Create the dhaturupa table."""

    json_file = pathlib.Path("dhatu/dhatuforms.txt")

    with json_file.open(encoding="utf-8") as f:
        data: dict[str, dict] = json.load(f)

    lakaras = data["01.0001"].keys()

    for lakara in lakaras:
        table_name = f"dhaturupa_{lakara}"
        create_dhaturupa_table(data, conn, table_name, lakara)


def create_dhaturupa_table(
    data: dict, conn: sqlite3.Connection, table_name: str, lakara: str
):
    """Create the dhaturupa table."""

    df = pd.DataFrame(
        columns=[
            "baseindex",
            "prathamapurusasingular",
            "prathamapurusadual",
            "prathamapurusaplural",
            "madhyamapurusasingular",
            "madhyamapurusadual",
            "madhyamapurusaplural",
            "uttamapurusasingular",
            "uttamapurusadual",
            "uttamapurusaplural",
        ]
    )
    for key, value in data.items():
        # print(key, value)
        forms = value[lakara]
        if not forms:
            continue

        rupas = forms.split(";")

        if len(rupas) != 9:
            raise ValueError(f"Error in {key}: {forms}")

        row = {
            "baseindex": key,
            "prathamapurusasingular": rupas[0],
            "prathamapurusadual": rupas[1],
            "prathamapurusaplural": rupas[2],
            "madhyamapurusasingular": rupas[3],
            "madhyamapurusadual": rupas[4],
            "madhyamapurusaplural": rupas[5],
            "uttamapurusasingular": rupas[6],
            "uttamapurusadual": rupas[7],
            "uttamapurusaplural": rupas[8],
        }

        df.loc[len(df)] = row

    df.to_sql(table_name, conn, if_exists="replace", index=False)


def main():
    """Main function to create the database."""
    conn = initiate_database()
    create_dhatu_table(conn)
    create_dhaturupa(conn)
    conn.close()


if __name__ == "__main__":
    main()
