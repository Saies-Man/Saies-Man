import streamlit as st
from product_json import JSONFileManager
import google.generativeai as genai
import base64
from concurrent.futures import ThreadPoolExecutor
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline
import re



# Set the Gemini API Key and initialize the API
GEMINI_API_KEY = "*********" # 키 바꾸기
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit Page Config (place this at the top and call only once)
st.set_page_config(page_title="불완전 판매 진단 챗봇", page_icon=r"C:\Users\USER\Desktop\openai\png\1.png", layout="wide")

def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Base64로 인코딩된 이미지
image_base64 = get_image_as_base64(r"C:\Users\USER\Desktop\openai\png\1.png")

# CSS로 폰트 변경 및 스타일 적용
st.markdown(
    """
    <style>
    @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

    body, h1, h2, h3, h4, h5, h6, .stTextInput, .stButton, .stTextarea, .stSelectbox, .stDateInput, .stNumberInput {
        font-family: 'Pretendard', sans-serif;
    }
    /* Targeting sidebar specifically */
    .stSidebar .css-1d391kg, .stSidebar .stTextInput, .stSidebar .stButton, .stSidebar .stTextarea, .stSidebar .stSelectbox, .stSidebar .stDateInput, .stSidebar .stNumberInput {
        font-family: 'Pretendard', sans-serif;
    }
    /* 헤더의 배경색을 파란색으로 변경 */
    header[data-testid="stHeader"] {
        background-color: #2269F7;
        color: white;
    }

    /* "RUNNING..." 텍스트를 변경 */
    [data-testid="stAppRunningIndicator"]::before {
        content: '작동 중...';
        visibility: visible;
    }

    /* "Stop" 버튼 텍스트를 변경 */
    [data-testid="stStopButton"] {
        visibility: hidden;
    }
    [data-testid="stStopButton"]::before {
        content: '정지';
        visibility: visible;
        position: absolute;
    }

    /* "Deploy" 버튼 텍스트를 변경 */
    [data-testid="stHeader"] > div > div:nth-child(3) > div > div > button:nth-child(3) {
        visibility: hidden;
    }
    [data-testid="stHeader"] > div > div:nth-child(3) > div > div > button:nth-child(3)::before {
        content: '배포';
        visibility: visible;
        position: absolute;
    }


    /* 타이틀 스타일 */
    .stApp .css-1lcbmhc {
        font-size: 1.5em; /* 타이틀 텍스트 크기 조정 */
        color: #003366;
        font-weight: bold;
    }

    /* 파일 업로더 스타일 */
    .stFileUploader {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
    }

    .stButton > button {
        background-color: #2269F7; /* Blue color */
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none; /* Removes default border */
        box-shadow: 4px 4px 8px rgba(0,0,0,0.3); /* Subtle 3D effect */
        transition: background-color 0.3s, box-shadow 0.1s, color 0.3s; /* Smooth transitions */
        
    }
    .stButton > button:hover {
        background-color: #00A3FF; /* Slightly darker blue on hover */
        color: white; /* Changes text color to black when hovered */
        box-shadow: 2px 2px 6px rgba(0,0,0,0.5); /* Deeper shadow on hover for 3D effect */
    }
    .stButton > button:active, .stButton > button:focus {
        background-color: #2269F7; /* Blue color when button is clicked */
        color: white; /* Text color remains white when button is clicked */
    }    
    /* 텍스트 영역 스타일 */
    .stTextArea {
        background-color: #f5f5f5;
        border-radius: 5px;
    }

    /* 이미지 크기 조절 */
    .title-image {
        width: 60px; /* 원하는 크기로 설정 */
        vertical-align: middle;
    }

    .title-text {
        display: inline;
        font-size: 1.0em; /* 텍스트 크기 조정 */
        color: #2269F7;
        font-weight: bold;
        vertical-align: middle;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <style>
    .title-text {{
        display: flex;
        align-items: center;
    }}
    .title-text span {{
        margin: 0;
        padding: 0;
    }}
    </style>
    <h1 class="title-text">
        <img src="data:image/png;base64,{image_base64}" class="title-image" style="margin: 0; padding: 0;"/>
        <span style="color:black; font-size:70px;">S</span><span style="color:#2169F7; font-size:70px;">ai</span><span style="color:black; font-size:70px;">es Man</span>
    </h1>
    """,
    unsafe_allow_html=True
)


 #Custom styles for centering the button
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)
    # Custom CSS to style the success message
