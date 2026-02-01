import streamlit as st
import google.generativeai as genai
import requests

st.set_page_config(page_title="AUTO CONTENT AI", layout="centered")
st.title("🚀 AUTO VIẾT CONTENT ĐĂNG BÀI")

# 1. Cấu hình API từ Secrets
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Bạn chưa dán API Key vào mục Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])
OPENAI_API_KEY = st.secrets.get("DALL_E_KEY") 

# 2. Hàm tìm Model Gemini (Giữ nguyên logic của bạn)
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

# 3. Hàm tạo ảnh (Đã sửa lỗi Indentation và xử lý lỗi hết tiền)
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
        return None
    except:
        return None

# 4. Giao diện người dùng
if model:
    topic = st.text_area("Sản phẩm của bạn là gì?", placeholder="Ví dụ: Mỹ phẩm trị mụn, Khóa học đầu tư...")
    
    if st.button("Tạo bài viết & Check Policy"):
        if topic:
            try:
                with st.spinner('Hệ thống đang xử lý...'):
                    # --- BƯỚC 1: TẠO NỘI DUNG ---
                    prompt_content = f"Viết bài quảng cáo Facebook hấp dẫn về: {topic}"
                    response = model.generate_content(prompt_content)
                    bai_viet = response.text
                    
                    st.success("✅ ĐÃ TẠO BÀI VIẾT")
                    st.write(bai_viet)
                    st.divider()

                    # --- BƯỚC 2: TẠO HÌNH ẢNH ---
                    st.subheader("🖼️ HÌNH ẢNH QUẢNG CÁO")
                    img_prompt = f"Professional commercial photography for {topic}, high quality, studio lighting."
                    image_url = generate_image_with_dalle(img_prompt)
                    
                    if image_url:
                        st.image(image_url, caption="Ảnh tạo bởi AI")
                    else:
                        st.info("💡 **Gợi ý hình ảnh:** Hệ thống tạo ảnh đang bảo trì. Bạn có thể sử dụng câu lệnh sau trên Bing Image Creator để có ảnh đẹp:")
                        st.code(img_prompt)
                    st.divider()

                    # --- BƯỚC 3: KIỂM TRA POLICY ---
                    st.subheader("🛡️ KIỂM TRA VI PHẠM FB")
                    prompt_policy = f"Phân tích lỗi vi phạm chính sách Facebook cho bài viết này: {bai_viet}"
                    policy_res = model.generate_content(prompt_policy)
                    st.warning(policy_res.text)

            except Exception as e:
                st.error(f"Lỗi: {e}")
        else:
            st.warning("Vui lòng nhập sản phẩm!")
else:
    st.error("Không thể kết nối AI.")
