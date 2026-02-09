# BiliDigest 🎬

**BiliDigest** 是一个简单实用的 B 站视频知识化工具。它能自动完成“下载、转录、校对、总结”全流程，帮助你将喜欢的视频快速转化为高质量的结构化笔记。

[English Description](#english-description) | [中文说明](#中文说明)

---

<a name="english-description"></a>

## English Description

BiliDigest is an automated tool designed to transform Bilibili videos into organized personal knowledge. 

### Key Features:

- **Automated Extraction**: Downloads audio directly from Bilibili links.
- **Local Transcription**: Uses OpenAI Whisper (locally) for speech-to-text.
- **AI Correction**: Automatically fixes transcription typos using DeepSeek (via SiliconFlow API).
- **Deep Summary**: Generates structured, detailed summaries proportional to the video length.
- **Knowledge Base**: Organizes files into folders and provides a built-in browser for retrieval.

---

<a name="中文说明"></a>

## 中文说明

BiliDigest 是一个帮助你将 B 站视频高效化为个人知识的自动化工具。

### 核心功能：

- **自动化提取**：输入链接，自动提取 B 站视频的最佳音质音频。
- **本地化转录**：调用 OpenAI Whisper 模型在本地进行语音转文字，隐私安全且免费。
- **AI 文稿校对**：调用 DeepSeek 模型智能修正转录中的同音错别字，输出完整校对稿。
- **深度总结**：根据视频时长自动调整详实度，生成包含大纲、要点详解与金句的深度报告。
- **知识库管理**：采用“一视频一文件夹”存储，支持在网页端直接检索和预览历史记录。

![产品界面图](assets/preview.png)

---

## 🛠️ 前置准备 (Prerequisites)

在运行本项目之前，请确保你的电脑已安装 **FFmpeg**：

1. **下载 FFmpeg**: [官方下载地址](https://ffmpeg.org/download.html)
2. **安装说明**:
   - **Windows**: 下载并解压，将 `bin` 文件夹路径添加到系统环境变量 `PATH` 中。
   - **Mac**: 执行 `brew install ffmpeg`
   - **Linux**: 执行 `sudo apt install ffmpeg`
3. **验证**: 在终端输入 `ffmpeg -version` 有显示即表示成功。

---

## 🚀 安装步骤 (Installation)

你可以选择直接安装到系统环境，或使用虚拟环境。

### 1. 克隆项目

```bash
git clone https://github.com/syn3024/BiliDigest.git
cd BiliDigest
```

### 2. 安装依赖 (使用清华镜像源加速)

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 安装 GPU 版 PyTorch (强烈建议 NVIDIA 显卡用户安装)

若不安装此项，Whisper 将在 CPU 上运行，速度较慢：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 📝 使用方法 (Usage)

### 快速启动 (Windows 推荐)

在根目录下找到 **`start.bat`**，直接双击运行即可。

### 手动启动

```bash
streamlit run app.py
```

### 浏览器访问

程序运行后，在浏览器打开：`http://localhost:8501`

### 操作流程

1. **侧边栏配置**: 填写你的 **SiliconFlow API Key**（默认已填充公测 Key，建议换成自己的）。
2. **处理视频**: 在文本框粘贴 B 站链接（支持批量），点击“开始任务”。
3. **查阅结果**: 切换到“内容浏览器”标签页，点击左侧历史记录即可直接阅读。

---

## 📂 项目结构 (Structure)

```text
BiliDigest/
├── app.py                # 程序主逻辑 (Streamlit UI)
├── start.bat             # Windows 一键启动脚本
├── requirements.txt      # 依赖库列表
├── README.md             # 项目说明文档
└── My_Knowledge_Base/    # 个人知识库 (自动创建)
    └── 视频标题/
        ├── audio_source.mp3  # 提取的原始音频
        ├── 标题_修正.txt      # AI 校对后的完整文稿
        └── 标题_总结.md      # AI 生成的深度总结报告
```

---

## ⚠️ 注意事项 (Notes)

- **首次运行**: Whisper 模型（如 `small`）在第一次使用时会自动下载（约几百 MB），请确保网络畅通。
- **API 限制**: 如果视频极长（超过 30 分钟），API 调用可能会消耗较多 Token，程序已内置分段校对逻辑以防止截断。
- **yt-dlp 更新**: B 站协议变动可能导致解析失败，若报错请运行 `pip install -U yt-dlp`。

---

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request 来协助完善 BiliDigest！
