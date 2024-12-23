import os

class AD_DeleteLocalAny:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Any": ("STRING", {"forceInput": True}),
                "File_Name": ("STRING", {"default": ""})
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Tips", "Deleted_Paths")
    OUTPUT_NODE = True
    FUNCTION = "delete_files"
    CATEGORY = "🌻 Addoor/Batch Operation"

    def delete_files(self, Any, File_Name):
        if not isinstance(Any, list):
            Any = [Any]
        
        if isinstance(File_Name, list):
            File_Name = File_Name[0] if File_Name else ""
        elif File_Name is None:
            File_Name = ""

        tips = []
        deleted_paths = []

        for item in Any:
            if os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for file in files:
                        if not File_Name or file.startswith(File_Name):
                            file_path = os.path.join(root, file)
                            try:
                                os.remove(file_path)
                                tips.append(f"Deleted file: {file_path}")
                                deleted_paths.append(file_path)
                            except Exception as e:
                                tips.append(f"Error deleting {file_path}: {str(e)}")
            elif os.path.isfile(item):
                try:
                    os.remove(item)
                    tips.append(f"Deleted file: {item}")
                    deleted_paths.append(item)
                except Exception as e:
                    tips.append(f"Error deleting {item}: {str(e)}")
            else:
                tips.append(f"'{item}' is not a valid file or directory path")

        return ('\n'.join(tips), '\n'.join(deleted_paths))

N_CLASS_MAPPINGS = {
    "AD_DeleteLocalAny": AD_DeleteLocalAny,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_DeleteLocalAny": "🌻 Delete Local Any",
}

