from transformers import MarianMTModel, MarianTokenizer, AutoConfig
from constants.constants import MODEL_NAME_PATTERNS


class ModelManager:
    def __init__(self):
        self._cache = {}

    def get_model(self, source_lang, target_lang):
        """Get or load the translation model for the given language pair."""
        model_name = self._resolve_model_name(source_lang, target_lang)
        if model_name not in self._cache:
            try:
                AutoConfig.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name)
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                self._cache[model_name] = {"model": model, "tokenizer": tokenizer}
            except Exception as e:
                raise ValueError(
                    f"Failed to load translation model '{model_name}': {e}"
                )
        return self._cache[model_name]["model"], self._cache[model_name]["tokenizer"]

    def _resolve_model_name(self, source_lang, target_lang):
        """Resolve the model name for the given language pair."""
        patterns = [
            pattern.format(src=source_lang, tgt=target_lang)
            for pattern in MODEL_NAME_PATTERNS
        ]
        for model_name in patterns:
            try:
                AutoConfig.from_pretrained(model_name)
                return model_name
            except OSError:
                continue
        raise ValueError(
            f"No valid MarianMT model found for {source_lang} → {target_lang}"
        )
