from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document, SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
import sqlite3
from typing import List

from crud.chatbot import get_user_summary, save_user_summary, save_user_keywords
from models.user import User
from sqlalchemy.orm import Session

# 🔐 환경 변수 로드 및 LLM 구성
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# 🍜 prac.db 식당 데이터 로딩
conn = sqlite3.connect("prac.db")
cursor = conn.cursor()
cursor.execute("SELECT id, name, address, phone, rating, latitude, longitude FROM restaurants")
rows = cursor.fetchall()

documents = []
for row in rows:
    id_, name, address, phone, rating, lat, lng = row
    menu_text = "메뉴 정보 없음"
    content = f"""식당명: {name}
주소: {address}
전화번호: {phone}
평점: {rating}
메뉴:
{menu_text}
"""
    documents.append(Document(
        page_content=content,
        metadata={"id": id_, "latitude": lat, "longitude": lng, "rating": rating}
    ))

docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(documents)
vectorstore = FAISS.from_documents(docs, embeddings)

# 키워드 추출
def extract_keywords_from_summary(summary: str) -> List[str]:
    messages = [
        SystemMessage(content="다음 요약에서 사용자의 음식 취향을 나타내는 핵심 키워드 3~5개만 쉼표로 추출해줘."),
        HumanMessage(content=summary)
    ]
    result = llm(messages).content.strip()
    return [kw.strip() for kw in result.split(",") if kw.strip()]

# 의도 분류
def classify_intent(query: str, summary: str) -> str:
    messages = [
        SystemMessage(content="다음 질문이 음식 추천 의도인지 대화 의도인지 판단해줘. 결과는 '추천' 또는 '대화'로만 응답해."),
        HumanMessage(content=f"요약: {summary}\n질문: {query}")
    ]
    return llm(messages).content.strip()

# 메인 응답 생성 함수
def generate_chat_response(user: User, message: str, db: Session):
    summary_obj = get_user_summary(db, user.id)
    summary = getattr(summary_obj, "summary", "")

    intent = classify_intent(message, summary)

    if intent != "추천":
        messages = [
            SystemMessage(content="너는 음식 추천 챗봇이야. 사용자와 자연스럽게 대화해."),
            HumanMessage(content=message)
        ]
        result = llm(messages).content.strip()
        summary += f"\n[User]: {message}\n[Bot]: {result}"
        save_user_summary(db, user.id, summary)
        return {"response": result}

    # 추천 요청 처리
    results = vectorstore.similarity_search(message, k=3)
    if not results:
        return {"response": "입력하신 정보로는 추천할 수 있는 식당이 없습니다. 위치나 키워드를 다시 시도해주세요."}

    recommended = []
    for doc in results:
        lines = doc.page_content.strip().splitlines()
        name_line = next((line for line in lines if "식당명:" in line), lines[0])
        recommended.append(f"📍 {name_line.strip()}")

    response_text = "\n".join(recommended)

    summary += f"\n[User]: {message}\n[Bot]: {response_text}"
    save_user_summary(db, user.id, summary)
    keywords = extract_keywords_from_summary(summary)
    save_user_keywords(db, user.id, keywords)

    return {"response": response_text}
