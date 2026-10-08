import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Mini MacroSnap", page_icon="🥗")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

@st.cache_resource
def get_client():
    return genai.Client(api_key=GEMINI_API_KEY)

client = get_client()

SYSTEM_PROMPT = """You are Mini MacroSnap, a friendly AI nutrition buddy.
Analyze food descriptions and meal photos.
Give:
1. Meal name
2. Estimated calories
3. Estimated protein, carbs, and fat
Say clearly that estimates are approximate.
Keep the answer short and easy to understand.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🥗 Mini MacroSnap")
st.caption("AI meal analyzer powered by Gemini")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["kind"] == "image":
            st.image(message["content"])
        else:
            st.write(message["content"])

user_input = st.chat_input(
    "Describe your meal or attach a photo",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"]
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = [SYSTEM_PROMPT]

    if photo:
        photo_bytes = photo.getvalue()
        st.session_state.messages.append({
            "role": "user",
            "kind": "image",
            "content": photo_bytes
        })
        parts.append(types.Part.from_bytes(
            data=photo_bytes,
            mime_type=photo.type
        ))

    if text:
        st.session_state.messages.append({
            "role": "user",
            "kind": "text",
            "content": text
        })
        parts.append(text)
    elif photo:
        parts.append(
            "Identify this meal and estimate its calories and macros."
        )

    with st.spinner("Analyzing your meal..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=parts
            )
            answer = response.text
        except Exception as error:
            answer = f"Error: {error}"

    st.session_state.messages.append({
        "role": "assistant",
        "kind": "text",
        "content": answer
    })
    st.rerun()

if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
