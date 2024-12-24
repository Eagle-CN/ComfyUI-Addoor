import os
import csv
import requests
import random
import time
import json

class AD_CSVTranslator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": ""}),
                "source_column": ("INT", {"default": 1, "min": 1, "max": 1000}),
                "target_column": ("INT", {"default": 2, "min": 1, "max": 1000}),
                "source_lang": (["auto", "en", "zh-CN"],),
                "target_lang": (["zh-CN", "en"],),
                "translate_first_row": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("updated_csv_path", "seed")
    FUNCTION = "translate_csv"
    OUTPUT_NODE = True
    CATEGORY = "🌻 Addoor/CSV"

    def translate_csv(self, csv_path, source_column, target_column, source_lang, target_lang, translate_first_row, seed):
        if not os.path.exists(csv_path):
            return (f"Error: CSV file not found at {csv_path}", seed)

        random.seed(seed)

        try:
            rows = self.ensure_csv_structure(csv_path, source_column, target_column)

            start_row = 0 if translate_first_row else 1

            for i, row in enumerate(rows[start_row:], start=start_row):
                max_col = max(source_column, target_column)
                if len(row) < max_col:
                    # Extend the row if it's shorter than the maximum column index
                    row.extend([''] * (max_col - len(row)))

                text_to_translate = row[source_column - 1]
                translated_text = self.translate_text(text_to_translate, source_lang, target_lang)
                row[target_column - 1] = translated_text
                print(f"Row {i+1}: Original: '{text_to_translate}', Translated: '{translated_text}'")
                time.sleep(0.5)  # Add a slight delay between translations

            with open(csv_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(rows)

            return (csv_path, seed)
        except Exception as e:
            return (f"Error processing CSV: {str(e)}", seed)

    def ensure_csv_structure(self, csv_path, source_column, target_column):
        max_col = max(source_column, target_column)
        rows_updated = False

        with open(csv_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

        for row in rows:
            if len(row) < max_col:
                row.extend([''] * (max_col - len(row)))
                rows_updated = True

        if rows_updated:
            with open(csv_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(rows)

        return rows

    def translate_text(self, text, source_lang, target_lang):
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            print(f"API Response: {response.text}")  # Log the full API response
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list) and len(data[0]) > 0:
                translated_text = data[0][0][0]
                print(f"Successfully translated: '{text}' to '{translated_text}'")
                return translated_text
            else:
                print(f"Unexpected API response structure: {json.dumps(data, ensure_ascii=False)}")
                return text
        except requests.RequestException as e:
            print(f"Translation error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error response: {e.response.text}")
            return text  # Return original text if translation fails

