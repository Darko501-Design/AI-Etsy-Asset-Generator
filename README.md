# 🎨 AI Etsy Asset Generator V.0 (demo)

> ระบบผู้ช่วยสร้างรูปภาพและเนื้อหาสำหรับลงขายบน Etsy โดยใช้ **Gemini AI + Nano Banana**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-4285F4?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-Non--Commercial-red)

---

## ✨ มันทำอะไรได้?

แค่พิมพ์ไอเดียสินค้าเป็นภาษาไทยหรืออังกฤษ ระบบจะสร้างให้คุณครบทุกอย่าง:

| ฟีเจอร์ | รายละเอียด |
|---------|-----------|
| 🖼️ **สร้างรูปภาพสินค้า** | AI วาดรูปจาก Prompt อัตโนมัติ พร้อมดาวน์โหลด |
| 📝 **ชื่อสินค้า (Title)** | SEO-optimized สำหรับ Etsy โดยเฉพาะ |
| 📋 **รายละเอียดสินค้า (Description)** | เขียนคำอธิบายดึงดูดลูกค้า พร้อมก๊อปปี้ไปวาง |
| 🏷️ **คีย์เวิร์ด SEO (Tags)** | 13 คำ ออกแบบให้ติดอันดับค้นหาบน Etsy |

---

## 🚀 วิธีติดตั้งและใช้งาน

### สิ่งที่ต้องมี
- ✅ คอมพิวเตอร์ Windows
- ✅ Python 3.10 ขึ้นไป ([ดาวน์โหลดที่นี่](https://www.python.org/downloads/))
- ✅ Gemini API Key ฟรี ([กดขอที่นี่](https://aistudio.google.com/app/apikey))

### ขั้นตอน

1. **ดาวน์โหลดโปรเจกต์**
   ```
   กดปุ่ม "Code" สีเขียวด้านบน > Download ZIP > แตกไฟล์
   ```

2. **ใส่ API Key**
   - สร้างโฟลเดอร์ชื่อ `API Key` ในโฟลเดอร์โปรเจกต์
   - สร้างไฟล์ `API_KEY.txt` ในโฟลเดอร์ `API Key`
   - นำ API Key ไปวางในไฟล์ (แค่บรรทัดเดียว ไม่ต้องมีอะไรอื่น)

3. **เปิดใช้งาน**
   ```
   ดับเบิ้ลคลิกไฟล์ start.bat
   ```
   
4. **เสร็จสิ้น!** หน้าเว็บจะเปิดขึ้นมาอัตโนมัติ พิมพ์ไอเดียแล้วกดสร้างได้เลย!

---

## 📸 ตัวอย่างหน้าจอ

> *จะเพิ่ม screenshot ในเร็วๆ นี้*

---

## 🛠️ เทคโนโลยีที่ใช้

- **Gemini AI (gemini-2.5-flash)** — คิด Title, Description, Tags และ Image Prompt
- **Nano Banana** — โมเดลสร้างรูปภาพของ Google
- **Streamlit** — สร้างหน้าเว็บ
- **Python** — ภาษาโปรแกรมหลัก

---

## ⚠️ ข้อควรรู้

- โปรเจกต์นี้เป็น **demo** สำหรับทดลองใช้งาน
- ต้องมี **Gemini API Key** (ขอฟรีได้จาก Google AI Studio)
- รูปภาพที่สร้างจาก AI อาจต้องนำไป **Upscale** ก่อนใช้งานจริง
- หากนำไปขายบน Etsy ต้อง **เปิดเผยว่าสร้างจาก AI** ตามนโยบายของ Etsy

---

## 📜 License

**© 2026 Darko501-Design. All Rights Reserved.**

โปรเจกต์นี้เผยแพร่ภายใต้สัญญาอนุญาต **Non-Commercial License**:
- ✅ ใช้งานส่วนตัวได้ฟรี
- ✅ ดัดแปลง แก้ไข แชร์ต่อได้
- ❌ **ห้ามนำไปขายหรือใช้เชิงพาณิชย์**

ดูรายละเอียดเพิ่มเติมในไฟล์ [LICENSE](LICENSE)

---

## 💬 ติดต่อ

หากมีคำถาม ข้อเสนอแนะ หรือพบปัญหา สามารถเปิด [Issue](https://github.com/Darko501-Design/AI-Etsy-Asset-Generator/issues) ได้เลยครับ
