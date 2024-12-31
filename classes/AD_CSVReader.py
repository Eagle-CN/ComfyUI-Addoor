import os
import csv
import random

class AD_CSVReader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "", "multiline": False}),
                "column_index": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "increment": ("INT", {"default": 1, "min": -1000, "max": 1000}),
            },
            "optional": {
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "forceInput": True, "tooltip": "Start from this row (0 or 1 for first row)"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "INT", "STRING", "STRING", "INT", "STRING")
    RETURN_NAMES = ("File_Path", "Seed", "Increment", "Full_Content", "Lines", "Total_Lines", "Selected_Line")
    FUNCTION = "read_csv"
    OUTPUT_NODE = True
    CATEGORY = "🌻 Addoor/CSV"
    OUTPUT_IS_LIST = (False, False, False, False, True, False, False)

    def __init__(self):
        self.current_index = None

    def read_csv(self, file_path, column_index, seed, increment, index=None):
        if not os.path.exists(file_path):
            return file_path, seed, increment, f"Error: File not found at {file_path}", [], 0, ""

        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                lines = list(csv_reader)
                total_lines = len(lines)

                if column_index == 0:
                    # Use all columns
                    processed_lines = [','.join(row) for row in lines]
                elif 0 < column_index <= len(lines[0]):
                    # Use specific column
                    processed_lines = [row[column_index - 1] for row in lines if len(row) >= column_index]
                else:
                    return file_path, seed, increment, f"Error: Invalid column index {column_index}", [], total_lines, ""

                full_content = '\n'.join(processed_lines)

                # Initialize or update current_index based on the new 'index' input
                if index is not None:
                    # Adjust index to start from 0 internally, but treat 0 and 1 as the first row
                    adjusted_index = max(0, index - 1)
                    self.current_index = adjusted_index % len(processed_lines)
                elif self.current_index is None:
                    if increment == 0:
                        # Random starting point
                        random.seed(seed)
                        self.current_index = random.randint(0, len(processed_lines) - 1)
                    else:
                        # Start from the beginning
                        self.current_index = 0

                print(f"DEBUG: Current index set to {self.current_index}")

                # Select a line based on increment
                if increment == 0:
                    # Random selection using seed
                    random.seed(seed)
                    selected_index = random.randint(0, len(processed_lines) - 1)
                else:
                    # Sequential selection based on increment
                    selected_index = self.current_index
                    self.current_index = (self.current_index + increment) % len(processed_lines)

                selected_line = processed_lines[selected_index]

                return file_path, seed, increment, full_content, processed_lines, total_lines, selected_line

        except Exception as e:
            return file_path, seed, increment, f"Error reading CSV file: {str(e)}", [], 0, ""

