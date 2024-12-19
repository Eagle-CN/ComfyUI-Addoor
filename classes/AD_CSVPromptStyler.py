import os
import csv

class AD_CSVPromptStyler:
    DEFAULT_CSV_PATH = "./custom_nodes/ComfyUI-Addoor/styles.csv"

    def __init__(self):
        self.styles = self.get_styles(self.DEFAULT_CSV_PATH)
        self.style_data = self.read_csv(self.DEFAULT_CSV_PATH)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": cls.DEFAULT_CSV_PATH}),
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": (cls.get_styles(cls.DEFAULT_CSV_PATH), ),
                "log_prompt": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("styled_positive", "styled_negative", "selected_style")
    FUNCTION = "apply_style"
    OUTPUT_NODE = True
    CATEGORY = "🌻 葵花宝典/CSV控制器"

    @staticmethod
    def get_styles(csv_path):
        styles = ["None"]
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    next(csv_reader)  # Skip header row
                    styles.extend([row[0] for row in csv_reader if row])
            except Exception as e:
                print(f"Error reading styles from {csv_path}: {str(e)}")
        return styles

    @staticmethod
    def read_csv(csv_path):
        style_data = {"None": {"prompt": "{prompt}", "negative_prompt": ""}}
        if not os.path.exists(csv_path):
            print(f"Error: File not found at {csv_path}")
            return style_data

        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    if len(row) >= 3:
                        style_name, positive_prompt, negative_prompt = row[0], row[1], row[2]
                        style_data[style_name] = {
                            "prompt": positive_prompt,
                            "negative_prompt": negative_prompt
                        }
        except Exception as e:
            print(f"Error reading CSV file {csv_path}: {str(e)}")
        return style_data

    def apply_style(self, csv_path, text_positive, text_negative, style, log_prompt):
        # If a new CSV path is provided, reload styles and style data
        if csv_path != self.DEFAULT_CSV_PATH:
            self.styles = self.get_styles(csv_path)
            self.style_data = self.read_csv(csv_path)

        if style not in self.style_data:
            print(f"Style '{style}' not found. Using default.")
            style = "None"

        style_info = self.style_data[style]
        styled_positive = style_info["prompt"].replace("{prompt}", text_positive)
        styled_negative = f"{style_info['negative_prompt']}, {text_negative}" if style_info['negative_prompt'] and text_negative else style_info['negative_prompt'] or text_negative

        if log_prompt:
            print(f"Selected style: {style}")
            print(f"Original positive: {text_positive}")
            print(f"Original negative: {text_negative}")
            print(f"Styled positive: {styled_positive}")
            print(f"Styled negative: {styled_negative}")

        return styled_positive, styled_negative, style

N_CLASS_MAPPINGS = {
    "AD_CSVPromptStyler": AD_CSVPromptStyler,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_CSVPromptStyler": "🌻 CSV Prompt Styler",
}

