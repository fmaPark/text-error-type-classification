import torch
from transformers import BertTokenizer, BertForSequenceClassification, BertForQuestionAnswering

def make_question(label):
    if label == 1:
        return "한글 맞춤법, 띄어쓰기 오류가 발생한 부분은?"
    elif label == 2:
        return "단어 선택 오류가 발생한 부분은?"
    elif label == 3:
        return "비문이 발생한 부분은?"
    elif label == 4:
        return "미완성 또는 불완전한 문장이 발생한 부분은?"
    elif label == 5:
        return "키워드 또는 중요 내용 오류가 발생한 부분은?"
    elif label == 6:
        return "유사한 내용 반복 오류가 발생한 부분은?"
    else :
        return None

# 학습된 모델 경로
classification_model_path = "model/error_classification_model_16_16_30_klue"
qa_model_path = "model/question-answering-temp"

# @@@@ text classification 예측 수행

# 토크나이저 및 모델 로드
tokenizer = BertTokenizer.from_pretrained(classification_model_path)
model = BertForSequenceClassification.from_pretrained(classification_model_path)

# 예측할 텍스트 입력
text_input = "[original]정헌율 익산시장이 유라시아 철도 거점 기반 구축과 일자리 도시 등 새해 익산의 5대 미래 비전을 발표했다. 특히 활력과 상생, 희망, 품격, 행복이라는 5대 역점 시책을 통해 살기좋은 익산을 만들겠다는 청사진을 내놨다. 정 시장은 3일 익산시청 상황실에서 신년 기자회견을 열고, 지난해 주요 성과와 올해 시정운영 방향을 밝혔다. 우선 지난해 성과로 성공적인 전국체전과 분야별 맞춤형 경제정책 추진, 아이부터 어르신까지 골고루 돌아가는 복지와 교육정책 추진, 문화재 활용사업과 풍성한 볼거리 체공, 시민과의 소통 강화, 편리한 도시환경 구축으로 일등 도시를 만드는 성과를 거뒀다고 평가했다. 올해에는 5대 핵심 프로젝트를 통해 보다 발전하는 익산시를 만들겠다는 계획이다. 익산이 가진 익산역의 장점을 살려 유라시아 철도의 시발역으로 기반을 구축할 방침이다. 호남선과 전라선, 군산선, 장항선 등 4개 철로가 분기하는 전국 유일한 철도역의 장점을 살려 남북철도 시발역으로, 그 기반이 될 전북권 광역전철망 구축과 KTX 익산역 복합환승센터를 추진할 계획이다. 특히 지역의 청년과 은퇴한 어르신, 경력 단절 여성이 일할 수 있는 일자리 도시의 원년으로 삼아 일자리 정책을 강화한다. 익산역과 중앙동 주변의 도시재생사업을 구체적으로 추진하고, 남중동 옛 도심에 10층 규모의 주민친화형 신청사 건립도 추진한다. 익산의 신성장산업인 안전보호 융복합사업, 홀로그램콘텐츠사업을 통해 밝은 익산의 미래를 그려나갈 방침이다. 아울러 미세먼지와 열섬화 현상을 해결하기 위해 푸른 숲 가꾸기에 전력을 기울여 나간다. 이와 함께 시정 내부적으로 추진할 5대 역점시책은 가장 먼저 부채를 2021년까지 전액 상환하고, 일자리 7100개 창출, 남부권 도서관과 금마도서관을 설립해 익산에 활력을 불어넣는다. 또한 도시와 농촌이 잘사는 상생 익산을 위한 농생명ICT검인증센터 설립, 스마트푸드 시스템 구축, 말 산업 체험관 건립 등을 통해 도시와 농촌의 상생을 추구한다. 무상보육 실현 등을 통한 희망 익산을 만들고, 백제 왕도의 정체성을 확립하기 위한 품격 익산도 조성한다. 정 시장은 지난해 성과에 멈추지 않고 올해 핵심 프로젝트와 역점 시책을 중심으로 계획된 목표를 모두 성취할 수 있도록 최선을 다하겠다고 말했다.[/original][summary]정헌율 익산시장이 3일 익산시청 상황실에서 신년 기자회견을 열고 유라시아 철도 거점 기반 구축과 일자리 도시 등 새해 익산의 5대 미래 비전을 발표하고 특히 활력과 상생, 희망, 품격, 행복이라는 5대 역점 시책을 통해 살기 좋은 익산을 만들겠다는 청사진을 내놨다.[/summary]"

# 텍스트 입력을 토큰화
inputs = tokenizer.encode_plus(
    text_input,
    max_length=512,
    truncation=True,
    padding="max_length",
    return_tensors="pt"
)

# 모델을 통한 레이블 예측
model.eval()
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()

# 예측된 레이블 출력
print("Original Text:", text_input)
print("Predicted Label:", predicted_label)

# @@@@ question-answering 예측 수행

# 학습된 모델 경로
qa_model_path = "model/question-answering-temp"

# 토크나이저 및 모델 로드
tokenizer = BertTokenizer.from_pretrained(qa_model_path)
model = BertForQuestionAnswering.from_pretrained(qa_model_path)

# 예측할 질문과 텍스트 입력
question = make_question(predicted_label)

if question:
    # 질문과 텍스트를 토큰화
    inputs = tokenizer.encode_plus(
        question,
        text_input,
        max_length=512,
        truncation=True,
        padding="max_length",
        return_tensors="pt"
    )

    # 모델을 통한 답변 예측
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        start_index = torch.argmax(start_logits)
        end_index = torch.argmax(end_logits) + 1
    
    # 예측된 답변 텍스트 추출
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_index:end_index]))

    # 결과 출력
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f'start_index: {start_index}')
    print(f'end_index: {end_index}')

else:
    print('올바른 문장입니다.')