# empty file
import random
import io
from gtts import gTTS
import streamlit as st


st.set_page_config(page_title="QuickQuiz", page_icon=":books:", layout="centered")

CSS = """
body { background-color: #f6f8fb; }
.card { background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%); border-radius:12px; padding:24px; box-shadow: 0 8px 24px rgba(17,24,39,0.06); }
.title { font-weight:700; font-size:22px; }
.muted { color:#6b7280 }
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

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



def generate_tts_bytes(text: str, lang: str = "en") -> bytes:
	"""Generate mp3 bytes for given text using gTTS."""
	tts = gTTS(text=text, lang=lang)
	bio = io.BytesIO()
	tts.write_to_fp(bio)
	bio.seek(0)
	return bio.read()


if "idx" not in st.session_state:
	st.session_state.idx = random.randrange(len(QUESTIONS))
	st.session_state.revealed = False


st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div style='display:flex;justify-content:space-between;align-items:center'>", unsafe_allow_html=True)
st.markdown(f"<div><div class='title'>QuickQuiz</div><div class='muted'>Tap the speaker to hear text</div></div>", unsafe_allow_html=True)
if st.button("Next Question", key="next"):
	prev = st.session_state.idx
	# pick a different random index when possible
	if len(QUESTIONS) > 1:
		idx = prev
		while idx == prev:
			idx = random.randrange(len(QUESTIONS))
		st.session_state.idx = idx
	else:
		st.session_state.idx = prev
	st.session_state.revealed = False
st.markdown("</div>", unsafe_allow_html=True)

q_text, a_text = QUESTIONS[st.session_state.idx]

st.markdown("<hr />", unsafe_allow_html=True)

st.markdown("<div style='display:flex;align-items:center;gap:16px'>", unsafe_allow_html=True)
col1, col2 = st.columns([8,1])
with col1:
	st.markdown(f"### {q_text}")
with col2:
	if st.button("🔊", key="q_speak"):
		audio_bytes = generate_tts_bytes(q_text)
		st.audio(audio_bytes, format="audio/mp3")
st.markdown("</div>", unsafe_allow_html=True)

show = st.button("Show Answer", key="show")
if show:
	st.session_state.revealed = True

if st.session_state.revealed:
	st.markdown("<div style='display:flex;align-items:center;gap:16px;margin-top:8px'>", unsafe_allow_html=True)
	a_col1, a_col2 = st.columns([8,1])
	with a_col1:
		st.success(a_text)
	with a_col2:
		if st.button("🔊", key="a_speak"):
			audio_bytes = generate_tts_bytes(a_text)
			st.audio(audio_bytes, format="audio/mp3")
	st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("\n---\n\nMade with ♥ using Streamlit. Click `Next Question` for a different item.")

