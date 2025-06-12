import pytest
from unittest.mock import patch, MagicMock
from core.translator.model_manager import ModelManager


@pytest.fixture
def model_manager():
    return ModelManager()


@patch("core.translator.model_manager.AutoConfig")
@patch("core.translator.model_manager.MarianMTModel")
@patch("core.translator.model_manager.MarianTokenizer")
def test_get_model_success(mock_tokenizer, mock_model, mock_config, model_manager):
    # Setup mocks
    mock_model.from_pretrained.return_value = MagicMock()
    mock_tokenizer.from_pretrained.return_value = MagicMock()

    # Execute
    model, tokenizer = model_manager.get_model("en", "es")

    # Verify
    assert model is not None
    assert tokenizer is not None
    mock_model.from_pretrained.call_count == 2
    mock_tokenizer.from_pretrained.call_count == 2

    # Test caching
    model2, tokenizer2 = model_manager.get_model("en", "es")
    assert model2 == model
    assert tokenizer2 == tokenizer
    # Should not call from_pretrained again
    assert mock_model.from_pretrained.call_count == 1
    assert mock_tokenizer.from_pretrained.call_count == 1


@patch("core.translator.model_manager.AutoConfig")
def test_get_model_invalid_language(mock_config, model_manager):
    # Setup mock to raise OSError for all model names
    mock_config.from_pretrained.side_effect = OSError()

    # Execute and verify
    with pytest.raises(ValueError, match="No valid MarianMT model found"):
        model_manager.get_model("en", "invalid_lang")


@patch("core.translator.model_manager.AutoConfig")
@patch("core.translator.model_manager.MarianMTModel")
def test_get_model_load_error(mock_model, mock_config, model_manager):
    # Setup mock to raise error during model loading
    mock_config.from_pretrained.return_value = MagicMock()
    mock_model.from_pretrained.side_effect = Exception("Load error")

    # Execute and verify
    with pytest.raises(ValueError, match="Failed to load translation model"):
        model_manager.get_model("en", "es")
