import pytest
from unittest.mock import MagicMock
from core.translator import Localizer


@pytest.fixture
def test_entries():
    return [{"key": "welcome", "text": "Welcome"}, {"key": "hello", "text": "Hello"}]


@pytest.fixture
def translator():
    return Localizer("en")


def test_translate_batch(translator, test_entries):
    # Mock the dependencies
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_model_manager = MagicMock()
    mock_translation_processor = MagicMock()
    mock_entry_processor = MagicMock()

    # Setup the mocks
    translator._model_manager = mock_model_manager
    translator._translation_processor = mock_translation_processor
    translator._entry_processor = mock_entry_processor

    mock_model_manager.get_model.return_value = (mock_model, mock_tokenizer)
    mock_entry_processor.collect_texts_for_translation.return_value = (
        ["Welcome", "Hello"],
        [(test_entries[0], None), (test_entries[1], None)],
    )
    mock_translation_processor.perform_translation.return_value = ["Bienvenido", "Hola"]
    mock_entry_processor.reconstruct_entries.return_value = [
        {"key": "welcome", "translated": "Bienvenido"},
        {"key": "hello", "translated": "Hola"},
    ]

    # Execute
    result = translator.translate_batch(test_entries, "es")

    # Verify
    assert result == [
        {"key": "welcome", "translated": "Bienvenido"},
        {"key": "hello", "translated": "Hola"},
    ]

    # Verify all components were called correctly
    mock_model_manager.get_model.assert_called_once_with("en", "es")
    mock_entry_processor.collect_texts_for_translation.assert_called_once_with(
        test_entries
    )
    mock_translation_processor.perform_translation.assert_called_once_with(
        ["Welcome", "Hello"], mock_model, mock_tokenizer
    )
    mock_entry_processor.reconstruct_entries.assert_called_once()
