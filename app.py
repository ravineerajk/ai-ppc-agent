import streamlit as st
from read_sheet import read_google_sheet
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set Streamlit page config
st.set_page_config(page_title="AI PPC Agent", layout="wide")
st.title("🤖 AI PPC Campaign Assistant")

# Sheet details (fixed for now)
sheet_name = "CampaignReport"
worksheet_name = "Sheet1"

# Check if API key and sheet names are present
if not openai_api_key:
    st.error("OpenAI API key not found. Make sure it's set in your `.env` file.")
else:
    try:
        # Load Google Sheet data
        df = read_google_sheet(sheet_name, worksheet_name)
        st.success(f"✅ Loaded {len(df)} rows from '{sheet_name}' → '{worksheet_name}'")

        # --- Filter Section ---
        st.subheader("🔍 Filter Data")

        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        num_cols = df.select_dtypes(include='number').columns.tolist()

        if cat_cols:
            selected_val = st.selectbox(f"Filter by {cat_cols[0]}:", ['All'] + df[cat_cols[0]].dropna().unique().tolist())
            if selected_val != 'All':
                df = df[df[cat_cols[0]] == selected_val]

        if num_cols:
            for col in num_cols[:2]:  # Show sliders for first 2 numeric columns
                min_val, max_val = int(df[col].min()), int(df[col].max())
                selected_range = st.slider(f"{col} range", min_val, max_val, (min_val, max_val))
                df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

        # --- Display Data ---
        st.dataframe(df, use_container_width=True)

        # --- GPT-4 Analysis ---
        st.subheader("🧠 AI Analysis")

        if st.button("Analyze with GPT-4"):
            st.info("Analyzing... please wait ⏳")

            client = OpenAI(api_key=openai_api_key)

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
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a world-class PPC strategist."},
                        {"role": "user", "content": prompt}
                    ]
                )
                suggestion = response.choices[0].message.content
                st.markdown("### 💡 GPT Suggestions")
                st.write(suggestion)

            except Exception as e:
                st.error(f"Error calling GPT: {e}")

    except Exception as e:
        st.error(f"Error loading data: {type(e).__name__} - {e}")