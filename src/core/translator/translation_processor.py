class TranslationProcessor:
    def perform_translation(self, texts, model, tokenizer):
        """Perform the actual translation using the model."""
        try:
            max_length = min(
                max(len(tokenizer.encode(text)) for text in texts) + 50, 256
            )
            batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            translations = tokenizer.batch_decode(
                model.generate(**batch, max_length=max_length), skip_special_tokens=True
            )
            return [self._clean_translation(text) for text in translations]
        except Exception as e:
            raise RuntimeError(f"Translation failed: {str(e)}")

    def _clean_translation(self, text):
        """Clean up common translation artifacts."""
        # Remove excessive dots
        text = text.replace(". . . . . .", "")
        text = text.replace(". . . . .", "")
        text = text.replace(". . . .", "")
        text = text.replace(". . .", "")

        # Remove trailing dots and spaces
        text = text.rstrip(". ")

        # Fix common HTML tag spacing issues
        text = text.replace("&lt; ", "&lt;")
        text = text.replace(" &gt;", "&gt;")

        return text.strip()
