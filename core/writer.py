import xml.etree.ElementTree as ET
import os
from utils.io import ensure_dir
from config.constants import ANDROID_XML_INDENT

def write_translations(translations, platform, lang_code, project_root):
    if platform == "ios":
        output_dir = os.path.join(project_root, f"{lang_code}.lproj")
        ensure_dir(output_dir)
        _write_ios(translations, output_dir)
    else:
        output_dir = os.path.join(project_root, f"app/src/main/res/values-{lang_code}")
        ensure_dir(output_dir)
        _write_android(translations, output_dir)

def _write_ios(data, output_dir):
    path = os.path.join(output_dir, "Localizable.strings")
    with open(path, "w") as f:
        for item in data:
            f.write(f'"{item["key"]}" = "{item["translated"]}";\n')

def _write_android(data, output_dir):
    resources = ET.Element("resources") 
    for item in data:
        el = ET.SubElement(resources, "string", name=item["key"])
        el.text = item["translated"]

    tree = ET.ElementTree(resources) 
    ET.indent(tree, space=ANDROID_XML_INDENT, level=0)
    tree.write(os.path.join(output_dir, "strings.xml"), encoding="utf-8", xml_declaration=True)
