import re
import xml.etree.ElementTree as ET
from config.constants import PLATFORMS

def parse_strings(file_path, platform):
    if platform not in PLATFORMS:
        raise ValueError(f"Invalid platform: {platform}. Must be either 'ios' or 'android'")
    if platform == "ios":
        return _parse_ios(file_path)
    return _parse_android(file_path)

def _parse_ios(path):
    with open(path, 'r') as f:
        content = f.read()
    matches = re.findall(r'"(.*?)"\s*=\s*"(.*?)";', content)
    return [{"key": k, "text": v} for k, v in matches]

def _parse_android(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return [{"key": elem.attrib["name"], "text": elem.text or ""} for elem in root.findall("string")]
