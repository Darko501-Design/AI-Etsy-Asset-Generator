import streamlit as st
import google.generativeai as genai
import requests
import os
import urllib.parse
import time

# 1. CIVITAI-STYLE HIGH-TECH DARK THEME (Custom CSS Overrides)
st.set_page_config(page_title="AI Etsy Asset Generator V.0 (demo)", page_icon="🎨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&family=Kanit:wght@300;400;600&display=swap');

/* พื้นหลังหลักและฟอนต์สไตล์ Civitai */
.stApp {
    background-color: #0b0c10;
    color: #e4e6eb;
    font-family: 'Inter', 'Kanit', sans-serif;
}

/* หัวข้อหลักแบบมินิมอลแต่ทรงพลัง */
h1 {
    color: #ffffff !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 15px rgba(124, 58, 237, 0.4) !important;
    text-align: center;
    margin-bottom: 0.5rem !important;
}

h2, h3 {
    color: #ffffff !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #2e303e;
    padding-bottom: 8px;
    margin-top: 1.5rem !important;
}

/* ฟอร์มและกล่องคอนเทนเนอร์สไตล์ Civitai Card */
[data-testid="stForm"] {
    border: 1px solid #2e303e !important;
    background-color: #161822 !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
    padding: 2rem !important;
}

/* ปรับแต่งปุ่มกดหลัก (Civitai Accent Button) */
button[kind="primaryFormSubmit"], .stButton > button {
    background-color: #7c3aed !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', 'Kanit', sans-serif;
    padding: 0.6rem 2rem !important;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100%;
}

button[kind="primaryFormSubmit"]:hover, .stButton > button:hover {
    background-color: #9061f9 !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.6) !important;
    transform: translateY(-2px);
}

/* แผงควบคุมด้านข้าง (Sidebar) */
section[data-testid="stSidebar"] {
    background-color: #11121a !important;
    border-right: 1px solid #2e303e !important;
}

/* กล่องแสดงผลรูปภาพสไตล์การ์ดแสดงผลงาน Civitai */
[data-testid="stImage"] {
    border-radius: 12px !important;
    border: 1px solid #2e303e !important;
    background-color: #1a1b23 !important;
    padding: 8px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-testid="stImage"]:hover {
    transform: translateY(-5px) !important;
    border-color: #7c3aed !important;
    box-shadow: 0 12px 25px rgba(124, 58, 237, 0.4) !important;
}

/* ช่องกรอกข้อความและ Selectbox */
div[data-baseweb="input"], div[data-baseweb="select"] {
    background-color: #1f202e !important;
    border: 1px solid #3a3f58 !important;
    border-radius: 8px !important;
    transition: border-color 0.2s ease;
}

div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
    border-color: #7c3aed !important;
}

input, select, textarea {
    color: #ffffff !important;
}

/* กล่องแสดงโค้ดคำอธิบายแบบเรียบหรู */
code {
    background-color: #0f1015 !important;
    color: #10b981 !important; /* สีเขียวมิ้นต์แบบโมเดิร์น */
    border-left: 4px solid #7c3aed !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 4px;
}

