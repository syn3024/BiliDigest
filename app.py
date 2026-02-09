import streamlit as st
import os
import re
import time
import yt_dlp
import whisper
import requests

# ================= 1. 配置与常量 =================
DEFAULT_API_KEY = "sk-xxx"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"


# ================= 2. 核心工具函数 =================

def sanitize_filename(filename):
    """极致清洗：去除Windows非法字符，并强行删掉结尾的空格和点"""
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    filename = filename.strip().rstrip('.')
    return filename


def get_video_info(url):
    """获取视频标题"""
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'untitled')


def ai_call(system_prompt, user_content, api_key, model_name, max_tokens=4000):
    """通用 AI 调用函数"""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.5,
        "max_tokens": max_tokens,
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 调用失败: {str(e)}"


# ================= 3. AI 业务指令 =================

def correct_transcript(text, api_key, model_name):
    """
    分段修正逻辑：解决长文本截断问题
    """
    # 每段处理的字符数（建议3000-4000字，保证修正后不超限）
    chunk_size = 3000
    # 将文本切分为列表
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    corrected_chunks = []
    progress_bar = st.progress(0)

    for idx, chunk in enumerate(chunks):
        st.write(f"正在校对第 {idx + 1}/{len(chunks)} 段文本...")

        system_prompt = (
            "你是一个文本重写机器。你的唯一任务是输出修正后的全文。\n"
            "【严格禁令】：\n"
            "1. 严禁输出开场白或解释说明。\n"
            "2. 严禁输出修改记录清单。\n"
            "3. 严禁删减内容，必须保持原文语序。\n"
            "请直接输出修正后的文本。"
        )
        # 强制要求不要解释，直接返回原文修正版
        user_prompt = f"请修正以下文本的错别字：\n\n{chunk}"

        # 调用 AI
        corrected_part = ai_call(system_prompt, user_prompt, api_key, model_name, max_tokens=4000)

        # 简单清洗：有些AI还是会忍不住输出“好的，这是修正版：”，我们要把它切掉
        clean_part = re.sub(r'^(好的|这是|修正|以下).*?：\n*', '', corrected_part).strip()

        corrected_chunks.append(clean_part)
        progress_bar.progress((idx + 1) / len(chunks))

    return "\n".join(corrected_chunks)


def generate_summary(text, api_key, model_name):
    """使用详实的 Prompt 生成深度总结报告"""
    system_prompt = "你是一位专业的内容分析师和文案专家，擅长将长篇视频转录文本提炼为逻辑严密、细节丰富的深度摘要。"
    user_prompt = f"""
# 任务
请对提供的视频转录文本进行深度解析。你的目标是：根据原文的长度和信息量，按比例生成对应详实度的报告。
原文越长，你的总结应当越细致，严禁过度压缩细节。

# 输出要求
1. **核心主旨**：用一句话精准概括视频核心目的。
2. **详实程度标准**：
   - 保持高信息密度。
   - 如果原文内容丰富，请务必保留关键的逻辑推导过程、具体的案例、重要的数据和金句。
   - 总结字数应与原文长度正相关（目标：每分钟原视频内容对应约 50-80 字的精选总结）。
3. **结构化呈现**：
   - **【内容大纲】**：按逻辑或时间顺序，分章节/分阶段列出视频讲述的内容。
   - **【要点详解】**：对每个章节进行细致展开，不仅列出结论，还要简述其背后的理由、细节或操作步骤。
   - **【核心金句/关键结论】**：提取视频中最具价值的 3-5 句话。

# 待总结的视频转录文本：
{text}
"""
    # 详实总结需要更多的输出空间，设置为 4000
    return ai_call(system_prompt, user_prompt, api_key, model_name, max_tokens=40000)


# ================= 4. UI 界面布局 =================

st.set_page_config(page_title="B站 AI 知识库", page_icon="📚", layout="wide")

# 初始化浏览状态
if "view_data" not in st.session_state:
    st.session_state.view_data = None

