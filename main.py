import argparse
from core.parser import parse_strings
from core.translator import Localizer
from core.writer import write_translations

def main():
    parser = argparse.ArgumentParser(description="AI Localizer")
    parser.add_argument("--platform", choices=["android", "ios"], required=True)
    parser.add_argument("--source_file", required=True)
    parser.add_argument("--source_language_code", required=True)
    parser.add_argument("--target_language_code_list", required=True)
    parser.add_argument("--project_root", required=True)
    args = parser.parse_args()

    entries = parse_strings(args.source_file, args.platform)
    target_langs = args.target_language_code_list.split("|")

    translator = Localizer(args.source_language_code)
    for lang in target_langs:
        translated = translator.translate_batch(entries, lang)
        write_translations(translated, args.platform, lang, args.project_root)

if __name__ == "__main__":
    main()