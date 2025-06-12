import argparse
from core.parser import StringParser
from core.writer import StringWriter
from core.translator import Localizer
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


def translate_language(args, target_lang, entries):
    """Translate entries for a single target language."""
    print(f"Translating to {target_lang}")
    translator = Localizer(args.source_language_code)
    translations = translator.translate_batch(entries, target_lang)
    string_writer = StringWriter(args.platform)
    string_writer.write_translations(translations, target_lang, args.project_root)
    return target_lang


def main():
    parser = argparse.ArgumentParser(description="Localize Android or iOS strings")
    parser.add_argument("--platform", required=True, choices=["android", "ios"])
    parser.add_argument("--source_file", required=True)
    parser.add_argument("--source_language_code", required=True)
    parser.add_argument("--target_language_code_list", required=True)
    parser.add_argument("--project_root", required=True)
    args = parser.parse_args()

    string_parser = StringParser(args.platform)
    entries = string_parser.parse(args.source_file)

    target_languages = args.target_language_code_list.split("|")

    # Determine number of workers (use all available cores)
    num_workers = min(len(target_languages), multiprocessing.cpu_count())

    # Process translations in parallel
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit translation tasks for each language
        futures = [
            executor.submit(translate_language, args, lang, entries)
            for lang in target_languages
        ]

        # Wait for all translations to complete
        for future in futures:
            try:
                completed_lang = future.result()
                print(f"Completed translation to {completed_lang}")
            except Exception as e:
                print(f"Error during translation: {str(e)}")


if __name__ == "__main__":
    main()
