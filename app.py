import streamlit as st
import random

st.set_page_config(page_title="Kids Stories App", page_icon="📚", layout="centered")

# --------------------------
# Custom CSS for a beautiful UI
# --------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }

    h1 {
        text-align: center;
        color: #ff6f61;
        font-size: 2.8rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
    }

    .stSelectbox label, .stTextInput label {
        font-weight: 600;
        color: #4a4a4a;
        font-size: 1.05rem;
    }

    .story-card {
        background: white;
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border-left: 6px solid #ff6f61;
        line-height: 1.9;
        font-size: 1.1rem;
        color: #333;
    }

    .story-title {
        color: #ff6f61;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        text-align: center;
    }

    .moral-box {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border-radius: 14px;
        padding: 1rem 1.5rem;
        margin-top: 1.2rem;
        font-weight: 600;
        color: #e65100;
        text-align: center;
        font-size: 1.05rem;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #ff6f61, #ff9a76);
        color: white;
        font-size: 1.15rem;
        font-weight: 700;
        border: none;
        border-radius: 30px;
        padding: 0.7rem 2.5rem;
        margin: 1rem auto;
        display: block;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(255,111,97,0.35);
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,111,97,0.5);
    }

    div.stDownloadButton > button {
        background: linear-gradient(90deg, #43a047, #66bb6a);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        margin: 0.5rem auto;
        display: block;
        transition: transform 0.2s;
        box-shadow: 0 4px 15px rgba(67,160,71,0.3);
    }

    div.stDownloadButton > button:hover {
        transform: translateY(-2px);
    }

    .header-emoji {
        text-align: center;
        font-size: 3rem;
        margin-bottom: -0.5rem;
    }

    .sub-text {
        text-align: center;
        color: #777;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------
# Story generator function
# --------------------------
def generate_story(character_name, age_group, theme, story_length, moral):
    openings = [
        f"Once upon a time, there was a cheerful child named {character_name}.",
        f"In a bright little village, {character_name} loved going on adventures.",
        f"Long ago, in a magical place, {character_name} discovered something unusual one morning."
    ]

    theme_lines = {
        "Friendship": [
            f"One day, {character_name} met a shy little friend who needed help.",
            f"At the park, {character_name} found someone sitting alone and decided to say hello.",
            f"{character_name} learned that being kind can turn strangers into wonderful friends."
        ],
        "Magic": [
            f"Behind the old tree, {character_name} found a glowing door to a magical land.",
            f"A tiny sparkling fairy appeared and asked {character_name} for help.",
            f"{character_name} discovered a secret wand hidden under a pile of golden leaves."
        ],
        "Animals": [
            f"In the forest, {character_name} heard a tiny cry and found a lost baby rabbit.",
            f"A clever parrot flew down and began talking to {character_name}.",
            f"{character_name} followed a trail of paw prints to an amazing surprise."
        ],
        "Adventure": [
            f"With a small backpack and a big smile, {character_name} set out on a brave journey.",
            f"{character_name} found an old map that led to a hidden treasure.",
            f"A mysterious path appeared, and {character_name} decided to explore it."
        ],
        "Princess": [
            f"In a shining kingdom, {character_name} visited a beautiful palace full of secrets.",
            f"A kind princess invited {character_name} to help prepare for a royal celebration.",
            f"{character_name} found a missing crown jewel and promised to return it."
        ],
        "Space": [
            f"One starry night, {character_name} climbed into a little rocket and flew into space.",
            f"On the moon, {character_name} met a funny alien with purple shoes.",
            f"{character_name} saw a blinking star map pointing toward a new planet."
        ]
    }

    middle_events = [
        f"At first, things seemed difficult, but {character_name} did not give up.",
        f"There was a problem to solve, and everyone looked to {character_name} for help.",
        f"{character_name} felt nervous for a moment, but remembered to be brave.",
        f"Using kindness, clever thinking, and courage, {character_name} found a way forward.",
        f"Along the way, {character_name} made new friends who joined the journey.",
        f"With a little creativity, {character_name} surprised everyone with a brilliant idea.",
        f"The path was not easy, but {character_name} kept going with a smile.",
        f"Together with new friends, {character_name} overcame every obstacle."
    ]

    endings = [
        f"In the end, everything turned out beautifully, and {character_name} returned home with a happy heart.",
        f"From that day on, {character_name} was remembered as kind, brave, and wise.",
        f"{character_name} smiled, knowing that even small acts can make a big difference.",
        f"And so, {character_name} went to sleep that night feeling proud and grateful for the amazing day."
    ]

    moral_lines = {
        "Kindness": "💛 **Moral:** Kindness always makes the world brighter.",
        "Honesty": "💙 **Moral:** Honesty is always the best choice.",
        "Bravery": "🧡 **Moral:** Being brave does not mean never feeling scared — it means trying anyway.",
        "Sharing": "💚 **Moral:** Sharing brings joy to everyone around us.",
        "Helping Others": "💜 **Moral:** Helping others makes us stronger together.",
        "Confidence": "❤️ **Moral:** Believe in yourself and never stop trying."
    }

    # Length-based paragraph count
    if story_length == "Short":
        parts = 4
    elif story_length == "Medium":
        parts = 6
    else:
        parts = 8

    story = []
    story.append(random.choice(openings))
    story.append(random.choice(theme_lines[theme]))

    used_middles = random.sample(middle_events, min(parts - 3, len(middle_events)))
    for line in used_middles:
        story.append(line)

    story.append(random.choice(endings))
    story.append(moral_lines[moral])

    # Age-based language adjustment
    if age_group == "3-5":
        title = f"🌈 {character_name}'s Little {theme} Story"
    elif age_group == "6-8":
        title = f"✨ {character_name} and the Wonderful {theme} Adventure"
    else:
        title = f"🚀 {character_name}'s Amazing {theme} Journey"

    return title, "\n\n".join(story)


# --------------------------
# App UI
# --------------------------
st.markdown('<div class="header-emoji">📖✨🌟</div>', unsafe_allow_html=True)
st.title("Kids Stories App")
st.markdown('<div class="sub-text">Create beautiful and fun stories for children — in just one click!</div>', unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    character_name = st.text_input("👤 Main character's name", "Lily")
    theme = st.selectbox(
        "🎨 Story theme",
        ["Friendship", "Magic", "Animals", "Adventure", "Princess", "Space"]
    )
    moral = st.selectbox(
        "💡 Moral of the story",
        ["Kindness", "Honesty", "Bravery", "Sharing", "Helping Others", "Confidence"]
    )

with col2:
    age_group = st.selectbox(
        "🎂 Age group",
        ["3-5", "6-8", "9-12"]
    )
    story_length = st.selectbox(
        "📏 Story length",
        ["Short", "Medium", "Long"]
    )

st.write("")

if st.button("✨ Generate Story ✨"):
    with st.spinner("Creating a magical story..."):
        import time
        time.sleep(1)  # Small delay for effect
        title, story = generate_story(character_name, age_group, theme, story_length, moral)

    # Split moral from story for styled rendering
    story_parts = story.rsplit("\n\n", 1)
    story_body = story_parts[0] if len(story_parts) > 1 else story
    moral_text = story_parts[1] if len(story_parts) > 1 else ""

    st.markdown(f'<div class="story-card"><div class="story-title">{title}</div>{story_body.replace(chr(10)+chr(10), "<br><br>")}</div>', unsafe_allow_html=True)

    if moral_text:
        st.markdown(f'<div class="moral-box">{moral_text}</div>', unsafe_allow_html=True)

    st.write("")

    # Plain text version for download
    plain_title = title.encode('ascii', 'ignore').decode('ascii').strip()
    plain_story = story.replace("**Moral:**", "Moral:").encode('ascii', 'ignore').decode('ascii').strip()

    st.download_button(
        label="📥 Download Story as Text",
        data=f"{plain_title}\n\n{plain_story}",
        file_name=f"{character_name.lower()}_story.txt",
        mime="text/plain"
    )

st.markdown('<div class="footer">Made with ❤️ for little readers everywhere | Kids Stories App</div>', unsafe_allow_html=True)
