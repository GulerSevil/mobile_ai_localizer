import pytest
from unittest.mock import MagicMock
from core.translator.translation_processor import TranslationProcessor


@pytest.fixture
def translation_processor():
    return TranslationProcessor()


def test_perform_translation(translation_processor):
    # Setup
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_model.generate.return_value = MagicMock()
    mock_tokenizer.encode.return_value = [1, 2, 3]
    mock_tokenizer.batch_decode.return_value = ["Hola", "Mundo"]

    # Execute
    result = translation_processor.perform_translation(
        ["Hello", "World"], mock_model, mock_tokenizer
    )

    # Verify
    assert result == ["Hola", "Mundo"]
    mock_tokenizer.encode.assert_called()
    mock_model.generate.assert_called_once()
    mock_tokenizer.batch_decode.assert_called_once()


def test_perform_translation_error(translation_processor):
    # Setup
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_tokenizer.encode.side_effect = Exception("Translation error")

    # Execute and verify
    with pytest.raises(RuntimeError, match="Translation failed"):
        translation_processor.perform_translation(
            ["Hello", "World"], mock_model, mock_tokenizer
        )


def test_clean_translation(translation_processor):
    test_cases = [
        # Input text, Expected output
        ("Hello . . . . . .", "Hello"),
        ("Hello . . . . .", "Hello"),
        ("Hello . . . .", "Hello"),
        ("Hello . . .", "Hello"),
        ("Hello &lt; a &gt;", "Hello &lt;a&gt;"),
        ("Hello &lt;a &gt;", "Hello &lt;a&gt;"),
        ("Hello &lt; a&gt;", "Hello &lt;a&gt;"),
        ("Hello...", "Hello"),
        ("Hello .", "Hello"),
    ]

    for input_text, expected in test_cases:
        result = translation_processor._clean_translation(input_text)
        assert result == expected, f"Failed for input: {input_text}"
