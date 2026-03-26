import streamlit as st
import random

st.set_page_config(page_title="Kids Stories App", page_icon="📚", layout="centered")

# --------------------------
# Custom CSS — magical fairytale theme with cute visuals
# --------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bubblegum+Sans&family=Nunito:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    /* --- Dreamy animated background --- */
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 25%, #e8eaf6 50%, #e0f7fa 75%, #fff8e1 100%);
        background-size: 400% 400%;
        animation: gradientShift 12s ease infinite;
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- Floating decorations --- */
    .floating-decor {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .floating-decor span {
        position: absolute;
        font-size: 2rem;
        animation: floatUp 8s linear infinite;
        opacity: 0.5;
    }
    .floating-decor span:nth-child(1)  { left:  5%; animation-delay: 0s;   font-size: 1.8rem; }
    .floating-decor span:nth-child(2)  { left: 15%; animation-delay: 1.5s; font-size: 2.2rem; }
    .floating-decor span:nth-child(3)  { left: 25%; animation-delay: 3s;   font-size: 1.5rem; }
    .floating-decor span:nth-child(4)  { left: 38%; animation-delay: 0.8s; font-size: 2rem;   }
    .floating-decor span:nth-child(5)  { left: 50%; animation-delay: 2.2s; font-size: 1.6rem; }
    .floating-decor span:nth-child(6)  { left: 62%; animation-delay: 4s;   font-size: 2.4rem; }
    .floating-decor span:nth-child(7)  { left: 72%; animation-delay: 1s;   font-size: 1.4rem; }
    .floating-decor span:nth-child(8)  { left: 82%; animation-delay: 3.5s; font-size: 2rem;   }
    .floating-decor span:nth-child(9)  { left: 90%; animation-delay: 2s;   font-size: 1.8rem; }
    .floating-decor span:nth-child(10) { left: 95%; animation-delay: 5s;   font-size: 1.5rem; }

    @keyframes floatUp {
        0%   { transform: translateY(110vh) rotate(0deg);   opacity: 0; }
        10%  { opacity: 0.5; }
        90%  { opacity: 0.5; }
        100% { transform: translateY(-10vh) rotate(360deg);  opacity: 0; }
    }

    /* --- Sparkle animation for stars --- */
    @keyframes sparkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50%      { opacity: 1;   transform: scale(1.3); }
    }

    /* --- Title --- */
    h1 {
        font-family: 'Bubblegum Sans', cursive !important;
        text-align: center;
        color: #e91e63 !important;
        font-size: 3.2rem !important;
        text-shadow: 3px 3px 6px rgba(233,30,99,0.2);
        position: relative;
        z-index: 1;
    }

    h2, h3 {
        font-family: 'Bubblegum Sans', cursive !important;
        color: #7b1fa2 !important;
    }

    .stSelectbox label, .stTextInput label {
        font-weight: 700;
        color: #6a1b9a;
        font-size: 1.05rem;
    }

    /* --- Hero banner --- */
    .hero-banner {
        text-align: center;
        padding: 1.5rem 1rem 0.5rem;
        position: relative;
        z-index: 1;
    }
    .hero-banner .hero-animals {
        font-size: 3.5rem;
        letter-spacing: 12px;
        animation: bounce 2s ease-in-out infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-10px); }
    }
    .hero-banner .hero-title {
        font-family: 'Bubblegum Sans', cursive;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #e91e63, #ff6f00, #7b1fa2, #1976d2);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rainbowText 4s ease infinite;
    }
    @keyframes rainbowText {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-banner .hero-sub {
        color: #666;
        font-size: 1.15rem;
        margin-top: 0.3rem;
    }

    /* --- Theme visual cards --- */
    .theme-visual {
        text-align: center;
        font-size: 4rem;
        padding: 0.4rem 0 0.2rem;
        position: relative;
        z-index: 1;
    }

    /* --- Cute scene banner per theme --- */
    .scene-banner {
        text-align: center;
        font-size: 2.5rem;
        letter-spacing: 6px;
        padding: 0.5rem;
        margin: 0.8rem 0;
        border-radius: 20px;
        position: relative;
        z-index: 1;
    }
    .scene-friendship { background: linear-gradient(90deg, #fce4ec, #f8bbd0, #fce4ec); }
    .scene-magic       { background: linear-gradient(90deg, #ede7f6, #d1c4e9, #ede7f6); }
    .scene-animals     { background: linear-gradient(90deg, #e8f5e9, #c8e6c9, #e8f5e9); }
    .scene-adventure   { background: linear-gradient(90deg, #fff3e0, #ffe0b2, #fff3e0); }
    .scene-princess    { background: linear-gradient(90deg, #fce4ec, #f8bbd0, #fce4ec); }
    .scene-space       { background: linear-gradient(90deg, #e8eaf6, #c5cae9, #e8eaf6); }

    /* --- Story card with cute border --- */
    .story-card {
        background: linear-gradient(135deg, #fffde7 0%, #fff9c4 50%, #fff8e1 100%);
        border-radius: 24px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
        box-shadow: 0 10px 40px rgba(255,152,0,0.12);
        border: 3px dashed #ffcc80;
        line-height: 2;
        font-size: 1.12rem;
        color: #37474f;
        position: relative;
        z-index: 1;
    }
    .story-card::before {
        content: "📖";
        position: absolute;
        top: -18px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 2rem;
        background: #fffde7;
        padding: 0 10px;
    }

    .story-title {
        font-family: 'Bubblegum Sans', cursive;
        color: #d84315;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.08);
    }

    .moral-box {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-top: 1.2rem;
        font-weight: 700;
        color: #2e7d32;
        text-align: center;
        font-size: 1.1rem;
        border: 2px solid #a5d6a7;
        position: relative;
        z-index: 1;
    }
    .moral-box::before {
        content: "🌟";
        font-size: 1.5rem;
        margin-right: 8px;
    }

    /* --- Cute character cards for theme selection --- */
    .theme-cards {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin: 0.5rem 0;
        position: relative;
        z-index: 1;
    }
    .theme-card {
        background: white;
        border-radius: 16px;
        padding: 8px 14px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s;
        cursor: default;
    }
    .theme-card:hover {
        transform: scale(1.08);
    }
    .theme-card .tc-icon { font-size: 1.6rem; }
    .theme-card .tc-label { font-size: 0.75rem; font-weight: 600; color: #555; }

    /* --- Button styles --- */
    div.stButton > button {
        background: linear-gradient(90deg, #e91e63, #ff6f00, #ffc107) !important;
        background-size: 200% 200% !important;
        animation: btnGlow 3s ease infinite !important;
        color: white !important;
        font-family: 'Bubblegum Sans', cursive !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 3rem !important;
        margin: 1rem auto !important;
        display: block !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        box-shadow: 0 6px 25px rgba(233,30,99,0.35) !important;
    }
    @keyframes btnGlow {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(233,30,99,0.5) !important;
    }

    div.stDownloadButton > button {
        background: linear-gradient(90deg, #43a047, #66bb6a) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        margin: 0.5rem auto !important;
        display: block !important;
        transition: transform 0.2s !important;
        box-shadow: 0 4px 15px rgba(67,160,71,0.3) !important;
    }
    div.stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
    }

    /* --- Footer --- */
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding: 1.5rem;
        position: relative;
        z-index: 1;
    }
    .footer-animals {
        font-size: 1.8rem;
        letter-spacing: 8px;
        margin-bottom: 0.5rem;
    }

    /* --- Cute divider --- */
    .cute-divider {
        text-align: center;
        font-size: 1.5rem;
        letter-spacing: 10px;
        margin: 1rem 0;
        opacity: 0.7;
        position: relative;
        z-index: 1;
    }

    /* --- Reading scene illustration --- */
    .story-scene {
        text-align: center;
        font-size: 3rem;
        margin: 0.5rem 0;
        letter-spacing: 5px;
        position: relative;
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# ----- Floating background decorations -----
st.markdown("""
<div class="floating-decor">
    <span>⭐</span><span>🦋</span><span>🌸</span><span>🍄</span><span>✨</span>
    <span>🌙</span><span>🦄</span><span>🌈</span><span>🎀</span><span>💫</span>
</div>
""", unsafe_allow_html=True)


# --------------------------
# Theme visuals mapping
# --------------------------
THEME_VISUALS = {
    "Friendship": {
        "scene": "👧🤝👦  💕  🌻🏡🌳",
        "icon": "💕",
        "class": "scene-friendship",
        "story_deco": "🌸",
    },
    "Magic": {
        "scene": "🧙‍♂️✨🪄  🏰  🌙🔮🦄",
        "icon": "🔮",
        "class": "scene-magic",
        "story_deco": "✨",
    },
    "Animals": {
        "scene": "🐰🦊🐻  🌲🌿  🦋🐦🦔",
        "icon": "🐾",
        "class": "scene-animals",
        "story_deco": "🐾",
    },
    "Adventure": {
        "scene": "🗺️⛵🏔️  🌅  🧭🎒🏝️",
        "icon": "🗺️",
        "class": "scene-adventure",
        "story_deco": "⚡",
    },
    "Princess": {
        "scene": "👸🏰👑  💎  🦢🌹🎀",
        "icon": "👑",
        "class": "scene-princess",
        "story_deco": "💎",
    },
    "Space": {
        "scene": "🚀🌍🌙  ⭐  👽🛸🪐",
        "icon": "🚀",
        "class": "scene-space",
        "story_deco": "🌟",
    },
}


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
        "Kindness": "💛 Kindness always makes the world brighter.",
        "Honesty": "💙 Honesty is always the best choice.",
        "Bravery": "🧡 Being brave does not mean never feeling scared — it means trying anyway.",
        "Sharing": "💚 Sharing brings joy to everyone around us.",
        "Helping Others": "💜 Helping others makes us stronger together.",
        "Confidence": "❤️ Believe in yourself and never stop trying."
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

# Hero banner with cute animated characters
st.markdown("""
<div class="hero-banner">
    <div class="hero-animals">🐰🦊🐻🦄🐱🦋</div>
    <div class="hero-title">Kids Stories App</div>
    <div class="hero-sub">Create magical, fun stories for children — in just one click!</div>
</div>
""", unsafe_allow_html=True)

# Cute theme showcase
st.markdown("""
<div class="theme-cards">
    <div class="theme-card"><div class="tc-icon">👧💕👦</div><div class="tc-label">Friendship</div></div>
    <div class="theme-card"><div class="tc-icon">🧙‍♂️🔮✨</div><div class="tc-label">Magic</div></div>
    <div class="theme-card"><div class="tc-icon">🐰🦊🐻</div><div class="tc-label">Animals</div></div>
    <div class="theme-card"><div class="tc-icon">🗺️⛵🏔️</div><div class="tc-label">Adventure</div></div>
    <div class="theme-card"><div class="tc-icon">👸🏰👑</div><div class="tc-label">Princess</div></div>
    <div class="theme-card"><div class="tc-icon">🚀🌙👽</div><div class="tc-label">Space</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cute-divider">🌸🦋🌻🍄🌈</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    character_name = st.text_input("🧒 Main character's name", "Lily")
    theme = st.selectbox(
        "🎨 Story theme",
        ["Friendship", "Magic", "Animals", "Adventure", "Princess", "Space"]
    )
    moral = st.selectbox(
        "🌟 Moral of the story",
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

# Show theme scene preview
tv = THEME_VISUALS[theme]
st.markdown(f'<div class="scene-banner {tv["class"]}">{tv["scene"]}</div>', unsafe_allow_html=True)

st.write("")

if st.button("🪄 Create My Story! ✨"):
    with st.spinner("✨ Sprinkling fairy dust on your story... ✨"):
        import time
        time.sleep(1.2)
        title, story = generate_story(character_name, age_group, theme, story_length, moral)

    # Split moral from story for styled rendering
    story_parts = story.rsplit("\n\n", 1)
    story_body = story_parts[0] if len(story_parts) > 1 else story
    moral_text = story_parts[1] if len(story_parts) > 1 else ""

    # Theme-appropriate story scene illustration
    st.markdown(f'<div class="story-scene">{tv["scene"]}</div>', unsafe_allow_html=True)

    # Story card with decorations
    deco = tv["story_deco"]
    decorated_body = story_body.replace(chr(10)+chr(10), f"<br><br>{deco} ")
    st.markdown(
        f'<div class="story-card">'
        f'<div class="story-title">{title}</div>'
        f'{deco} {decorated_body}'
        f'</div>',
        unsafe_allow_html=True
    )

    if moral_text:
        st.markdown(f'<div class="moral-box">{moral_text}</div>', unsafe_allow_html=True)

    st.markdown('<div class="cute-divider">⭐🌈⭐🌈⭐</div>', unsafe_allow_html=True)

    # Plain text version for download
    plain_title = title.encode('ascii', 'ignore').decode('ascii').strip()
    plain_story = story.encode('ascii', 'ignore').decode('ascii').strip()

    st.download_button(
        label="📥 Download My Story",
        data=f"{plain_title}\n\n{plain_story}",
        file_name=f"{character_name.lower()}_story.txt",
        mime="text/plain"
    )

st.markdown("""
<div class="footer">
    <div class="footer-animals">🐰🌸🦊🌻🐻🌈🦋✨🦄💫</div>
    Made with ❤️ for little readers everywhere<br>
    <small>Kids Stories App — Where imagination comes alive!</small>
</div>
""", unsafe_allow_html=True)
