import os
import csv
import re

class AD_TxtToCSVCombiner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_directory": ("STRING", {"default": "./input_txt_files"}),
                "output_directory": ("STRING", {"default": "./output"}),
                "output_filename": ("STRING", {"default": "combined_output.csv"}),
                "add_header": ("BOOLEAN", {"default": True}),
                "sort_by_filename": ("BOOLEAN", {"default": True, "label": "Sort by filename (disable for number prefix sort)"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_csv_path",)
    FUNCTION = "combine_txt_to_csv"
    OUTPUT_NODE = True
    CATEGORY = "🌻 Addoor/CSV Controller"

    def combine_txt_to_csv(self, input_directory, output_directory, output_filename, add_header, sort_by_filename):
        if not os.path.exists(input_directory):
            return (f"Error: Input directory '{input_directory}' does not exist.",)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_csv_path = os.path.join(output_directory, output_filename)

        try:
            # Get all txt files in the input directory
            txt_files = [f for f in os.listdir(input_directory) if f.endswith('.txt')]

            # Sort files based on the sort_by_filename parameter
            if sort_by_filename:
                txt_files.sort()  # Default to sorting by filename
            else:
                # Sort by number prefix
                txt_files.sort(key=lambda x: int(re.search(r'^\d+', x).group()) if re.search(r'^\d+', x) else float('inf'))

            with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
            
                # Write header if specified
                if add_header:
                    csv_writer.writerow(['Filename', 'Content'])

                for filename in txt_files:
                    file_path = os.path.join(input_directory, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as txtfile:
                            content = txtfile.read().strip()
                    
                        # Replace newlines with space, but keep paragraph structure
                        content = ' '.join(line.strip() for line in content.split('\n') if line.strip())
                    
                        csv_writer.writerow([os.path.splitext(filename)[0], content])
                    except Exception as e:
                        print(f"Error reading file {filename}: {str(e)}")

            return (output_csv_path,)
        except Exception as e:
            return (f"Error creating CSV: {str(e)}",)

N_CLASS_MAPPINGS = {
    "AD_TxtToCSVCombiner": AD_TxtToCSVCombiner,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_TxtToCSVCombiner": "🌻 Txt to CSV Combiner",
}

