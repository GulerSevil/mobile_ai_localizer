class EntryProcessor:
    def collect_texts_for_translation(self, entries):
        """Collect texts from entries and maintain mapping to original entries."""
        texts = []
        entry_mapping = []

        for entry in entries:
            if entry["type"] == "string":
                # Handle both Android and iOS string entries
                if "translated" in entry:
                    texts.append(entry["translated"])
                    entry_mapping.append((entry, None))
            elif entry["type"] == "plurals":
                for idx, item in enumerate(entry["items"]):
                    texts.append(item["translated"])
                    entry_mapping.append((entry, idx))
            elif entry["type"] == "string-array":
                for idx, item in enumerate(entry["items"]):
                    texts.append(item["translated"])
                    entry_mapping.append((entry, idx))

        return texts, entry_mapping

    def reconstruct_entries(self, entry_mapping, translations):
        """Reconstruct the original entry structure with translations."""
        translated_entries = {}

        for (entry, item_idx), translated_text in zip(entry_mapping, translations):
            translated_text = translated_text.strip("'\"")

            if item_idx is None:  # Simple string
                translated_entries[id(entry)] = {
                    "key": entry["key"],
                    "translated": translated_text,
                    "type": entry["type"],
                }
            else:  # Plurals or string-array
                if id(entry) not in translated_entries:
                    translated_entries[id(entry)] = {
                        "key": entry["key"],
                        "items": [item.copy() for item in entry["items"]],
                        "type": entry["type"],
                    }

                # Update the specific item with translation
                translated_entries[id(entry)]["items"][item_idx][
                    "translated"
                ] = translated_text

        return list(translated_entries.values())
