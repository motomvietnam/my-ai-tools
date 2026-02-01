import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AUTO CONTENT AI", layout="wide")

# 1. Cấu hình API
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Bạn chưa cấu hình GEMINI_KEY trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 2. Khởi tạo Model (Cố định bản Flash để tránh lỗi 404)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Hàm kiểm tra vi phạm Facebook
def check_policy(content):
    prompt = f"Phân tích các lỗi vi phạm chính sách quảng cáo Facebook (như cam kết quá mức, trị dứt điểm, từ ngữ bị cấm, nhạy cảm) cho nội dung sau: {content}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Không thể kiểm tra chính sách lúc này."

# 4. Giao diện
st.title("🚀 AUTO CONTENT AI PRO")
st.subheader("Hệ thống viết bài & Kiểm tra vi phạm Facebook")

topic = st.text_area("Nhập sản phẩm/dịch vụ của bạn:", placeholder="Ví dụ: Giày thể thao nam cao cấp...")

if st.button("Tạo Nội Dung & Check Policy"):
    if topic:
        col1, col2 = st.columns(2)
        
        with st.spinner('Đang xử lý...'):
            # Bước 1: Tạo bài viết
            res_content = model.generate_content(f"Viết bài quảng cáo Facebook hấp dẫn cho: {topic}")
            article = res_content.text
            
            with col1:
                st.success("📝 BÀI VIẾT QUẢNG CÁO")
                st.write(article)
                st.button("Sao chép bài viết", on_click=lambda: st.write("Đã sao chép!")) # Giả lập

            # Bước 2: Check Policy
            with col2:
                st.warning("🛡️ KIỂM TRA VI PHẠM (POLICY)")
                policy_feedback = check_policy(article)
                st.write(policy_feedback)
                
            st.divider()
            st.info("💡 Mẹo: Bạn nên dùng hình ảnh thực tế của sản phẩm để tăng tỷ lệ chuyển đổi!")
    else:
        st.warning("Vui lòng nhập thông tin sản phẩm!")
