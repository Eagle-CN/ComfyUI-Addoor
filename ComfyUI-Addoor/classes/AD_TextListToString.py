import os
import csv

def get_text_files(directory):
    text_extensions = ['.txt', '.csv']
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in text_extensions):
                file_paths.append(os.path.join(root, file))
    return sorted(file_paths)

def extract_file_names(file_paths, skip, load):
    start_index = skip
    end_index = skip + load
    subset_file_paths = file_paths[start_index:end_index]
    return [os.path.splitext(os.path.basename(path))[0] for path in subset_file_paths]

def extract_file_paths(file_paths, skip, load):
    start_index = skip
    end_index = skip + load
    return file_paths[start_index:end_index]

def read_text_file(file_path):
    try:
        if file_path.lower().endswith('.csv'):
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                return '\n'.join([','.join(row) for row in reader])
        else:
            with open(file_path, 'r', encoding='utf-8') as txtfile:
                return txtfile.read()
    except Exception as e:
        print(f"读取文件 '{file_path}' 时出错: {e}")
        return None

class AD_TextListToString:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Directory": ("STRING", {"default": ""}),
                "Load_Cap": ("INT", {"default": 100, "min": 1, "max": 1000}),
                "Skip_Frame": ("INT", {"default": 0, "min": 0, "max": 100})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "INT", "STRING")
    RETURN_NAMES = ("File_Names", "File_Contents", "File_Paths", "File_Names_Suffix", "Count", "Merged_Content")
    FUNCTION = "load_text_files"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True, True, True, True, False, False)
    CATEGORY = "Addoor"

    def load_text_files(self, Directory, Load_Cap, Skip_Frame):
        file_paths = get_text_files(Directory)
        
        if not file_paths:
            return ([], [], [], [], 0, "")
        
        valid_file_paths = extract_file_paths(file_paths, Skip_Frame, Load_Cap)
        file_contents = []
        merged_content = ""
        for file_path in valid_file_paths:
            content = read_text_file(file_path)
            if content is not None:
                file_contents.append(content)
                merged_content += content + "\n\n"  # 用两个换行符分隔不同文件的内容
        
        file_names_suffix = [os.path.basename(path) for path in valid_file_paths]
        file_names = extract_file_names(file_paths, Skip_Frame, Load_Cap)
        count = len(file_contents)
        
        return (file_names, file_contents, valid_file_paths, file_names_suffix, count, merged_content.strip())

N_CLASS_MAPPINGS = {
    "AD_TextListToString": AD_TextListToString,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_TextListToString": "AD Text List To String",  # 文本列表转字符串
}

