import streamlit as st
import random


st.set_page_config(page_title="Emoji Code Breaker", page_icon="🎯",initial_sidebar_state="collapsed")


# ---- Background colors

urls=["",""]
page_bg_color = """
<style>
.stApp{
    background-color: #4d8f6c;
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

custom_css = """

<style>

div[data-baseweb="select"] > div {
    background-color: chartreuse;
}
/* Hide original SVG paths in the toggle button */
button[data-testid="stBaseButton-headerNoPadding"] svg path {
    display: none !important;
}

button[data-testid="stBaseButton-headerNoPadding"]::before {
    content: "";
    position: relative;
    top: -6px;
    left: 12px;
    width: 20px;
    height: 2px;
    background: currentColor;
    box-shadow:
        0 6px currentColor,
        0 12px currentColor;
}
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)

with st.sidebar:
    st.title('How to play')
    st.write("- Every game has a different fruit secret")
    st.write("- Crack the Code")
    st.write("- Note your Attemot Count")
    st.write("- Share with Friends!")





# List of emojis to choose from
emoji_pool = ["🍎", "🍌", "🍇", "🍉", "🍍", "🍓"]

# Initialize session state
if "secret_code" not in st.session_state or st.button("🔁 New Game"):
    st.session_state.secret_code = random.choices(emoji_pool, k=3)
    st.session_state.attempts = []
    st.session_state.attempts_count = 0
    st.session_state.game_over = False

st.title("🎯 :violet[Emoji Code] :blue[Breaker]")
st.markdown("Guess the secret 3-emoji code!")


# Emoji selectors
col1, col2, col3 = st.columns(3)
with col1:
    guess1 = st.selectbox("Emoji 1", emoji_pool, key="g1")
with col2:
    guess2 = st.selectbox("Emoji 2", emoji_pool, key="g2")
with col3:
    guess3 = st.selectbox("Emoji 3", emoji_pool, key="g3")

guess = [guess1, guess2, guess3]

if (not st.session_state.game_over):
    if st.button("🔍 Submit Guess"):
        feedback = []
        secret = st.session_state.secret_code.copy()
        temp_guess = guess.copy()
        st.session_state.attempts_count += 1
    
        # First pass: correct emoji in correct position
        for i in range(3):
            if temp_guess[i] == secret[i]:
                feedback.append("✅")
                secret[i] = None
                temp_guess[i] = None
            else:
                feedback.append(None)
    
        # Second pass: correct emoji in wrong position
        for i in range(3):
            if temp_guess[i] and temp_guess[i] in secret:
                feedback[i] = "🔁"
                secret[secret.index(temp_guess[i])] = None
            elif feedback[i] is None:
                feedback[i] = "❌"
    
        if len(st.session_state.attempts) == 0:
            st.session_state.attempts.append((guess.copy(), feedback.copy()))
        else:
            st.session_state.attempts[0] = (guess.copy(), feedback.copy())


# Show attempts
st.subheader("Your Attempts")
st.write("Attempts Count: ", st.session_state.attempts_count)
for attempt, result in st.session_state.attempts:
    showText = ""#.join(attempt), "→", " ".join(result)
    for emoji in attempt:
        showText += emoji+" "
    showText+= "→"
    for emoji in result:
        showText += emoji+" "
    st.badge(showText, color="orange", icon=":material/person_play:")

# Check win
if any(result == ["✅", "✅", "✅"] for _, result in st.session_state.attempts):
    st.balloons()
    st.success("🎉 You cracked the code!")
    st.write("Secret code was:", " ".join(st.session_state.secret_code))
    st.session_state.game_over = True