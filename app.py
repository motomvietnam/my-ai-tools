import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình API
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
except:
    st.error("Lỗi: Chưa cấu hình API Key trong mục Secrets!")

st.title("🛠️ XƯỞNG AI MARKETING")

# 2. Tạo Menu bên trái
menu = st.sidebar.selectbox("Chọn công cụ:", ["Viết Bài Facebook", "Kiểm Duyệt Ảnh Ads"])

if menu == "Viết Bài Facebook":
    st.header("✍️ AI Viết Content")
    topic = st.text_input("Sản phẩm của bạn là gì?")
    if st.button("Tạo bài viết ngay"):
        response = model.generate_content(f"Viết bài quảng cáo Facebook hấp dẫn về: {topic}")
        st.write(response.text)

elif menu == "Kiểm Duyệt Ảnh Ads":
    st.header("🛡️ AI Soi Ảnh Vi Phạm")
    file = st.file_uploader("Tải ảnh lên để quét:", type=['jpg', 'png'])
    if file and st.button("Bắt đầu quét"):
        img = Image.open(file)
        response = model.generate_content(["Kiểm tra xem ảnh này có vi phạm chính sách Facebook (hở hang, bạo lực, súng ống) không?", img])
        st.info(response.text)



