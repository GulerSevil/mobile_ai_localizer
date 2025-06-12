import pytest
from core.translator.entry_processor import EntryProcessor


@pytest.fixture
def entry_processor():
    return EntryProcessor()


def test_collect_texts_android_simple(entry_processor):
    entries = [
        {"key": "welcome", "translated": "Welcome", "type": "string"},
        {"key": "hello", "translated": "Hello", "type": "string"},
    ]

    texts, mapping = entry_processor.collect_texts_for_translation(entries)

    assert texts == ["Welcome", "Hello"]
    assert len(mapping) == 2
    assert mapping[0][0] == entries[0]
    assert mapping[1][0] == entries[1]


def test_collect_texts_android_plurals(entry_processor):
    entries = [
        {
            "key": "items",
            "type": "plurals",
            "items": [
                {"quantity": "one", "translated": "1 item"},
                {"quantity": "other", "translated": "%d items"},
            ],
        }
    ]

    texts, mapping = entry_processor.collect_texts_for_translation(entries)

    assert texts == ["1 item", "%d items"]
    assert len(mapping) == 2
    assert mapping[0][0] == entries[0]
    assert mapping[0][1] == 0
    assert mapping[1][0] == entries[0]
    assert mapping[1][1] == 1


def test_collect_texts_android_string_array(entry_processor):
    entries = [
        {
            "key": "languages",
            "type": "string-array",
            "items": [
                {"translated": "English"},
                {"translated": "Spanish"},
                {"translated": "French"},
            ],
        }
    ]

    texts, mapping = entry_processor.collect_texts_for_translation(entries)

    assert texts == ["English", "Spanish", "French"]
    assert len(mapping) == 3
    assert mapping[0][0] == entries[0]
    assert mapping[0][1] == 0


def test_collect_texts_ios(entry_processor):
    entries = [
        {"key": "welcome", "translated": "Welcome", "type": "string"},
        {"key": "hello", "translated": "Hello", "type": "string"},
    ]

    texts, mapping = entry_processor.collect_texts_for_translation(entries)

    assert texts == ["Welcome", "Hello"]
    assert len(mapping) == 2
    assert mapping[0][0] == entries[0]
    assert mapping[1][0] == entries[1]


def test_reconstruct_entries_android_simple(entry_processor):
    entries = [
        {"key": "welcome", "translated": "Welcome", "type": "string"},
        {"key": "hello", "translated": "Hello", "type": "string"},
    ]
    mapping = [(entries[0], None), (entries[1], None)]
    translations = ["Bienvenido", "Hola"]

    result = entry_processor.reconstruct_entries(mapping, translations)

    assert result == [
        {"key": "welcome", "translated": "Bienvenido", "type": "string"},
        {"key": "hello", "translated": "Hola", "type": "string"},
    ]


def test_reconstruct_entries_android_plurals(entry_processor):
    entries = [
        {
            "key": "items",
            "type": "plurals",
            "items": [
                {"quantity": "one", "translated": "1 item"},
                {"quantity": "other", "translated": "%d items"},
            ],
        }
    ]
    mapping = [(entries[0], 0), (entries[0], 1)]
    translations = ["1 artículo", "%d artículos"]

    result = entry_processor.reconstruct_entries(mapping, translations)

    assert result == [
        {
            "key": "items",
            "type": "plurals",
            "items": [
                {"quantity": "one", "translated": "1 artículo"},
                {"quantity": "other", "translated": "%d artículos"},
            ],
        }
    ]


def test_reconstruct_entries_ios(entry_processor):
    entries = [
        {"key": "welcome", "translated": "Welcome", "type": "string"},
        {"key": "hello", "translated": "Hello", "type": "string"},
    ]
    mapping = [(entries[0], None), (entries[1], None)]
    translations = ["Bienvenido", "Hola"]

    result = entry_processor.reconstruct_entries(mapping, translations)

    assert result == [
        {"key": "welcome", "translated": "Bienvenido", "type": "string"},
        {"key": "hello", "translated": "Hola", "type": "string"},
    ]
