# QuickQuiz (Streamlit)

A lightweight static quiz app built with Streamlit. It shows a random question from the list, lets you reveal the answer, and provides speaker buttons to play the question and answer using gTTS audio.

## Features
- Random question selection
- Show/hide answer
- Text-to-speech playback for question and answer

## Requirements
- Python 3.8+
- Internet access for gTTS to generate audio

## Install
```bash
python -m pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```

## Notes
- gTTS uses Google Text-to-Speech API and requires internet access.
- Audio is generated on the server-side and streamed to the browser via Streamlit's `st.audio`.

If you'd like offline TTS or different styling, tell me and I can update the app.