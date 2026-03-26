import streamlit as st
import streamlit.components.v1 as components
import random
import json

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

    /* --- Image slideshow --- */
    .slideshow-container {
        position: relative;
        width: 100%;
        max-width: 500px;
        margin: 1rem auto;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        z-index: 1;
        background: white;
    }
    .slideshow-container img, .slideshow-container lottie-player {
        width: 100%;
        height: 350px;
        object-fit: contain;
        border-radius: 24px;
        transition: opacity 0.8s ease-in-out;
    }
    .slide-caption {
        text-align: center;
        font-family: 'Bubblegum Sans', cursive;
        font-size: 1.15rem;
        color: #7b1fa2;
        margin-top: 0.5rem;
        padding: 0 1rem;
    }

    /* --- Lottie animation container --- */
    .lottie-stage {
        width: 100%;
        max-width: 500px;
        margin: 0.5rem auto;
        border-radius: 24px;
        overflow: hidden;
        background: linear-gradient(135deg, #ffe0f0, #e0f0ff, #f0ffe0);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        position: relative;
        z-index: 1;
    }
    .lottie-stage lottie-player {
        width: 100%;
        height: 320px;
    }

    /* --- Audio player controls --- */
    .audio-controls {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 1.2rem 0;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    .audio-btn {
        background: linear-gradient(135deg, #7b1fa2, #ab47bc);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: 700;
        font-family: 'Nunito', sans-serif;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(123,31,162,0.3);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .audio-btn:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 20px rgba(123,31,162,0.5);
    }
    .audio-btn.stop-btn {
        background: linear-gradient(135deg, #c62828, #ef5350);
        box-shadow: 0 4px 15px rgba(198,40,40,0.3);
    }
    .audio-btn.pause-btn {
        background: linear-gradient(135deg, #f57c00, #ffb74d);
        box-shadow: 0 4px 15px rgba(245,124,0,0.3);
    }

    /* --- Narration highlight box --- */
    .narration-box {
        background: linear-gradient(135deg, #ede7f6, #e8eaf6);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        color: #4a148c;
        border: 2px solid #ce93d8;
        position: relative;
        z-index: 1;
    }
    .narration-box .now-playing {
        font-size: 0.85rem;
        color: #9c27b0;
        margin-bottom: 0.3rem;
    }

    /* --- Speed selector --- */
    .speed-selector {
        text-align: center;
        margin: 0.5rem 0;
        position: relative;
        z-index: 1;
    }
    .speed-selector select {
        padding: 6px 16px;
        border-radius: 20px;
        border: 2px solid #ce93d8;
        font-family: 'Nunito', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        color: #4a148c;
        background: white;
        cursor: pointer;
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
        "animations": [
            ("https://lottie.host/4ab414f5-e2b4-4434-8d4e-5a592fda3e05/vKJEhJYLOz.json", "Best friends holding hands 💕"),
            ("https://lottie.host/0c7a64c5-87e0-4c84-b9f5-2d3dbf1d9e2a/i1JFxdGLTp.json", "Kids playing together in the park 🌻"),
            ("https://lottie.host/e8c8f13e-9e42-4b38-9b50-46e73f5f6a1e/2KXziXfJRH.json", "A warm hug between friends 🤗"),
            ("https://lottie.host/bd79f96a-2b7a-4ae1-afe7-ae77d8c1f3c5/jNY3EiXlJJ.json", "Sharing stories under a tree 🌳"),
        ],
        "moods": ["warm", "happy", "gentle", "cheerful"],
    },
    "Magic": {
        "scene": "🧙‍♂️✨🪄  🏰  🌙🔮🦄",
        "icon": "🔮",
        "class": "scene-magic",
        "story_deco": "✨",
        "animations": [
            ("https://lottie.host/f3f5b3a5-bcbd-4150-b38c-a1a5f37d6a13/4kfMJbXuDd.json", "A wizard casting sparkly spells ✨"),
            ("https://lottie.host/a0ef2a83-1c47-4a4d-938a-c6c50e04e1ae/iQswf7pYVh.json", "A magical unicorn galloping 🦄"),
            ("https://lottie.host/90ce5fcc-f8ce-4133-b1c8-a1cee1db49a9/ZLdvPNZn4U.json", "Enchanted fairy with wand 🧚"),
            ("https://lottie.host/7e3f3d2a-3a7f-4d41-b5a1-1c5e6f6d9e3a/xPmJ1HfY5K.json", "A glowing magical potion 🔮"),
        ],
        "moods": ["mysterious", "wonder", "whispery", "magical"],
    },
    "Animals": {
        "scene": "🐰🦊🐻  🌲🌿  🦋🐦🦔",
        "icon": "🐾",
        "class": "scene-animals",
        "story_deco": "🐾",
        "animations": [
            ("https://lottie.host/a5d3f1e2-5e4a-4b3c-9d2a-1f3e5a7c9b1d/kPmL2GfX3H.json", "A cute bunny hopping around 🐰"),
            ("https://lottie.host/b6e4g2f3-6f5b-5c4d-0e3b-2g4f6b8d0c2e/lQnM3HgY4I.json", "A friendly bear waving hello 🐻"),
            ("https://lottie.host/c7f5h3g4-7g6c-6d5e-1f4c-3h5g7c9e1d3f/mRoN4IhZ5J.json", "A cheeky fox in the forest 🦊"),
            ("https://lottie.host/d8g6i4h5-8h7d-7e6f-2g5d-4i6h8d0f2e4g/nSpO5JiA6K.json", "Colorful butterflies dancing 🦋"),
        ],
        "moods": ["playful", "curious", "funny", "gentle"],
    },
    "Adventure": {
        "scene": "🗺️⛵🏔️  🌅  🧭🎒🏝️",
        "icon": "🗺️",
        "class": "scene-adventure",
        "story_deco": "⚡",
        "animations": [
            ("https://lottie.host/e9h7j5i6-9i8e-8f7g-3h6e-5j7i9e1g3f5h/oTqP6KjB7L.json", "Setting off on a big adventure! 🎒"),
            ("https://lottie.host/f0i8k6j7-0j9f-9g8h-4i7f-6k8j0f2h4g6i/pUrQ7LkC8M.json", "Sailing across the sea ⛵"),
            ("https://lottie.host/g1j9l7k8-1k0g-0h9i-5j8g-7l9k1g3i5h7j/qVsR8MlD9N.json", "Climbing a tall mountain 🏔️"),
            ("https://lottie.host/h2k0m8l9-2l1h-1i0j-6k9h-8m0l2h4j6i8k/rWtS9NmE0O.json", "Finding a hidden treasure chest 💎"),
        ],
        "moods": ["excited", "dramatic", "brave", "thrilling"],
    },
    "Princess": {
        "scene": "👸🏰👑  💎  🦢🌹🎀",
        "icon": "👑",
        "class": "scene-princess",
        "story_deco": "💎",
        "animations": [
            ("https://lottie.host/i3l1n9m0-3m2i-2j1k-7l0i-9n1m3i5k7j9l/sXuT0OnF1P.json", "A beautiful princess dancing 👸"),
            ("https://lottie.host/j4m2o0n1-4n3j-3k2l-8m1j-0o2n4j6l8k0m/tYvU1PoG2Q.json", "A grand castle shining bright 🏰"),
            ("https://lottie.host/k5n3p1o2-5o4k-4l3m-9n2k-1p3o5k7m9l1n/uZwV2QpH3R.json", "Royal crown sparkling with gems 👑"),
            ("https://lottie.host/l6o4q2p3-6p5l-5m4n-0o3l-2q4p6l8n0m2o/vAxW3RqI4S.json", "A magical royal garden 🌹"),
        ],
        "moods": ["elegant", "dreamy", "gentle", "grand"],
    },
    "Space": {
        "scene": "🚀🌍🌙  ⭐  👽🛸🪐",
        "icon": "🚀",
        "class": "scene-space",
        "story_deco": "🌟",
        "animations": [
            ("https://lottie.host/m7p5r3q4-7q6m-6n5o-1p4m-3r5q7m9o1n3p/wByX4SrJ5T.json", "A rocket blasting into space! 🚀"),
            ("https://lottie.host/n8q6s4r5-8r7n-7o6p-2q5n-4s6r8n0p2o4q/xCzY5TsK6U.json", "A friendly green alien waving 👽"),
            ("https://lottie.host/o9r7t5s6-9s8o-8p7q-3r6o-5t7s9o1q3p5r/yDAZ6UtL7V.json", "Spinning planets and stars 🪐"),
            ("https://lottie.host/p0s8u6t7-0t9p-9q8r-4s7p-6u8t0p2r4q6s/zEBA7VuM8W.json", "Walking on the moon 🌙"),
        ],
        "moods": ["wonder", "funny", "excited", "cosmic"],
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

    st.markdown('<div class="cute-divider">🔊🎵🔊🎵🔊</div>', unsafe_allow_html=True)

    # ---- AUDIO NARRATION + CARTOON ANIMATION STAGE ----
    st.markdown("### 🎧 Listen to Your Story")

    # Prepare story paragraphs and animation data
    story_paragraphs = story.split("\n\n")
    animations = tv["animations"]
    moods = tv.get("moods", ["happy", "gentle", "excited", "warm"])

    # Build JSON data for the JavaScript component
    narration_data = json.dumps({
        "title": title,
        "paragraphs": story_paragraphs,
        "animations": [{"url": a[0], "caption": a[1]} for a in animations],
        "moods": moods,
        "theme": theme,
    })

    # Complete HTML/JS component — Lottie animations + storytelling voice
    audio_html = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script>

    <div id="story-player" style="position:relative; z-index:1;">
        <!-- Cartoon Animation Stage -->
        <div class="lottie-stage" id="lottie-stage">
            <lottie-player
                id="lottie-anim"
                src="{animations[0][0]}"
                background="transparent"
                speed="1"
                loop
                autoplay
                style="width:100%; height:320px;">
            </lottie-player>
        </div>
        <div class="slide-caption" id="slide-caption">🎬 {animations[0][1]}</div>

        <!-- Currently reading paragraph -->
        <div class="narration-box" id="narration-box">
            <div class="now-playing" id="now-playing-label">🎵 Story time! Press play to begin...</div>
            <div id="current-text" style="font-size:1.15rem; line-height:1.7;">
                Press ▶️ Play to hear your magical story read aloud!
            </div>
        </div>

        <!-- Voice & Speed selector -->
        <div class="speed-selector">
            🗣️ Narrator Voice:
            <select id="voice-select" style="margin-right:12px;">
                <option value="auto">🎭 Auto (Best match)</option>
            </select>
            Speed:
            <select id="speed-select">
                <option value="0.55">🐢 Very Slow (Toddlers)</option>
                <option value="0.7">🐰 Slow & Gentle</option>
                <option value="0.85" selected>🎙️ Storyteller</option>
                <option value="1.0">📖 Normal</option>
            </select>
        </div>

        <!-- Controls -->
        <div class="audio-controls">
            <button class="audio-btn" onclick="playStory()">▶️ Play Story</button>
            <button class="audio-btn pause-btn" onclick="pauseStory()">⏸️ Pause</button>
            <button class="audio-btn" onclick="resumeStory()">⏯️ Resume</button>
            <button class="audio-btn stop-btn" onclick="stopStory()">⏹️ Stop</button>
        </div>
    </div>

    <script>
        const data = {narration_data};
        const paragraphs = data.paragraphs;
        const animations = data.animations;
        const moods = data.moods;
        const storyTheme = data.theme;
        let currentPara = 0;
        let synth = window.speechSynthesis;
        let isPlaying = false;
        let bestVoice = null;

        // --- Voice Setup: find the softest, friendliest voice ---
        function loadVoices() {{
            const voices = synth.getVoices();
            const voiceSelect = document.getElementById('voice-select');

            // Priority order for kid-friendly voices
            const preferred = [
                'Google UK English Female',
                'Microsoft Zira',
                'Samantha',
                'Google US English',
                'Karen',
                'Moira',
                'Tessa',
                'Fiona',
                'Victoria',
                'Microsoft Hazel',
            ];

            // Populate voice dropdown
            voiceSelect.innerHTML = '<option value="auto">🎭 Auto (Best match)</option>';
            voices.forEach((v, i) => {{
                const opt = document.createElement('option');
                opt.value = i;
                opt.textContent = v.name + (v.lang ? ' (' + v.lang + ')' : '');
                voiceSelect.appendChild(opt);
            }});

            // Auto-select best voice
            for (let name of preferred) {{
                const found = voices.find(v => v.name.includes(name));
                if (found) {{ bestVoice = found; break; }}
            }}
            // Fallback: any English female-sounding voice
            if (!bestVoice) {{
                bestVoice = voices.find(v => v.lang.startsWith('en') && (v.name.toLowerCase().includes('female') || v.name.includes('Zira') || v.name.includes('Samantha')));
            }}
            if (!bestVoice && voices.length > 0) {{
                bestVoice = voices.find(v => v.lang.startsWith('en')) || voices[0];
            }}
        }}

        if (synth.onvoiceschanged !== undefined) {{
            synth.onvoiceschanged = loadVoices;
        }}
        loadVoices();

        // --- Mood-based voice parameters for storytelling ---
        function getMoodParams(paraIndex, totalParas) {{
            const position = paraIndex / totalParas; // 0 to 1
            const moodIdx = Math.min(paraIndex, moods.length - 1);
            const mood = moods[moodIdx] || 'happy';
            let pitch = 1.0;
            let rateMultiplier = 1.0;
            let pauseAfter = 600; // ms pause between paragraphs

            // Opening — slow, warm, inviting
            if (paraIndex === 0) {{
                pitch = 1.05;
                rateMultiplier = 0.9;
                pauseAfter = 800;
            }}
            // Ending / moral — slow, soft, meaningful
            else if (paraIndex >= totalParas - 2) {{
                pitch = 0.95;
                rateMultiplier = 0.85;
                pauseAfter = 1000;
            }}
            // Middle sections — mood-based
            else {{
                switch(mood) {{
                    case 'warm':
                    case 'gentle':
                    case 'dreamy':
                    case 'elegant':
                        pitch = 1.0; rateMultiplier = 0.92; pauseAfter = 700;
                        break;
                    case 'happy':
                    case 'cheerful':
                    case 'playful':
                        pitch = 1.15; rateMultiplier = 1.0; pauseAfter = 500;
                        break;
                    case 'mysterious':
                    case 'whispery':
                    case 'magical':
                    case 'cosmic':
                        pitch = 0.9; rateMultiplier = 0.85; pauseAfter = 900;
                        break;
                    case 'excited':
                    case 'thrilling':
                    case 'dramatic':
                    case 'brave':
                        pitch = 1.1; rateMultiplier = 1.05; pauseAfter = 600;
                        break;
                    case 'funny':
                    case 'curious':
                        pitch = 1.2; rateMultiplier = 0.95; pauseAfter = 700;
                        break;
                    case 'wonder':
                        pitch = 1.05; rateMultiplier = 0.88; pauseAfter = 800;
                        break;
                    default:
                        pitch = 1.0; rateMultiplier = 1.0; pauseAfter = 600;
                }}
            }}

            return {{ pitch, rateMultiplier, pauseAfter }};
        }}

        // --- Add storytelling flair to text ---
        function addStorytellingPauses(text) {{
            // Add slight pauses at commas and dramatic moments
            let enhanced = text;
            // Natural pauses
            enhanced = enhanced.replace(/\\.\\.\\./, '... ');
            enhanced = enhanced.replace(/!/, '! ');
            enhanced = enhanced.replace(/\\?/, '? ');
            return enhanced;
        }}

        // --- Update Lottie animation for current paragraph ---
        function updateAnimation(paraIndex) {{
            const animIdx = Math.floor((paraIndex / paragraphs.length) * animations.length) % animations.length;
            const anim = animations[animIdx];
            const player = document.getElementById('lottie-anim');
            const caption = document.getElementById('slide-caption');

            try {{
                player.load(anim.url);
                caption.innerHTML = '🎬 ' + anim.caption;
            }} catch(e) {{
                // Fallback: just update caption
                caption.innerHTML = '🎬 ' + anim.caption;
            }}
        }}

        // --- Speak a paragraph with storytelling style ---
        function speakParagraph(index) {{
            if (index >= paragraphs.length) {{
                isPlaying = false;
                document.getElementById('now-playing-label').textContent = '🎉 Story Complete!';
                document.getElementById('current-text').innerHTML =
                    '<span style="font-size:1.3rem;">✨ The End! ✨</span><br>' +
                    '<span style="color:#666; font-size:0.95rem;">Hope you loved the story! Press Play to hear it again 💕</span>';
                return;
            }}

            currentPara = index;
            const text = paragraphs[index];
            const storyText = addStorytellingPauses(text);
            const totalParas = paragraphs.length;
            const mood = getMoodParams(index, totalParas);

            // Update UI
            const paraNum = index + 1;
            let label = '📖 Reading...';
            if (index === 0) label = '📖 Once upon a time...';
            else if (index === totalParas - 1) label = '🌟 And the moral is...';
            else if (index === totalParas - 2) label = '🏁 And so, the story ends...';
            else label = '📖 Chapter ' + paraNum + ' of ' + totalParas;

            document.getElementById('now-playing-label').textContent = label;
            document.getElementById('current-text').textContent = text;

            // Update cartoon animation
            updateAnimation(index);

            // Create utterance with storytelling parameters
            const utterance = new SpeechSynthesisUtterance(storyText);
            const baseSpeed = parseFloat(document.getElementById('speed-select').value);
            utterance.rate = baseSpeed * mood.rateMultiplier;
            utterance.pitch = mood.pitch;
            utterance.volume = 1;

            // Use selected voice or auto-detected best voice
            const voiceSelect = document.getElementById('voice-select');
            if (voiceSelect.value !== 'auto') {{
                const voices = synth.getVoices();
                utterance.voice = voices[parseInt(voiceSelect.value)];
            }} else if (bestVoice) {{
                utterance.voice = bestVoice;
            }}

            // Dramatic pause between paragraphs, then continue
            utterance.onend = () => {{
                setTimeout(() => {{
                    speakParagraph(index + 1);
                }}, mood.pauseAfter);
            }};

            synth.speak(utterance);
        }}

        function playStory() {{
            synth.cancel();
            isPlaying = true;
            currentPara = 0;
            // Small delay to ensure voices are loaded
            setTimeout(() => speakParagraph(0), 300);
        }}

        function pauseStory() {{
            synth.pause();
            document.getElementById('now-playing-label').textContent = '⏸️ Paused...';
        }}

        function resumeStory() {{
            synth.resume();
            document.getElementById('now-playing-label').textContent = '📖 Resuming...';
        }}

        function stopStory() {{
            synth.cancel();
            isPlaying = false;
            document.getElementById('now-playing-label').textContent = '🎵 Story time! Press play to begin...';
            document.getElementById('current-text').textContent = 'Press ▶️ Play to hear your magical story read aloud!';
        }}
    </script>

    <style>
        .lottie-stage {{
            width: 100%;
            max-width: 500px;
            margin: 0.5rem auto;
            border-radius: 24px;
            overflow: hidden;
            background: linear-gradient(135deg, #ffe0f0, #e0f0ff, #f0ffe0);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }}
        .slide-caption {{
            text-align: center;
            font-family: 'Bubblegum Sans', cursive;
            font-size: 1.15rem;
            color: #7b1fa2;
            margin-top: 0.5rem;
            padding: 0 1rem;
        }}
        .narration-box {{
            background: linear-gradient(135deg, #ede7f6, #e8eaf6);
            border-radius: 16px;
            padding: 1rem 1.5rem;
            margin: 0.8rem 0;
            text-align: center;
            font-weight: 600;
            color: #4a148c;
            border: 2px solid #ce93d8;
        }}
        .narration-box .now-playing {{
            font-size: 0.85rem;
            color: #9c27b0;
            margin-bottom: 0.3rem;
        }}
        .speed-selector {{
            text-align: center;
            margin: 0.5rem 0;
        }}
        .speed-selector select {{
            padding: 6px 16px;
            border-radius: 20px;
            border: 2px solid #ce93d8;
            font-weight: 600;
            font-size: 0.9rem;
            color: #4a148c;
            background: white;
            cursor: pointer;
        }}
        .audio-controls {{
            display: flex;
            justify-content: center;
            gap: 12px;
            margin: 1.2rem 0;
            flex-wrap: wrap;
        }}
        .audio-btn {{
            background: linear-gradient(135deg, #7b1fa2, #ab47bc);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 24px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(123,31,162,0.3);
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .audio-btn:hover {{
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 6px 20px rgba(123,31,162,0.5);
        }}
        .audio-btn.stop-btn {{
            background: linear-gradient(135deg, #c62828, #ef5350);
            box-shadow: 0 4px 15px rgba(198,40,40,0.3);
        }}
        .audio-btn.pause-btn {{
            background: linear-gradient(135deg, #f57c00, #ffb74d);
            box-shadow: 0 4px 15px rgba(245,124,0,0.3);
        }}
    </style>
    """

    components.html(audio_html, height=780, scrolling=False)

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
