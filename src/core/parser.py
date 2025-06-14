import xml.etree.ElementTree as ET
from typing import List, Dict
import re
from config.constants import PLATFORMS

class StringParser:
    def __init__(self, platform: str):
        self.platform = platform

    def parse(self, file_path: str) -> List[Dict[str, str]]:
        if self.platform not in PLATFORMS:
            raise ValueError(f"Invalid platform: {self.platform}. Must be either 'ios' or 'android'")
        if self.platform == "ios":
            return self._parse_ios_strings(file_path)
        return self._parse_android_strings(file_path)

    def _parse_android_strings(self, file_path: str) -> List[Dict[str, str]]:
        try:
            # Register the CDATA handler
            ET.register_namespace('', 'http://schemas.android.com/apk/res/android')
            
            # Parse with a custom parser that preserves CDATA
            parser = ET.XMLParser(encoding='utf-8')
            tree = ET.parse(file_path, parser=parser)
            root = tree.getroot()
            results = []

            for elem in root:
                if elem.tag == "string":
                    # Handle CDATA content
                    text = elem.text or ""
                    if elem.text and elem.text.strip().startswith("<![CDATA["):
                        text = text.replace("<![CDATA[", "").replace("]]>", "")
                    results.append({
                        "key": elem.attrib.get("name"),
                        "text": text.strip()
                    })
                elif elem.tag == "plurals":
                    items = []
                    for item in elem.findall("item"):
                        items.append({
                            "quantity": item.attrib.get("quantity"),
                            "text": (item.text or "").strip()
                        })
                    if items:
                        results.append({
                            "key": elem.attrib.get("name"),
                            "text": items[0]["text"]  # Use first item as default
                        })
                elif elem.tag == "string-array":
                    items = []
                    for item in elem.findall("item"):
                        items.append((item.text or "").strip())
                    if items:
                        results.append({
                            "key": elem.attrib.get("name"),
                            "text": items[0]  # Use first item as default
                        })
            print(results)
            return results
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing Android strings file: {str(e)}")

    def _parse_ios_strings(self, file_path: str) -> List[Dict[str, str]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.findall(r'"(.*?)"\s*=\s*"(.*?)";', content)
                return [{"key": k, "text": v} for k, v in matches]
        except Exception as e:
            raise ValueError(f"Error parsing iOS strings file: {str(e)}")