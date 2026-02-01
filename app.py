import streamlit as st
import google.generativeai as genai

# 1. Cấu hình
if "GEMINI_KEY" not in st.secrets:
    st.error("Chưa dán API Key vào Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 2. Giao diện
st.title("🚀 CÔNG CỤ AI MARKETING")

# Dùng model ổn định nhất của Google
model = genai.GenerativeModel('gemini-1.5-flash')

topic = st.text_input("Nội dung cần viết bài:", placeholder="Ví dụ: Giày nam cao cấp")

if st.button("Bắt đầu tạo"):
    if topic:
        try:
            with st.spinner('Đang xử lý...'):
                response = model.generate_content(f"Viết bài quảng cáo Facebook về: {topic}")
                st.markdown("### Kết quả:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Lỗi: {e}")
    else:
        st.warning("Vui lòng nhập nội dung!")