# --- 侧边栏 ---
with st.sidebar:
    st.title("⚙️ 系统配置")
    api_key = st.text_input("SiliconFlow API Key", value=DEFAULT_API_KEY, type="password")
    save_root = st.text_input("📁 存储库根目录", value=os.path.join(os.getcwd(), "My_Knowledge_Base"))
    model_choice = st.selectbox("AI 模型", ["deepseek-ai/DeepSeek-V3", "deepseek-ai/DeepSeek-R1"])
    whisper_size = st.selectbox("Whisper 模型", ["tiny", "base", "small", "medium"], index=2)

    st.divider()
    st.title("📂 历史库检索")

    if os.path.exists(save_root):
        # 扫描文件夹
        folders = [f for f in os.listdir(save_root) if os.path.isdir(os.path.join(save_root, f))]
        folders.sort(key=lambda x: os.path.getmtime(os.path.join(save_root, x)), reverse=True)

        search_q = st.text_input("🔍 搜索视频...")
        for folder in folders:
            if search_q.lower() in folder.lower():
                if st.button(folder, key=folder, use_container_width=True):
                    f_path = os.path.join(save_root, folder)
                    content = {"title": folder}
                    for f in os.listdir(f_path):
                        if f.endswith("总结.md"):
                            with open(os.path.join(f_path, f), "r", encoding="utf-8") as file:
                                content["summary"] = file.read()
                        if f.endswith("修正.txt"):
                            with open(os.path.join(f_path, f), "r", encoding="utf-8") as file:
                                content["transcript"] = file.read()
                    st.session_state.view_data = content
    else:
        st.info("暂无数据。")

# --- 主界面 ---
tab1, tab2 = st.tabs(["🚀 处理新视频", "📖 内容浏览器"])

with tab1:
    urls_input = st.text_area("输入B站链接（每行一个）", height=150, placeholder="https://www.bilibili.com/video/BV...")

    if st.button("开始批量任务"):
        if not api_key or not urls_input.strip():
            st.error("请完善配置和链接")
        else:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]

            # 加载 Whisper (放在循环外只加载一次)
            with st.spinner(f"正在准备 Whisper {whisper_size} 模型..."):
                model = whisper.load_model(whisper_size)

            for url in urls:
                with st.status(f"处理中: {url}") as status:
                    try:
                        # 1. 获取标题与路径管理 (修复分身文件夹)
                        raw_title = get_video_info(url)
                        safe_title = sanitize_filename(raw_title)
                        video_folder = os.path.abspath(os.path.join(save_root, safe_title))
                        os.makedirs(video_folder, exist_ok=True)

                        # 2. 下载音频 (固定内部文件名)
                        st.write("📥 提取音频...")
                        inner_name = "audio_source"
                        out_tmpl = os.path.join(video_folder, inner_name)
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'postprocessors': [
                                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                            'outtmpl': out_tmpl,
                            'quiet': True,
                            'restrictfilenames': True,  # 强制安全命名
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])

                        audio_path = os.path.abspath(out_tmpl + ".mp3")

                        # 防御性检查
                        if not os.path.exists(audio_path):
                            st.warning("预期路径未找到音频，尝试自动捕捉...")
                            all_mp3s = [f for f in os.listdir(video_folder) if f.endswith(".mp3")]
                            if all_mp3s: audio_path = os.path.join(video_folder, all_mp3s[0])

                        # 3. Whisper 转写
                        st.write("🎙️ 语音转文字...")
                        raw_res = model.transcribe(audio_path)
                        raw_text = raw_res["text"]

                        # 4. AI 文本校对 (强制输出全文)
                        st.write("✨ AI 正在校对全文...")
                        corrected_text = correct_transcript(raw_text, api_key, model_choice)
                        with open(os.path.join(video_folder, f"{safe_title}_修正.txt"), "w", encoding="utf-8") as f:
                            f.write(corrected_text)

                        # 5. AI 详实总结
                        st.write("🧠 AI 正在生成详实总结报告...")
                        summary = generate_summary(corrected_text, api_key, model_choice)
                        with open(os.path.join(video_folder, f"{safe_title}_总结.md"), "w", encoding="utf-8") as f:
                            f.write(f"# {raw_title}\n\n链接: {url}\n\n{summary}")

                        status.update(label=f"✅ 完成: {raw_title}", state="complete")
                    except Exception as e:
                        st.error(f"处理失败 {url}: {str(e)}")

            st.success("批量处理结束！")
            st.rerun()

with tab2:
    if st.session_state.view_data:
        vd = st.session_state.view_data
        st.title(vd["title"])
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("📝 详实总结报告")
            st.markdown(vd.get("summary", "暂无总结内容"))
        with c2:
            st.subheader("📜 校对后的全文文稿")
            st.text_area("内容预览", vd.get("transcript", "暂无文稿内容"), height=800)
    else:
        st.info("👈 请从左侧侧边栏选择历史记录进行查看。")