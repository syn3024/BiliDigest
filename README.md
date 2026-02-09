# BiliDigest 🎬

**BiliDigest** 是一个简单实用的 B 站视频知识化工具。它能自动完成“下载、转录、校对、总结”全流程，帮助你将喜欢的视频快速转化为高质量的结构化笔记。

---

## English Description

BiliDigest is an automated tool designed to transform Bilibili videos into organized personal knowledge.

### Key Features:

- **Automated Extraction**: Downloads audio directly from Bilibili links.
- **Local Transcription**: Uses OpenAI Whisper (locally) for speech-to-text.
- **AI Correction**: Automatically fixes transcription typos and technical terms using DeepSeek (via SiliconFlow API).
- **Deep Summary**: Generates structured, detailed summaries proportional to the video length.
- **Knowledge Base**: Organizes files into "one folder per video" and provides a built-in browser for historical retrieval.

---

## 中文说明

BiliDigest 是一个帮助你将 B 站视频高效内化为个人知识的自动化工具。

### 核心功能：

- **自动化提取**：输入 B 站链接，自动提取最佳音质音频。
- **本地化转录**：调用 OpenAI Whisper 模型在本地进行语音转文字，隐私安全且免费。
- **AI 文稿校对**：调用 DeepSeek 模型智能修正转录中的同音错别字与专有名词。
- **深度总结**：根据视频字数自动调整详实度，生成包含大纲、要点详解与金句的报告。
- **知识库管理**：采用“一视频一文件夹”的存储方式，支持在网页端直接检索和浏览历史记录。

---

## 🛠️ 前置准备 (Prerequisites)

在运行本项目之前，请确保你的电脑已安装以下非 Python 工具：

1. **FFmpeg** (必须):
  
  - 用于音频提取和 Whisper 转录。
  - **Windows**: 下载并解压，将 `bin` 文件夹路径添加到系统环境变量 `PATH` 中。
  - **Mac**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg`
2. **NVIDIA GPU 驱动** (推荐):
  
  - 若要使用显卡加速转录，请确保已安装 NVIDIA 驱动。

---

## 🚀 安装步骤 (Installation)

1. **克隆项目**:
  
  ```bash
  git clone https://github.com/syn3024/BiliDigest.git
  cd BiliDigest
  ```
  
2. **创建虚拟环境**:
  
  ```bash
  python -m venv .venv
  # 激活环境 (Windows)
  .venv\Scripts\activate
  # 激活环境 (Linux/Mac)
  source .venv/bin/activate
  ```
  
3. **安装依赖**:
  
  ```bash
  pip install -r requirements.txt
  ```
  
4. **安装 GPU 版 PyTorch (强烈推荐)**:
  如果你有 NVIDIA 显卡，请运行以下命令以启用 GPU 加速：
  
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```
  

---

## 📝 使用方法 (Usage)

### 快速启动 (One-click Start)

- **Windows**: 在完成上述安装步骤后，直接双击项目根目录下的 **`start.bat`** 即可一键启动。
- 程序启动后将运行在浏览器：**`http://localhost:8501`**

### 手动启动 (Manual Start)

```bash
streamlit run app.py
```

### 操作流程

1. **配置参数**: 在网页侧边栏输入你的 **SiliconFlow API Key**。
2. **开始处理**: 在输入框粘贴 B 站视频链接（支持批量），点击“开始批量任务”。
3. **浏览结果**: 处理完成后，切换到“内容浏览器”标签页，点击左侧历史记录即可直接查看。

---

## 📂 项目结构 (Structure)

```text
BiliDigest/
├── app.py                # 程序主逻辑 (Streamlit UI)
├── start.bat             # Windows 一键启动脚本
├── requirements.txt      # 依赖库列表
├── README.md             # 项目说明文档
└── My_Knowledge_Base/    # 默认存储库 (自动创建)
    └── 视频标题/
        ├── audio_source.mp3  # 提取的原始音频
        ├── 标题_修正.txt      # AI 校对后的全文稿
        └── 标题_总结.md      # AI 生成的深度总结报告
```

---

## ⚠️ 注意事项 (Notes)

- **环境要求**: `start.bat` 脚本默认调用 `.venv` 文件夹中的 Python 环境，请确保已按安装步骤创建。
- **API 安全**: 请勿将包含 API Key 的代码上传至公开仓库。本项目已默认留空。
- **Whisper 模型**: 首次运行选定模型时，程序会自动下载模型文件，请保持网络畅通。
- **yt-dlp 更新**: 若遇到链接解析失败，请尝试运行 `pip install -U yt-dlp`。

---

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request 来完善这个项目！
