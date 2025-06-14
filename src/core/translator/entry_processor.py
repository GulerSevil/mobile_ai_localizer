class EntryProcessor:
    def collect_texts_for_translation(self, entries):
        """Collect texts from entries and maintain mapping to original entries."""
        texts = []
        entry_mapping = []

        for entry in entries:
            if "text" in entry:  # Android simple string
                texts.append(entry["text"])
                entry_mapping.append((entry, None))
            elif "items" in entry:  # Android plurals or string-array
                for idx, item in enumerate(entry["items"]):
                    if isinstance(item, dict):  # plurals
                        if "text" in item:
                            texts.append(item["text"])
                            entry_mapping.append((entry, idx))
                    else:  # string-array
                        texts.append(item)
                        entry_mapping.append((entry, idx))
            elif "translated" in entry:  # iOS entry
                texts.append(entry["translated"])
                entry_mapping.append((entry, None))

        return texts, entry_mapping

    def reconstruct_entries(self, entry_mapping, translations):
        """Reconstruct the original entry structure with translations."""
        translated_entries = {}

        for (entry, item_idx), translated_text in zip(entry_mapping, translations):
            translated_text = translated_text.strip("'\"")

            if item_idx is None:  # Simple string or iOS string
                if "text" in entry:  # Android
                    translated_entries[id(entry)] = {
                        "name": entry["name"],
                        "text": translated_text,
                        "type": entry["type"],
                    }
                else:  # iOS
                    translated_entries[id(entry)] = {
                        "key": entry["key"],
                        "translated": translated_text,
                    }
            else:  # Plurals or string-array
                if id(entry) not in translated_entries:
                    translated_entries[id(entry)] = {
                        "name": entry["name"],
                        "items": entry["items"].copy(),
                        "type": entry["type"],
                    }

                if isinstance(entry["items"][0], dict):  # plurals
                    translated_entries[id(entry)]["items"][item_idx][
                        "text"
                    ] = translated_text
                else:  # string-array
                    translated_entries[id(entry)]["items"][item_idx] = translated_text

        return list(translated_entries.values())
