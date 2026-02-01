import streamlit as st
import google.generativeai as genai

# 1. Cấu hình API
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Bạn chưa cấu hình GEMINI_KEY trong mục Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Tự động tìm model khả dụng để tránh lỗi NotFound
@st.cache_resource
def get_model():
    # Danh sách ưu tiên các model từ mới đến cũ
    priority_models = [
        'gemini-1.5-flash', 
        'gemini-1.5-flash-latest', 
        'gemini-pro', 
        'gemini-1.0-pro'
    ]
    
    # Thử từng cái, cái nào chạy được thì lấy
    for model_name in priority_models:
        try:
            m = genai.GenerativeModel(model_name)
            # Thử tạo một nội dung cực ngắn để test
            m.generate_content("hi", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = get_model()

# 2. Giao diện
st.title("🚀 XƯỞNG AI MARKETING")

if model is None:
    st.error("Không tìm thấy Model AI nào khả dụng. Vui lòng kiểm tra lại API Key hoặc vùng hỗ trợ.")
else:
    topic = st.text_input("Sản phẩm của bạn là gì?")
    if st.button("Tạo bài viết ngay"):
        if topic:
            try:
                with st.spinner('Đang tạo nội dung...'):
                    response = model.generate_content(f"Viết bài quảng cáo Facebook hấp dẫn về: {topic}")
                    st.success("Thành công!")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi: {e}")
        else:
            st.warning("Vui lòng nhập tên sản phẩm!")