st.markdown(
    """
    <style>
    .custom-success {
        color: #FFFFFF !important;
        background-color: #2269F7 !important;
        padding: 10px;
        border-radius: 5px;
        text-align: center; /* 텍스트를 가로 중앙에 정렬 */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Directory for JSON Files
directory = r'C:\Users\USER\Desktop\openai\test_간투_json'
manager = JSONFileManager(directory)
product_list = manager.df['name'].tolist()

# Initialize session state for page management
if 'page' not in st.session_state:
    st.session_state['page'] = 'first'  

def first_page():
    # Top section with the title and description
    st.title("펀드 불완전판매 진단 서비스")

    # Section for salesperson information
    with st.form(key='salesperson_form'):
        st.markdown("### 판매원 정보 입력")
        st.caption("판매직원 판매를 시작할 담당자 정보를 확인하세요.")
        # Salesperson's name
        text_input = st.text_input(label="판매원 성명")
        
        # Branch name   
        branch_choice = st.selectbox(
            "지점명",
            options=[
                "",
                "강남역점",
                "건대입구점",
                "경희대지점",
                "광화문점",
                "논현점",
                "대학로점",
                "동대문점",
                "명동지점",
                "삼성점",
                "신촌점",
                "압구정점",
                "여의도점",
                "을지로점",
                "이태원점",
                "잠실점",
                "종로점",
                "홍대점",
                "휘경동지점"
            ]
        )

        submitted_salesperson = st.form_submit_button("판매원 정보 조회")
    
    if submitted_salesperson:
        st.markdown("""
        <style>
            .salesperson-complete {
                text-align: center;
                color: white;
                background-color: #2269F7;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px; /* 상단 여백 */
                margin-bottom: 20px; /* 하단 여백 */
                padding: 10px 300px; /* 내부 여백 조절: 상하 10px, 좌우 20px */
                display: inline-block; /* 텍스트 내용에 맞춘 배경 크기 */
                border-radius: 10px; /* 모서리 둥글게 처리 */
                width: auto; /* 너비 자동 조절 */
                box-sizing: border-box; /* 패딩과 테두리를 너비에 포함 */
            }
            /* 센터 정렬을 위한 컨테이너 */
            .container {
                text-align: center; /* 텍스트 중앙 정렬 */
                width: 100%; /* 컨테이너 전체 너비 */
            }
        </style>
        <div class="container">
            <h2 class='salesperson-complete'>판매원 정보 조회가 완료되었습니다</h2>
        </div>
        """, unsafe_allow_html=True)
        st.session_state['salesperson_submitted'] = True

    # Section for customer profile if salesperson information is submitted
    if st.session_state.get('salesperson_submitted', False):
        with st.form(key='customer_profile_form'):
            st.markdown("### 고객 프로필 입력")
            st.caption("고객님의 특성을 확인해주세요.")
            # Vulnerable group
            vulnerable_group = st.selectbox(
                "금융취약계층", 
                options=["","해당 사항 없음", "고령자(만65세 이상)", "은퇴자", "주부", "초고령자(만80세 이상)"]
            )
            
            # Investment preference
            investment_preference = st.selectbox(
                "투자성향", 
                options=["","공격투자형", "적극투자형", "위험중립형", "안정추구형", "안정형"]
            )
            
            # Investment experience
            investment_experience = st.selectbox(
                "금융상품 투자경험", 
                options=["",
                    "[매우 낮은 수준] 금융투자상품에 투자해 본 경험이 없음",
                    "[낮은 수준] 널리 알려진 금융투자상품 (주식, 채권 및 펀드 등)의 구조 및 위험을 일정부분 이해하고 있는 정도",
                    "[높은 수준] 투자할 수 있는 대부분의 금융상품의 차이를 구별할 수 있는 정도",
                    "[매우 높은 수준] 금융상품을 비롯하여 모든 투자대상 상품의 차이를 이해할 수 있는 정도"
                ]
            )

            submitted_profile = st.form_submit_button("고객 프로필 조회")
        
        if submitted_profile:
            st.markdown("""
            <style>
            .custom-header {
                text-align: center;
                color: white;
                background-color: #2269F7;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px; /* Top margin */
                margin-bottom: 20px; /* Bottom margin */
                padding: 10px 300px; /* Adjusted padding: 10px vertical, 40px horizontal */
                display: inline-block; /* Aligns the background to the text width */
                border-radius: 10px; /* Rounded corners */
            }

            /* 센터 정렬을 위한 컨테이너 */
            .container {
                text-align: center; /* 텍스트 중앙 정렬 */
                width: 100%; /* 컨테이너 전체 너비 */
            }
            </style>
            <div class="container">
                <h2 class='custom-header'>
                    고객 프로필 조회가 완료되었습니다
                </h2>
            </div>
            """, unsafe_allow_html=True)
            # Setting a flag to show the '검토시작' button
            st.session_state['profile_submitted'] = True

    # A big button (e.g., an action trigger), shows only if 'profile_submitted' is True
    if st.session_state.get('profile_submitted', False):
        if st.button("검토시작"):
            st.session_state['page'] = 'main'

    # Sidebar success message
    # Display the styled message in the sidebar
    st.sidebar.markdown('<div class="custom-success">펀드 판매 적합성 평가 AGENT</div>', unsafe_allow_html=True)

    # List of steps
    steps = ['판매 직원 정보 입력', '투자설명서, 상담내용 업로드', '진단결과']

    # Dictionary to hold the status of each step
    step_status = {}

    # Creating checkboxes for each step
    st.sidebar.title("STEP")
    for step in steps:
        if step == '판매 직원 정보 입력':
            step_status[step] = st.sidebar.checkbox(step, value=True)
        else:
            step_status[step] = st.sidebar.checkbox(step)
    # CSS를 주입하여 특정 요소의 배경색 변경
    st.markdown("""
    <style>
    #root > div:first-child > div:nth-child(1) > div > div > div > section:nth-child(1) > div:nth-child(1) {
        background-color: #F2F2F2;  /* 흰색배경 */
    }
    </style>
    """, unsafe_allow_html=True)


def main_page():
    # Product Selection Dropdown
    st.title("펀드 불완전판매 진단 서비스")
    selected_product = st.selectbox("상품을 선택하세요:", [""] + product_list, index=0)
    # Display JSON content if a product is selected
    if selected_product:
        json_content = manager.read_json_as_text(selected_product)
        if json_content:
            st.session_state['json_content'] = json_content  # Save JSON content to session state

    # File Uploader
    uploaded_file = st.file_uploader("상담 내용을 업로드하세요:", type=["txt", "md"])
    if uploaded_file is not None:
        raw_text = uploaded_file.read().decode("utf-8-sig")
        st.text_area("파일 내용:", value=raw_text, height=250)
        st.session_state['raw_text'] = raw_text  # Save raw text to session state

    # Button to Start Incomplete Sale Check
    if st.button("불완전 검사 시작"):
        if 'json_content' in st.session_state and 'raw_text' in st.session_state:
            st.session_state['page'] = 'second'  # Change page state to 'second'
    # Sidebar steps for main_page
    steps = ['판매 직원 정보 입력', '투자설명서, 상담내용 업로드', '진단결과']

    # Dictionary to hold the status of each step
    step_status = {}
    st.sidebar.markdown('<div class="custom-success">펀드 판매 적합성 평가 AGENT</div>', unsafe_allow_html=True)
    # Creating checkboxes for each step
    st.sidebar.title("STEP")
    for step in steps:
        if step in ['판매 직원 정보 입력', '투자설명서, 상담내용 업로드']:
            step_status[step] = st.sidebar.checkbox(step, value=True)
        else:
            step_status[step] = st.sidebar.checkbox(step)

            
def second_page():
    st.title("펀드 불완전판매 진단 서비스")
    st.title("불완전 판매 진단 결과 ")
    # Retrieve saved JSON content and raw text from session state
    json_content = st.session_state.get('json_content', '')
    raw_text = st.session_state.get('raw_text', '')
    # Sidebar steps for main_page
    steps = ['판매 직원 정보 입력', '투자설명서, 상담내용 업로드', '진단결과']

    # Dictionary to hold the status of each step
    step_status = {}
    st.sidebar.markdown('<div class="custom-success">펀드 판매 적합성 평가 AGENT</div>', unsafe_allow_html=True)
    # Creating checkboxes for each step
    st.sidebar.title("STEP")
    for step in steps:
        if step in ['판매 직원 정보 입력', '투자설명서, 상담내용 업로드','진단결과']:
            step_status[step] = st.sidebar.checkbox(step, value=True)
        else:
            step_status[step] = st.sidebar.checkbox(step)    

    # Generate the prompts
    prompt_case1 = generate_prompt_case1(json_content, raw_text, model, tokenizer) 
    prompt_case2 = generate_prompt_case2(json_content, raw_text)

    # Define a function to generate answers in parallel
    def generate_answer_in_parallel(prompt):
        return generate_answer(prompt)

    # Use ThreadPoolExecutor to run the answer generation in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(generate_answer_in_parallel, prompt_case1),
            executor.submit(generate_answer_in_parallel, prompt_case2)
        ]
        
        # Retrieve the results
        answer1 = futures[0].result()
        answer2 = futures[1].result()

    # Combine the answers
    combined_answer = format_combined_answer(answer1, answer2)
    
    # Display the combined answer
    st.write(combined_answer)

def generate_prompt_case1(json_content, raw_text, model, tokenizer):
    # Extract counselor's speech and run predictions
    text_sentences = extract_speech_sentences(raw_text)
    predictions = run_predictions(text_sentences, model, tokenizer)
    
    # Process predictions and create prompt for case 3
    prompt = "부당할 수 있는 권유 문장:\n"
    for text, label in predictions:
        if label == "부당할 수 있는 권유 문장":
            prompt += f"{text}\n"
    prompt += """
    위에서 제시된 문장들은 투자 상담에서 상담사가 말한 부당할 수 있는 권유 문장들이야.
    제시된 문장들을 순서대로 나열하고 해당 문장들이 왜 부당한 권유 문장인지 엔터친 후 그 문장 밑에 두줄로 짧게 요약해줘.
    결론이나 개선방향등은 언급하지말고 내가 부탁한 것만 대답해줘
    만약에 제시된 문장들이 없을 경우에는 "부당한 권유 문장이 없습니다." 라고만 대답해.
    제시된 문장들이 있을 경우에는 "다음은 부당한 권유 문장일 수 있습니다. 주의가 필요합니다."라고 시작할 것.
    """        
    return prompt

def generate_prompt_case2(json_content, raw_text):
    # Here, add your detailed prompt creation logic
    prompt = f"""
