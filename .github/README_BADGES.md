# GitHub Actions Badge Templates

Add these badges to your README.md file to show the status of your workflows:

## Test Status Badge

```markdown
![Tests](https://github.com/arindamsaha1507/vyakarana/workflows/Tests%20and%20Coverage/badge.svg)
```

## Code Quality Badge

```markdown
![Code Quality](https://github.com/arindamsaha1507/vyakarana/workflows/Code%20Quality/badge.svg)
```

## Coverage Badge (requires codecov.io setup)

```markdown
[![codecov](https://codecov.io/gh/arindamsaha1507/vyakarana/branch/master/graph/badge.svg)](https://codecov.io/gh/arindamsaha1507/vyakarana)
```

## Python Version Badge

```markdown
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
```

## License Badge

```markdown
![License](https://img.shields.io/badge/license-MIT-green)
```

## Example README Section

Add this section to your README.md:

```markdown
## CI/CD Status

![Tests](https://github.com/arindamsaha1507/vyakarana/workflows/Tests%20and%20Coverage/badge.svg)
![Code Quality](https://github.com/arindamsaha1507/vyakarana/workflows/Code%20Quality/badge.svg)
[![codecov](https://codecov.io/gh/arindamsaha1507/vyakarana/branch/master/graph/badge.svg)](https://codecov.io/gh/arindamsaha1507/vyakarana)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
```

## Coverage Setup (Optional)

To enable code coverage reporting via Codecov:

1. Go to https://codecov.io/
2. Sign in with your GitHub account
3. Add your repository
4. The workflow will automatically upload coverage reports

No additional setup required - the workflow includes Codecov integration!