/* การตกแต่งสัญลักษณ์พิเศษ */
.badge {
    background-color: #2e303e;
    color: #a0aec0;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# 2. พจนานุกรมแปลภาษา (TH / EN)
translations = {
    "TH": {
        "title": "🎨 AI Etsy Asset Generator V.0 (demo)",
        "subtitle": "สร้างเนื้อหาและภาพประกอบสำหรับลงขายบน Etsy โดยอัตโนมัติด้วยพลังของ **Gemini 2.5**",
        "settings": "⚙️ ตั้งค่าระบบ (Settings)",
        "api_key_found": "✅ ตรวจพบ API Key ในระบบแล้ว พร้อมใช้งาน!",
        "api_key_input": "กรอก Google Gemini API Key:",
        "api_key_help": "💡 หรือบันทึกไว้ในไฟล์ `API Key/API_KEY.txt` เพื่อล็อกอินอัตโนมัติ",
        "instructions_header": "💡 ขั้นตอนการใช้งาน:",
        "instructions": "1. ป้อนไอเดียสินค้าในช่องขวา\n2. เลือกขนาด (Aspect Ratio) และจำนวนภาพ\n3. กดปุ่ม '🚀 สร้างสินค้า' หรือกดปุ่ม Enter บนแป้นพิมพ์",
        "idea_label": "💡 ไอเดียสินค้าของคุณ (เช่น สติกเกอร์น้องแมวอวกาศ, ลายดอกไม้สีน้ำวินเทจ):",
        "idea_placeholder": "พิมพ์ไอเดียของคุณที่นี่...",
        "ratio_label": "📐 เลือกขนาดอัตราส่วนภาพ (Aspect Ratio):",
        "count_label": "🖼️ จำนวนรูปภาพที่ต้องการเจน (1-8 รูป):",
        "btn_generate": "🚀 สร้างสรรค์สินค้า",
        "err_no_key": "⚠️ ไม่พบ API Key กรุณากรอกที่แถบด้านซ้าย หรือจัดเก็บในไฟล์ระบบครับ",
        "err_no_idea": "⚠️ กรุณากรอกไอเดียสินค้าของคุณก่อนครับ",
        "spinner_text": "⏳ กำลังให้ Gemini วิเคราะห์และเขียนรายละเอียดสินค้า (Title, Description, Tags)...",
        "spinner_img": "⏳ กำลังดาวน์โหลดและประมวลผลรูปภาพที่ {idx} จาก {total}...",
        "success_text": "✨ ข้อมูลสินค้าเขียนเสร็จแล้ว! กำลังโหลดรูปภาพทั้งหมด...",
        "img_header": "🖼️ แกลเลอรี่ภาพผลงาน ({count} รูป)",
        "listing_header": "📝 ข้อมูลสำหรับนำไปคัดลอกลงร้านค้า Etsy",
        "title_label": "📋 ชื่อสินค้าแนะนำสำหรับ SEO (Title)",
        "desc_label": "📋 คำอธิบายสินค้า (Description)",
        "tags_label": "🏷️ คีย์เวิร์ดสำหรับแท็กค้นหา (Tags 13 คำ)",
        "prompt_used": "💡 Prompt วาดภาพที่ Gemini ออกแบบให้สำหรับใช้วาดรูปนี้:",
    },
    "EN": {
        "title": "🎨 AI Etsy Asset Generator V.0 (demo)",
        "subtitle": "Generate complete Etsy listings and illustrations automatically with **Gemini 2.5**",
        "settings": "⚙️ Settings",
        "api_key_found": "✅ API Key loaded from system. Ready!",
        "api_key_input": "Enter Google Gemini API Key:",
        "api_key_help": "💡 Or save it in `API Key/API_KEY.txt` to auto-login next time.",
        "instructions_header": "💡 Simple Steps:",
        "instructions": "1. Type your product idea on the right.\n2. Choose aspect ratio and image count.\n3. Click '🚀 Generate' or press Enter!",
        "idea_label": "💡 Your Product Idea (e.g., cute space cat stickers, watercolor floral pattern):",
        "idea_placeholder": "Type your product idea here...",
        "ratio_label": "📐 Aspect Ratio:",
        "count_label": "🖼️ Number of Images to Generate (1-8):",
        "btn_generate": "🚀 Generate Etsy Assets",
        "err_no_key": "⚠️ API Key not found. Please enter it in the sidebar or save to `API Key/API_KEY.txt`.",
        "err_no_idea": "⚠️ Please enter a product idea first.",
        "spinner_text": "⏳ Gemini is writing SEO Title, Description, and Image Prompts...",
        "spinner_img": "⏳ Downloading and rendering image #{idx} of {total}...",
        "success_text": "✨ Listing text generated! Rendering all images now...",
        "img_header": "🖼️ Product Gallery ({count} images)",
        "listing_header": "📝 Etsy Listing Details",
        "title_label": "📋 SEO Optimized Product Title",
        "desc_label": "📋 Product Description",
        "tags_label": "🏷️ Search Tags (13 Keywords)",
        "prompt_used": "💡 Image Prompt written by Gemini:",
    }
}

# 3. ขนาดพิกเซลตามอัตราส่วนภาพ
aspect_ratios = {
    "1:1 (Square)": (1024, 1024),
    "3:4 (Portrait)": (768, 1024),
    "4:3 (Landscape)": (1024, 768),
    "16:9 (Widescreen)": (1024, 576),
    "9:16 (Story)": (576, 1024),
    "4:6 (Etsy Print)": (680, 1020),
    "3:5 (Tall Poster)": (600, 1000)
}

# ฟังก์ชันดาวน์โหลดรูปภาพแบบมี Retry ป้องกันภาพมาไม่ครบ
def fetch_image_bytes(url):
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200 and len(r.content) > 5000:
                return r.content
        except Exception:
            pass
        time.sleep(1)
    return None

# 4. ตั้งค่า Sidebar
with st.sidebar:
    lang_choice = st.radio("🌐 Language / ภาษา", ["🇺🇸 English", "🇹🇭 ไทย"], horizontal=True)
    lang_code = "TH" if lang_choice == "🇹🇭 ไทย" else "EN"
    t = translations[lang_code]
    
    st.divider()
    st.header(t["settings"])
    
    api_key = ""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    api_key_file = os.path.join(script_dir, "API Key", "API_KEY.txt")

    if os.path.exists(api_key_file):
        with open(api_key_file, "r", encoding="utf-8") as f:
            api_key = f.read().strip()

    if api_key:
        st.success(t["api_key_found"])
    else:
        api_key = st.text_input(t["api_key_input"], type="password")
        st.markdown(t["api_key_help"])
    
    st.divider()
    st.markdown(f"### {t['instructions_header']}")
    st.markdown(t["instructions"])

# 5. ส่วนควบคุมหน้าจอหลัก
st.title(t["title"])
st.markdown(f"<p style='text-align: center; color: #a0aec0; margin-bottom: 2rem;'>{t['subtitle']}</p>", unsafe_allow_html=True)

# ระบบฟอร์มรับข้อมูล (พิมพ์เสร็จแล้วเคาะ Enter ได้เลย)
with st.form(key="generator_form"):
    idea = st.text_input(t["idea_label"], placeholder=t["idea_placeholder"])
    
    col_opt1, col_opt2 = st.columns([1, 1])
    with col_opt1:
        ratio_name = st.selectbox(t["ratio_label"], list(aspect_ratios.keys()))
    with col_opt2:
        image_count = st.slider(t["count_label"], 1, 8, 4)
        
    submit_button = st.form_submit_button(label=t["btn_generate"])

# 6. ประมวลผลและแสดงผลลัพธ์
if submit_button:
    if not api_key:
        st.error(t["err_no_key"])
    elif not idea:
        st.error(t["err_no_idea"])
    else:
        try:
            genai.configure(api_key=api_key.strip())
            
            # เรียกใช้งาน Gemini 2.5-flash
            with st.spinner(t["spinner_text"]):
                model = genai.GenerativeModel('gemini-2.5-flash') 
                prompt = f"""
                You are an expert Etsy seller and AI Prompt Engineer. I want to sell a digital product based on this idea: "{idea}".
                Please generate the following for my Etsy listing in English.
                Format the output strictly using these exact headers:
                
                **TITLE**
                [Provide an SEO-optimized Etsy title, max 140 characters, using strong keywords separated by commas or pipes]
                
                **DESCRIPTION**
                [Provide an engaging product description. Include material notes, usage ideas, and a friendly tone. Use emojis.]
                
                **TAGS**
                [Provide exactly 13 Etsy tags (max 20 characters each), separated by commas. Focus on long-tail keywords.]
                
                **IMAGE PROMPT**
                [Provide a highly detailed, professional AI image generation prompt for this exact product idea. Describe the style, colors, lighting, and composition. E.g., 'Watercolor clipart of a cute space cat, white background, isolated, vibrant colors, 4k resolution, high quality, flat vector style']
                """
                
                response = model.generate_content(prompt)
                text_result = response.text
                
                try:
                    title_part = text_result.split("**TITLE**")[1].split("**DESCRIPTION**")[0].strip()
                    desc_part = text_result.split("**DESCRIPTION**")[1].split("**TAGS**")[0].strip()
                    tags_part = text_result.split("**TAGS**")[1].split("**IMAGE PROMPT**")[0].strip()
                    image_prompt = text_result.split("**IMAGE PROMPT**")[1].strip()
                except Exception as e:
                    st.error("❌ Model response formatting error. Please retry.")
                    st.stop()

            st.success(t["success_text"])
            
            # สร้างคอลัมน์ซ้าย-ขวา
            col_left, col_right = st.columns([6, 5])
            
            with col_left:
                st.subheader(t["img_header"].format(count=image_count))
                
                width, height = aspect_ratios[ratio_name]
                cols_per_row = 3 if image_count > 4 else 2
                rows_count = (image_count + cols_per_row - 1) // cols_per_row
                
                # ลูปดาวน์โหลดรูปภาพเก็บใส่หน่วยความจำก่อน เพื่อรับประกันว่ารูปแสดงผลครบ 100%
                image_bytes_list = []
                progress_bar = st.progress(0)
                
                for idx in range(image_count):
                    # แสดงสถานะความคืบหน้าการโหลดแต่ละรูป
                    with st.spinner(t["spinner_img"].format(idx=idx+1, total=image_count)):
                        seed = 42 + (idx * 150)
                        safe_prompt = urllib.parse.quote(image_prompt)
                        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&nologo=true&seed={seed}"
                        
                        img_bytes = fetch_image_bytes(image_url)
                        if img_bytes:
                            image_bytes_list.append(img_bytes)
                        progress_bar.progress((idx + 1) / image_count)
                
                # ลบแถบความคืบหน้าออกหลังโหลดเสร็จ
                progress_bar.empty()
                
                # แสดงรูปในตารางสไตล์การ์ด Civitai
                for r in range(rows_count):
                    grid_cols = st.columns(cols_per_row)
                    for c in range(cols_per_row):
                        img_idx = r * cols_per_row + c
                        if img_idx < len(image_bytes_list):
                            with grid_cols[c]:
                                st.image(
                                    image_bytes_list[img_idx], 
                                    caption=f"Image #{img_idx + 1}", 
                                    use_container_width=True
                                )
                
                st.info(f"{t['prompt_used']}\n\n`{image_prompt}`")

            with col_right:
                st.subheader(t["listing_header"])
                
                st.markdown(t["title_label"])
                st.code(title_part, language="text")
                
                st.markdown(t["desc_label"])
                st.code(desc_part, language="text")
                
                st.markdown(t["tags_label"])
                st.code(tags_part, language="text")

        except Exception as e:
            st.error("❌ SYSTEM ERROR")
            st.error(str(e))
