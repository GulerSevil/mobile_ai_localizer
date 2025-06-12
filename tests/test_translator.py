import pytest
from unittest.mock import patch, MagicMock
from core.translator import Localizer

@pytest.fixture
def test_entries():
    return [
        {"key": "welcome", "text": "Welcome"},
        {"key": "hello", "text": "Hello"}
    ]

@pytest.fixture
def translator():
    return Localizer("en")

@patch('core.translator.AutoConfig')
@patch('core.translator.MarianMTModel')
@patch('core.translator.MarianTokenizer')
def test_translate_batch(mock_tokenizer, mock_model, mock_config, translator, test_entries):
    # Mock the model and tokenizer
    mock_model_instance = MagicMock()
    mock_tokenizer_instance = MagicMock()
    
    # Configure mock returns
    mock_config.from_pretrained.return_value = MagicMock()
    mock_model.from_pretrained.return_value = mock_model_instance
    mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
    
    # Mock tokenizer behavior
    mock_tokenizer_instance.return_value = {
        "input_ids": MagicMock(),
        "attention_mask": MagicMock()
    }
    mock_tokenizer_instance.batch_decode.return_value = ["Bienvenido", "Hola"]
    
    # Mock model behavior
    mock_model_instance.generate.return_value = MagicMock()

    # Test translation
    result = translator.translate_batch(test_entries, "es")
    
    # Verify results
    expected = [
        {"key": "welcome", "translated": "Bienvenido"},
        {"key": "hello", "translated": "Hola"}
    ]
    assert result == expected
    
    # Verify model and tokenizer were called correctly
    mock_tokenizer_instance.assert_called_once()
    mock_model_instance.generate.assert_called_once()

def test_invalid_model(translator, test_entries):
    with pytest.raises(ValueError):
        translator.translate_batch(test_entries, "invalid_lang") 