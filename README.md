# Mobile AI Localizer

A GitHub Action for automated localization of Android and iOS string resources using AI translation.

## Features

- Supports both Android and iOS string resources
- Uses MarianMT models for high-quality translations
- Handles multiple target languages
- Preserves string formatting
- Maintains file structure
- Creates Pull Requests with translations

## Usage

### GitHub Action

```yaml
name: Localize Strings

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  localize:
    runs-on: ubuntu-latest
    steps:
      - name: Localize strings
        uses: GulerSevil/mobile_ai_localizer@v0.0.1
        with:
          platform: android
          source_file: app/src/main/res/values/strings.xml
          source_language_code: en
          target_language_code_list: es|fr|de
          project_root: ${{ github.workspace }}
          pr_title: "Update translations"
          pr_body: "This PR updates translations for Spanish, French, and German"
          gh_token: ${{ secrets.GITHUB_TOKEN }}
```

### Command Line

```bash
# First time setup
sh setup.sh

# Run localization
python main.py \
  --platform android \
  --source_file app/src/main/res/values/strings.xml \
  --source_language_code en \
  --target_language_code_list es|fr|de \
  --project_root .
```

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| platform | Yes | android | The platform to localize (android or ios) |
| source_file | Yes | - | Path to the source strings file |
| source_language_code | Yes | - | Source language code (e.g. en) |
| target_language_code_list | Yes | - | Pipe-separated list of target language codes (e.g. de\|fr\|tr) |
| project_root | Yes | ${{ github.workspace }} | Path to the project root |
| pr_title | No | "Update translations" | Title for the PR |
| pr_body | No | "This PR updates translations based on the latest changes." | Body for the PR |
| gh_token | Yes | - | GitHub token for creating PRs. Use `${{ secrets.GITHUB_TOKEN }}` for standard permissions or a custom token with appropriate permissions. |

## Output

### Android
```
${project_root}/app/src/main/res/
├── values/
│   └── strings.xml
├── values-es/
│   └── strings.xml
├── values-fr/
│   └── strings.xml
└── values-de/
    └── strings.xml
```

### iOS
```
${project_root}/
├── en.lproj/
│   └── Localizable.strings
├── es.lproj/
│   └── Localizable.strings
├── fr.lproj/
│   └── Localizable.strings
└── de.lproj/
    └── Localizable.strings
```

## Requirements

- Python 3.11+

## Development

1. Clone the repository
2. Run setup script: `sh setup.sh`
3. Run tests: `pytest`

## License

MIT License
