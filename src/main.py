import argparse
from core.parser import StringParser
from core.writer import StringWriter
from core.translator import Localizer

def main():
    parser = argparse.ArgumentParser(description='Localize Android or iOS strings')
    parser.add_argument('--platform', required=True, choices=['android', 'ios'])
    parser.add_argument('--source_file', required=True)
    parser.add_argument('--source_language_code', required=True)
    parser.add_argument('--target_language_code_list', required=True)
    parser.add_argument('--project_root', required=True)
    args = parser.parse_args()
    
    string_parser = StringParser(args.platform)
    string_writer = StringWriter(args.platform)
    translator = Localizer(args.source_language_code)
    
    entries = string_parser.parse(args.source_file)
    
    for target_lang in args.target_language_code_list.split('|'):
        translations = translator.translate_batch(entries, target_lang)
        string_writer.write(translations, target_lang, args.project_root)

if __name__ == '__main__':
    main() 