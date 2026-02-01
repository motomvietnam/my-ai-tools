import streamlit as st
import google.generativeai as genai
import requests # Thư viện để gọi API tạo ảnh
import json # Để xử lý JSON

st.set_page_config(page_title="AUTO CONTENT AI", layout="centered")
st.title("🚀 AUTO VIẾT CONTENT ĐĂNG BÀI")

# 1. Cấu hình API từ Secrets
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Bạn chưa dán API Key Gemini vào mục Secrets của Streamlit!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 2. Khởi tạo API Key DALL-E (Cho tính năng tạo hình ảnh)
# Bạn CẦN TẠO một SECRET mới tên là DALL_E_KEY = "sk-..."
OPENAI_API_KEY = st.secrets.get("DALL_E_KEY") 
if not OPENAI_API_KEY:
    st.warning("⚠️ Để TẠO HÌNH ẢNH, vui lòng thêm DALL_E_KEY (OpenAI API Key) vào Streamlit Secrets.")

# 3. Hàm tự động tìm Model khả dụng (Giữ nguyên từ code gốc của bạn)
@st.cache_resource
def find_working_model():
    test_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            for name in test_names:
                full_name = f"models/{name}"
                if full_name in available_models or name in available_models:
                    return genai.GenerativeModel(name)
            return genai.GenerativeModel(available_models[0])
    except:
        return genai.GenerativeModel('gemini-pro')
    return None

model = find_working_model()

# --- Hàm Tạo Hình ảnh bằng DALL-E 3 ---
def generate_image_with_dalle(prompt_text):
    if not OPENAI_API_KEY:
        st.error("Không tìm thấy DALL_E_KEY. Vui lòng thêm vào Streamlit Secrets để tạo ảnh.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt_text,
        "n": 1,
        "size": "1024x1024" 
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
        response.raise_for_status() # Báo lỗi nếu status code không phải 200
        image_url = response.json()["data"][0]["url"]
        return image_url
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi gọi API DALL-E: {e}")
        try:
            st.json(response.json()) # In ra chi tiết lỗi từ API nếu có
        except:
            pass
        return None

# 4. Giao diện người dùng
if model:
    topic = st.text_area("Sản phẩm của bạn là gì?", placeholder="Ví dụ: Mỹ phẩm trị mụn, Khóa học đầu tư...")
    
    if st.button("Tạo bài viết & Hình ảnh & Kiểm tra Policy"):
        if topic:
            try:
                # --- BƯỚC 1: TẠO NỘI DUNG ---
                with st.spinner('Hệ thống đang viết bài quảng cáo...'):
                    prompt_content = f"Viết bài quảng cáo Facebook hấp dẫn, sử dụng emoji, tối ưu chuyển đổi về: {topic}"
                    response_content = model.generate_content(prompt_content)
                    bai_viet = response_content.text
                    
                    st.success("✅ ĐÃ TẠO BÀI VIẾT")
                    st.markdown(bai_viet)
                    st.markdown("---")

               def generate_image_with_dalle(prompt_text):
    if not OPENAI_API_KEY:
        return None
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"model": "dall-e-3", "prompt": prompt_text, "n": 1, "size": "1024x1024"}
    
    try:
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["data"][0]["url"]
        else:
            # Nếu hết tiền hoặc lỗi, trả về None chứ không báo lỗi đỏ 
            return None
    except:
        return None


                # --- BƯỚC 3: KIỂM TRA VI PHẠM (POLICY) ---
                st.subheader("🛡️ KIỂM TRA VI PHẠM CHÍNH SÁCH FB")
                with st.spinner('AI đang phân tích vi phạm...'):
                    prompt_policy = f"Phân tích bài viết sau xem có vi phạm chính sách quảng cáo Facebook không (các từ khóa bị cấm, cam kết quá mức, từ nhạy cảm về cơ thể, y tế...): {bai_viet}"
                    policy_response = model.generate_content(prompt_policy)
                    st.info(policy_feedback := policy_response.text)

            except Exception as e:
                st.error(f"Lỗi khi xử lý: {e}")
        else:
            st.warning("Vui lòng nhập thông tin sản phẩm!")
else:
    st.error("Không thể kết nối với bất kỳ Model AI nào. Hãy kiểm tra lại API Key Gemini.")