<persona>
너는 펀드 상담사를 관리하는 매니저야. 매니저가 해야할 일은 상담사가 펀드 상품 판매 상담 시 간이투자서json(간투json)을 비교하고 결과를 알려주는 역할이야.
</persona>

<instruction>
step1: json_content을 분석해
"document_n": 문서번호
"id" 값의 의미
0: 상품분류등급
1: 투자목적 및 전략
2: 분류
3: 투자비용
4: 투자실적 추이 (연평균 수익률, 단위: %)
5: 운용전문 인력
6: 투자자 유의사항
7: 주요투자 위험
8: 환매방법
9: 매입방법
10: 환매 수수료
11: 기준가
12: 과세
13: 전환절차 및 방법
14: 모집기간
15: 효력발생일
16: 모집(판매) 기간
17: 존속기간
18: 참조
19: 집합투자 기구의 종류
"index": 해당 id에서 몇 번째 문장인지
"bold": 중요한 문장
"weight": 중요한 문장
"text": 텍스트

step2:매니저는 고객과 상담사가 대화에서 id=0:상품분류등급, id=1:투자목적 및 전략, id=6:투자자 유의사항, id=7:주요투자 위험, id=8:환매 수수료가 모두 언급되었는 지 확인해 줘. 언급이 없는 경우, 이는 언급 자체를 하지 않은 경우야.

