# ComfyUI-Addoor

ComfyUI-Addoor is a custom node plugin package for ComfyUI, providing various utility functions for file operations and data processing.

## Chinese Localization

To use the Chinese localization:
1. Download the `addoor_zh.json` file.
2. Place it in the `/ComfyUI/custom_nodes/AIGODLIKE-COMFYUI-TRANSLATION/zh-CN/Nodes` directory.
3. Restart ComfyUI.

## Features and Usage Notes

1. 🌻 CSV Reader (AD_CSVReader)
 - Reads CSV files and outputs their content.
 - Inputs:
   - file_path: Path to the CSV file.
   - column_index: Index of the column to read (0 for all columns).
   - seed: Random seed for row selection.
   - increment: Increment for row selection.
 - Outputs: File path, seed value, increment value, full content, list of lines, total line count, selected line.

2. 🌻 Batch Image Load From Directory (AD_BatchImageLoadFromDir)
 - Loads multiple images from a specified directory.
 - Inputs:
   - Directory: Path to the folder containing images.
   - Load_Cap: Maximum number of images to load.
   - Skip_Frame: Number of images to skip before starting to load.
   - seed: Random seed.
 - Outputs: Loaded images, image paths, image names with suffix, image names, and count.
 - Note: Supports various image formats including jpg, jpeg, png, bmp, gif, and webp.

3. 🌻 Delete Local Any (AD_DeleteLocalAny)
 - Deletes specified files or directories.
 - Inputs:
   - Any: File or directory path(s) to delete.
   - File_Name: Optional specific filename to delete within directories.
 - Outputs: Operation status and deleted file paths.
 - Note: Use with caution as deletions are permanent.

4. 🌻 Text List To String (AD_TextListToString)
 - Loads text files from a directory and combines their contents.
 - Inputs:
   - Directory: Path to the folder containing text files.
   - Load_Cap: Maximum number of files to load.
   - Skip_Frame: Number of files to skip before starting to load.
   - seed: Random seed.
 - Outputs: File names, contents, paths, file names with suffix, count, and merged content.
 - Note: Supports txt and csv files.

5. 🌻 Any File List (AD_AnyFileList)
 - Lists files in a directory with various filtering options.
 - Inputs:
   - Directory: Path to search for files.
   - Load_Cap: Maximum number of files to list.
   - Skip_Frame: Number of files to skip before starting to list.
   - Filter_By: File type filter (e.g., images, text).
   - Extension: Specific file extension to filter.
   - Deep_Search: Whether to search subdirectories.
   - seed: Random seed.
 - Outputs: Output directory, image list, text list, file path list, file name list, file name with extension list, total file count, and merged text.
 - Note: Versatile node for file management and content extraction.

6. 🌻 Zip Save (AD_ZipSave)
 - Creates a zip archive of a specified directory.
 - Inputs:
   - Input_Directory: Directory to zip.
   - Output_Directory: Where to save the zip file.
   - Zip_Filename: Name for the output zip file.
 - Outputs: Path to the created zip file and operation status.
 - Note: Useful for backing up or sharing multiple files at once.

7. 🌻 Image Saver (AD_ImageSaver)
 - Saves images to a specified directory with customizable naming.
 - Inputs:
   - Images: Image data to save.
   - Directory: Where to save the images.
   - Filename_Prefix: Prefix for the saved image filenames.
   - Open_Output_Directory: Whether to open the output folder after saving.
 - Outputs: Path to the saved images.
 - Note: Supports metadata saving and automatic file numbering.

8. 🌻 Flux Train Step Math (AD_FluxTrainStepMath)
 - Calculates training steps for machine learning models.
 - Inputs:
   - Material_Count: Number of training materials.
   - Training_Times_Per_Image: Number of times to train on each image.
   - Epoch: Number of epochs for training.
   - equation: Custom equation for step calculation.
 - Outputs: Total training steps and steps per epoch.
 - Note: Useful for planning and optimizing training processes.

9. 🌻 Text Saver (AD_TextSaver)
 - Saves text content to a file with customizable naming and formatting.
 - Inputs:
   - text: Content to save.
   - directory: Where to save the text file.
   - filename_prefix: Prefix for the saved file name.
   - filename_delimiter: Character to use between prefix and number.
   - filename_number_padding: Number of digits for file numbering.
   - file_extension: File extension for the saved file.
   - encoding: Text encoding (default UTF-8).
 - Outputs: Path to the saved text file.
 - Note: Supports time-based tokens in directory and filename prefix.

10. 🌻 Prompt Replace (AD_PromptReplace)
 - Replaces text in a prompt based on specified criteria and random selection.
 - Inputs:
   - Content: The main text content to be processed.
   - Match: The text to be replaced.
   - Replace: The text to replace the matched content.
   - seed: Random seed for selection.
   - Increment: Value to increment or decrement the seed.
   - Random_Mode: Mode for line selection.
 - Outputs: Replaced text and new seed value.
 - Note: Useful for creating variations in prompts or text content with controlled randomness.

11. 🌻 Hugging Face Download (AD_HFDownload)
 - Downloads models or datasets from Hugging Face.
 - Inputs:
   - download_url: Download URL.
   - repo_id: Repository ID.
   - save_path: Path to save the downloaded content.
   - resource_type: Type of resource (model or dataset).
   - use_mirror: Whether to use a mirror site.
   - create_folder: Whether to create a new folder for the download.
   - filename: Specific filename to download.
   - hf_token: Hugging Face token for authentication.
 - Outputs: Download path and status.
 - Note: Supports downloading various resources from Hugging Face.

12. 🌻 Image Color Filter (AD_ImageColorFilter)
 - Applies various color adjustments and filter effects to images.
 - Inputs:
   - image: The image to process.
   - exposure: Exposure adjustment.
   - clarity: Clarity adjustment.
   - highlights: Highlights adjustment.
   - shadows: Shadows adjustment.
   - contrast: Contrast adjustment.
   - saturation: Saturation adjustment.
   - vibrance: Vibrance adjustment.
   - temperature: Color temperature adjustment.
   - sharpness: Sharpness adjustment.
 - Outputs: Processed image.
 - Note: Provides comprehensive image color and quality adjustment capabilities.

## Installation

1. Copy the `ComfyUI-Addoor` folder to the `custom_nodes` directory in your ComfyUI installation.
2. Ensure that the required dependencies are installed (see `requirements.txt`).
3. Restart ComfyUI.

## Usage

After installation, the new nodes will be available in the ComfyUI interface under the "Addoor" category. Refer to the feature descriptions above for specific usage of each node.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

