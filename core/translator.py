from transformers import MarianMTModel, MarianTokenizer, AutoConfig
import html
from config.constants import MODEL_NAME_PATTERNS

class Localizer:
    def __init__(self, source_lang):
        self.source_lang = source_lang
        self._cache = {}
    
    def _get_model(self, target_lang):
        model_name = self._resolve_model_name(self.source_lang, target_lang)
        if model_name not in self._cache:
            try:
                AutoConfig.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name)
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                self._cache[model_name] = {"model": model, "tokenizer": tokenizer}
            except Exception as e:
                raise ValueError(f"Failed to load translation model '{model_name}': {e}")
        return self._cache[model_name]

    def _resolve_model_name(self, source_lang, target_lang):
        patterns =  [pattern.format(src=source_lang, tgt=target_lang) for pattern in MODEL_NAME_PATTERNS]
        for model_name in patterns:
            try:
                AutoConfig.from_pretrained(model_name)
                return model_name
            except OSError:
                continue
        raise ValueError(f"No valid MarianMT model found for {source_lang} → {target_lang}")

    def translate_batch(self, entries, target_lang):
        pair = self._get_model(target_lang)
        texts = [entry['text'] for entry in entries]
        model = pair['model']
        tokenizer = pair['tokenizer']

        batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        gen = model.generate(**batch, max_length=512)
        translations = tokenizer.batch_decode(gen, skip_special_tokens=True)

        return [
            {"key": entry["key"], "translated": translated_text.strip('\'"')}
            for entry, translated_text in zip(entries, translations)
        ]
