import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Marketing Tool", layout="centered")
st.title("🚀 XƯỞNG AI MARKETING")

# 1. Cấu hình API từ Secrets
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Bạn chưa dán API Key vào mục Secrets của Streamlit!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 2. Hàm tự động tìm Model khả dụng (Để sửa lỗi 404)
@st.cache_resource
def find_working_model():
    # Danh sách các tên model từ mới đến cũ
    test_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    # Cách 1: Thử liệt kê từ hệ thống
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            # Ưu tiên lấy bản flash cho nhanh
            for name in test_names:
                full_name = f"models/{name}"
                if full_name in available_models or name in available_models:
                    return genai.GenerativeModel(name)
            return genai.GenerativeModel(available_models[0])
    except:
        # Cách 2: Nếu không liệt kê được, thử đoán tên chuẩn
        return genai.GenerativeModel('gemini-pro')
    return None

model = find_working_model()

# 3. Giao diện người dùng
if model:
    topic = st.text_area("Sản phẩm của bạn là gì?", placeholder="Ví dụ: Khóa học chạy quảng cáo Facebook từ A-Z...")
    
    if st.button("Tạo bài viết ngay"):
        if topic:
            try:
                with st.spinner('AI đang viết bài...'):
                    response = model.generate_content(f"Viết bài quảng cáo Facebook hấp dẫn về: {topic}")
                    st.success("Đã tạo xong!")
                    st.markdown("---")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi khi tạo nội dung: {e}")
        else:
            st.warning("Vui lòng nhập thông tin sản phẩm!")
else:
    st.error("Không thể kết nối với bất kỳ Model AI nào. Hãy kiểm tra lại API Key.")
