import random
import io
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="QuickQuiz Kids", page_icon="🧒", layout="centered")

# ------------------ STYLES ------------------
st.markdown("""
<style>
body { background: #eef2ff; }
.card {
    background: linear-gradient(135deg, #ffffff, #f0f4ff);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.08);
}
.title {
    font-size: 26px;
    font-weight: 800;
    color: #1e3a8a;
}
.correct {
    background: #dcfce7;
    color: #166534;
    padding: 12px;
    border-radius: 12px;
    font-weight: 600;
}
.wrong {
    background: #fee2e2;
    color: #991b1b;
    padding: 12px;
    border-radius: 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ------------------ QUESTIONS + IMAGES ------------------
QUESTIONS = [
    ("Which animal is known as the Ship of the Desert?", "Camel",
     "https://cdn-icons-png.flaticon.com/512/616/616408.png"),

    ("How many legs does a spider have?", "Eight",
     "https://cdn-icons-png.flaticon.com/512/616/616430.png"),

    ("National river of India?", "Ganga",
     "https://cdn-icons-png.flaticon.com/512/684/684908.png"),

    ("The Sun rises in the ________?", "East",
     "https://cdn-icons-png.flaticon.com/512/3222/3222798.png"),

    ("Which is the largest planet?", "Jupiter",
     "https://cdn-icons-png.flaticon.com/512/3222/3222806.png"),
]

# ------------------ HELPERS ------------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    bio = io.BytesIO()
    tts.write_to_fp(bio)
    bio.seek(0)
    st.audio(bio.read(), format="audio/mp3")

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# ------------------ SESSION ------------------
if "idx" not in st.session_state:
    st.session_state.idx = random.randrange(len(QUESTIONS))
    st.session_state.submitted = False
    st.session_state.result = ""

# ------------------ UI ------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

header1, header2 = st.columns([8,2])
with header1:
    st.markdown("<div class='title'>QuickQuiz Kids 🎉</div>", unsafe_allow_html=True)
with header2:
    if st.button("Next ➡️"):
        st.session_state.idx = random.randrange(len(QUESTIONS))
        st.session_state.submitted = False
        st.session_state.result = ""

question, answer, img_url = QUESTIONS[st.session_state.idx]

st.markdown("---")

# ------------------ IMAGE ------------------
st.image(load_image(img_url), width=200)

# ------------------ QUESTION ------------------
qcol1, qcol2 = st.columns([8,2])
with qcol1:
    st.markdown(f"### {question}")
with qcol2:
    if st.button("🔊"):
        speak(question)

st.markdown("### 🎤 Speak your answer")

audio = st.audio_input("Tap to speak", disabled=st.session_state.submitted)

if audio and not st.session_state.submitted:
    with open("temp.wav", "wb") as f:
        f.write(audio.getbuffer())

    user_answer = speech_to_text("temp.wav")

    st.session_state.submitted = True

    if user_answer.lower().strip() == answer.lower():
        st.session_state.result = "correct"
    else:
        st.session_state.result = "wrong"

# ------------------ RESULT ------------------
if st.session_state.submitted:
    if st.session_state.result == "correct":
        st.markdown("<div class='correct'>✅ Correct!</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='wrong'>❌ Wrong</div>", unsafe_allow_html=True)

    acol1, acol2 = st.columns([8,2])
    with acol1:
        st.info(f"📘 Correct Answer: **{answer}**")
    with acol2:
        if st.button("🔊 Answer"):
            speak(answer)

st.markdown("</div>", unsafe_allow_html=True)

st.caption("🎓 Learn with Fun • Voice Enabled • Kid Friendly")
