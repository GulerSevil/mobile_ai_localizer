# AI Localizer

A GitHub Action for automated localization of Android and iOS string resources using AI translation.

## Features

- Supports both Android (`strings.xml`) and iOS (`Localizable.strings`) string resources
- Uses MarianMT models for high-quality translations
- Handles multiple target languages in a single run
- Preserves string formatting and special characters
- Maintains the original file structure and naming conventions

## Usage

### GitHub Action

```yaml
- name: Localize Strings
  uses: your-username/ai_localizer@v1
  with:
    platform: 'android'  # or 'ios'
    source_file: 'app/src/main/res/values/strings.xml'  # path to source strings file
    source_language_code: 'en'  # source language code
    target_language_code_list: 'es|fr|de'  # pipe-separated list of target languages
    project_root: '.'  # root directory of your project
```

### Command Line

```bash
python main.py \
  --platform android \
  --source_file app/src/main/res/values/strings.xml \
  --source_language_code en \
  --target_language_code_list "es|fr|de" \
  --project_root .
```

## Input Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `platform` | Target platform: `android` or `ios` | Yes |
| `source_file` | Path to the source strings file | Yes |
| `source_language_code` | Source language code (e.g., 'en') | Yes |
| `target_language_code_list` | Pipe-separated list of target languages (e.g., 'es\|fr\|de') | Yes |
| `project_root` | Root directory of your project | Yes |

## Output

For Android:
- Creates `values-{lang}` directories in `app/src/main/res/`
- Generates `strings.xml` files with translated strings

For iOS:
- Creates `{lang}.lproj` directories
- Generates `Localizable.strings` files with translated strings

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License
