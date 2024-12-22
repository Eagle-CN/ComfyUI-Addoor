<p align="center">
  <a href="https://github.com/Eagle-CN/ComfyUI-Addoor" target="blank">
    <img src="https://i.ibb.co/6nJzL9n/1.png" alt="Logo" width="156" height="156">
  </a>
  <h2 align="center" style="font-weight: 600">葵花宝典</h2>

  <p align="center">
    ComfyUI的强大插件
    <br />
    <a href="https://github.com/Eagle-CN/ComfyUI-Addoor" target="blank"><strong>📘 查看文档</strong></a>&nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="#%EF%B8%8F-安装" target="blank"><strong>📦️ 下载安装</strong></a>&nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="https://github.com/Eagle-CN/ComfyUI-Addoor/issues" target="blank"><strong>🐛 报告Bug</strong></a>
    <br />
    <br />
  </p>
</p>

## ✨ 特性

- 🔄 CSV读取和处理
- 📁 批量图片加载和文件操作
- 🗜️ ZIP文件创建
- 💾 图像和文本保存
- 🧮 训练步骤计算
- 🔄 提示词替换和样式化
- 🌐 Hugging Face模型下载
- 🎨 图像颜色滤镜
- 📊 文本到CSV转换
- 🟨 图像绘制矩形
- 🌁 高级图像加载
- 🆔 图像索引器
- ...更多功能正在开发中！

## 📦️ 安装

1. 确保你已经安装了ComfyUI。
2. 克隆本仓库到ComfyUI的`custom_nodes`目录：

```sh
cd ComfyUI/custom_nodes
git clone https://github.com/Eagle-CN/ComfyUI-Addoor.git
```

3. 安装依赖：

```sh
cd ComfyUI-Addoor
pip install -r requirements.txt
```

4. 重启ComfyUI，葵花宝典的节点将出现在节点列表中。
5. 使用中文本地化：
   1. 下载 `addoor_zh.json` 文件。
   2. 将其放置在 `/ComfyUI/custom_nodes/AIGODLIKE-COMFYUI-TRANSLATION/zh-CN/Nodes` 目录下。
   3. 重启 ComfyUI。

## 🚀 使用方法

葵花宝典为ComfyUI添加了多个新节点，每个节点都有特定的功能：

1. **CSV读取器**：读取和处理CSV文件。
2. **批量图片加载**：从指定目录批量加载图片。
3. **文件删除**：删除指定的文件或目录。
4. **文本列表转换**：将文本文件列表转换为字符串。
5. **文件列表**：列出目录中的文件，支持多种过滤选项。
6. **ZIP保存**：创建ZIP压缩文件。
7. **图像保存器**：保存图像到指定目录。
8. **训练步骤计算**：计算机器学习模型的训练步骤。
9. **文本保存器**：保存文本内容到文件。
10. **提示词替换**：替换文本中的特定内容。
11. **Hugging Face下载**：从Hugging Face下载模型或数据集。
12. **图像颜色滤镜**：应用各种颜色调整和滤镜效果。
13. **CSV提示词样式器**：使用CSV文件中的样式美化提示词。
14. **文本到CSV合并器**：将多个文本文件合并为一个CSV文件。
15. **图像绘制矩形**：在图像上绘制简单的矩形。
16. **高级图像加载**：具有附加选项的高级图像加载。
17. **图像索引器**：从批量图像中索引和选择图像。

每个节点都可以在ComfyUI的界面中找到，并可以与其他节点连接以创建复杂的工作流。

## 📘 节点说明和注意事项

1. **CSV读取器 (AD_CSVReader)**
   - 说明：读取CSV文件并输出其内容。
   - 注意：支持选择特定列和随机行选择。

2. **批量图片加载 (AD_BatchImageLoadFromDir)**
   - 说明：从指定目录批量加载图片。
   - 注意：支持多种图片格式，包括jpg、jpeg、png、bmp、gif和webp。

3. **文件删除 (AD_DeleteLocalAny)**
   - 说明：删除指定的文件或目录。
   - 注意：使用时要小心，删除操作是永久性的。

4. **文本列表转换 (AD_TextListToString)**
   - 说明：加载文本文件并合并其内容。
   - 注意：支持txt和csv文件。

5. **文件列表 (AD_AnyFileList)**
   - 说明：列出目录中的文件，具有各种过滤选项。
   - 注意：可用于文件管理和内容提取。

6. **ZIP保存 (AD_ZipSave)**
   - 说明：创建指定目录的zip压缩文件。
   - 注意：适用于备份或一次性共享多个文件。

7. **图像保存器 (AD_ImageSaver)**
   - 说明：将图像保存到指定目录，具有可自定义的命名。
   - 注意：支持元数据保存和自动文件编号。

8. **训练步骤计算 (AD_FluxTrainStepMath)**
   - 说明：计算机器学习模型的训练步骤。
   - 注意：用于规划和优化训练过程。

9. **文本保存器 (AD_TextSaver)**
   - 说明：将文本内容保存到文件，具有可自定义的命名和格式。
   - 注意：支持在目录和文件名前缀中使用基于时间的标记。

10. **提示词替换 (AD_PromptReplace)**
    - 说明：根据指定条件和随机选择替换提示词中的文本。
    - 注意：适用于创建提示词或文本内容的变体，具有可控的随机性。

11. **Hugging Face下载 (AD_HFDownload)**
    - 说明：从Hugging Face下载模型或数据集。
    - 注意：支持使用镜像站点和身份验证。

12. **图像颜色滤镜 (AD_ImageColorFilter)**
    - 说明：对图像应用各种颜色调整和滤镜效果。
    - 注意：提供全面的图像颜色和质量调整功能。

13. **CSV提示词样式器 (AD_CSVPromptStyler)**
    - 说明：使用CSV文件中定义的样式来美化提示词。
    - 注意：可以轻松应用预定义的提示词样式。

14. **文本到CSV合并器 (AD_TxtToCSVCombiner)**
    - 说明：将多个文本文件合并为一个CSV文件。
    - 注意：支持文件排序和可选的表头添加。

15. **图像绘制矩形 (AD_ImageDrawRectangleSimple)**
   - 说明：在图像上绘制具有可自定义属性的简单矩形。
   - 注意：允许调整矩形的位置、大小、颜色和不透明度。

16. **高级图像加载 (AD_LoadImageAdvanced)**
   - 说明：使用高级选项和附加输出加载图像。
   - 注意：提供更多图像加载控制，包括蒙版生成和文件名输出。

17. **图像索引器 (AD_ImageIndexer)**
   - 说明：从输入的图像批次中索引和选择图像。
   - 注意：适用于循环浏览或从较大集合中随机选择图像。


## 🤝 贡献

欢迎贡献代码、报告问题或提出新功能建议！请查看我们的[贡献指南](CONTRIBUTING.md)了解更多信息。

## 📜 许可证

本项目采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 🙏 致谢

- 感谢ComfyUI团队创建了如此强大的框架。
- 感谢所有为本项目做出贡献的开发者。

yuan

