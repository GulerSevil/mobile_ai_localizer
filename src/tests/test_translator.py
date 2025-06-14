import pytest
from unittest.mock import patch, MagicMock
from core.translator import Localizer

def test_localizer_initialization():
    localizer = Localizer('en')
    assert localizer.source_lang == 'en'
    assert localizer._cache == {}

def test_resolve_model_name():
    with patch('core.translator.AutoConfig') as mock_config:
        mock_config.from_pretrained.side_effect = [OSError(), MagicMock()]
        
        localizer = Localizer('en')
        model_name = localizer._resolve_model_name('en', 'es')
        
        assert model_name == 'Helsinki-NLP/opus-mt-en-es-small'
        assert mock_config.from_pretrained.call_count == 2

def test_resolve_model_name_no_valid_model():
    with patch('core.translator.AutoConfig') as mock_config:
        # Make all model attempts fail
        mock_config.from_pretrained.side_effect = OSError("Model not found")
        
        localizer = Localizer('en')
        with pytest.raises(ValueError, match="No valid MarianMT model found"):
            localizer._resolve_model_name('en', 'es')

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
    mock_model_instance = MagicMock()
    mock_tokenizer_instance = MagicMock()
    
    mock_config.from_pretrained.return_value = MagicMock()
    mock_model.from_pretrained.return_value = mock_model_instance
    mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
    
    mock_tokenizer_instance.return_value = {
        "input_ids": MagicMock(),
        "attention_mask": MagicMock()
    }
    mock_tokenizer_instance.batch_decode.return_value = ["Bienvenido", "Hola"]
    
    mock_model_instance.generate.return_value = MagicMock()

    result = translator.translate_batch(test_entries, "es")
    
    expected = [
        {"key": "welcome", "translated": "Bienvenido"},
        {"key": "hello", "translated": "Hola"}
    ]
    assert result == expected
    
    mock_tokenizer_instance.assert_called_once()
    mock_model_instance.generate.assert_called_once()

def test_invalid_model(translator, test_entries):
    with pytest.raises(ValueError):
        translator.translate_batch(test_entries, "invalid_lang") 