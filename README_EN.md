<p align="center">
  <a href="https://github.com/Eagle-CN/ComfyUI-Addoor" target="blank">
    <img src="https://i.ibb.co/6nJzL9n/1.png" alt="Logo" width="156" height="156">
  </a>
  <h2 align="center" style="font-weight: 600">ComfyUI-Addoor</h2>

  <p align="center">
    Powerful plugin for ComfyUI
    <br />
    <a href="https://github.com/Eagle-CN/ComfyUI-Addoor" target="blank"><strong>📘 Explore the docs</strong></a>&nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="#%EF%B8%8F-installation" target="blank"><strong>📦️ Installation</strong></a>&nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="https://github.com/Eagle-CN/ComfyUI-Addoor/issues" target="blank"><strong>🐛 Report Bug</strong></a>
    <br />
    <br />
  </p>
</p>

## ✨ Features

- 🔄 CSV reading and processing
- 📁 Batch image loading and file operations
- 🗜️ ZIP file creation
- 💾 Image and text saving
- 🧮 Training step calculation
- 🔄 Prompt replacement and styling
- 🌐 Hugging Face model downloading
- 🎨 Image color filtering
- 📊 Text to CSV conversion
- ...and more features in development!

## 📦️ Installation

1. Make sure you have ComfyUI installed.
2. Clone this repository into the `custom_nodes` directory of ComfyUI:

\`\`\`sh
cd ComfyUI/custom_nodes
git clone https://github.com/Eagle-CN/ComfyUI-Addoor.git
\`\`\`

3. Install the dependencies:

\`\`\`sh
cd ComfyUI-Addoor
pip install -r requirements.txt
\`\`\`

4. Restart ComfyUI, and the ComfyUI-Addoor nodes will appear in the node list.

## 🚀 Usage

ComfyUI-Addoor adds several new nodes to ComfyUI, each with specific functionality:

1. **CSV Reader**: Read and process CSV files.
2. **Batch Image Load**: Load images in batch from a specified directory.
3. **Delete Local Any**: Delete specified files or directories.
4. **Text List To String**: Convert a list of text files to a string.
5. **Any File List**: List files in a directory with various filtering options.
6. **Zip Save**: Create ZIP archive files.
7. **Image Saver**: Save images to a specified directory.
8. **Flux Train Step Math**: Calculate training steps for machine learning models.
9. **Text Saver**: Save text content to a file.
10. **Prompt Replace**: Replace specific content in text.
11. **Hugging Face Download**: Download models or datasets from Hugging Face.
12. **Image Color Filter**: Apply various color adjustments and filter effects.
13. **CSV Prompt Styler**: Style prompts using styles from a CSV file.
14. **Txt To CSV Combiner**: Combine multiple text files into a single CSV file.

Each node can be found in the ComfyUI interface and can be connected with other nodes to create complex workflows.

## 📘 Node Descriptions and Usage Notes

1. **CSV Reader (AD_CSVReader)**
   - Description: Reads CSV files and outputs their content.
   - Note: Supports selecting specific columns and random row selection.

2. **Batch Image Load (AD_BatchImageLoadFromDir)**
   - Description: Loads multiple images from a specified directory.
   - Note: Supports various image formats including jpg, jpeg, png, bmp, gif, and webp.

3. **Delete Local Any (AD_DeleteLocalAny)**
   - Description: Deletes specified files or directories.
   - Note: Use with caution as deletions are permanent.

4. **Text List To String (AD_TextListToString)**
   - Description: Loads text files and combines their contents.
   - Note: Supports txt and csv files.

5. **Any File List (AD_AnyFileList)**
   - Description: Lists files in a directory with various filtering options.
   - Note: Useful for file management and content extraction.

6. **Zip Save (AD_ZipSave)**
   - Description: Creates a zip archive of a specified directory.
   - Note: Useful for backing up or sharing multiple files at once.

7. **Image Saver (AD_ImageSaver)**
   - Description: Saves images to a specified directory with customizable naming.
   - Note: Supports metadata saving and automatic file numbering.

8. **Flux Train Step Math (AD_FluxTrainStepMath)**
   - Description: Calculates training steps for machine learning models.
   - Note: Useful for planning and optimizing training processes.

9. **Text Saver (AD_TextSaver)**
   - Description: Saves text content to a file with customizable naming and formatting.
   - Note: Supports time-based tokens in directory and filename prefix.

10. **Prompt Replace (AD_PromptReplace)**
    - Description: Replaces text in a prompt based on specified criteria and random selection.
    - Note: Useful for creating variations in prompts or text content with controlled randomness.

11. **Hugging Face Download (AD_HFDownload)**
    - Description: Downloads models or datasets from Hugging Face.
    - Note: Supports using mirror sites and authentication.

12. **Image Color Filter (AD_ImageColorFilter)**
    - Description: Applies various color adjustments and filter effects to images.
    - Note: Provides comprehensive image color and quality adjustment capabilities.

13. **CSV Prompt Styler (AD_CSVPromptStyler)**
    - Description: Styles prompts using styles defined in a CSV file.
    - Note: Allows easy application of predefined prompt styles.

14. **Txt To CSV Combiner (AD_TxtToCSVCombiner)**
    - Description: Combines multiple text files into a single CSV file.
    - Note: Supports file sorting and optional header addition.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! See our [Contributing Guide](CONTRIBUTING.md) for more information.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Thanks to the ComfyUI team for creating such a powerful framework.
- Thanks to all the developers who have contributed to this project.

