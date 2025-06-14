import os
import xml.etree.ElementTree as ET
from typing import List, Dict
from config.constants import ANDROID_XML_INDENT

class StringWriter:
    def __init__(self, platform: str):
        self.platform = platform

    def write(self, translations: List[Dict[str, str]], language: str, output_dir: str) -> None:
        if self.platform == 'android':
            self._write_android_strings(translations, language, output_dir)
        elif self.platform == 'ios':
            self._write_ios_strings(translations, language, output_dir)
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

    def _write_android_strings(self, translations: List[Dict], language: str, output_dir: str) -> None:
        dir_path = os.path.join(output_dir, f"app/src/main/res/values-{language}")
        os.makedirs(dir_path, exist_ok=True)

        root = ET.Element("resources")

        for entry in translations:
            entry_type = entry.get("type")

            if entry_type == "string":
                string_elem = ET.SubElement(root, "string")
                string_elem.set("name", entry["name"])
                string_elem.text = entry["text"]

            elif entry_type == "plurals":
                plural_elem = ET.SubElement(root, "plurals")
                plural_elem.set("name", entry["name"])
                for item in entry["items"]:
                    item_elem = ET.SubElement(plural_elem, "item")
                    item_elem.set("quantity", item["quantity"])
                    item_elem.text = item["text"]

            elif entry_type == "string-array":
                array_elem = ET.SubElement(root, "string-array")
                array_elem.set("name", entry["name"])
                for item_text in entry["items"]:
                    item_elem = ET.SubElement(array_elem, "item")
                    item_elem.text = item_text

        tree = ET.ElementTree(root)
        ET.indent(tree, space=ANDROID_XML_INDENT, level=0)
        file_path = os.path.join(dir_path, "strings.xml")
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

    def _write_ios_strings(self, translations: List[Dict[str, str]], language: str, output_dir: str) -> None:
        dir_path = os.path.join(output_dir, f"{language}.lproj")
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, "Localizable.strings")
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in translations:
                f.write(f'"{entry["key"]}" = "{entry["translated"]}";\n') 