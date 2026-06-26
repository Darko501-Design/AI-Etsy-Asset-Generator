import streamlit as st
import google.generativeai as genai
import requests
import os

st.set_page_config(page_title="AI Etsy Asset Generator V.0 (demo)", page_icon="🎨", layout="wide")

st.title("🎨 AI Etsy Asset Generator V.0 (demo)")
st.markdown("ระบบผู้ช่วยสร้างรูปภาพและเนื้อหาสำหรับลงขายบน Etsy โดยใช้ **Gemini AI**")

# ระบบอ่าน API Key จากไฟล์ (ใช้ path แบบ relative เพื่อให้ทำงานได้ในเครื่องของทุกคน)
api_key = ""
script_dir = os.path.dirname(os.path.abspath(__file__))
api_key_file = os.path.join(script_dir, "API Key", "API_KEY.txt")

# เช็คว่ามีไฟล์อยู่และอ่านค่ามา
if os.path.exists(api_key_file):
    with open(api_key_file, "r", encoding="utf-8") as f:
        api_key = f.read().strip()

# Sidebar
with st.sidebar:
    st.header("⚙️ ตั้งค่า (Settings)")
    if api_key:
        st.success("✅ ระบบพบ API Key ของคุณฝังอยู่ในไฟล์เรียบร้อยแล้ว พร้อมใช้งาน!")
    else:
        api_key = st.text_input("ใส่ Google Gemini API Key:", type="password")
        st.markdown("[👉 คลิกที่นี่เพื่อขอ API Key ฟรี](https://aistudio.google.com/app/apikey)")
        st.warning("💡 หรือสร้างโฟลเดอร์ `API Key` แล้วสร้างไฟล์ `API_KEY.txt` วาง Key ไว้ข้างใน ระบบจะอ่านให้อัตโนมัติ")
    
    st.divider()
    st.markdown("💡 **วิธีใช้งาน:**")
    st.markdown("1. พิมพ์ไอเดียสินค้าในช่องด้านขวา\n2. กดปุ่ม '🚀 สร้างสินค้า'\n3. รอระบบประมวลผล (10-20 วินาที)")

# Main Content
idea = st.text_input("💡 ไอเดียสินค้าของคุณ (เช่น สติกเกอร์น้องแมวอวกาศ, ลายแพทเทิร์นดอกไม้สีน้ำวินเทจ):", placeholder="พิมพ์ไอเดียของคุณที่นี่...")

if st.button("🚀 สร้างสินค้า (Generate)", use_container_width=True):
    if not api_key:
        st.error("⚠️ ไม่พบ API Key ครับ กรุณาใส่ในช่องด้านซ้าย หรือสร้างไฟล์ `API Key/API_KEY.txt` ครับ")
    elif not idea:
        st.error("⚠️ กรุณาพิมพ์ไอเดียสินค้าก่อนครับ")
    else:
        try:
            # 1. ตั้งค่า API Key (ตัดช่องว่างอัตโนมัติเพื่อป้องกัน Error)
            genai.configure(api_key=api_key.strip())
            
            with st.spinner("⏳ กำลังให้ Gemini คิด Title, Description และ Tags สำหรับขายบน Etsy..."):
                # 2. เรียกใช้ Gemini AI รุ่น 2.5-flash (รองรับทุก API Key)
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
                
                # แยกส่วนข้อมูลที่ได้
                try:
                    title_part = text_result.split("**TITLE**")[1].split("**DESCRIPTION**")[0].strip()
                    desc_part = text_result.split("**DESCRIPTION**")[1].split("**TAGS**")[0].strip()
                    tags_part = text_result.split("**TAGS**")[1].split("**IMAGE PROMPT**")[0].strip()
                    image_prompt = text_result.split("**IMAGE PROMPT**")[1].strip()
                except Exception as e:
                    st.error("❌ เกิดข้อผิดพลาดในการจัดรูปแบบคำตอบจาก AI ลองกดสร้างใหม่อีกครั้ง")
                    st.stop()

            st.success("✨ ข้อมูล Etsy สำเร็จแล้ว! กำลังวาดรูปภาพ...")
            
            # 3. แสดงผลหน้าจอ
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("🖼️ รูปภาพสินค้า (Image)")
                with st.spinner("⏳ กำลังวาดรูปภาพจาก Prompt ของ Gemini..."):
                    import urllib.parse
                    safe_prompt = urllib.parse.quote(image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true"
                    
                    st.image(image_url, caption="คลิกขวาที่รูป > 'Save image as' เพื่อนำไปใช้", use_column_width=True)
                    st.info(f"**💡 Prompt ที่ Gemini คิดให้เพื่อใช้วาดรูปนี้:**\n\n{image_prompt}")

            with col2:
                st.subheader("📝 ข้อมูลสำหรับลงขาย Etsy")
                
                st.markdown("📋 **ชื่อสินค้า (Title) - ก๊อปปี้ไปวางได้เลย**")
                st.code(title_part, language="text")
                
                st.markdown("📋 **รายละเอียด (Description)**")
                st.code(desc_part, language="text")
                
                st.markdown("🏷️ **คีย์เวิร์ด (Tags 13 คำ)**")
                st.code(tags_part, language="text")

        except Exception as e:
            st.error("❌ เกิดข้อผิดพลาดจากฝั่ง Google API (API Key หรือระบบเครือข่าย)")
            st.error(f"รายละเอียด: {str(e)}")
            st.info("💡 คำแนะนำ: ลองเช็คให้แน่ใจว่า API Key ถูกต้อง หรือลองขอ API Key ใหม่จาก https://aistudio.google.com/app/apikey")
