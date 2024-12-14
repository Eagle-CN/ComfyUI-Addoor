# ComfyUI-Addoor

## 中文本地化

使用中文本地化：
1. 下载 `addoor_zh.json` 文件。
2. 将其放置在 `/ComfyUI/custom_nodes/AIGODLIKE-COMFYUI-TRANSLATION/zh-CN/Nodes` 目录下。
3. 重启 ComfyUI。

ComfyUI-Addoor 是一个为 ComfyUI 设计的自定义节点插件包，提供了各种文件操作和数据处理的实用功能。

## 功能和使用注意事项

1. 🌻 批量从目录加载图片 (AD_BatchImageLoadFromDir)
   - 从指定目录加载多张图片。
   - 输入：
     - Directory：包含图片的文件夹路径。
     - Load_Cap：要加载的最大图片数量。
     - Skip_Frame：开始加载前要跳过的图片数量。
   - 输出：加载的图片、图片路径、图片名称和数量。
   - 注意：支持多种图片格式，包括 jpg、jpeg、png、bmp、gif 和 webp。

2. 🌻 删除本地任意文件 (AD_DeleteLocalAny)
   - 删除指定的文件或目录。
   - 输入：
     - Any：要删除的文件或目录路径。
     - File_Name：可选的特定文件名，用于在目录中删除。
   - 输出：操作状态和已删除的文件路径。
   - 注意：请谨慎使用，因为删除操作是永久性的。

3. 🌻 文本列表转字符串 (AD_TextListToString)
   - 从目录加载文本文件并合并其内容。
   - 输入：
     - Directory：包含文本文件的文件夹路径。
     - Load_Cap：要加载的最大文件数量。
     - Skip_Frame：开始加载前要跳过的文件数量。
   - 输出：文件名、内容、路径和合并后的内容。
   - 注意：支持 txt 和 csv 文件。

4. 🌻 任意文件列表 (AD_AnyFileList)
   - 列出目录中的文件，具有各种过滤选项。
   - 输入：
     - Directory：要搜索文件的路径。
     - Load_Cap：要列出的最大文件数量。
     - Skip_Frame：开始列出前要跳过的文件数量。
     - Filter_By：文件类型过滤器（如图片、文本）。
     - Extension：要过滤的特定文件扩展名。
     - Deep_Search：是否搜索子目录。
   - 输出：文件路径、名称和内容（对于支持的文件类型）。
   - 注意：用于文件管理和内容提取的多功能节点。

5. 🌻 Zip 保存 (AD_ZipSave)
   - 创建指定目录的 zip 压缩文件。
   - 输入：
     - Input_Directory：要压缩的目录。
     - Output_Directory：保存 zip 文件的位置。
     - Zip_Filename：输出 zip 文件的名称。
   - 输出：创建的 zip 文件路径和操作状态。
   - 注意：适用于备份或一次性共享多个文件。

6. 🌻 图像保存器 (AD_ImageSaver)
   - 将图像保存到指定目录，具有可自定义的命名。
   - 输入：
     - Images：要保存的图像数据。
     - Directory：保存图像的位置。
     - Filename_Prefix：保存的图像文件名前缀。
     - Open_Output_Directory：保存后是否打开输出文件夹。
   - 输出：保存的图像路径。
   - 注意：支持元数据保存和自动文件编号。

7. 🌻 Flux 训练步骤计算 (AD_FluxTrainStepMath)
   - 计算机器学习模型的训练步骤。
   - 输入：
     - Material_Count：训练材料数量。
     - Training_Times_Per_Image：每张图像的训练次数。
     - Epoch：训练的轮数。
     - equation：自定义步骤计算公式。
   - 输出：总训练步骤和每轮步骤数。
   - 注意：用于规划和优化训练过程。

8. 🌻 文本保存器 (AD_TextSaver)
   - 将文本内容保存到文件，具有可自定义的命名和格式。
   - 输入：
     - text：要保存的内容。
     - directory：保存文本文件的位置。
     - filename_prefix：保存的文件名前缀。
     - filename_delimiter：前缀和编号之间使用的字符。
     - filename_number_padding：文件编号的位数。
     - file_extension：保存文件的扩展名。
     - encoding：文本编码（默认 UTF-8）。
   - 输出：保存的文本文件路径。
   - 注意：支持在目录和文件名前缀中使用基于时间的标记。

9. 🌻 提示词替换 (AD_PromptReplace)
   - 根据指定条件和随机选择替换提示词中的文本。
   - 输入：
     - Content：要处理的主要文本内容。
     - Match：要替换的文本。
     - Replace：用于替换匹配内容的文本。
     - seed：随机选择的种子。
     - Increment：种子的增量值。
     - Random_Mode：行选择模式（正常、反向、奇数/偶数正向/反向）。
   - 输出：替换后的文本和新的种子值。
   - 注意：适用于创建提示词或文本内容的变体，具有可控的随机性。

## 安装

1. 将 `ComfyUI-Addoor` 文件夹复制到 ComfyUI 安装目录中的 `custom_nodes` 目录。
2. 确保已安装所需的依赖项（参见 `requirements.txt`）。
3. 重启 ComfyUI。

## 使用

安装后，新节点将在 ComfyUI 界面的 "Addoor" 类别下可用。请参考上面的功能描述以了解每个节点的具体用法。

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。

