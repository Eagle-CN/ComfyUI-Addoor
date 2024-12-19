import os
import re
from datetime import datetime

class AD_TextSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "directory": ("STRING", {"default": "./ComfyUI/output"}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "filename_delimiter": ("STRING", {"default": "_"}),
                "filename_number_padding": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1}),
            },
            "optional": {
                "file_extension": ("STRING", {"default": ".txt"}),
                "encoding": ("STRING", {"default": "utf-8"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("File_Path",)
    FUNCTION = "save_text_file"
    OUTPUT_NODE = True
    CATEGORY = "🌻 Addoor/Output Saving"

    def save_text_file(self, text, directory, filename_prefix='ComfyUI', filename_delimiter='_', filename_number_padding=4, file_extension='.txt', encoding='utf-8'):
        directory = self.parse_tokens(directory)
        filename_prefix = self.parse_tokens(filename_prefix)

        os.makedirs(directory, exist_ok=True)

        filename = self.generate_filename(directory, filename_prefix, filename_delimiter, filename_number_padding, file_extension)
        file_path = os.path.join(directory, filename)

        try:
            with open(file_path, 'w', encoding=encoding, newline='\n') as f:
                f.write(text)
            print(f"Text saved successfully to {file_path}")
        except OSError as e:
            print(f"Error saving file {file_path}: {str(e)}")
            return ("",)

        return (file_path,)

    def generate_filename(self, directory, prefix, delimiter, number_padding, extension):
        if number_padding == 0:
            return f"{prefix}{extension}"

        pattern = f"{re.escape(prefix)}{re.escape(delimiter)}(\\d{{{number_padding}}})"
        existing_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        existing_counters = [
            int(re.search(pattern, filename).group(1))
            for filename in existing_files
            if re.match(pattern, filename)
        ]

        counter = max(existing_counters, default=0) + 1
        return f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"

    def parse_tokens(self, string):
        time_token = re.search(r'\[time$$(.*?)$$\]', string)
        if time_token:
            time_format = time_token.group(1)
            current_time = datetime.now().strftime(time_format)
            string = string.replace(time_token.group(0), current_time)
        return string

N_CLASS_MAPPINGS = {
    "AD_TextSaver": AD_TextSaver,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_TextSaver": "🌻 Text Saver",
}

