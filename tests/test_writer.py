import pytest
import os
import tempfile
import xml.etree.ElementTree as ET
from core.writer import write_translations

@pytest.fixture
def test_translations():
    return [
        {"key": "welcome", "translated": "Bienvenido"},
        {"key": "hello", "translated": "Hola"}
    ]

@pytest.fixture
def test_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up test directory
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)

def test_write_ios(test_translations, test_dir):
    # Test iOS writing
    write_translations(test_translations, "ios", "es", test_dir)
    
    # Verify directory structure
    expected_dir = os.path.join(test_dir, "es.lproj")
    assert os.path.exists(expected_dir)
    
    # Verify file content
    file_path = os.path.join(expected_dir, "Localizable.strings")
    assert os.path.exists(file_path)
    
    with open(file_path, 'r') as f:
        content = f.read()
        assert '"welcome" = "Bienvenido";' in content
        assert '"hello" = "Hola";' in content

def test_write_android(test_translations, test_dir):
    # Test Android writing
    write_translations(test_translations, "android", "es", test_dir)
    
    # Verify directory structure
    expected_dir = os.path.join(test_dir, "app/src/main/res/values-es")
    assert os.path.exists(expected_dir)
    
    # Verify file content
    file_path = os.path.join(expected_dir, "strings.xml")
    assert os.path.exists(file_path)
    
    # Parse and verify XML content
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Verify XML structure
    assert root.tag == "resources"
    strings = root.findall("string")
    assert len(strings) == 2
    
    # Verify content
    translations_dict = {elem.get("name"): elem.text for elem in strings}
    assert translations_dict["welcome"] == "Bienvenido"
    assert translations_dict["hello"] == "Hola" 