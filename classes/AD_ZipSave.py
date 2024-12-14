import os
import zipfile
import time

class AD_ZipSave:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input_Directory": ("STRING", {"default": ""}),
                "Output_Directory": ("STRING", {"default": ""}),
                "Zip_Filename": ("STRING", {"default": "archive.zip"}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Zip_Path", "Status")
    FUNCTION = "zip_and_save"
    OUTPUT_NODE = True
    CATEGORY = "Addoor"

    def zip_and_save(self, Input_Directory: str, Output_Directory: str, Zip_Filename: str) -> tuple[str, str]:
        if not os.path.exists(Input_Directory):
            return ("", f"Error: Input directory not found: {Input_Directory}")

        try:
            os.makedirs(Output_Directory, exist_ok=True)
        except Exception as e:
            return ("", f"Error creating output directory: {str(e)}")

        Zip_Filename = Zip_Filename if Zip_Filename.lower().endswith('.zip') else Zip_Filename + '.zip'
        zip_path = os.path.join(Output_Directory, Zip_Filename)

        try:
            start_time = time.time()
            print(f"Starting to create zip file: {zip_path}")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(Input_Directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if file_path != zip_path:
                            arcname = os.path.relpath(file_path, Input_Directory)
                            zipf.write(file_path, arcname)

            end_time = time.time()
            total_time = end_time - start_time
            zip_size = os.path.getsize(zip_path) / (1024 * 1024)  # Convert to MB
            
            status = f"Zip file created successfully. Size: {zip_size:.2f}MB, Time taken: {total_time:.2f}s"
            print(status)
            return (zip_path, status)

        except Exception as e:
            error_message = f"Error creating zip file: {str(e)}"
            print(error_message)
            return ("", error_message)

N_CLASS_MAPPINGS = {
    "AD_ZipSave": AD_ZipSave,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_ZipSave": "🌻 Zip Save",
}