step3:매니저는 raw_text에서 언급 자체를 하지 않은 경우를 제외하고 id=0:상품분류등급, id=1:투자목적 및 전략, id=6:투자자 유의사항, id=7:주요투자 위험, id=8:환매 수수료 반드시 이 5가지에 대한 상담사의 답변 문장이 몇 개인지 세야 해.

example:

상담사: 이 펀드는 국내 채권에 주로 투자하며, 유진챔피언ESG중기채증권모투자신탁과 유진챔피언단기채증권모투자신탁에 60%이상 투자하여 수익을 추구합니다. 금리 국면에 따라 모펀드 간의 투자 비중을 조절합니다.

문장 갯수: 1문장

step4:**상담사의 답변 갯수를 토대로 json_content에서 반드시 문장 갯수만 비교를 해줘**

example:

상담사의 답변 갯수: 2개

json_content에서 비교해야 할 문장: index0, index1

상담사의 답변 갯수: 5개

json_content에서 비교해야 할 문장: index0, index1, index2, index3, index4

**비교해야 할 위치**

1. json_content의 id=0:상품분류등급은 raw_text의 상담사의 답변중 상품명의 숫자등급과 비교
2. json_content의 id=1:투자목적 및 전략은 raw_text의 **”**고객: 이 펀드는 어디에 투자하는 상품인가요?”에 대한 상담사의 답변과 비교
3. json_content의 id=6:투자자 유의사항은 raw_text의 ”고객: 펀드에 투자할 때 조심해야 할 게 있나요?”와 "이 펀드에 투자할 때 유의할 점이 있나요?"라는 질문에 상담사의 답변과 비교
4. json_content의 id=7:주요투자 위험은 raw_text의 ”고객: 이 펀드의 위험성은 어떤가요?”라는 질문에 상담사의 답변
5. json_content의 id=8:환매 수수료는 raw_text의 ”고객: 환매수수료는 어떻게 되나요?”라는 질문에 상담사의 답변과 비교

