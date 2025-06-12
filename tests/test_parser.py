import pytest
import os
import tempfile
from core.parser import parse_strings

@pytest.fixture
def ios_file():
    content = '''
    "welcome_message" = "Welcome to our app!";
    "settings_title" = "Settings";
    "cancel_button" = "Cancel";
    '''
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        f.close()
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def android_file():
    content = '''<?xml version="1.0" encoding="utf-8"?>
    <resources>
        <string name="welcome_message">Welcome to our app!</string>
        <string name="settings_title">Settings</string>
        <string name="cancel_button">Cancel</string>
    </resources>
    '''
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        f.close()
    yield f.name
    os.unlink(f.name)

def test_parse_ios(ios_file):
    result = parse_strings(ios_file, "ios")
    expected = [
        {"key": "welcome_message", "text": "Welcome to our app!"},
        {"key": "settings_title", "text": "Settings"},
        {"key": "cancel_button", "text": "Cancel"}
    ]
    assert result == expected

def test_parse_android(android_file):
    result = parse_strings(android_file, "android")
    expected = [
        {"key": "welcome_message", "text": "Welcome to our app!"},
        {"key": "settings_title", "text": "Settings"},
        {"key": "cancel_button", "text": "Cancel"}
    ]
    assert result == expected

def test_parse_invalid_platform():
    with pytest.raises(ValueError, match="Invalid platform: invalid_platform. Must be either 'ios' or 'android'"):
        parse_strings("dummy_file", "invalid_platform") 