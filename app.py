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
	# General Knowledge Questions
    ("Which animal is known as the \"Ship of the Desert\"?", "Camel"),
    ("How many legs does a spider have?", "Eight"),
    ("National river of India?", "Ganga"),
    ("National reptile of India?", "King Cobra"),
    ("How many continents are there in the world?", "Seven"),
    ("Name the biggest continent in the world.", "Asia"),
    ("The Sun rises in the ________?", "East"),
    ("Name the largest planet in our Solar System.", "Jupiter"),
    ("Who is the first woman Prime Minister of India?", "Indira Gandhi"),
    ("Name the first man to walk on the Moon.", "Neil Armstrong"),
    ("How many days are there in a year?", "365"),
    ("How many days are there in a week?", "7"),
    ("Which month of the year has less days?", "February"),

    # Transportation
    ("Who drives a vehicle?", "Driver"),
    ("Who drives a boat?", "Sailor"),
    ("Who drives a ship?", "Captain"),
    ("Who drives a train?", "Locomotive pilot"),
    ("Who flies an airplane?", "Pilot"),

    # Animal Facts
    ("Which is the largest animal in the world?", "Blue Whale"),
    ("Which animal cannot close its eyes?", "Fish"),
    ("Which animal can survive without a head?", "Cockroach"),
    ("Which animal has no heart?", "Jellyfish"),
    ("Which is the slowest animal in the world?", "Snail / Sloth"),

    # India - Important G.K.
    ("When do we celebrate Independence Day?", "15th August"),
    ("Who is our Prime Minister?", "Narendra Modi"),
    ("Which is the biggest flower in the world?", "Rafflesia"),
    ("Which is the tallest animal in the world?", "Giraffe"),
    ("Which country invented paper?", "China"),

    # Colours
    ("What are the primary colours?", "Red, Blue, and Yellow"),
    ("What are the secondary colours?", "Green, Orange, and Purple"),
    ("How many colours are there in the rainbow?", "Seven"),
    ("Name the colours in the rainbow?", "VIBGYOR-Violet, Indigo, Blue, Green, Yellow, Orange, Red"),
    ("What colour do you get when you mix red and blue?", "Purple"),

    # Fruits
    ("Name few fruits with many seeds?", "Watermelon, Papaya, and Pomegranate"),
    ("Name a fruit which has one seed?", "Mango, Plum, Cherry"),
    ("Which fruit is known as the \"king of fruits\"?", "Mango"),
    ("Which fruit is red in colour and good for the heart?", "Apple"),

    # Vegetables
    ("Name few underground vegetables?", "Carrot, Potato, and Beetroot"),
    ("Name few green vegetables?", "Spinach, Cabbage, and Broccoli"),
    ("Which vegetable is used to make French fries?", "Potato"),
    ("Which vegetable is long and orange in colour?", "Carrot"),
    ("Which vegetable looks like a small tree?", "Broccoli"),

    # Body Parts
    ("How many sense organs do we have?", "Five"),
    ("Name the 5 sense organs?", "Eyes, Ears, Nose, Tongue, Skin"),
    ("Which body part helps us smell?", "Nose"),
    ("Which body part helps us hear sounds?", "Ears"),
    ("Which body part helps us taste food?", "Tongue"),
    ("Which body part helps us walk and run?", "Legs"),

    # Shapes
    ("How many sides does a triangle have?", "Three"),
    ("Which shape has four equal sides?", "Square"),
    ("Which shape has no edges?", "Circle"),
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

question, answer = QUESTIONS[st.session_state.idx]

st.markdown("---")

# ------------------ IMAGE ------------------
st.image(load_image('https://cdn-icons-png.flaticon.com/512/3222/3222806.png'), width=200)

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
