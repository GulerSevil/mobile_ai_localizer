import xml.etree.ElementTree as ET
from typing import List, Dict
import re
from constants.constants import PLATFORMS
import os


class StringParser:
    def __init__(self, platform: str):
        self.platform = platform

    def parse(self, file_path: str) -> List[Dict[str, str]]:
        if self.platform not in PLATFORMS:
            raise ValueError(
                f"Invalid platform: {self.platform}. Must be either 'ios' or 'android'"
            )
        if self.platform == "ios":
            return self._parse_ios_strings(file_path)
        return self._parse_android_strings(file_path)

    def _parse_android_strings(self, file_path: str) -> List[Dict[str, str]]:
        print("Parsing Android strings")
        try:
            # Register the namespace
            ET.register_namespace("", "http://schemas.android.com/apk/res/android")

            # Parse the XML file
            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.parse(file_path, parser=parser)
            root = tree.getroot()
            results = []

            for elem in root:
                if elem.tag == "string":
                    results.append(
                        {
                            "name": elem.attrib.get("name"),
                            "text": elem.text or "",
                            "type": "string",
                        }
                    )
                elif elem.tag == "plurals":
                    items = []
                    for item in elem.findall("item"):
                        items.append(
                            {
                                "quantity": item.attrib.get("quantity"),
                                "text": item.text or "",
                            }
                        )
                    if items:
                        results.append(
                            {
                                "name": elem.attrib.get("name"),
                                "items": items,
                                "type": "plurals",
                            }
                        )
                elif elem.tag == "string-array":
                    items = []
                    for item in elem.findall("item"):
                        items.append(item.text or "")
                    if items:
                        results.append(
                            {
                                "name": elem.attrib.get("name"),
                                "items": items,
                                "type": "string-array",
                            }
                        )
            return results

        except ET.ParseError as e:
            raise ValueError(f"Invalid XML file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing Android strings file: {str(e)}")

    def _parse_ios_strings(self, file_path: str) -> List[Dict[str, str]]:
        try:
            print(f"Attempting to read iOS strings file from: {os.path.abspath(file_path)}")
            
            if not os.path.exists(file_path):
                print(f"File not found at: {file_path}")
                raise FileNotFoundError(f"iOS strings file not found at: {file_path}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    print("Warning: File content is empty or contains only whitespace")
                    return []
                
                # Remove comments
                content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Remove /* */ comments
                content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)  # Remove // comments
                
                pattern = r'"((?:[^"\\]|\\.)*)"\s*=\s*"((?:[^"\\]|\\.)*)";'
                matches = re.findall(pattern, content)
                
                results = []
                for key, value in matches:
                    key = key.encode().decode('unicode_escape')
                    value = value.encode().decode('unicode_escape')
                    results.append({"key": key, "translated": value})
                
                return results
                
        except Exception as e:
            print(f"Error details: {str(e)}")
            raise ValueError(f"Error parsing iOS strings file: {str(e)}")
