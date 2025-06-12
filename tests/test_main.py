import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock, call
import sys
from io import StringIO
from main import main

@pytest.fixture
def test_dir():
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "strings.xml")
    with open(source_file, 'w') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
        <resources>
            <string name="welcome">Welcome</string>
            <string name="hello">Hello</string>
        </resources>''')
    yield temp_dir
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)

@pytest.fixture
def mock_translator():
    with patch('main.Localizer') as mock:
        instance = MagicMock()
        mock.return_value = instance
        instance.translate_batch.return_value = [
            {"key": "welcome", "translated": "Bienvenido"}, 
            {"key": "hello", "translated": "Hola"}
        ]
        yield instance

@pytest.fixture
def mock_parser():
    with patch('main.parse_strings') as mock:
        mock.return_value = [
            {"key": "welcome", "text": "Welcome"},
            {"key": "hello", "text": "Hello"}
        ]
        yield mock

@pytest.fixture
def mock_writer():
    with patch('main.write_translations') as mock:
        yield mock

def test_main_success_with_one_target_language(test_dir, mock_parser, mock_translator, mock_writer):
    source_file = os.path.join(test_dir, "strings.xml")
    with patch('sys.argv', ['main.py', '--platform', 'android', '--source_file', source_file,
                           '--source_language_code', 'en', '--target_language_code_list', 'es',
                           '--project_root', test_dir]):
        main()
        mock_parser.assert_called_once_with(source_file, 'android')
        mock_translator.translate_batch.assert_called_once_with(
            mock_parser.return_value, 'es'
        )
        mock_writer.assert_called_once_with(
            mock_translator.translate_batch.return_value, 'android', 'es', test_dir
        )
    
def test_main_success_with_multiple_target_languages(test_dir, mock_parser, mock_translator, mock_writer):
    source_file = os.path.join(test_dir, "strings.xml")
    with patch('sys.argv', ['main.py', '--platform', 'android', '--source_file', source_file,
                           '--source_language_code', 'en', '--target_language_code_list', 'es|fr',
                           '--project_root', test_dir]):
        main()
        mock_translator.translate_batch.assert_has_calls([
            call(mock_parser.return_value, 'es'),
            call(mock_parser.return_value, 'fr')
        ])
        assert mock_writer.call_count == 2

def test_main_invalid_platform(test_dir):
    source_file = os.path.join(test_dir, "strings.xml")
    with patch('sys.argv', ['main.py', '--platform', 'invalid', '--source_file', source_file,
                           '--source_language_code', 'en', '--target_language_code_list', 'es',
                           '--project_root', test_dir]):
        with pytest.raises(SystemExit):
            main() 