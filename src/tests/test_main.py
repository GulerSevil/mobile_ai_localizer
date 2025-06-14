import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock, call
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
        yield mock

@pytest.fixture
def mock_parser():
    with patch('main.StringParser') as mock:
        instance = MagicMock()
        mock.return_value = instance
        instance.parse.return_value = [
            {"key": "welcome", "text": "Welcome"},
            {"key": "hello", "text": "Hello"}
        ]
        yield mock

@pytest.fixture
def mock_writer():
    with patch('main.StringWriter') as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield mock

def test_main_success_with_one_target_language(test_dir, mock_parser, mock_translator, mock_writer):
    source_file = os.path.join(test_dir, "strings.xml")
    with patch('sys.argv', ['main.py', '--platform', 'android', '--source_file', source_file,
                           '--source_language_code', 'en', '--target_language_code_list', 'es',
                           '--project_root', test_dir]):
        main()
        
        mock_parser.assert_called_once_with('android')
        mock_parser.return_value.parse.assert_called_once_with(source_file)
        
        mock_translator.assert_called_once_with('en')
        mock_translator.return_value.translate_batch.assert_called_once_with(
            mock_parser.return_value.parse.return_value, 'es'
        )
        
        mock_writer.assert_called_once_with('android')
        mock_writer.return_value.write.assert_called_once_with(
            mock_translator.return_value.translate_batch.return_value, 'es', test_dir
        )
    
def test_main_success_with_multiple_target_languages(test_dir, mock_parser, mock_translator, mock_writer):
    source_file = os.path.join(test_dir, "strings.xml")
    with patch('sys.argv', ['main.py', '--platform', 'android', '--source_file', source_file,
                           '--source_language_code', 'en', '--target_language_code_list', 'es|fr',
                           '--project_root', test_dir]):
        main()
        
        mock_parser.assert_called_once_with('android')
        mock_parser.return_value.parse.assert_called_once_with(source_file)
        
        mock_translator.assert_called_once_with('en')
        mock_translator.return_value.translate_batch.assert_has_calls([
            call(mock_parser.return_value.parse.return_value, 'es'),
            call(mock_parser.return_value.parse.return_value, 'fr')
        ])
        
        mock_writer.assert_called_once_with('android')
        assert mock_writer.return_value.write.call_count == 2
        mock_writer.return_value.write.assert_has_calls([
            call(mock_translator.return_value.translate_batch.return_value, 'es', test_dir),
            call(mock_translator.return_value.translate_batch.return_value, 'fr', test_dir)
        ])

def test_main_invalid_platform(test_dir):
    source_file = os.path.join(test_dir, "strings.xml")
    with patch('sys.argv', ['main.py', '--platform', 'invalid', '--source_file', source_file,
                           '--source_language_code', 'en', '--target_language_code_list', 'es',
                           '--project_root', test_dir]):
        with pytest.raises(SystemExit):
            main() 