step4:**매니저는 raw_text의 상담사의 답변이  +{{비교해야 할 json문장}}중에서 단어 하나하나 검토하면서 생략된 부분을 반드시 찾아야해**

step5:**매니저는 raw_text의 상담사의 답변이  +{{비교해야 할 json문장}}중에서 단어 하나하나 검토하면서 달라진 부분을 반드시 찾아야 해.**
</instruction>

<format>
1.답변을 말할 때 이모티콘(이모지)는 반드시 사용 하지마.
2.**답변할 때 생략된 부분과 달라진 부분만 알려줘 알려줘**
example:
**1. 투자목적 및 전략**
- **생략된 부분 결과**: +{{비교해야 할 json문장}}에서 생략된 부분을 **bold** 표시해서 알려줘 
- **달라진 부분 결과**: raw_text에서 상담사의 답변에서 달라지 부분을 **bold** 표시해서 알려줘
</format>
                간이 투자서 json 파일 : '{json_content}'
                상담 내용 : '{raw_text}'
              QUESTION: 간이 투자서와 상담내용을 비교했을 때 생략되거나 달라진 부분이 있어?
              """
    return prompt


def generate_answer(prompt):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    answer = model.generate_content(prompt)
    return answer.text.strip()

def format_combined_answer(answer1, answer2):
    return f"{answer1}\n\n---------\n\n{answer2}"

def extract_speech_sentences(raw_text):
    text_sentences = []
    lines = raw_text.split('\n')
    for line in lines:
        if line.startswith("상담사:"):
            speech = line.replace("상담사:", "").strip()
            speech = speech.replace("?", ".")
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', speech)
            text_sentences.extend(sentences)
    return text_sentences

def run_predictions(text_sentences, model, tokenizer, batch_size=16):
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None)
    
    labeled_predictions = []
    for i in range(0, len(text_sentences), batch_size):
        batch = text_sentences[i:i + batch_size]
        predictions = pipeline(batch)
        
        for text, prediction in zip(batch, predictions):
            scores = {pred['label']: pred['score'] for pred in prediction}
            if scores['LABEL_1'] > scores['LABEL_0']:
                label = "부당할 수 있는 권유 문장"
            else:
                label = "정상적인 문장"
            labeled_predictions.append((text, label))
    
    return labeled_predictions

# Load the model and tokenizer
model = BertForSequenceClassification.from_pretrained(r'C:\Users\USER\Desktop\openai\saved_model', from_tf=False, use_safetensors=True)
tokenizer = BertTokenizer.from_pretrained(r'C:\Users\USER\Desktop\openai\saved_model')

# Routing based on page state
if st.session_state['page'] == 'first':
    first_page()
    
elif st.session_state['page'] == 'main':
    main_page()
elif st.session_state['page'] == 'second':
    second_page()