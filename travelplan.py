# app.py
import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.utilities import DuckDuckGoSearchAPIWrapper

st.set_page_config(page_title="観戦旅行プランAI", page_icon="⚽")
st.title("⚽ 観戦旅行プランAI")

# 入力フォーム
with st.form("input_form"):
    api_key = st.text_input("🔑 OpenAI APIキーを入力してください", type="password")
    sport = st.text_input("🏟️ スポーツ種目", "サッカー")
    country = st.text_input("🌍 旅行先の国", "スペイン")
    year = st.text_input("📅 年", "2025")
    month = st.text_input("📆 月", "April")
    submitted = st.form_submit_button("旅行プランを作成する")

if submitted:
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        os.environ["OPENAI_API_KEY"] = api_key

        # モデルとツールの初期化
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            max_tokens=1500,
        )

        search = DuckDuckGoSearchAPIWrapper()
        search_tool = Tool(
            name="Search",
            func=search.run,
            description="サッカーなどの試合スケジュールを調べるためのWeb検索ツールです。"
        )

        agent = initialize_agent(
            tools=[search_tool],
            llm=llm,
            agent="chat-zero-shot-react-description",
            verbose=True,
        )

        # プロンプト生成
        task_prompt = f"""
あなたはプロの旅行プランナーです。

【タスク】
・{year}年{month}に開催される{sport}の試合と{country}への海外旅行プランを作成してください。
・DuckDuckGo検索ツールを使って現地の試合スケジュールを調べてください。
・試合日を中心に5日間の旅行プランを立ててください。
・観戦、観光、移動、食事、宿泊など、具体的な日程を含めてください。
"""

        # 実行
        with st.spinner("AIが旅行プランを作成中です..."):
            try:
                response = agent.run(task_prompt)
                st.success("旅行プランが完成しました！")
                st.text_area("📋 旅行プラン", response, height=400)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
