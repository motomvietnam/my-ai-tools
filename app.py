import streamlit as st
import google.generativeai as genai

st.title("🚀 XƯỞNG AI MARKETING")

# 1. Kết nối API
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Chưa có API Key!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 2. Tự động lấy Model khả dụng
@st.cache_resource
def get_working_model():
    try:
        # Lấy danh sách tất cả model mà API Key của bạn được phép dùng
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Ưu tiên lấy bản flash hoặc pro
                if 'gemini-1.5-flash' in m.name or 'gemini-pro' in m.name:
                    return genai.GenerativeModel(m.name)
        return None
    except Exception as e:
        st.error(f"Lỗi khi liệt kê model: {e}")
        return None

model = get_working_model()

# 3. Giao diện sử dụng
if model:
    st.info(f"Đang sử dụng Model: {model.model_name}")
    topic = st.text_input("Sản phẩm của bạn là gì?")
    
    if st.button("Tạo bài viết ngay"):
        if topic:
            try:
                response = model.generate_content(f"Viết bài quảng cáo Facebook về: {topic}")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi khi tạo nội dung: {e}")
        else:
            st.warning("Vui lòng nhập sản phẩm!")
else:
    st.error("Tài khoản của bạn hiện chưa được Google cấp quyền cho model nào. Hãy thử tạo API Key ở một 'New Project' khác.")
