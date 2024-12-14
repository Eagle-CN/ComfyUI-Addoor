import os
import csv

class AD_TextListToString:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Directory": ("STRING", {"default": ""}),
                "Load_Cap": ("INT", {"default": 100, "min": 1, "max": 1000}),
                "Skip_Frame": ("INT", {"default": 0, "min": 0, "max": 100}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "INT", "STRING")
    RETURN_NAMES = ("File_Names", "File_Contents", "File_Paths", "File_Names_Suffix", "Count", "Merged_Content")
    FUNCTION = "load_text_files"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True, True, True, True, False, False)
    CATEGORY = "Addoor"

    def load_text_files(self, Directory, Load_Cap, Skip_Frame):
        text_extensions = ['.txt', '.csv']
        file_paths = []
        for root, dirs, files in os.walk(Directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in text_extensions):
                    file_paths.append(os.path.join(root, file))
        file_paths = sorted(file_paths)[Skip_Frame:Skip_Frame + Load_Cap]
        
        file_names = []
        file_contents = []
        file_names_suffix = []
        merged_content = ""
        
        for file_path in file_paths:
            try:
                if file_path.lower().endswith('.csv'):
                    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                        content = '\n'.join([','.join(row) for row in csv.reader(csvfile)])
                else:
                    with open(file_path, 'r', encoding='utf-8') as txtfile:
                        content = txtfile.read()
                
                file_names.append(os.path.splitext(os.path.basename(file_path))[0])
                file_contents.append(content)
                file_names_suffix.append(os.path.basename(file_path))
                merged_content += content + "\n\n"
            except Exception as e:
                print(f"Error reading file '{file_path}': {e}")
        
        count = len(file_contents)
        return (file_names, file_contents, file_paths, file_names_suffix, count, merged_content.strip())

N_CLASS_MAPPINGS = {
    "AD_TextListToString": AD_TextListToString,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_TextListToString": "🌻 Text List To String",
}

