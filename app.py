import streamlit as st
import google.generativeai as genai

st.title("🚀 XƯỞNG AI MARKETING")

if "GEMINI_KEY" not in st.secrets:
    st.error("Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# SỬ DỤNG GEMINI 1.5 FLASH ĐỂ KHÔNG BỊ HẾT QUOTA (GIỚI HẠN)
model = genai.GenerativeModel('gemini-1.5-flash')

topic = st.text_input("Sản phẩm của bạn là gì?", placeholder="Ví dụ: Mỹ phẩm thiên nhiên")

if st.button("Tạo bài viết ngay"):
    if topic:
        try:
            with st.spinner('Đang tạo nội dung (Bản Flash siêu tốc)...'):
                response = model.generate_content(f"Viết bài quảng cáo Facebook hấp dẫn về: {topic}")
                st.success("Thành công!")
                st.write(response.text)
        except Exception as e:
            if "429" in str(e):
                st.error("Lỗi: Bạn nhấn nút quá nhanh hoặc hết hạn mức. Hãy đợi 30 giây rồi thử lại nhé!")
            else:
                st.error(f"Lỗi: {e}")
