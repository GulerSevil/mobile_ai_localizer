from .model_manager import ModelManager
from .translation_processor import TranslationProcessor
from .entry_processor import EntryProcessor


class Localizer:
    def __init__(self, source_lang):
        self.source_lang = source_lang
        self._model_manager = ModelManager()
        self._translation_processor = TranslationProcessor()
        self._entry_processor = EntryProcessor()

    def translate_batch(self, entries, target_lang):
        """Translate a batch of entries to the target language."""
        model, tokenizer = self._model_manager.get_model(self.source_lang, target_lang)

        texts, entry_mapping = self._entry_processor.collect_texts_for_translation(
            entries
        )

        translations = self._translation_processor.perform_translation(
            texts, model, tokenizer
        )

        return self._entry_processor.reconstruct_entries(entry_mapping, translations)
