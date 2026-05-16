import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI
import os
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="🎬 CineMind AI",
    page_icon="🎥",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    color: white;
}

/* Header */
.main-title {
    font-size: 60px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg,#ff4b2b,#ff416c,#ffcc70);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #d3d3d3;
    margin-bottom: 40px;
}

/* Text Area */
textarea {
    border-radius: 20px !important;
    border: 2px solid #ff4b91 !important;
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
    padding: 15px !important;
    font-size: 16px !important;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 15px;
    height: 55px;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(90deg,#ff416c,#ff4b2b);
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 20px rgba(255,75,145,0.5);
}

/* Cards */
.movie-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 25px;
    padding: 25px;
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
}

/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.07);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 18px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD ENV
# =========================================================
load_dotenv()

# =========================================================
# MODEL
# =========================================================
@st.cache_resource
def get_model():
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY")
    )

model = get_model()

# =========================================================
# SCHEMA
# =========================================================
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

# =========================================================
# PROMPT
# =========================================================
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an AI movie information extractor.

Extract movie details from the paragraph.

Return ONLY valid JSON.

{format_instructions}
"""),
    ("human", "{paragraph}")
])

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.image("https://cdn-icons-png.flaticon.com/512/3418/3418886.png", width=120)

    st.title("🎬 CineMind AI")

    st.markdown("---")

    st.subheader("✨ Features")

    st.write("""
✅ AI Movie Analysis  
✅ JSON Structured Output  
✅ Beautiful UI  
✅ Fast Extraction  
✅ Smart Genre Detection  
""")

    st.markdown("---")

    if st.button("🎥 Load Demo Example"):

        st.session_state.example = """
Interstellar is a 2014 epic science fiction film directed by Christopher Nolan.
The film stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, and Michael Caine.
It follows a team of astronauts traveling through a wormhole in search of a new home for humanity.
The movie received a rating of 8.7 and won the Academy Award for Best Visual Effects.
"""

# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">🎥 CineMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Transform movie descriptions into intelligent structured data ✨</div>',
    unsafe_allow_html=True
)

# =========================================================
# INPUT AREA
# =========================================================
paragraph = st.text_area(
    "📄 Enter Movie Description",
    height=250,
    value=st.session_state.get("example", ""),
    placeholder="Paste any movie description here..."
)

# =========================================================
# EXTRACT BUTTON
# =========================================================
if st.button("🚀 Analyze Movie"):

    if not paragraph.strip():
        st.warning("⚠ Please enter a movie paragraph.")
    else:

        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        with st.spinner("🧠 AI is understanding the movie..."):

            try:

                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions()
                })

                response = model.invoke(final_prompt)

                movie_data = parser.parse(response.content)

                st.success("✅ Movie Analysis Completed!")

                # =========================================================
                # METRICS
                # =========================================================
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>🎬</h2>
                        <h3>{movie_data.title}</h3>
                        <p>Movie Title</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>📅</h2>
                        <h3>{movie_data.release_year}</h3>
                        <p>Release Year</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>⭐</h2>
                        <h3>{movie_data.rating}</h3>
                        <p>IMDb Rating</p>
                    </div>
                    """, unsafe_allow_html=True)

                # =========================================================
                # MOVIE DETAILS CARD
                # =========================================================
                st.markdown(f"""
                <div class="movie-card">

                <h1>🎞 {movie_data.title}</h1>

                <hr>

                <h3>🎬 Director</h3>
                <p>{movie_data.director}</p>

                <h3>🎭 Genres</h3>
                <p>{", ".join(movie_data.genre)}</p>

                <h3>👨‍🎤 Cast</h3>
                <p>{", ".join(movie_data.cast)}</p>

                <h3>📝 Summary</h3>
                <p>{movie_data.summary}</p>

                </div>
                """, unsafe_allow_html=True)

                # =========================================================
                # TABS
                # =========================================================
                tab1, tab2 = st.tabs(["📦 JSON Output", "🤖 Raw Response"])

                with tab1:
                    st.json(movie_data.dict())

                with tab2:
                    st.code(response.content, language="json")

                # =========================================================
                # DOWNLOAD BUTTON
                # =========================================================
                st.download_button(
                    label="⬇ Download JSON",
                    data=str(movie_data.dict()),
                    file_name="movie_data.json",
                    mime="application/json"
                )

                st.balloons()

            except Exception as e:

                st.error("❌ Failed to parse response or API issue.")

                with st.expander("See Error Details"):
                    st.exception(e)