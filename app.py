import streamlit as st
from google_play_scraper import reviews, Sort
import anthropic
import google.generativeai as genai
import pandas as pd

st.set_page_config(page_title="AI Review Discovery Engine", page_icon="🎧", layout="wide")

st.title("🎧 AI-Powered Review Discovery Engine")
st.caption(
    "Point this at any Play Store app → it scrapes live reviews → AI analyzes them "
    "for music-discovery insights, automatically. Built to study Spotify's discovery problem."
)

with st.sidebar:
    st.header("⚙️ Settings")
    app_id = st.text_input(
        "Play Store App ID",
        value="com.spotify.music",
        help="Any Play Store app ID works. Default is Spotify."
    )
    count = st.slider("Number of reviews to scrape", 50, 500, 150, step=50)
    sort_choice = st.selectbox("Sort reviews by", ["Newest", "Most Relevant"])

    provider = st.radio(
        "AI Provider",
        ["Gemini (free)", "Claude"],
        help="Gemini's API has a free tier with no credit card needed. Claude requires paid credits."
    )

    if provider == "Gemini (free)":
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get a free key (no card required) at aistudio.google.com/apikey"
        )
    else:
        api_key = st.text_input(
            "Claude API Key",
            type="password",
            help="Your Anthropic API key — used only for this session, never stored or logged."
        )

    run = st.button("🔍 Scrape & Analyze", type="primary", use_container_width=True)

ANALYSIS_QUESTIONS = """1. Why do users struggle to discover new music? (root causes, not symptoms)
2. What are the most common frustrations with recommendations?
3. What listening behaviors are users trying to achieve?
4. What causes users to repeatedly listen to the same content?
5. Which user segments (identify 2-4 distinct ones) experience different discovery challenges, and how do their challenges differ?
6. What unmet needs emerge consistently across these reviews?"""

if run:
    if not api_key:
        st.error("⚠️ Please enter your API key in the sidebar to run the analysis.")
        st.stop()
    if not app_id:
        st.error("⚠️ Please enter a Play Store App ID.")
        st.stop()

    sort_map = {"Newest": Sort.NEWEST, "Most Relevant": Sort.MOST_RELEVANT}

    with st.spinner(f"📥 Scraping {count} live reviews for '{app_id}' from the Play Store..."):
        try:
            result, _ = reviews(
                app_id,
                lang='en',
                country='us',
                sort=sort_map[sort_choice],
                count=count,
            )
        except Exception as e:
            st.error(f"Scraping failed — check the App ID is correct. Error: {e}")
            st.stop()

    if not result:
        st.warning("No reviews found for this App ID. Double-check the package name (e.g. com.spotify.music).")
        st.stop()

    df = pd.DataFrame(result)[["userName", "score", "at", "content"]]
    df.columns = ["User", "Rating", "Date", "Review"]
    st.success(f"✅ Scraped {len(df)} real, live reviews for `{app_id}`.")

    with st.expander("📋 View raw scraped reviews"):
        st.dataframe(df, use_container_width=True, height=300)

    review_corpus = "\n---\n".join(df["Review"].dropna().astype(str).tolist())

    prompt = f"""You are a senior product research analyst at a music streaming company.
Below are real, live Google Play Store reviews. Analyze them ONLY based on what is actually
written — do not invent facts. Answer the following questions, grounded strictly in the review text,
using bullet points. For each insight, include a short paraphrased (not verbatim) example so the
finding is traceable back to real user language.

{ANALYSIS_QUESTIONS}

Format your response with clear markdown headers for each of the 6 questions.

REVIEWS:
{review_corpus}
"""

    with st.spinner(f"🧠 {provider.split(' ')[0]} is analyzing the reviews for discovery-related themes..."):
        try:
            if provider == "Gemini (free)":
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                analysis = response.text
            else:
                client = anthropic.Anthropic(api_key=api_key)
                msg = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=3000,
                    messages=[{"role": "user", "content": prompt}],
                )
                analysis = msg.content[0].text
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

    st.subheader("🧠 AI-Generated Discovery Insights")
    st.markdown(analysis)

    st.download_button(
        "⬇️ Download insights as .txt",
        analysis,
        file_name=f"{app_id}_discovery_insights.txt",
    )

else:
    st.info("👈 Choose a provider, enter your API key in the sidebar, and click **Scrape & Analyze** to run the live workflow.")
    st.markdown("""
### How this workflow works
1. **Point** — Give it any Play Store app ID (defaults to Spotify's `com.spotify.music`).
2. **Scrape** — It pulls real, live reviews directly from the Google Play Store. No manual copy-paste, no static dataset — re-run it any time for fresh data.
3. **Analyze** — The scraped reviews are sent to an AI model (Gemini or Claude), which extracts discovery-related themes,
   frustrations, user segments, and unmet needs — grounded in actual review language.
4. **Repeatable** — Point it at a competitor app, or re-run later to track how sentiment shifts over time.

This is the automated review-analysis engine referenced in the graduation project deck.
""")

st.markdown("---")
st.caption("Built as an AI-native review discovery workflow · Spotify Growth PM Graduation Project")
