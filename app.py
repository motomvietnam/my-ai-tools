import streamlit as st
import google.generativeai as genai
import requests # Thư viện để gọi API kiểm tra vi phạm
import json # Để xử lý dữ liệu JSON từ API

st.set_page_config(page_title="AUTO CONTENT AI", layout="centered")
st.title("✍️ AUTO CONTENT AI")
st.caption("Tự động hóa nội dung và hình ảnh Marketing, kiểm tra vi phạm Facebook.")

# 1. Cấu hình API Google Gemini
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Chưa dán API Key vào mục Secrets của Streamlit!")
    st.stop()

# Cấu hình API Google Gemini
if "GEMINI_KEY" not in st.secrets:
    st.error("Lỗi: Chưa dán API Key vào mục Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Cố định model để tránh lỗi kết nối
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Thử kết nối nhẹ để kiểm tra
    model.generate_content("test", generation_config={"max_output_tokens": 1})
except Exception as e:
    st.error(f"Lỗi kết nối API: {e}")
    st.stop()
    return None

model = find_working_model()

# --- Hàm hỗ trợ AI Image Generation (DALL-E 3 thông qua API) ---
# DALL-E 3 API Key (cần thêm vào Secrets)
# Tạo một secret mới: DALL_E_KEY = "sk-..."
# Bạn cần đăng ký tài khoản OpenAI và lấy API Key cho DALL-E 3
# Hiện tại, Google Gemini cũng có thể tạo ảnh, nhưng OpenAI DALL-E 3 cho chất lượng cao hơn và dễ kiểm soát hơn.
# Nếu bạn muốn dùng Gemini để tạo ảnh, tôi sẽ điều chỉnh.
OPENAI_API_KEY = st.secrets.get("DALL_E_KEY") 

def generate_image_with_dalle(prompt_text):
    if not OPENAI_API_KEY:
        st.warning("Để tạo ảnh, vui lòng thêm 'DALL_E_KEY' (API Key của OpenAI) vào mục Secrets.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt_text,
        "n": 1,
        "size": "1024x1024" # Kích thước ảnh chuẩn cho DALL-E 3
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
        response.raise_for_status() # Báo lỗi nếu status code không phải 200
        image_url = response.json()["data"][0]["url"]
        return image_url
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi tạo hình ảnh (DALL-E): {e}")
        st.json(response.json()) # In ra chi tiết lỗi từ API
        return None

# --- Hàm kiểm tra vi phạm quy định Facebook (đơn giản hóa) ---
# Đây là một hàm MÔ PHỎNG, không kết nối trực tiếp với API của Facebook.
# Facebook không có API công khai để kiểm tra vi phạm trực tiếp cho nội dung.
# Chúng ta sẽ dùng AI để phân tích và đưa ra cảnh báo.
def check_facebook_violations(content_text):
    if not model: # Đảm bảo model Gemini đã được tải
        return "Không thể kiểm tra vi phạm do lỗi kết nối AI."
    
    prompt = f"""Phân tích đoạn nội dung quảng cáo Facebook sau đây và chỉ ra CÁC ĐIỂM CÓ THỂ VI PHẠM chính sách quảng cáo của Facebook (nếu có). 
    Tập trung vào các quy tắc về:
    - Ngôn ngữ mang tính cam kết/hứa hẹn quá mức ("Đảm bảo", "Chắc chắn thành công").
    - Ngôn ngữ phân biệt đối xử (tuổi tác, giới tính, chủng tộc).
    - Ngôn ngữ liên quan đến sản phẩm/dịch vụ bị cấm (thuốc lá, cờ bạc, súng, dược phẩm không rõ nguồn gốc).
    - Ngôn ngữ tấn công vào điểm yếu cơ thể, ngoại hình ("Giảm cân cấp tốc", "Trị mụn dứt điểm").
    - Ngôn ngữ đòi hỏi hành động khẩn cấp gây áp lực ("Mua ngay kẻo hết", "Duy nhất hôm nay").
    
    Nếu không có vi phạm rõ ràng, hãy ghi "Nội dung có vẻ an toàn, nhưng vẫn cần kiểm tra lại thủ công theo chính sách của Facebook."

    Nội dung cần kiểm tra:
    "{content_text}"
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi khi kiểm tra vi phạm: {e}"

# --- Giao diện người dùng ---
if model:
    st.success(f"Đang sử dụng Model AI: {model.model_name}")
    
    with st.expander("Hướng dẫn sử dụng", expanded=False):
        st.markdown("""
        1. Nhập **Sản phẩm/Dịch vụ** bạn muốn quảng cáo.
        2. AI sẽ tự động tạo bài viết, hình ảnh và phân tích khả năng vi phạm chính sách Facebook.
        3. Kiểm tra kết quả và chỉnh sửa nếu cần.
        """)

    topic = st.text_area("Sản phẩm/Dịch vụ bạn muốn quảng cáo:", placeholder="Ví dụ: Khóa học Digital Marketing chuyên sâu, Giày thể thao siêu nhẹ...")
    
    if st.button("Tạo nội dung & Kiểm tra ngay"):
        if topic:
            # 1. Tạo nội dung văn bản
            st.subheader("1. Nội dung bài viết:")
            with st.spinner('AI đang viết bài quảng cáo...'):
                prompt_text_content = f"Viết một bài quảng cáo Facebook hấp dẫn, tối ưu để bán {topic}. Bài viết nên có tiêu đề, mô tả sản phẩm/lợi ích, và kêu gọi hành động rõ ràng. Nên dùng emoji để thu hút."
                content_response = model.generate_content(prompt_text_content)
                generated_content = content_response.text
                st.write(generated_content)
            
            # 2. Tạo hình ảnh AI
            st.subheader("2. Hình ảnh gợi ý:")
            with st.spinner('AI đang tạo hình ảnh cho bài viết...'):
                image_prompt = f"Một hình ảnh quảng cáo thu hút, sáng tạo cho {topic}. Phong cách hiện đại, màu sắc tươi sáng."
                image_url = generate_image_with_dalle(image_prompt)
                if image_url:
                    st.image(image_url, caption="Hình ảnh được tạo bởi AI (DALL-E 3)")
                else:
                    st.warning("Không thể tạo hình ảnh. Vui lòng kiểm tra API Key DALL-E hoặc thử lại.")
            
            # 3. Kiểm tra vi phạm Facebook
            st.subheader("3. Kiểm tra vi phạm chính sách Facebook:")
            with st.spinner('AI đang phân tích vi phạm...'):
                violation_result = check_facebook_violations(generated_content)
                if "an toàn" in violation_result:
                    st.success("✅ " + violation_result)
                else:
                    st.warning("⚠️ " + violation_result)
        else:
            st.warning("Vui lòng nhập thông tin sản phẩm/dịch vụ!")
else:
    st.error("Không thể kết nối với Model AI. Vui lòng kiểm tra lại API Key Gemini của bạn.")

