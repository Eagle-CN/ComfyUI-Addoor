import os

class AD_DeleteLocalImage:
    def __init__(self):
        pass

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
    FUNCTION = "delete_images"
    CATEGORY = "Addoor"

    def delete_images(self, Any, File_Name):
        # 确保 Any 是列表
        if not isinstance(Any, list):
            Any = [Any]
    
        # 确保 File_Name 是字符串
        if isinstance(File_Name, list):
            File_Name = File_Name[0] if File_Name else ""
        elif File_Name is None:
            File_Name = ""

        tips = []
        deleted_paths = []

        def delete_file(path):
            try:
                if os.path.exists(path):
                    os.remove(path)
                    tips.append(f"文件 '{path}' 已删除")
                    deleted_paths.append(path)
                    return True
                else:
                    tips.append(f"文件 '{path}' 不存在，无法删除")
                    return False
            except Exception as e:
                tips.append(f"删除文件 '{path}' 时发生错误: {str(e)}")
                return False

        def process_directory(directory, file_name=None):
            if os.path.isdir(directory):
                files_deleted = False
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        if file_name:
                            file_name_no_ext = os.path.splitext(file_name)[0]
                            if file.startswith(file_name_no_ext):
                                if delete_file(file_path):
                                    files_deleted = True
                                break
                        else:
                            if delete_file(file_path):
                                files_deleted = True
                if not files_deleted:
                    if file_name:
                        tips.append(f"在路径 '{directory}' 下没有找到名为 '{file_name}' 的文件")
                    else:
                        tips.append(f"路径 '{directory}' 下没有找到可删除的文件")
            else:
                tips.append(f"'{directory}' 不是有效的目录路径")

        for item in Any:
            if os.path.isdir(item):
                process_directory(item, File_Name)
            elif os.path.isfile(item):
                delete_file(item)
            else:
                tips.append(f"'{item}' 不是有效的文件或目录路径")

        return ('\n'.join(tips), '\n'.join(deleted_paths))

N_CLASS_MAPPINGS = {
    "AD_DeleteLocalImage": AD_DeleteLocalImage,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_DeleteLocalImage": "AD Delete Local Image",  # 删除本地图片
}

