import pytest
import os
import tempfile
import xml.etree.ElementTree as ET
from core.parser import StringParser
from core.writer import StringWriter

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
    writer = StringWriter('ios')
    writer.write(test_translations, "es", test_dir)
    
    expected_dir = os.path.join(test_dir, "es.lproj")
    assert os.path.exists(expected_dir)
    
    file_path = os.path.join(expected_dir, "Localizable.strings")
    assert os.path.exists(file_path)
    
    with open(file_path, 'r') as f:
        content = f.read()
        assert '"welcome" = "Bienvenido";' in content
        assert '"hello" = "Hola";' in content

def test_write_android(test_translations, test_dir):
    writer = StringWriter('android')
    writer.write(test_translations, "es", test_dir)
    
    expected_dir = os.path.join(test_dir, "app/src/main/res/values-es")
    assert os.path.exists(expected_dir)
    
    file_path = os.path.join(expected_dir, "strings.xml")
    assert os.path.exists(file_path)
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    assert root.tag == "resources"
    strings = root.findall("string")
    assert len(strings) == 2
    
    translations_dict = {elem.get("name"): elem.text for elem in strings}
    assert translations_dict["welcome"] == "Bienvenido"
    assert translations_dict["hello"] == "Hola"

def test_read_ios(test_dir):
    content = '''"welcome" = "Welcome";
"hello" = "Hello";'''
    file_path = os.path.join(test_dir, "Localizable.strings")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    
    parser = StringParser('ios')
    entries = parser.parse(file_path)
    
    assert len(entries) == 2
    assert entries[0]['key'] == 'welcome'  # The parser should strip the quotes
    assert entries[0]['text'] == 'Welcome'
    assert entries[1]['key'] == 'hello'    # The parser should strip the quotes
    assert entries[1]['text'] == 'Hello'

def test_read_android(test_dir):
    content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="welcome">Welcome</string>
    <string name="hello">Hello</string>
</resources>'''
    file_path = os.path.join(test_dir, "strings.xml")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    
    parser = StringParser('android')
    entries = parser.parse(file_path)
    
    assert len(entries) == 2
    assert entries[0]['key'] == 'welcome'
    assert entries[0]['text'] == 'Welcome'
    assert entries[1]['key'] == 'hello'
    assert entries[1]['text'] == 'Hello'

def test_invalid_platform():
    with pytest.raises(ValueError, match="Unsupported platform"):
        writer = StringWriter('invalid')
        writer.write([], "es", "test_dir") 