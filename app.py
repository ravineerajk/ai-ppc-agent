import streamlit as st
from read_sheet import read_google_sheet
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Load env vars (used locally)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

st.set_page_config(page_title="AI PPC Agent", layout="wide")
st.title("🤖 AI PPC Campaign Assistant")

# Google Sheet Info
sheet_name = "CampaignReport"
worksheet_name = "Sheet1"

# Check OpenAI key
if not openai.api_key:
    st.error("❌ OpenAI API key not found.")
else:
    try:
        df = read_google_sheet(sheet_name, worksheet_name)
        st.success(f"✅ Loaded {len(df)} rows from '{sheet_name}' → '{worksheet_name}'")

        # --- Filters ---
        st.subheader("🔍 Filter Data")
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        num_cols = df.select_dtypes(include='number').columns.tolist()

        if cat_cols:
            selected = st.selectbox(f"Filter by {cat_cols[0]}:", ['All'] + df[cat_cols[0]].dropna().unique().tolist())
            if selected != 'All':
                df = df[df[cat_cols[0]] == selected]

        if num_cols:
            for col in num_cols[:2]:
                min_val, max_val = int(df[col].min()), int(df[col].max())
                selected_range = st.slider(f"{col} range", min_val, max_val, (min_val, max_val))
                df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

        st.dataframe(df, use_container_width=True)

        # --- GPT Analysis ---
        st.subheader("🧠 AI Analysis")

        if st.button("Analyze with GPT-4"):
            st.info("Analyzing... please wait ⏳")

            prompt = f"""
You are a senior PPC expert. Based on this Google Ads campaign data, give smart recommendations.

Please cover:
- Underperforming campaigns
- Which ones should get more budget
- Suggested bid/keyword/ad copy improvements
- Any unusual patterns or red flags

Here is the data (first 15 rows):

{df.head(15).to_string(index=False)}
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # or gpt-4 if you have access
                    messages=[
                        {"role": "system", "content": "You are a world-class PPC strategist."},
                        {"role": "user", "content": prompt}
                    ]
                )
                suggestion = response.choices[0].message.content
                st.markdown("### 💡 GPT Suggestions")
                st.write(suggestion)

            except Exception as e:
                st.error(f"Error calling GPT: {type(e).__name__} - {e}")

    except Exception as e:
        st.error(f"Error loading data: {type(e).__name__} - {e}")