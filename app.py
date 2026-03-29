import io
import json
import math
import random
import re
import sqlite3
import struct
import time
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import quote_plus

import requests
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Wonderloom",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_PATH = "storyspark.db"

APP_NAME = "Wonderloom"
APP_TAGLINE = "Magical stories. Bright young minds."
STORY_SCHEMA_VERSION = "2.0"

AGE_GROUPS = ["3-5", "6-8", "9-12"]
DEFAULT_RECOMMENDATION_OPTIONS = [
    "All Children",
    "Ages 3–5",
    "Ages 5–8",
    "Ages 8–12",
]
RECOMMENDATION_AGE_MAP = {
    "Ages 3–5": {"3-5"},
    "Ages 5–8": {"5-8", "6-8"},
    "Ages 8–12": {"8-12", "9-12"},
}
CATEGORY_OPTIONS = ["Bedtime", "Adventure", "Funny", "Magical"]
STORY_TYPES = CATEGORY_OPTIONS
STORY_MODES = ["Quick Story", "Bedtime Story", "Adventure Mode", "Learn & Grow"]
CHARACTER_OPTIONS = ["Animals", "Superheroes", "Princess", "Robots", "Friendly Monsters", "Kids"]
LOCATION_OPTIONS = ["Jungle", "Space", "Ocean", "School", "Magical Land", "Mountain Village"]
MORAL_OPTIONS = ["Kindness", "Honesty", "Bravery", "Sharing"]
VOICE_STYLES = ["Female Storyteller", "Male Storyteller", "Fun Cartoon Voice"]
DIFFICULTY_OPTIONS = {
    "Easy (3-5)": "3-5",
    "Medium (5-8)": "6-8",
    "Advanced (8-12)": "9-12",
}
QUIZ_FEEDBACK_MESSAGES = ["Great job!", "Almost there!", "Brilliant thinking!", "You are growing wiser with every story!"]

MUSIC_TRACKS = {
    "Off": None,
    "Cozy Kids Lullaby": "__internal_cozy_lullaby__",
    "Adventure Beat": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "Fantasy Ambience": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
}

SFX_TRACKS = {
    "Birds": "https://actions.google.com/sounds/v1/animals/birds_in_forest.ogg",
    "Magic": "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg",
    "Footsteps": "https://actions.google.com/sounds/v1/foley/footsteps_on_gravel.ogg",
}

# Story-specific sound effects
CATEGORY_SOUNDS = {
    "Adventure": "https://actions.google.com/sounds/v1/animals/lion_roar.ogg",
    "Bedtime": "https://actions.google.com/sounds/v1/alarms/gentle_bell.ogg",
    "Funny": "https://actions.google.com/sounds/v1/cartoon/cartoon_laugh.ogg",
    "Magical": "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg",
}

# Mode-specific sound effects
MODE_SOUNDS = {
    "Quick Story": "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg",
    "Bedtime Story": "https://actions.google.com/sounds/v1/alarms/gentle_bell.ogg",
    "Adventure Mode": "https://actions.google.com/sounds/v1/animals/lion_roar.ogg",
    "Learn & Grow": "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg",
}

# Location-specific sound effects
LOCATION_SOUNDS = {
    "Jungle": "https://actions.google.com/sounds/v1/animals/birds_in_forest.ogg",
    "Space": "https://actions.google.com/sounds/v1/scifi/laser_beam.ogg",
    "Ocean": "https://actions.google.com/sounds/v1/animals/sea_waves.ogg",
    "School": "https://actions.google.com/sounds/v1/alarms/school_bell.ogg",
    "Magical Land": "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg",
    "Mountain Village": "https://actions.google.com/sounds/v1/alarms/gentle_bell.ogg",
}

# Moral-specific sound effects  
MORAL_SOUNDS = {
    "Kindness": "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg",
    "Honesty": "https://actions.google.com/sounds/v1/alarms/gentle_bell.ogg",
    "Bravery": "https://actions.google.com/sounds/v1/animals/lion_roar.ogg",
    "Sharing": "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg",
}

# Page turning sound
PAGE_TURN_SOUND = "https://actions.google.com/sounds/v1/paper/page_flip.ogg"

MORAL_LINES = {
    "Kindness": "Kindness turns small moments into big magic.",
    "Honesty": "Honesty builds trust and bright futures.",
    "Bravery": "Bravery means trying, even when your knees shake.",
    "Sharing": "Sharing joy makes everyone shine brighter.",
}

DEFAULT_FEATURED = [
    {"title": "The Moonlight Kite", "tag": "Bedtime", "blurb": "A gentle story to drift into sweet sleep."},
    {"title": "Captain Mango in Space", "tag": "Adventure", "blurb": "A brave mission with laughter and stars."},
    {"title": "The Library Dragon", "tag": "Educational", "blurb": "Learning words with a curious dragon friend."},
]

REAL_ESTATE_PROPERTIES = [
    {
        "id": 1,
        "name": "Skyline Crown Residences",
        "community": "Downtown Dubai",
        "price_aed": 3250000,
        "bedrooms": 3,
        "bathrooms": 4,
        "area_sqft": 2180,
        "roi": 8.9,
        "status": "Ready",
        "type": "Apartment",
        "image": "https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=1400&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80",
        ],
        "map": "https://maps.google.com/?q=Downtown+Dubai",
    },
    {
        "id": 2,
        "name": "Palm Horizon Villas",
        "community": "Palm Jumeirah",
        "price_aed": 12800000,
        "bedrooms": 5,
        "bathrooms": 6,
        "area_sqft": 6840,
        "roi": 7.1,
        "status": "Ready",
        "type": "Villa",
        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1400&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1613977257362-707ba9348227?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?auto=format&fit=crop&w=1200&q=80",
        ],
        "map": "https://maps.google.com/?q=Palm+Jumeirah+Dubai",
    },
    {
        "id": 3,
        "name": "Canal Edge Signature",
        "community": "Business Bay",
        "price_aed": 2490000,
        "bedrooms": 2,
        "bathrooms": 3,
        "area_sqft": 1710,
        "roi": 9.3,
        "status": "Off-plan",
        "type": "Apartment",
        "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1400&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?auto=format&fit=crop&w=1200&q=80",
        ],
        "map": "https://maps.google.com/?q=Business+Bay+Dubai",
    },
    {
        "id": 4,
        "name": "Marina Crest Collection",
        "community": "Dubai Marina",
        "price_aed": 3810000,
        "bedrooms": 3,
        "bathrooms": 4,
        "area_sqft": 2440,
        "roi": 8.4,
        "status": "Ready",
        "type": "Apartment",
        "image": "https://images.unsplash.com/photo-1600607687644-c7f34b5063ec?auto=format&fit=crop&w=1400&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=1200&q=80",
        ],
        "map": "https://maps.google.com/?q=Dubai+Marina",
    },
    {
        "id": 5,
        "name": "Desert Pearl Mansions",
        "community": "Tilal Al Ghaf",
        "price_aed": 15200000,
        "bedrooms": 6,
        "bathrooms": 7,
        "area_sqft": 7600,
        "roi": 6.8,
        "status": "Off-plan",
        "type": "Mansion",
        "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1400&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1576941089067-2de3c901e126?auto=format&fit=crop&w=1200&q=80",
        ],
        "map": "https://maps.google.com/?q=Tilal+Al+Ghaf",
    },
    {
        "id": 6,
        "name": "Lagoon Aura Townhomes",
        "community": "Dubai Creek Harbour",
        "price_aed": 2780000,
        "bedrooms": 3,
        "bathrooms": 4,
        "area_sqft": 1970,
        "roi": 8.7,
        "status": "Off-plan",
        "type": "Townhouse",
        "image": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?auto=format&fit=crop&w=1400&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1613553429707-70117cd7f3f1?auto=format&fit=crop&w=1200&q=80",
        ],
        "map": "https://maps.google.com/?q=Dubai+Creek+Harbour",
    },
]


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT NOT NULL,
            age_group TEXT NOT NULL,
            avatar TEXT DEFAULT '⭐',
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER,
            title TEXT NOT NULL,
            story_type TEXT NOT NULL,
            mode TEXT NOT NULL,
            moral TEXT NOT NULL,
            location TEXT NOT NULL,
            characters TEXT NOT NULL,
            content_json TEXT NOT NULL,
            content_text TEXT NOT NULL,
            favorite INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            last_read_at TEXT,
            read_count INTEGER DEFAULT 0,
            FOREIGN KEY(profile_id) REFERENCES profiles(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def set_setting(key: str, value: str) -> None:
    conn = db()
    conn.execute(
        "INSERT INTO settings(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()
    conn.close()


def get_setting(key: str, default: str = "") -> str:
    conn = db()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def difficulty_label_from_age(age_group: str) -> str:
    for label, mapped_age in DIFFICULTY_OPTIONS.items():
        if mapped_age == age_group:
            return label
    return "Medium (5-8)"


def reset_quiz_state() -> None:
    st.session_state.quiz_active = False
    st.session_state.quiz_story_id = None
    st.session_state.quiz_score = None
    st.session_state.quiz_total = None


def get_story_of_the_day() -> Dict[str, str]:
    rows = list_stories("all")
    if rows:
        day_index = int(datetime.now().strftime("%j")) % len(rows)
        story = rows[day_index]
        return {
            "title": story["title"],
            "tag": story["story_type"],
            "blurb": f"A {story['story_type'].lower()} pick for today from {APP_NAME}.",
        }
    random.seed(datetime.now().strftime("%Y-%m-%d"))
    return random.choice(DEFAULT_FEATURED)


def get_next_story_recommendation(current_story_id: int, story_type: str) -> Optional[sqlite3.Row]:
    conn = db()
    row = conn.execute(
        "SELECT * FROM stories WHERE id != ? AND story_type = ? ORDER BY favorite DESC, read_count ASC, created_at DESC LIMIT 1",
        (current_story_id, story_type),
    ).fetchone()
    if row is None:
        row = conn.execute(
            "SELECT * FROM stories WHERE id != ? ORDER BY favorite DESC, read_count ASC, created_at DESC LIMIT 1",
            (current_story_id,),
        ).fetchone()
    conn.close()
    return row


def choose_feedback_message(score: int, total: int, messages: Optional[List[str]] = None) -> str:
    pool = messages or QUIZ_FEEDBACK_MESSAGES
    if total <= 0:
        return pool[0]
    ratio = score / total
    if ratio >= 0.85:
        return pool[min(2, len(pool) - 1)]
    if ratio >= 0.55:
        return pool[0]
    return pool[min(1, len(pool) - 1)]


def normalize_story_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        payload = {}

    title = str(payload.get("title", "Untitled Story")).strip() or "Untitled Story"
    subtitle = str(payload.get("subtitle", "A gentle story for little readers.")).strip()
    age_group = str(payload.get("age_group", "6-8")).strip() or "6-8"
    category = str(payload.get("category", payload.get("story_type", "Magical"))).strip() or "Magical"
    moral = str(payload.get("moral", MORAL_LINES["Kindness"]))
    story_text = str(payload.get("story", "")).strip()

    scenes_in = payload.get("scenes") if isinstance(payload.get("scenes"), list) else []
    scenes: List[Dict[str, str]] = []
    for idx, raw_scene in enumerate(scenes_in):
        if not isinstance(raw_scene, dict):
            continue
        scene_text = str(raw_scene.get("text", "")).strip()
        scenes.append(
            {
                "heading": str(raw_scene.get("heading", f"Scene {idx + 1}")).strip() or f"Scene {idx + 1}",
                "text": scene_text,
                "dialogue": str(raw_scene.get("dialogue", "Let's keep going together.")).strip(),
                "choice_a": str(raw_scene.get("choice_a", "Follow the silver trail")).strip(),
                "choice_b": str(raw_scene.get("choice_b", "Listen beside the old tree")).strip(),
                "reaction": str(raw_scene.get("reaction", "curious")).strip(),
                "image_prompt": str(raw_scene.get("image_prompt", scene_text[:140] or "Magical children's storybook scene")).strip(),
                "image_url": str(raw_scene.get("image_url", "")).strip(),
            }
        )

    if not story_text and scenes:
        story_text = "\n\n".join(scene.get("text", "") for scene in scenes if scene.get("text"))
    if not scenes and story_text:
        scenes = paragraphs_to_scenes(story_text)
        for scene in scenes:
            scene.setdefault("image_prompt", scene.get("text", "Magical children's storybook scene")[:140])
            scene.setdefault("image_url", "")

    full_text = str(payload.get("full_text", "")).strip()
    if not full_text:
        if story_text:
            full_text = f"{story_text}\n\nMoral: {moral}"
        else:
            full_text = "\n\n".join([f"{s['heading']}\n{s['text']}\n{s['dialogue']}" for s in scenes]) + f"\n\nMoral: {moral}"

    feedback_messages = payload.get("feedback_messages", QUIZ_FEEDBACK_MESSAGES)
    if not isinstance(feedback_messages, list) or not feedback_messages:
        feedback_messages = QUIZ_FEEDBACK_MESSAGES
    feedback_messages = [str(m).strip() for m in feedback_messages if str(m).strip()]

    normalized: Dict[str, Any] = {
        "schema_version": STORY_SCHEMA_VERSION,
        "app_name": str(payload.get("app_name", APP_NAME)).strip() or APP_NAME,
        "tagline": str(payload.get("tagline", APP_TAGLINE)).strip() or APP_TAGLINE,
        "title": title,
        "subtitle": subtitle,
        "story": story_text,
        "age_group": age_group,
        "category": category,
        "moral": moral,
        "scenes": scenes,
        "questions": payload.get("questions", {"memory": [], "understanding": [], "thinking": []}),
        "feedback_messages": feedback_messages,
        "full_text": full_text,
    }
    normalized["questions"] = ensure_story_questions(normalized)
    return normalized


def upgrade_story_json_schema() -> Dict[str, int]:
    conn = db()
    rows = conn.execute("SELECT id, content_json FROM stories").fetchall()
    scanned = 0
    upgraded = 0
    for row in rows:
        scanned += 1
        try:
            raw = json.loads(row["content_json"])
            normalized = normalize_story_payload(raw)
            if raw != normalized:
                conn.execute(
                    "UPDATE stories SET content_json=?, content_text=? WHERE id=?",
                    (json.dumps(normalized), normalized.get("full_text", ""), row["id"]),
                )
                upgraded += 1
        except Exception:
            continue
    conn.commit()
    conn.close()
    return {"scanned": scanned, "upgraded": upgraded}


@st.cache_data(show_spinner=False)
def build_cozy_lullaby_wav() -> bytes:
    sample_rate = 22050
    notes = [261.63, 329.63, 392.00, 329.63, 293.66, 349.23, 392.00, 349.23]
    note_seconds = 0.45
    total_samples = int(len(notes) * note_seconds * sample_rate)
    frames = bytearray()

    for n in range(total_samples):
        t = n / sample_rate
        note_index = int(t / note_seconds) % len(notes)
        local_t = t - int(t / note_seconds) * note_seconds
        freq = notes[note_index]
        # Soft envelope to avoid harsh edges/clicks.
        attack = min(local_t / 0.08, 1.0)
        release = min((note_seconds - local_t) / 0.12, 1.0)
        env = max(0.0, min(attack, release))
        tone = math.sin(2.0 * math.pi * freq * local_t)
        harmony = 0.4 * math.sin(2.0 * math.pi * (freq / 2.0) * local_t)
        sample = int(12000 * env * (0.72 * tone + 0.28 * harmony))
        frames.extend(struct.pack("<h", max(-32767, min(32767, sample))))

    wav = io.BytesIO()
    # Minimal PCM WAV header + data (mono, 16-bit).
    data_size = len(frames)
    byte_rate = sample_rate * 2
    wav.write(b"RIFF")
    wav.write(struct.pack("<I", 36 + data_size))
    wav.write(b"WAVEfmt ")
    wav.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, byte_rate, 2, 16))
    wav.write(b"data")
    wav.write(struct.pack("<I", data_size))
    wav.write(frames)
    return wav.getvalue()


def render_music_track(track_key: str) -> None:
    source = MUSIC_TRACKS.get(track_key)
    if not source:
        return
    if source == "__internal_cozy_lullaby__":
        st.audio(build_cozy_lullaby_wav(), format="audio/wav")
        return
    if isinstance(source, str):
        st.audio(source, format="audio/mp3")


def create_profile(child_name: str, age_group: str, avatar: str) -> int:
    now = datetime.now().isoformat(timespec="seconds")
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO profiles(child_name, age_group, avatar, created_at) VALUES(?,?,?,?)",
        (child_name, age_group, avatar, now),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def get_profiles() -> List[sqlite3.Row]:
    conn = db()
    rows = conn.execute("SELECT * FROM profiles ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows


def save_story(profile_id: Optional[int], payload: Dict[str, Any], story_type: str, mode: str, moral: str, location: str, characters: List[str]) -> int:
    payload = normalize_story_payload(payload)
    now = datetime.now().isoformat(timespec="seconds")
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO stories(profile_id, title, story_type, mode, moral, location, characters, content_json, content_text, created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """,
        (
            profile_id,
            payload["title"],
            story_type,
            mode,
            moral,
            location,
            json.dumps(characters),
            json.dumps(payload),
            payload["full_text"],
            now,
        ),
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def story_title_exists(title: str) -> bool:
    conn = db()
    row = conn.execute("SELECT 1 FROM stories WHERE title=? LIMIT 1", (title,)).fetchone()
    conn.close()
    return row is not None


def infer_story_type(text: str) -> str:
    lowered = text.lower()
    checks = [
        ("Bedtime", ["moon", "sleep", "bed", "night", "lullaby"]),
        ("Adventure", ["journey", "map", "hill", "bridge", "adventure"]),
        ("Funny", ["laugh", "giggle", "funny", "silly"]),
        ("Educational", ["learn", "fact", "library", "school"]),
        ("Fantasy", ["magic", "dragon", "sparkle", "wand", "star"]),
        ("Moral", ["kindness", "honesty", "sharing", "bravery", "lesson"]),
    ]
    for story_type, keywords in checks:
        if any(keyword in lowered for keyword in keywords):
            return story_type
    return "Fantasy"


def infer_mode(story_type: str, age_group: str) -> str:
    if story_type == "Bedtime":
        return "Bedtime Story"
    if story_type == "Adventure":
        return "Adventure Mode"
    if story_type == "Educational":
        return "Learn & Grow"
    if age_group == "3-5":
        return "Quick Story"
    return "Quick Story"


def infer_moral_key(moral_text: str) -> str:
    lowered = moral_text.lower()
    for moral in MORAL_OPTIONS:
        if moral.lower() in lowered:
            return moral
    return "Kindness"


def paragraphs_to_scenes(story_text: str) -> List[Dict[str, str]]:
    # Split on blank lines, drop the "Moral:" trailer paragraph for scene building
    raw = [part.strip() for part in story_text.split("\n\n") if part.strip()]
    paragraphs = [p for p in raw if not p.lower().startswith("moral:")]

    # Group every 2 paragraphs into one scene so each scene has substantial content
    grouped: List[str] = []
    for i in range(0, len(paragraphs), 2):
        chunk = paragraphs[i : i + 2]
        grouped.append("  ".join(chunk))

    choice_pairs = [
        ("Follow the glowing path", "Knock on the tiny wooden door"),
        ("Ask the robin for help", "Look under the silver leaves"),
        ("Share the last cookie", "Save it for later"),
        ("Cross the soft bridge", "Wait and watch the river"),
        ("Climb the mossy hill", "Follow the firefly trail"),
        ("Call out to a stranger", "Stay hidden in the reeds"),
    ]
    dialogues = [
        '"We can do this together!" the little hero whispered bravely.',
        '"Something magical is waiting for us," said the companion with wide eyes.',
        '"Every problem has a kind answer," the hero reminded themself softly.',
        '"Let\'s find out what happens next," said the hero with a curious smile.',
        '"I think I know the way," the companion said, pointing ahead.',
        '"We just need to be patient," the hero said, taking a deep breath.',
    ]
    reactions = ["happy", "curious", "excited", "surprised", "determined", "hopeful"]
    scenes: List[Dict[str, str]] = []
    for idx, text in enumerate(grouped):
        c1, c2 = choice_pairs[idx % len(choice_pairs)]
        scenes.append(
            {
                "heading": f"Scene {idx + 1}",
                "text": text,
                "dialogue": dialogues[idx % len(dialogues)],
                "choice_a": c1,
                "choice_b": c2,
                "reaction": reactions[idx % len(reactions)],
            }
        )
    return scenes


def external_story_to_payload(item: Dict[str, Any]) -> Dict[str, Any]:
    title = str(item.get("title", "Untitled Story")).strip() or "Untitled Story"
    subtitle = str(item.get("subtitle", "A gentle story for little readers.")).strip()
    story_text = str(item.get("story", "")).strip()
    moral_text = str(item.get("moral", "Kindness makes every place feel warmer.")).strip()
    inferred_category = str(item.get("category") or item.get("story_type") or infer_story_type(f"{title} {subtitle} {story_text} {moral_text}"))
    scenes = item.get("scenes") if isinstance(item.get("scenes"), list) and item.get("scenes") else paragraphs_to_scenes(story_text)
    payload = {
        "app_name": str(item.get("app_name", APP_NAME)),
        "tagline": str(item.get("tagline", APP_TAGLINE)),
        "schema_version": str(item.get("schema_version", STORY_SCHEMA_VERSION)),
        "title": title,
        "subtitle": subtitle,
        "story": story_text,
        "age_group": str(item.get("age_group", "6-8")),
        "category": inferred_category,
        "scenes": scenes,
        "moral": moral_text,
        "questions": item.get("questions", {"memory": [], "understanding": [], "thinking": []}),
        "feedback_messages": item.get("feedback_messages", QUIZ_FEEDBACK_MESSAGES),
        "full_text": story_text + ("\n\nMoral: " + moral_text if moral_text else ""),
    }
    return normalize_story_payload(payload)


def unique_story_title(base_title: str) -> str:
    clean = base_title.strip() or "Untitled Story"
    if not story_title_exists(clean):
        return clean
    suffix = 2
    while story_title_exists(f"{clean} ({suffix})"):
        suffix += 1
    return f"{clean} ({suffix})"


def import_story_json_file(file_path: str, allow_duplicate_titles: bool = False) -> Dict[str, int]:
    path = Path(file_path)
    if not path.exists():
        return {"imported": 0, "skipped": 0, "forced": 0}

    data = json.loads(path.read_text(encoding="utf-8"))
    stories = data.get("stories", data) if isinstance(data, dict) else data
    imported = 0
    skipped = 0
    forced = 0

    for item in stories:
        if not isinstance(item, dict):
            skipped += 1
            continue
        title = str(item.get("title", "")).strip()
        if not title:
            skipped += 1
            continue
        if story_title_exists(title):
            if allow_duplicate_titles:
                item = dict(item)
                item["title"] = unique_story_title(title)
                forced += 1
            else:
                skipped += 1
                continue

        payload = external_story_to_payload(item)
        story_text_blob = f"{item.get('title', '')} {item.get('subtitle', '')} {item.get('story', '')} {item.get('moral', '')}"
        story_type = infer_story_type(story_text_blob)
        age_group = str(item.get("age_group", "6-8"))
        mode = infer_mode(story_type, age_group)
        moral_key = infer_moral_key(str(item.get("moral", "")))
        save_story(
            profile_id=None,
            payload=payload,
            story_type=story_type,
            mode=mode,
            moral=moral_key,
            location="Library Collection",
            characters=["Kids", "Animals"],
        )
        imported += 1

    return {"imported": imported, "skipped": skipped, "forced": forced}


def mark_read(story_id: int) -> None:
    conn = db()
    conn.execute(
        "UPDATE stories SET read_count = read_count + 1, last_read_at=? WHERE id=?",
        (datetime.now().isoformat(timespec="seconds"), story_id),
    )
    conn.commit()
    conn.close()


def toggle_favorite(story_id: int) -> None:
    conn = db()
    conn.execute("UPDATE stories SET favorite = CASE favorite WHEN 1 THEN 0 ELSE 1 END WHERE id=?", (story_id,))
    conn.commit()
    conn.close()


def get_story(story_id: int) -> Optional[sqlite3.Row]:
    conn = db()
    row = conn.execute("SELECT * FROM stories WHERE id=?", (story_id,)).fetchone()
    conn.close()
    return row


def list_stories(filter_mode: str = "all") -> List[sqlite3.Row]:
    conn = db()
    if filter_mode == "favorites":
        rows = conn.execute("SELECT * FROM stories WHERE favorite=1 ORDER BY created_at DESC").fetchall()
    elif filter_mode == "recent":
        rows = conn.execute("SELECT * FROM stories ORDER BY COALESCE(last_read_at, created_at) DESC LIMIT 25").fetchall()
    else:
        rows = conn.execute("SELECT * FROM stories ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows


def story_payload_from_row(row: sqlite3.Row) -> Dict[str, Any]:
    try:
        payload = json.loads(row["content_json"])
        return normalize_story_payload(payload)
    except Exception:
        return {}


def story_category_from_row(row: sqlite3.Row) -> str:
    payload = story_payload_from_row(row)
    category = str(payload.get("category", row["story_type"])).strip() if payload else str(row["story_type"])
    return category if category in STORY_TYPES else row["story_type"]


def get_category_recommendations(profile_id: Optional[int], category: str, limit: int = 4) -> List[sqlite3.Row]:
    rows = list_stories("all")
    category_rows: List[sqlite3.Row] = [r for r in rows if story_category_from_row(r) == category]
    if not category_rows:
        category_rows = rows

    # Prefer profile-authored stories first when available, then favorites, then least-read fresh content.
    if profile_id is not None:
        profile_rows = [r for r in category_rows if r["profile_id"] == profile_id]
        other_rows = [r for r in category_rows if r["profile_id"] != profile_id]
        category_rows = profile_rows + other_rows

    ranked = sorted(category_rows, key=lambda r: (-int(r["favorite"]), int(r["read_count"]), str(r["created_at"])), reverse=False)
    return ranked[:limit]


def get_last_story() -> Optional[sqlite3.Row]:
    conn = db()
    row = conn.execute("SELECT * FROM stories ORDER BY created_at DESC LIMIT 1").fetchone()
    conn.close()
    return row


def get_recommendations(profile_id: Optional[int]) -> List[str]:
    if profile_id is None:
        return ["Magical", "Adventure", "Bedtime"]

    conn = db()
    rows = conn.execute(
        "SELECT story_type, COUNT(*) AS c FROM stories WHERE profile_id=? GROUP BY story_type ORDER BY c DESC",
        (profile_id,),
    ).fetchall()
    conn.close()
    if not rows:
        return ["Bedtime", "Magical", "Funny"]
    ranked = [r["story_type"] for r in rows]
    fallback = [s for s in STORY_TYPES if s not in ranked]
    return (ranked + fallback)[:3]


def _normalize_age_band(age_group: str) -> str:
    return str(age_group).replace("–", "-").strip()


def get_recommendation_options(profiles: List[sqlite3.Row]) -> Tuple[List[str], Dict[str, sqlite3.Row]]:
    options = list(DEFAULT_RECOMMENDATION_OPTIONS)
    profile_option_map: Dict[str, sqlite3.Row] = {}
    for profile in profiles:
        label = f"{profile['avatar']} {profile['child_name']} ({profile['age_group']})"
        options.append(label)
        profile_option_map[label] = profile

    # Keep ordering stable and prevent duplicate labels.
    unique_options = list(dict.fromkeys(options))
    if not unique_options:
        unique_options = list(DEFAULT_RECOMMENDATION_OPTIONS)
    return unique_options, profile_option_map


def filter_stories_by_age(rows: List[sqlite3.Row], profiles: List[sqlite3.Row], selected_option: str) -> List[sqlite3.Row]:
    valid_ages = RECOMMENDATION_AGE_MAP.get(selected_option)
    if not valid_ages:
        return rows

    profile_ids = {
        int(profile["id"])
        for profile in profiles
        if _normalize_age_band(profile["age_group"]) in valid_ages
    }
    if not profile_ids:
        return rows

    filtered_rows = [row for row in rows if row["profile_id"] in profile_ids]
    return filtered_rows or rows


def get_recommendation_seed_categories(
    selected_option: str,
    profiles: List[sqlite3.Row],
    profile_option_map: Dict[str, sqlite3.Row],
) -> List[str]:
    if selected_option in profile_option_map:
        return get_recommendations(int(profile_option_map[selected_option]["id"]))

    rows = list_stories("all")
    if selected_option in RECOMMENDATION_AGE_MAP:
        rows = filter_stories_by_age(rows, profiles, selected_option)

    if not rows:
        return ["Magical", "Adventure", "Bedtime"]

    category_counts: Dict[str, int] = {}
    for row in rows:
        category = story_category_from_row(row)
        category_counts[category] = category_counts.get(category, 0) + 1

    ranked = sorted(category_counts.keys(), key=lambda cat: category_counts[cat], reverse=True)
    fallback = [category for category in STORY_TYPES if category not in ranked]
    return (ranked + fallback)[:3]


def get_home_recommendation_rows(
    selected_option: str,
    profiles: List[sqlite3.Row],
    profile_option_map: Dict[str, sqlite3.Row],
    active_category: str,
    limit: int = 4,
) -> List[sqlite3.Row]:
    all_rows = list_stories("all")
    category_rows = [row for row in all_rows if story_category_from_row(row) == active_category]
    scoped_rows = category_rows or all_rows

    if selected_option in profile_option_map:
        profile_id = int(profile_option_map[selected_option]["id"])
        selected_rows = [row for row in scoped_rows if row["profile_id"] == profile_id]
        other_rows = [row for row in scoped_rows if row["profile_id"] != profile_id]
        scoped_rows = selected_rows + other_rows
    elif selected_option in RECOMMENDATION_AGE_MAP:
        scoped_rows = filter_stories_by_age(scoped_rows, profiles, selected_option)

    ranked_rows = sorted(
        scoped_rows,
        key=lambda row: (-int(row["favorite"]), int(row["read_count"]), str(row["created_at"])),
    )
    return ranked_rows[:limit]


def render_recommendation_filter(profiles: List[sqlite3.Row]) -> Tuple[str, Dict[str, sqlite3.Row]]:
    options, profile_option_map = get_recommendation_options(profiles)
    current_value = str(st.session_state.get("home_recommendation_filter", DEFAULT_RECOMMENDATION_OPTIONS[0]))
    if current_value not in options:
        current_value = options[0]

    selected_option = st.selectbox(
        "Recommendations for",
        options=options,
        index=options.index(current_value),
        key="home_recommendation_filter_select",
        help="Choose all children, an age band, or a specific profile.",
    )

    st.session_state.home_recommendation_filter = selected_option
    st.session_state.home_selected_profile_label = selected_option if selected_option in profile_option_map else "All Children"
    return selected_option, profile_option_map


def get_auto_difficulty(age_group: str, profile_id: Optional[int]) -> str:
    base = {"3-5": "gentle", "6-8": "balanced", "9-12": "rich"}[age_group]
    if profile_id is None:
        return base
    conn = db()
    row = conn.execute("SELECT AVG(read_count) avg_reads FROM stories WHERE profile_id=?", (profile_id,)).fetchone()
    conn.close()
    avg_reads = row["avg_reads"] if row and row["avg_reads"] is not None else 0
    if avg_reads > 2 and base != "rich":
        return "balanced" if base == "gentle" else "rich"
    return base


def play_sound(sound_url: str, sound_name: str = "sound") -> None:
    """Play a sound effect using HTML5 audio."""
    if not sound_url or sound_url.strip() == "":
        return
    
    audio_html = f"""
    <audio autoplay>
        <source src="{sound_url}" type="audio/ogg">
        <source src="{sound_url}" type="audio/mpeg">
    </audio>
    """
    components.html(audio_html, height=0)


def safe_json_extract(text: str) -> Optional[Dict[str, Any]]:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def build_story_questions(context: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    name = context["name"]
    place = context["place"]
    companion = context["companion"]
    special_object = context["special_object"]
    problem = context["problem"]
    feeling = context["feeling"]
    moral = context["moral"]

    memory = [
        {
            "question": f"What did {name} discover at the beginning of the story?",
            "options": [special_object, "a silver whistle", "a ribbon kite", "a pebble crown"],
            "answer": special_object,
        },
        {
            "question": "Where did the adventure begin?",
            "options": [place, "Rainbow Hollow", "Willow Bay", "Cloudbell Hill"],
            "answer": place,
        },
        {
            "question": f"Who helped {name} during the journey?",
            "options": [companion, "a moon gardener", "a paper dragon", "a tiny drummer"],
            "answer": companion,
        },
        {
            "question": "What was the main problem to solve?",
            "options": [problem, "A kite got caught in a bell tower", "A parade forgot its drums", "A teapot floated into the trees"],
            "answer": problem,
        },
    ]
    understanding = [
        {
            "question": f"Why did {name} feel nervous at first?",
            "answer": f"{name} felt {feeling} because the problem seemed big and important, and there was no instant answer.",
        },
        {
            "question": f"How did {companion} help the adventure move forward?",
            "answer": f"{companion} offered calm guidance, encouragement, and a way to keep noticing small clues instead of giving up.",
        },
        {
            "question": "What finally helped the problem begin to change?",
            "answer": f"Careful observation, patience, teamwork, and {moral.lower()} together helped the problem soften.",
        },
        {
            "question": "How did the setting change by the end of the story?",
            "answer": "The setting felt brighter, safer, and more alive, showing that inner courage can transform the world around us.",
        },
    ]
    thinking = [
        {"question": f"If you had found the {special_object}, what would you have done first?"},
        {"question": f"What other magical helper could have joined {name} and {companion}?"},
        {"question": f"How would you show {moral.lower()} in your own day?"},
    ]
    return {"memory": memory, "understanding": understanding, "thinking": thinking}


def ensure_story_questions(story: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    existing = story.get("questions", {}) if isinstance(story.get("questions"), dict) else {}
    has_memory = isinstance(existing.get("memory"), list) and len(existing.get("memory", [])) >= 3
    has_understanding = isinstance(existing.get("understanding"), list) and len(existing.get("understanding", [])) >= 3
    has_thinking = isinstance(existing.get("thinking"), list) and len(existing.get("thinking", [])) >= 2
    if has_memory and has_understanding and has_thinking:
        return existing

    scenes = story.get("scenes", []) if isinstance(story.get("scenes"), list) else []
    title = str(story.get("title", "This Story")).strip() or "This Story"
    moral = str(story.get("moral", "Kindness makes every place brighter.")).strip() or "Kindness makes every place brighter."
    scene_count = max(1, len(scenes))
    first_heading = scenes[0].get("heading", "Scene 1") if scenes else "Scene 1"
    first_choice = scenes[0].get("choice_a", "Take the brave step") if scenes else "Take the brave step"
    second_choice = scenes[0].get("choice_b", "Listen and observe") if scenes else "Listen and observe"

    memory = [
        {
            "question": "What is the title of the story you just read?",
            "options": [title, "The Hidden Rainbow", "The Whispering Bridge", "The Lantern Trail"],
            "answer": title,
        },
        {
            "question": "How many scenes did this story have?",
            "options": [str(scene_count), str(scene_count + 1), str(max(1, scene_count - 1)), "8"],
            "answer": str(scene_count),
        },
        {
            "question": "Which heading appeared first in the story?",
            "options": [first_heading, "Final Scene", "Chapter Opening", "Moonlight Turn"],
            "answer": first_heading,
        },
        {
            "question": "What lesson did the story emphasize most?",
            "options": [moral, "Winning quickly is always best.", "Problems should be ignored.", "Only magic can solve things."],
            "answer": moral,
        },
    ]

    understanding = [
        {
            "question": "How did the character make progress when the problem felt difficult?",
            "answer": "The character moved forward by staying calm, making thoughtful choices, and taking one small step at a time.",
        },
        {
            "question": "Why was the main choice important to the story outcome?",
            "answer": f"The choice shaped the path and emotions of the journey, such as choosing '{first_choice}' or '{second_choice}'.",
        },
        {
            "question": "What emotional change happened from beginning to end?",
            "answer": "The character shifted from uncertainty to confidence, and the world around them became brighter and safer.",
        },
    ]

    thinking = [
        {"question": "If you were inside this story, what would your first smart choice be and why?"},
        {"question": "How would you change one scene to make the ending even more magical?"},
    ]

    fallback = {"memory": memory, "understanding": understanding, "thinking": thinking}
    story["questions"] = fallback
    return fallback


def ai_generate_story(api_provider: str, api_key: str, model: str, prompt_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not api_key:
        return None

    base_url = "https://api.openai.com/v1/chat/completions" if api_provider == "OpenAI" else "https://api.mistral.ai/v1/chat/completions"
    system_prompt = (
        f"You create premium educational children's stories for {APP_NAME}. "
        "Return ONLY valid JSON with required keys: app_name, tagline, title, subtitle, story, age_group, moral, scenes, questions, feedback_messages. "
        "Story must be 400-700 words, immersive, magical, child-friendly, with a beginning, middle, end, and 1-2 dialogues. "
        "Scenes must be 5-8 items and each scene needs: heading, text, dialogue, choice_a, choice_b, reaction, image_prompt. "
        "Questions must include memory (3-5 MCQs with options and answer), understanding (3-5 with answer), thinking (2-3 open-ended)."
    )
    user_prompt = json.dumps(prompt_payload)

    try:
        res = requests.post(
            base_url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "temperature": 0.9,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=25,
        )
        res.raise_for_status()
        body = res.json()
        content = body["choices"][0]["message"]["content"]
        data = safe_json_extract(content)
        if not data:
            return None
        if data.get("story") and data.get("scenes") and data.get("questions"):
            data.setdefault("app_name", APP_NAME)
            data.setdefault("tagline", APP_TAGLINE)
            data.setdefault("feedback_messages", QUIZ_FEEDBACK_MESSAGES)
            data.setdefault("full_text", f"{data.get('story', '').strip()}\n\nMoral: {data.get('moral', '')}".strip())
            return data
        return None
    except Exception:
        return None


def local_generate_story(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data["child_name"]
    age = data["age_group"]
    story_type = data["story_type"]
    chars = data["characters"]
    location = data["location"]
    moral = data["moral"]
    difficulty = data["difficulty"]
    voice_guidance = data.get("voice_guidance", "").strip()

    rng = random.Random(f"{name}|{age}|{story_type}|{location}|{moral}|{'-'.join(chars)}")
    character_guides = {
        "Animals": "a lantern-eyed fox",
        "Superheroes": "a cape-swishing sky scout",
        "Princess": "a velvet-shoed princess",
        "Robots": "a brass-hearted helper bot",
        "Friendly Monsters": "a fuzzy blueberry monster",
        "Kids": "a bright-eyed neighborhood friend",
    }
    place_details = {
        "Jungle": "between fern ladders and whispering parrots",
        "Space": "beneath a sky where planets looked near enough to cup in both hands",
        "Ocean": "where silver foam kept time with the tide",
        "School": "beside painted walls and a sunflower patch near the gate",
        "Magical Land": "under trees that wore bells of light instead of fruit",
        "Mountain Village": "where cedar smoke curled gently above the roofs",
    }
    object_options = {
        "Bedtime": ["moon-lantern", "sleepy star clock", "pocket lullaby bell"],
        "Adventure": ["wind-map", "compass feather", "golden trail key"],
        "Funny": ["giggle compass", "hiccup teacup", "tickle umbrella"],
        "Magical": ["dew-glass lantern", "singing acorn globe", "starlight ribbon jar"],
    }
    problem_options = {
        "Bedtime": ["the night garden had forgotten how to yawn", "the clouds were too restless to let the moon settle"],
        "Adventure": ["a hidden bridge had gone silent and would not reveal the crossing", "a trail of clues ended beside a locked stone arch"],
        "Funny": ["the village fountain had begun to sneeze bubbles over every hat", "the morning birds had mixed up all the songs and could not stop laughing"],
        "Magical": ["the oldest tree had misplaced its glow and the valley felt dim", "a ribbon of light had tangled itself around the meadow wind"],
    }
    companion = character_guides.get(chars[0] if chars else "Kids", "a bright-eyed neighborhood friend")
    special_object = rng.choice(object_options.get(story_type, object_options["Magical"]))
    problem = rng.choice(problem_options.get(story_type, problem_options["Magical"]))
    feeling = rng.choice(["small", "uncertain", "trembly", "quietly brave"])
    place_detail = place_details.get(location, "in a corner of the world that felt newly enchanted")
    moral_line = MORAL_LINES.get(moral, MORAL_LINES["Kindness"])

    title = f"{name} and the {special_object.title()}"
    subtitle = f"{story_type} • {difficulty.title()} reading journey • Ages {age}"
    paragraphs = [
        (
            f"On a pale gold morning in the {location.lower()}, {place_detail}, {name} noticed a {special_object} resting on a stone as if it had been waiting all night. "
            f"It was cool in the hand and faintly bright, and when {name} lifted it, the leaves, roofs, or waves nearby seemed to lean closer. "
            f"Even the air felt expectant, as though the day had already opened a secret door."
        ),
        (
            f"From behind a bend came {companion}, who looked at the shimmer and said, \"That belongs to the place where {problem}.\" "
            f"{name} swallowed a nervous breath. Being the one who stepped forward sounded important and a little frightening, yet the path ahead seemed to ask kindly rather than loudly."
        ),
        (
            f"So they walked on together, passing small marvels that made the world feel both playful and wise: moss that glowed at the edges, puddles that held pieces of sky, and birds that hopped as if keeping time to an invisible drum. "
            f"Whenever worry brushed close, {name} remembered to look carefully, listen gently, and leave enough quiet for an answer to arrive."
        ),
        (
            f"Near the heart of the place they found the true trouble. {problem.capitalize()}, and the people, creatures, or flowers around it had grown hesitant, as if joy itself were tiptoeing. "
            f"{name} felt {feeling}, because some problems seem to fill the whole horizon when you first stand before them. Still, the {special_object} warmed a little, almost like a hand saying keep going."
        ),
        (
            f"\"We do not need a giant answer,\" said {companion}. \"We need the next right one.\" "
            f"That helped. {name} knelt, watched closely, asked a few patient questions, and chose {moral.lower()} over hurry. "
            f"One careful act led to another, and soon the trouble loosened, not with thunder, but with a soft bright change that spread from the smallest corner outward."
        ),
        (
            f"By evening the {location.lower()} felt restored. Colors returned where they had dulled, laughter lifted where it had hidden, and the path home seemed shorter because hearts were lighter. "
            f"{name} tucked the {special_object} close, learning that courage does not always roar and magic does not always flash. Sometimes both arrive quietly, dressed as attention, tenderness, and a willingness to begin."
        ),
    ]
    if voice_guidance:
        paragraphs[0] += f" A loving wish floated alongside the morning too: {voice_guidance[:140]}."
    if age == "3-5":
        paragraphs = [p.replace("hesitant", "a little shy").replace("tenderness", "kind care") for p in paragraphs]
    elif age == "9-12":
        paragraphs[2] += " The path invited them to compare clues, notice patterns, and ask why some gentle actions work better than loud ones."
        paragraphs[4] += f" {name} tested small ideas, observed what changed, and adjusted thoughtfully."

    image_prompts = [
        f"Cinematic children's book illustration of {name} discovering a {special_object} in the {location.lower()}, warm golden light, premium magical realism.",
        f"Premium storybook scene of {name} meeting {companion}, emotional wonder, inviting path, painterly detail.",
        f"Wide cinematic journey scene through the {location.lower()} with playful details, luminous atmosphere, child-friendly fantasy.",
        f"Dramatic but gentle illustration of the central problem: {problem}, rich atmosphere, emotional storytelling lighting.",
        f"Turning-point illustration of {name} solving the problem with {moral.lower()} and patience, hopeful faces, glowing environment.",
        f"Golden evening finale in the {location.lower()}, restored beauty, community joy, premium animated-film finish.",
    ]
    choices = [
        ("Follow the silver trail", "Listen beside the old tree"),
        ("Ask a gentle question", "Study the glowing clues"),
        ("Share the idea with everyone", "Try one small step first"),
        ("Cross the bright bridge", "Wait for the wind to guide you"),
        ("Carry the lantern forward", "Sing softly to the path"),
        ("Wave to the stars", "Thank the garden kindly"),
    ]
    scenes: List[Dict[str, str]] = []
    for idx, paragraph in enumerate(paragraphs):
        choice_a, choice_b = choices[idx % len(choices)]
        scenes.append(
            {
                "heading": f"Scene {idx + 1}",
                "text": paragraph,
                "dialogue": f"{name}: I will look carefully before I rush.",
                "choice_a": choice_a,
                "choice_b": choice_b,
                "reaction": ["curious", "hopeful", "thoughtful", "delighted", "brave", "glowing"][idx % 6],
                "image_prompt": image_prompts[idx],
            }
        )

    story_text = "\n\n".join(paragraphs)
    questions = build_story_questions(
        {
            "name": name,
            "place": location,
            "companion": companion,
            "special_object": special_object,
            "problem": problem,
            "feeling": feeling,
            "moral": moral,
        }
    )
    return {
        "app_name": APP_NAME,
        "tagline": APP_TAGLINE,
        "title": title,
        "subtitle": subtitle,
        "story": story_text,
        "age_group": age,
        "category": story_type,
        "moral": moral_line,
        "scenes": scenes,
        "questions": questions,
        "feedback_messages": QUIZ_FEEDBACK_MESSAGES,
        "full_text": f"{story_text}\n\nMoral: {moral_line}",
    }


def generate_story(payload: Dict[str, Any]) -> Dict[str, Any]:
    provider = payload.get("api_provider", "Local Magic Engine")
    if provider in ["OpenAI", "Mistral"]:
        generated = ai_generate_story(
            api_provider=provider,
            api_key=payload.get("api_key", ""),
            model=payload.get("model", "gpt-4o-mini"),
            prompt_payload=payload,
        )
        if generated and generated.get("scenes") and generated.get("questions") and generated.get("story"):
            return normalize_story_payload(generated)
    return normalize_story_payload(local_generate_story(payload))


def rebuild_all_story_scenes() -> Dict[str, int]:
    """Re-process scenes for all stories using the improved paragraphs_to_scenes() grouping."""
    conn = db()
    rows = conn.execute("SELECT id, content_json, content_text FROM stories").fetchall()
    updated = 0
    for row in rows:
        try:
            payload = json.loads(row["content_json"])
            full_text = row["content_text"] or payload.get("full_text", "")
            if not full_text:
                continue
            # Strip the Moral trailer before scene-building
            story_body = full_text.split("\n\nMoral:")[0].strip()
            new_scenes = paragraphs_to_scenes(story_body)
            payload["scenes"] = new_scenes
            conn.execute(
                "UPDATE stories SET content_json=? WHERE id=?",
                (json.dumps(payload), row["id"]),
            )
            updated += 1
        except Exception:
            pass
    conn.commit()
    conn.close()
    return {"updated": updated}


def add_curated_library_stories(count: int = 5) -> int:
    curated_payloads = [
        {
            "child_name": "Lily",
            "age_group": "5-8",
            "story_type": "Fantasy",
            "mode": "Quick Story",
            "characters": ["Animals", "Kids"],
            "location": "Magical Land",
            "moral": "Kindness",
            "difficulty": "balanced",
            "api_provider": "Local Magic Engine",
        },
        {
            "child_name": "Arjun",
            "age_group": "8-12",
            "story_type": "Adventure",
            "mode": "Adventure Mode",
            "characters": ["Superheroes", "Kids"],
            "location": "Mountain Village",
            "moral": "Bravery",
            "difficulty": "rich",
            "api_provider": "Local Magic Engine",
        },
        {
            "child_name": "Mia",
            "age_group": "3-5",
            "story_type": "Bedtime",
            "mode": "Bedtime Story",
            "characters": ["Animals", "Princess"],
            "location": "Village",
            "moral": "Sharing",
            "difficulty": "gentle",
            "api_provider": "Local Magic Engine",
        },
        {
            "child_name": "Noah",
            "age_group": "5-8",
            "story_type": "Funny",
            "mode": "Learn & Grow",
            "characters": ["Friendly Monsters", "Robots"],
            "location": "School",
            "moral": "Honesty",
            "difficulty": "balanced",
            "api_provider": "Local Magic Engine",
        },
        {
            "child_name": "Zara",
            "age_group": "8-12",
            "story_type": "Educational",
            "mode": "Learn & Grow",
            "characters": ["Robots", "Kids"],
            "location": "Space",
            "moral": "Bravery",
            "difficulty": "rich",
            "api_provider": "Local Magic Engine",
        },
    ]

    created = 0
    for payload in curated_payloads[:count]:
        story = local_generate_story(payload)
        save_story(
            profile_id=None,
            payload=story,
            story_type=payload["story_type"],
            mode=payload["mode"],
            moral=payload["moral"],
            location=payload["location"],
            characters=payload["characters"],
        )
        created += 1
    return created


def seed_library_if_empty() -> None:
    conn = db()
    row = conn.execute("SELECT COUNT(*) AS c FROM stories").fetchone()
    conn.close()
    if row and int(row["c"]) == 0:
        add_curated_library_stories(5)


def transcribe_voice_note_openai(api_key: str, audio_file: Any) -> Optional[str]:
    if not api_key or audio_file is None:
        return None

    audio_bytes = audio_file.getvalue()
    filename = getattr(audio_file, "name", "voice_note.wav")
    mime_type = getattr(audio_file, "type", "audio/wav")

    for model_name in ["gpt-4o-mini-transcribe", "whisper-1"]:
        try:
            res = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {api_key}"},
                files={"file": (filename, audio_bytes, mime_type)},
                data={"model": model_name},
                timeout=45,
            )
            res.raise_for_status()
            body = res.json()
            text = body.get("text", "").strip()
            if text:
                return text
        except Exception:
            continue
    return None


def generate_scene_image_url(scene_text: str, provider: str, api_key: str, model: str) -> str:
    if provider == "OpenAI" and api_key:
        try:
            prompt = (
                "Child-friendly storybook illustration, vibrant colors, soft lighting, no text. "
                f"Scene description: {scene_text}"
            )
            res = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model or "gpt-image-1", "prompt": prompt, "size": "1024x1024"},
                timeout=45,
            )
            res.raise_for_status()
            body = res.json()
            if body.get("data") and body["data"][0].get("url"):
                return body["data"][0]["url"]
        except Exception:
            pass

    fallback_text = quote_plus(scene_text[:80])
    return f"https://placehold.co/1024x576/png?text={fallback_text}"


def enrich_story_with_scene_images(story: Dict[str, Any], provider: str, api_key: str, image_model: str) -> Dict[str, Any]:
    scenes = story.get("scenes", [])
    for scene in scenes:
        if not scene.get("image_url"):
            scene_prompt = scene.get("image_prompt") or scene.get("text", "Magical scene")
            scene["image_url"] = generate_scene_image_url(scene_prompt, provider, api_key, image_model)
    return story


def rebuild_full_text(story: Dict[str, Any]) -> str:
    blocks: List[str] = []
    for scene in story.get("scenes", []):
        blocks.append(f"{scene.get('heading', 'Scene')}\n{scene.get('text', '')}\n{scene.get('dialogue', '')}")
    return "\n\n".join(blocks) + f"\n\nMoral: {story.get('moral', '')}"


def apply_branch_choice(story: Dict[str, Any], scene_index: int, choice_text: str) -> str:
    scenes = story.get("scenes", [])
    if scene_index >= len(scenes):
        return "The story smiled and stayed magical."

    current_scene = scenes[scene_index]
    if "bridge" in choice_text.lower():
        reaction = "The bridge glowed brighter, and everyone felt a burst of confidence."
        next_bonus = "Because of that brave decision, the next path opened with golden light."
    elif "fireflies" in choice_text.lower():
        reaction = "The fireflies twirled happily and revealed a secret shortcut."
        next_bonus = "Because of that curious choice, a hidden clue appeared in the trees."
    else:
        reaction = "A warm breeze cheered the team and carried them forward."
        next_bonus = "Because of that thoughtful choice, the journey became clearer."

    current_scene["text"] = f"{current_scene.get('text', '')} {reaction}".strip()
    if scene_index + 1 < len(scenes):
        scenes[scene_index + 1]["text"] = f"{next_bonus} {scenes[scene_index + 1].get('text', '')}".strip()

    story["full_text"] = rebuild_full_text(story)
    return reaction


def create_pdf(story: Dict[str, Any]) -> bytes:
    # Keep PDF export optional so the story screen still works if the package is unavailable.
    try:
        FPDF = __import__("fpdf").FPDF
    except ModuleNotFoundError as exc:
        raise RuntimeError("PDF export requires the 'fpdf2' package.") from exc

    def pdf_safe_text(value: Any) -> str:
        text = "" if value is None else str(value)
        replacements = {
            "•": "-",
            "—": "-",
            "–": "-",
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "…": "...",
            "\u00a0": " ",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        # Core PDF fonts support Latin-1 only. Replace unsupported chars safely.
        return text.encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 10, pdf_safe_text(story.get("title", "Story")))
    pdf.set_font("Helvetica", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 8, pdf_safe_text(story.get("subtitle", "")))
    pdf.ln(2)
    for scene in story["scenes"]:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 8, pdf_safe_text(scene.get("heading", "Scene")))
        pdf.set_font("Helvetica", "", 11)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 7, pdf_safe_text(scene.get("text", "")))
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 7, pdf_safe_text(scene.get("dialogue", "")))
        pdf.ln(1)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 8, pdf_safe_text(f"Moral: {story.get('moral', '')}"))
    raw = pdf.output(dest="S")
    return raw.encode("latin-1") if isinstance(raw, str) else bytes(raw)


def init_state() -> None:
    if "screen" not in st.session_state:
        st.session_state.screen = "🏠 Home"
    if "platform_mode" not in st.session_state:
        saved_mode = get_setting("platform_mode", "kids")
        st.session_state.platform_mode = saved_mode if saved_mode in ["kids", "real_estate"] else "kids"
    if "active_story_id" not in st.session_state:
        st.session_state.active_story_id = None
    if "active_property_id" not in st.session_state:
        st.session_state.active_property_id = None
    if "scene_index" not in st.session_state:
        st.session_state.scene_index = 0
    if "current_story" not in st.session_state:
        st.session_state.current_story = None
    if "story_pages" not in st.session_state:
        st.session_state.story_pages = []
    if "current_page_index" not in st.session_state:
        st.session_state.current_page_index = 0
    if "total_pages" not in st.session_state:
        st.session_state.total_pages = 0
    if "choices" not in st.session_state:
        st.session_state.choices = []
    if "live_story" not in st.session_state:
        st.session_state.live_story = None
    if "live_story_id" not in st.session_state:
        st.session_state.live_story_id = None
    if "voice_guidance" not in st.session_state:
        st.session_state.voice_guidance = ""
    if "page_turning" not in st.session_state:
        st.session_state.page_turning = False
    if "page_turn_target" not in st.session_state:
        st.session_state.page_turn_target = None
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_story_id" not in st.session_state:
        st.session_state.quiz_story_id = None
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = None
    if "quiz_total" not in st.session_state:
        st.session_state.quiz_total = None
    if "home_category_filter" not in st.session_state:
        st.session_state.home_category_filter = "Magical"
    if "home_selected_profile_label" not in st.session_state:
        st.session_state.home_selected_profile_label = "All Children"
    if "home_recommendation_filter" not in st.session_state:
        st.session_state.home_recommendation_filter = st.session_state.home_selected_profile_label
    if "home_recommendation_filter_select" not in st.session_state:
        st.session_state.home_recommendation_filter_select = st.session_state.home_recommendation_filter
    if "home_last_recommendation_filter" not in st.session_state:
        st.session_state.home_last_recommendation_filter = st.session_state.home_recommendation_filter


def reset_story_navigation_state() -> None:
    st.session_state.current_story = None
    st.session_state.story_pages = []
    st.session_state.current_page_index = 0
    st.session_state.total_pages = 0
    st.session_state.scene_index = 0
    st.session_state.page_turning = False
    st.session_state.page_turn_target = None


def open_story_in_reader(story_id: int) -> None:
    st.session_state.active_story_id = story_id
    st.session_state.choices = []
    st.session_state.live_story = None
    st.session_state.live_story_id = None
    reset_story_navigation_state()
    reset_quiz_state()
    st.session_state.screen = "📚 Story Player"


def normalize_reader_line(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", str(text or "")).strip(" -:\n\t")
    cleaned = re.sub(r"^scene\s*\d+\s*[:\-]?\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def unique_lines(lines: List[str]) -> List[str]:
    cleaned: List[str] = []
    seen: set[str] = set()
    for raw_line in lines:
        line = normalize_reader_line(raw_line)
        if not line:
            continue
        fingerprint = re.sub(r"[^a-z0-9]+", " ", line.lower()).strip()
        if not fingerprint or fingerprint in seen:
            continue
        seen.add(fingerprint)
        cleaned.append(line)
    return cleaned


def split_story_into_pages(story: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Convert the stored story payload into clean, one-page-at-a-time reader pages.
    normalized_story = normalize_story_payload(story)
    scenes = normalized_story.get("scenes", []) if isinstance(normalized_story.get("scenes"), list) else []
    if not scenes and normalized_story.get("story"):
        scenes = paragraphs_to_scenes(str(normalized_story.get("story", "")))

    pages: List[Dict[str, Any]] = []
    seen_page_fingerprints: set[str] = set()
    for idx, raw_scene in enumerate(scenes):
        text_lines = unique_lines(re.split(r"\n+", str(raw_scene.get("text", ""))))
        dialogue_lines = unique_lines(re.split(r"\n+", str(raw_scene.get("dialogue", ""))))
        text_fingerprints = {re.sub(r"[^a-z0-9]+", " ", line.lower()).strip() for line in text_lines}
        dialogue_lines = [
            line
            for line in dialogue_lines
            if re.sub(r"[^a-z0-9]+", " ", line.lower()).strip() not in text_fingerprints
        ]

        heading = normalize_reader_line(raw_scene.get("heading", f"Page {idx + 1}")) or f"Page {idx + 1}"
        body = "\n\n".join(text_lines).strip()
        dialogue = "\n".join(dialogue_lines).strip()
        if not body and dialogue:
            body = dialogue
            dialogue = ""

        fingerprint = re.sub(r"[^a-z0-9]+", " ", f"{heading} {body} {dialogue}".lower()).strip()
        if fingerprint and fingerprint in seen_page_fingerprints:
            continue
        if fingerprint:
            seen_page_fingerprints.add(fingerprint)

        pages.append(
            {
                "scene_index": idx,
                "heading": heading,
                "text": body or "A new magical moment is ready to read.",
                "dialogue": dialogue,
                "choice_a": str(raw_scene.get("choice_a", "Follow the glowing path")).strip(),
                "choice_b": str(raw_scene.get("choice_b", "Listen beside the old tree")).strip(),
                "image_url": str(raw_scene.get("image_url", "")).strip(),
            }
        )

    if not pages:
        fallback_text = normalize_reader_line(normalized_story.get("story", "")) or normalize_reader_line(normalized_story.get("full_text", ""))
        pages = [
            {
                "scene_index": 0,
                "heading": normalized_story.get("title", "Story"),
                "text": fallback_text or "A story page will appear here once the adventure begins.",
                "dialogue": "",
                "choice_a": "Keep exploring",
                "choice_b": "Take a quiet breath",
                "image_url": "",
            }
        ]
    return pages


def sync_story_reader(story: Dict[str, Any], reset_index: bool = False) -> None:
    pages = split_story_into_pages(story)
    st.session_state.current_story = story
    st.session_state.story_pages = pages
    st.session_state.total_pages = len(pages)
    if reset_index:
        st.session_state.current_page_index = 0
    elif pages:
        st.session_state.current_page_index = min(
            max(0, st.session_state.get("current_page_index", 0)),
            len(pages) - 1,
        )
    else:
        st.session_state.current_page_index = 0

    if pages:
        page = pages[st.session_state.current_page_index]
        st.session_state.scene_index = int(page.get("scene_index", st.session_state.current_page_index))
    else:
        st.session_state.scene_index = 0


def render_story_page(page: Dict[str, Any], page_index: int, total_pages: int) -> None:
    if page.get("image_url"):
        st.image(page["image_url"], caption=f"Illustration for {page['heading']}", use_container_width=True)

    paragraphs = [part.strip() for part in re.split(r"\n{2,}", str(page.get("text", ""))) if part.strip()]
    paragraph_html = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
    dialogue = str(page.get("dialogue", "")).strip()
    dialogue_html = ""
    if dialogue:
        dialogue_html = (
            "<div class='story-dialogue'>"
            "<div class='story-dialogue-label'>Story Voice</div>"
            f"<p>{escape(dialogue)}</p>"
            "</div>"
        )

    st.markdown(
        f"""
        <div class='story-page-card'>
            <div class='story-page-meta'>
                <span class='mini-pill'>Page {page_index + 1} of {total_pages}</span>
                <span class='story-page-stars'>✨ ⭐ ✨</span>
            </div>
            <div class='story-page-heading'>{escape(str(page.get('heading', f'Page {page_index + 1}')))}</div>
            <div class='story-page-copy'>
                {paragraph_html}
            </div>
            {dialogue_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_navigation(story_id: int) -> None:
    total_pages = int(st.session_state.get("total_pages", 0) or 0)
    if total_pages <= 1:
        return

    current_page_index = min(
        max(0, st.session_state.get("current_page_index", 0)),
        total_pages - 1,
    )
    nav1, nav2, nav3 = st.columns([1.1, 1, 1.1])
    with nav1:
        if st.button(
            "⬅️ Previous Page",
            key=f"reader_prev_{story_id}_{current_page_index}",
            use_container_width=True,
            disabled=current_page_index == 0,
        ):
            play_sound(PAGE_TURN_SOUND, "page_turn")
            st.session_state.page_turning = True
            st.session_state.page_turn_target = current_page_index - 1
            st.rerun()
    with nav2:
        st.markdown(
            f"<div class='reader-nav-note'>Page {current_page_index + 1} / {total_pages}</div>",
            unsafe_allow_html=True,
        )
    with nav3:
        next_label = "Next Page ➡️" if current_page_index < total_pages - 1 else "Story Complete ✨"
        if st.button(
            next_label,
            key=f"reader_next_{story_id}_{current_page_index}",
            use_container_width=True,
            disabled=current_page_index >= total_pages - 1,
        ):
            play_sound(PAGE_TURN_SOUND, "page_turn")
            st.session_state.page_turning = True
            st.session_state.page_turn_target = current_page_index + 1
            st.rerun()


def nav_items_for_mode(mode: str) -> List[str]:
    if mode == "real_estate":
        return ["🏢 Home", "🔍 Properties", "📈 Investments", "🤝 Contact"]
    return ["🏠 Home", "✨ Create Story", "📚 Story Player", "🧸 Library", "👨‍👩‍👧 Parent Zone"]


def style_app(platform_mode: str) -> None:
    dark_mode = get_setting("dark_mode", "false") == "true"

    if platform_mode == "real_estate":
        st.markdown(
            """
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700;800&family=Manrope:wght@400;500;700&display=swap');
                :root {
                    --re-bg: linear-gradient(120deg, #0f1115, #1b1f27 45%, #2b2318 100%);
                    --re-card: rgba(255,255,255,0.93);
                    --re-text: #111827;
                    --re-gold: #c9a45c;
                    --re-accent: #c5a15e;
                    --re-muted: #6b7280;
                }
                .stApp {
                    background: var(--re-bg);
                    color: #f9fafb;
                }
                .block-container {
                    animation: fadeInUp 0.7s ease;
                }
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(16px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                section[data-testid="stSidebar"] {
                    background: #151922 !important;
                    border-right: 1px solid rgba(201,164,92,0.4);
                }
                section[data-testid="stSidebar"] * {
                    color: #f3f4f6 !important;
                }
                .re-hero {
                    border-radius: 22px;
                    overflow: hidden;
                    position: relative;
                    min-height: 290px;
                    border: 1px solid rgba(201,164,92,0.35);
                    background: linear-gradient(0deg, rgba(0,0,0,0.45), rgba(0,0,0,0.15)),
                                url('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=1800&q=80') center/cover no-repeat;
                    box-shadow: 0 22px 45px rgba(0,0,0,0.42);
                }
                .re-hero-content {
                    position: absolute;
                    left: 2rem;
                    bottom: 2rem;
                    max-width: 680px;
                }
                .re-badge {
                    display: inline-block;
                    padding: 0.28rem 0.8rem;
                    border: 1px solid rgba(255,255,255,0.55);
                    border-radius: 999px;
                    color: #fef3c7;
                    margin-bottom: 0.7rem;
                    font: 600 0.78rem 'Manrope', sans-serif;
                    letter-spacing: 0.08em;
                    background: rgba(0,0,0,0.25);
                }
                .re-title {
                    font-family: 'Playfair Display', serif;
                    font-size: 2.9rem;
                    color: #fff;
                    line-height: 1.06;
                    text-shadow: 0 8px 20px rgba(0,0,0,0.45);
                }
                .re-sub {
                    color: #e5e7eb;
                    font: 500 1rem 'Manrope', sans-serif;
                    margin-top: 0.5rem;
                }
                .panel {
                    background: var(--re-card);
                    color: var(--re-text);
                    border-radius: 18px;
                    border: 1px solid rgba(201,164,92,0.25);
                    padding: 1rem 1.1rem;
                    box-shadow: 0 10px 28px rgba(0,0,0,0.15);
                    transition: transform .25s ease, box-shadow .25s ease;
                }
                .panel:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 16px 30px rgba(0,0,0,0.2);
                }
                h1, h2, h3 {
                    font-family: 'Playfair Display', serif !important;
                    color: #f9fafb !important;
                }
                p, label, li, .stMarkdown, .stCaption {
                    font-family: 'Manrope', sans-serif !important;
                }
                .stButton > button {
                    border-radius: 999px !important;
                    border: 1px solid #d3b171 !important;
                    background: linear-gradient(120deg, #f4dfb2, #c9a45c) !important;
                    color: #1f2937 !important;
                    font-weight: 800 !important;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
                    transition: transform .2s ease !important;
                }
                .stButton > button:hover {
                    transform: translateY(-2px) scale(1.01) !important;
                }
                .lux-stat {
                    font-family: 'Playfair Display', serif;
                    color: #fef3c7;
                    font-size: 2rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        return

    if dark_mode:
        card = "rgba(33, 30, 58, 0.92)"
        text = "#f8f7ff"
        bg = "radial-gradient(1200px 550px at 8% -8%, #334155 0%, transparent 52%), linear-gradient(135deg, #0f172a, #1f2937, #312e81)"
        heading = "#f9fafb"
        panel_border = "rgba(255,255,255,0.2)"
        pill_bg = "#fde68a"
        pill_text = "#7c2d12"
        alert_bg = "#fef3c7"
        alert_text = "#1f2937"
        sidebar_bg = "#1e1b38"
        sidebar_text = "#f8f7ff"
        sidebar_muted = "#c7c3ff"
    else:
        card = "rgba(255,255,255,0.94)"
        text = "#1f1b45"
        bg = "radial-gradient(1000px 450px at 12% -5%, #a9d8ff 0%, transparent 55%), radial-gradient(900px 500px at 100% 8%, #ffc8dd 0%, transparent 55%), linear-gradient(130deg, #e9f8ff, #dff7ea, #f8e8ff)"
        heading = "#241e5a"
        panel_border = "rgba(255,255,255,0.88)"
        pill_bg = "#ffcf8d"
        pill_text = "#7c2d12"
        alert_bg = "#fff4cc"
        alert_text = "#111827"
        sidebar_bg = "#f5f1ff"
        sidebar_text = "#2b2151"
        sidebar_muted = "#4338ca"

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;700&family=Quicksand:wght@500;700&display=swap');
            .stApp {{
                background: {bg};
                color: {text};
            }}
            .block-container {{
                animation: fadeInUpKid 0.6s ease;
            }}
            @keyframes fadeInUpKid {{
                from {{ opacity: 0; transform: translateY(14px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            section[data-testid="stSidebar"] {{
                background: {sidebar_bg} !important;
                border-right: 1px solid rgba(255,255,255,0.2);
            }}
            section[data-testid="stSidebar"] * {{
                color: {sidebar_text} !important;
            }}
            section[data-testid="stSidebar"] [role="radiogroup"] label p {{
                color: {sidebar_text} !important;
                font-weight: 700 !important;
            }}
            section[data-testid="stSidebar"] [data-baseweb="radio"] svg {{
                fill: {sidebar_muted} !important;
            }}
            p, label, li, .stCaption, .stMarkdown, .stTextInput, .stSelectbox, .stRadio {{
                color: {text} !important;
                font-family: 'Quicksand', sans-serif !important;
            }}
            h1, h2, h3 {{
                font-family: 'Fredoka', sans-serif !important;
                color: {heading} !important;
            }}
            .panel {{
                background: {card};
                border-radius: 22px;
                border: 1px solid {panel_border};
                padding: 1rem 1.1rem;
                box-shadow: 0 14px 30px rgba(34, 24, 77, 0.16);
                transition: transform .2s ease, box-shadow .2s ease;
            }}
            .panel:hover {{
                transform: translateY(-4px) scale(1.01);
                box-shadow: 0 20px 34px rgba(34, 24, 77, 0.2);
            }}
            .stars, .clouds, .butterflies, .creatures {{
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 2;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
            }}
            .clouds span {{
                position: absolute;
                width: 120px;
                height: 36px;
                border-radius: 999px;
                background: rgba(255,255,255,.5);
                filter: blur(1px);
                animation: drift 24s linear infinite;
            }}
            .stars span {{
                position: absolute;
                font-size: 1.4rem;
                animation: twinkleStar 5s ease-in-out infinite;
                filter: drop-shadow(0 0 6px rgba(251, 191, 36, 0.55));
            }}
            .butterflies span {{
                position: absolute;
                font-size: 2rem;
                animation: flutter 3.5s ease-in-out infinite;
            }}
            .creatures span {{
                position: absolute;
                font-size: 2.2rem;
                animation: wander 8s ease-in-out infinite;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
            }}
            @keyframes twinkle {{
                0%, 100% {{ transform: scale(0.5); opacity: 0.3; }}
                50% {{ transform: scale(1.4); opacity: 1; }}
            }}
            @keyframes drift {{
                from {{ transform: translateX(-180px); }}
                to {{ transform: translateX(110vw); }}
            }}
            @keyframes twinkleStar {{
                0%, 100% {{ transform: translateY(0) scale(0.9); opacity: 0.45; }}
                50% {{ transform: translateY(-8px) scale(1.15); opacity: 1; }}
            }}
            @keyframes flutter {{
                0% {{ transform: translateX(0) translateY(0) rotate(0deg); }}
                25% {{ transform: translateX(30px) translateY(-20px) rotate(-15deg); }}
                50% {{ transform: translateX(0) translateY(-40px) rotate(0deg); }}
                75% {{ transform: translateX(-30px) translateY(-20px) rotate(15deg); }}
                100% {{ transform: translateX(0) translateY(0) rotate(0deg); }}
            }}
            @keyframes wander {{
                0% {{ transform: translateX(0) translateY(0) scale(1); opacity: 0.8; }}
                25% {{ transform: translateX(40px) translateY(-30px) scale(1.05); }}
                50% {{ transform: translateX(20px) translateY(-60px) scale(1); }}
                75% {{ transform: translateX(-30px) translateY(-40px) scale(0.95); }}
                100% {{ transform: translateX(0) translateY(0) scale(1); opacity: 0.8; }}
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-25px); }}
            }}
            .hero-title {{
                font-size: 3rem;
                line-height: 1.05;
                margin-bottom: 0.3rem;
            }}
            .story-hero {{
                position: relative;
                overflow: hidden;
                border-radius: 30px;
                padding: 1.6rem 1.5rem;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(224,242,254,0.86) 35%, rgba(243,232,255,0.92) 70%, rgba(254,240,138,0.78));
                border: 1px solid rgba(255,255,255,0.9);
                box-shadow: 0 18px 36px rgba(34, 24, 77, 0.16);
            }}
            .story-hero:before {{
                content: '';
                position: absolute;
                inset: auto -40px -80px auto;
                width: 220px;
                height: 220px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(251,191,36,0.28), rgba(251,191,36,0));
            }}
            .story-hero-title {{
                font-family: 'Fredoka', sans-serif;
                font-size: 3rem;
                line-height: 1.02;
                color: #1e1b4b;
                max-width: 640px;
            }}
            .story-hero-subtitle {{
                font-size: 1.05rem;
                max-width: 620px;
                color: #4338ca;
                font-weight: 700;
            }}
            .story-hero-decor span {{
                position: absolute;
                font-size: 1.8rem;
                opacity: 0.95;
                animation: driftPop 6s ease-in-out infinite;
            }}
            .story-hero-decor span:nth-child(2n) {{
                animation-duration: 7.2s;
            }}
            @keyframes driftPop {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                50% {{ transform: translateY(-10px) rotate(4deg); }}
            }}
            .home-card-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
                gap: 12px;
                margin: 0.5rem 0 1rem;
            }}
            .home-feature-card {{
                background: rgba(255,255,255,0.86);
                border: 1px solid rgba(255,255,255,0.95);
                border-radius: 24px;
                padding: 1rem;
                min-height: 168px;
                box-shadow: 0 14px 24px rgba(34, 24, 77, 0.12);
            }}
            .home-feature-card b {{
                display: block;
                color: #312e81;
                font-size: 1.05rem;
                margin-bottom: 0.35rem;
            }}
            .home-feature-card p {{
                color: #4338ca !important;
                margin: 0;
                font-size: 0.95rem;
                line-height: 1.5;
            }}
            .feature-icon {{
                font-size: 1.8rem;
                margin-bottom: 0.45rem;
            }}
            .story-page-card {{
                background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(240,249,255,0.92));
                border-radius: 28px;
                border: 1px solid rgba(255,255,255,0.95);
                padding: 1.35rem 1.3rem;
                box-shadow: 0 16px 32px rgba(34, 24, 77, 0.16);
                margin-top: 0.2rem;
            }}
            .story-page-meta {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 0.8rem;
                flex-wrap: wrap;
            }}
            .story-page-heading {{
                font-family: 'Fredoka', sans-serif;
                color: #1f245a;
                font-size: 1.9rem;
                margin-bottom: 0.75rem;
            }}
            .story-page-stars {{
                color: #f59e0b;
                font-weight: 800;
                letter-spacing: 0.15rem;
            }}
            .story-page-copy p {{
                background: rgba(255,255,255,0.72);
                border-radius: 18px;
                padding: 0.9rem 1rem;
                margin-bottom: 0.75rem;
                border: 1px solid rgba(191,219,254,0.8);
                color: #1f1b45 !important;
                font-size: 1.03rem;
                line-height: 1.8;
            }}
            .story-dialogue {{
                background: linear-gradient(135deg, rgba(254,240,138,0.45), rgba(253,164,175,0.24));
                border-radius: 20px;
                border: 1px solid rgba(253,186,116,0.65);
                padding: 0.95rem 1rem;
                margin-top: 0.8rem;
            }}
            .story-dialogue-label {{
                font-family: 'Fredoka', sans-serif;
                color: #9a3412;
                margin-bottom: 0.35rem;
                font-weight: 800;
            }}
            .story-dialogue p {{
                margin: 0;
                color: #1f1b45 !important;
                font-size: 1.02rem;
                line-height: 1.7;
                font-weight: 700;
            }}
            .reader-nav-note {{
                text-align: center;
                font-weight: 800;
                color: #4338ca;
                padding-top: 0.7rem;
            }}
            .mini-pill {{
                display: inline-block;
                border-radius: 999px;
                background: {pill_bg};
                color: {pill_text};
                font-weight: 800;
                padding: 0.2rem 0.7rem;
                font-size: 0.82rem;
            }}
            div[data-baseweb="notification"] {{
                background: {alert_bg} !important;
                border: 1px solid #f59e0b !important;
                border-radius: 14px !important;
            }}
            div[data-baseweb="notification"] p,
            div[data-baseweb="notification"] div,
            .stAlert p,
            .stAlert div {{
                color: {alert_text} !important;
                font-weight: 700 !important;
            }}
            .stSelectbox {{
                position: relative;
                z-index: 25;
            }}
            div[data-baseweb="select"] > div {{
                background: rgba(255, 255, 255, 0.96) !important;
                color: #1f1b45 !important;
                border: 1px solid rgba(96, 165, 250, 0.55) !important;
                border-radius: 14px !important;
                box-shadow: 0 8px 18px rgba(34, 24, 77, 0.12) !important;
            }}
            .stTextInput input,
            .stTextArea textarea,
            div[data-baseweb="input"] input,
            div[data-baseweb="textarea"] textarea {{
                background: rgba(255, 255, 255, 0.96) !important;
                color: #1f1b45 !important;
                border: 1px solid rgba(96, 165, 250, 0.45) !important;
                border-radius: 12px !important;
            }}
            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder,
            div[data-baseweb="input"] input::placeholder,
            div[data-baseweb="textarea"] textarea::placeholder {{
                color: #64748b !important;
                opacity: 1 !important;
            }}
            .stNumberInput input,
            .stDateInput input,
            .stTimeInput input {{
                background: rgba(255, 255, 255, 0.96) !important;
                color: #1f1b45 !important;
            }}
            div[data-baseweb="popover"] {{
                z-index: 10000 !important;
            }}
            ul[role="listbox"] {{
                background: #ffffff !important;
                border: 2px solid rgba(96, 165, 250, 0.5) !important;
                border-radius: 12px !important;
                box-shadow: 0 14px 28px rgba(34, 24, 77, 0.25) !important;
                padding: 8px 0 !important;
            }}
            li[role="option"] {{
                background-color: #ffffff !important;
                color: #1f1b45 !important;
                font-weight: 500 !important;
                padding: 10px 16px !important;
                margin: 2px 8px !important;
                border-radius: 8px !important;
            }}
            li[role="option"]:hover {{
                background-color: #f0f9ff !important;
                color: #1e40af !important;
            }}
            li[role="option"][aria-selected="true"] {{
                background: #dbeafe !important;
                color: #1e3a8a !important;
                font-weight: 600 !important;
            }}
            div.stButton > button {{
                background: linear-gradient(120deg, #60a5fa, #f472b6) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 999px !important;
                font-weight: 800 !important;
                box-shadow: 0 8px 18px rgba(96, 165, 250, 0.35) !important;
                transition: transform .2s ease !important;
            }}
            div.stDownloadButton > button,
            div.stLinkButton > a,
            div[data-testid="stLinkButton"] > a {{
                background: linear-gradient(120deg, #60a5fa, #f472b6) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 999px !important;
                font-weight: 800 !important;
                box-shadow: 0 8px 18px rgba(96, 165, 250, 0.35) !important;
                text-decoration: none !important;
                min-height: 2.5rem !important;
                width: 100% !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: transform .2s ease !important;
            }}
            div.stButton > button:hover {{
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 12px 24px rgba(96, 165, 250, 0.4) !important;
            }}
            div.stDownloadButton > button:hover,
            div.stLinkButton > a:hover,
            div[data-testid="stLinkButton"] > a:hover {{
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 12px 24px rgba(96, 165, 250, 0.4) !important;
            }}
        </style>

        <div class="clouds">
            <span style="top:6%; left:-100px; animation-delay:0s"></span>
            <span style="top:20%; left:-220px; animation-delay:7s"></span>
            <span style="top:42%; left:-180px; animation-delay:11s"></span>
        </div>
        <div class="stars">
            <span style="top:10%; left:18%; animation-delay:.2s">⭐</span>
            <span style="top:18%; left:84%; animation-delay:1.1s">✨</span>
            <span style="top:52%; left:6%; animation-delay:2.1s">⭐</span>
            <span style="top:76%; left:78%; animation-delay:1.7s">✨</span>
        </div>
        <div class="butterflies">
            <span style="top:15%; left:5%; animation-delay:0s">🦋</span>
            <span style="top:40%; left:92%; animation-delay:1.5s">🦋</span>
            <span style="top:25%; left:45%; animation-delay:0.8s">🦋</span>
        </div>
        <div class="creatures">
            <span style="top:35%; left:8%; animation-delay:0s">🐰</span>
            <span style="top:55%; left:85%; animation-delay:1.2s">🦊</span>
            <span style="top:20%; left:75%; animation-delay:2.5s">🐻</span>
            <span style="top:65%; left:20%; animation-delay:1.8s">🐾</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(platform_mode: str) -> None:
    if platform_mode == "real_estate":
        hero_html = """
        <div class='re-hero'>
            <div class='re-hero-content'>
                <div class='re-badge'>TRUE IDEAL REAL ESTATE</div>
                <div class='re-title'>Find Your Perfect Home in Dubai</div>
                <div class='re-sub'>Ultra-premium residences, investor-ready opportunities, and concierge-level guidance.</div>
            </div>
        </div>
        """
        st.markdown(hero_html, unsafe_allow_html=True)
        return

    hero_html = f"""
    <div class='panel' style='margin-bottom:0.6rem;'>
        <div class='mini-pill'>MAGICAL STORY UNIVERSE</div>
        <div class='hero-title'>{APP_NAME}</div>
        <div style='font-weight:700;opacity:0.9;'>{APP_TAGLINE}</div>
        <div style='margin-top:6px;font-size:1.2rem;'>🐦 🐰 🦊 🐻 ⭐ ✨</div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)


def screen_nav() -> None:
    with st.sidebar:
        st.markdown("## Experience")
        if st.session_state.platform_mode == "real_estate":
            if st.button("Switch to Kids Mode 🧸", key="switch_kids_mode"):
                st.session_state.platform_mode = "kids"
                set_setting("platform_mode", "kids")
                st.session_state.screen = nav_items_for_mode("kids")[0]
                st.rerun()
        else:
            st.caption("Story Mode Active 🧸")

        nav_items = nav_items_for_mode(st.session_state.platform_mode)
        if st.session_state.screen not in nav_items:
            st.session_state.screen = nav_items[0]

        st.markdown("## Navigation")
        choice = st.radio(
            "Go to",
            nav_items,
            index=nav_items.index(st.session_state.screen),
        )
        st.session_state.screen = choice

        st.markdown("## Theme")
        theme_label = "Evening Luxe Mode" if st.session_state.platform_mode == "real_estate" else "Night Reading Mode"
        dark = st.toggle(theme_label, value=get_setting("dark_mode", "false") == "true")
        set_setting("dark_mode", "true" if dark else "false")


def featured_carousel() -> None:
    cards = "".join(
        [
            f"<div style='min-width:240px;background:rgba(255,255,255,0.96);border-radius:16px;padding:12px;border:1px solid #ddd6fe;box-shadow:0 8px 18px rgba(67,56,202,0.14)'><div style='font-weight:800;color:#1f1b45'>{c['title']}</div><div style='font-size:0.82rem;color:#312e81;margin:4px 0;font-weight:700'>{c['tag']}</div><div style='font-size:0.92rem;color:#312e81'>{c['blurb']}</div></div>"
            for c in DEFAULT_FEATURED
        ]
    )
    html = f"""
    <div style='overflow:auto;display:flex;gap:10px;padding-bottom:8px'>{cards}</div>
    """
    components.html(html, height=140, scrolling=False)


def real_estate_featured_carousel(properties: List[Dict[str, Any]]) -> None:
        slides = "".join(
                [
                        f"""
                        <div class='re-slide' style="background:linear-gradient(0deg, rgba(12,16,24,.55), rgba(12,16,24,.18)), url('{item['image']}') center/cover no-repeat;">
                                <div class='re-slide-inner'>
                                        <div class='re-slide-badge'>{item['community']}</div>
                                        <div class='re-slide-title'>{item['name']}</div>
                                        <div class='re-slide-meta'>{item['bedrooms']} BR • {item['bathrooms']} BA • {item['area_sqft']} sq.ft • ROI {item['roi']}%</div>
                                        <div class='re-slide-price'>{format_aed(item['price_aed'])}</div>
                                </div>
                        </div>
                        """
                        for item in properties
                ]
        )
        dots = "".join([f"<button class='re-dot' data-idx='{idx}' aria-label='Slide {idx + 1}'></button>" for idx in range(len(properties))])
        html = f"""
        <style>
            .re-carousel {{
                position: relative;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 18px 34px rgba(0,0,0,.22);
                border: 1px solid rgba(201,164,92,.28);
                background: #0f1115;
            }}
            .re-track {{
                display: flex;
                width: 100%;
                transition: transform .85s cubic-bezier(.2,.8,.2,1);
            }}
            .re-slide {{
                min-width: 100%;
                height: 360px;
                position: relative;
            }}
            .re-slide-inner {{
                position: absolute;
                left: 1.5rem;
                bottom: 1.5rem;
                color: #fff;
                max-width: 70%;
            }}
            .re-slide-badge {{
                display: inline-block;
                border-radius: 999px;
                padding: .28rem .7rem;
                border: 1px solid rgba(255,255,255,.36);
                background: rgba(255,255,255,.12);
                margin-bottom: .7rem;
                font: 600 .8rem Georgia, serif;
            }}
            .re-slide-title {{
                font: 700 2rem Georgia, serif;
                line-height: 1.06;
                margin-bottom: .35rem;
            }}
            .re-slide-meta {{
                font: 500 .96rem Arial, sans-serif;
                opacity: .92;
            }}
            .re-slide-price {{
                margin-top: .8rem;
                font: 700 1.05rem Arial, sans-serif;
                color: #f6d28b;
            }}
            .re-carousel-nav {{
                position: absolute;
                inset: auto 1rem 1rem auto;
                display: flex;
                gap: .45rem;
            }}
            .re-dot {{
                width: 11px;
                height: 11px;
                border-radius: 50%;
                border: none;
                background: rgba(255,255,255,.42);
                cursor: pointer;
            }}
            .re-dot.active {{
                background: #f6d28b;
                transform: scale(1.15);
            }}
            .re-arrows {{
                position: absolute;
                inset: 50% 0 auto 0;
                display: flex;
                justify-content: space-between;
                transform: translateY(-50%);
                padding: 0 .9rem;
            }}
            .re-arrow {{
                width: 42px;
                height: 42px;
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,.28);
                background: rgba(15,17,21,.42);
                color: #fff;
                font-size: 1.1rem;
                cursor: pointer;
                backdrop-filter: blur(8px);
            }}
        </style>
        <div class='re-carousel' id='re-carousel'>
            <div class='re-track' id='re-track'>
                {slides}
            </div>
            <div class='re-arrows'>
                <button class='re-arrow' id='re-prev' aria-label='Previous property'>&lsaquo;</button>
                <button class='re-arrow' id='re-next' aria-label='Next property'>&rsaquo;</button>
            </div>
            <div class='re-carousel-nav' id='re-dots'>{dots}</div>
        </div>
        <script>
            const track = document.getElementById('re-track');
            const dots = Array.from(document.querySelectorAll('.re-dot'));
            const total = dots.length;
            let index = 0;
            let timer = null;

            function paint() {{
                track.style.transform = `translateX(-${{index * 100}}%)`;
                dots.forEach((dot, dotIndex) => dot.classList.toggle('active', dotIndex === index));
            }}

            function goTo(nextIndex) {{
                index = (nextIndex + total) % total;
                paint();
            }}

            function autoplay() {{
                clearInterval(timer);
                timer = setInterval(() => goTo(index + 1), 3800);
            }}

            document.getElementById('re-prev').addEventListener('click', () => {{ goTo(index - 1); autoplay(); }});
            document.getElementById('re-next').addEventListener('click', () => {{ goTo(index + 1); autoplay(); }});
            dots.forEach((dot, dotIndex) => dot.addEventListener('click', () => {{ goTo(dotIndex); autoplay(); }}));

            paint();
            autoplay();
        </script>
        """
        components.html(html, height=360, scrolling=False)


def format_aed(value: int) -> str:
    return f"AED {value:,.0f}"


def property_detail_panel(property_item: Dict[str, Any]) -> None:
    st.markdown(f"### {property_item['name']}")
    st.caption(
        f"{property_item['community']} • {property_item['type']} • {property_item['bedrooms']} BR • "
        f"{property_item['bathrooms']} BA • {property_item['area_sqft']} sq.ft"
    )

    st.image(property_item["image"], use_container_width=True)
    g1, g2 = st.columns(2)
    g1.image(property_item["gallery"][0], use_container_width=True)
    g2.image(property_item["gallery"][1], use_container_width=True)

    r1, r2, r3 = st.columns(3)
    r1.metric("Price", format_aed(property_item["price_aed"]))
    r2.metric("Projected ROI", f"{property_item['roi']}%")
    r3.metric("Status", property_item["status"])

    st.link_button("Open Location Map", property_item["map"])
    wa_text = quote_plus(f"Hi True Ideal, I want details for {property_item['name']} in {property_item['community']}.")
    st.link_button("WhatsApp Agent", f"https://wa.me/971501234567?text={wa_text}")


def real_estate_home_screen() -> None:
    st.markdown("### Luxury Portfolio")

    s1, s2, s3 = st.columns(3)
    s1.markdown("<div class='panel'><div style='font-size:.8rem;color:#6b7280;'>Curated Listings</div><div class='lux-stat'>250+</div></div>", unsafe_allow_html=True)
    s2.markdown("<div class='panel'><div style='font-size:.8rem;color:#6b7280;'>Avg ROI</div><div class='lux-stat'>8.4%</div></div>", unsafe_allow_html=True)
    s3.markdown("<div class='panel'><div style='font-size:.8rem;color:#6b7280;'>Investor Clients</div><div class='lux-stat'>1,900+</div></div>", unsafe_allow_html=True)

    st.markdown("#### Featured Properties")
    real_estate_featured_carousel(REAL_ESTATE_PROPERTIES[:5])

    c1, c2 = st.columns(2)
    if c1.button("Book a Viewing", key="re_book_viewing_home"):
        st.session_state.screen = "🤝 Contact"
        st.rerun()
    if c2.button("Get Best Deals", key="re_best_deals_home"):
        st.session_state.screen = "🔍 Properties"
        st.rerun()

    st.markdown("#### Why Choose Us")
    st.markdown(
        """
        <div class='panel'>
            <b>True Ideal Real Estate</b><br>
            Market intelligence, premium off-plan allocations, trusted developer network, and concierge-level after-sales support.
        </div>
        """,
        unsafe_allow_html=True,
    )


def real_estate_properties_screen() -> None:
    st.markdown("### Property Search")

    communities = sorted({p["community"] for p in REAL_ESTATE_PROPERTIES})
    max_price = max(p["price_aed"] for p in REAL_ESTATE_PROPERTIES)

    f1, f2, f3 = st.columns(3)
    selected_community = f1.selectbox("Location", ["All"] + communities)
    selected_price = f2.slider("Max Price (AED)", min_value=1000000, max_value=max_price, value=max_price, step=250000)
    selected_beds = f3.multiselect("Bedrooms", [1, 2, 3, 4, 5, 6], default=[2, 3, 4, 5, 6])

    results: List[Dict[str, Any]] = []
    for item in REAL_ESTATE_PROPERTIES:
        if selected_community != "All" and item["community"] != selected_community:
            continue
        if item["price_aed"] > selected_price:
            continue
        if item["bedrooms"] not in selected_beds:
            continue
        results.append(item)

    if not results:
        st.warning("No properties match your current filters.")
        return

    for item in results:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(
                f"""
                <div class='panel'>
                    <div style='font-weight:800;font-size:1.05rem;color:#111827'>{item['name']}</div>
                    <div style='color:#6b7280'>{item['community']} • {item['type']} • {item['bedrooms']} BR / {item['bathrooms']} BA • {item['area_sqft']} sq.ft</div>
                    <div style='margin-top:5px;color:#9a7a41;font-weight:800;'>
                        {format_aed(item['price_aed'])} • ROI {item['roi']}% • {item['status']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.image(item["image"], use_container_width=True)
            if st.button("View Property", key=f"property_view_{item['id']}"):
                st.session_state.active_property_id = item["id"]

    if st.session_state.active_property_id:
        selected = next((p for p in REAL_ESTATE_PROPERTIES if p["id"] == st.session_state.active_property_id), None)
        if selected:
            st.markdown("---")
            property_detail_panel(selected)


def real_estate_investments_screen() -> None:
    st.markdown("### Investment Insights")
    market = {
        "Downtown Dubai": 8.2,
        "Business Bay": 9.1,
        "Dubai Marina": 8.4,
        "Palm Jumeirah": 7.0,
        "Dubai Creek Harbour": 8.8,
    }
    st.line_chart(market)

    st.markdown("#### Appreciation Snapshot")
    st.markdown(
        """
        <div class='panel'>
            <b>5-Year Appreciation Trend</b><br>
            Prime communities continue to show strong rental demand and resilient capital growth. We shortlist units based on entry timing,
            payment plan structure, and exit liquidity to optimize your portfolio strategy.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Testimonials")
    t1, t2 = st.columns(2)
    t1.markdown("<div class='panel'><b>R. Khanna</b><br>\"Seamless advisory and sharp ROI guidance. Closed in 5 days.\"</div>", unsafe_allow_html=True)
    t2.markdown("<div class='panel'><b>S. Rahman</b><br>\"Clear data, premium inventory, and very professional follow-through.\"</div>", unsafe_allow_html=True)


def real_estate_contact_screen() -> None:
    st.markdown("### Book a Viewing")
    c1, c2 = st.columns(2)
    with c1:
        full_name = st.text_input("Full Name")
        phone = st.text_input("Phone / WhatsApp")
    with c2:
        email = st.text_input("Email")
        budget = st.selectbox("Budget", ["AED 1M-3M", "AED 3M-7M", "AED 7M+"])

    preferred_community = st.selectbox("Preferred Community", sorted({p["community"] for p in REAL_ESTATE_PROPERTIES}))
    notes = st.text_area("Requirements", placeholder="Type, bedrooms, payment plan preference, handover timeline...")

    if st.button("Submit Viewing Request", key="submit_re_viewing"):
        if not full_name.strip() or not phone.strip():
            st.warning("Please add your name and phone number.")
        else:
            st.success("Request submitted. Our advisor will contact you shortly.")

    wa_text = quote_plus(
        f"Hi True Ideal, I want the best deals in {preferred_community}. Budget: {budget}. Notes: {notes[:120]}"
    )
    st.link_button("Get Best Deals on WhatsApp", f"https://wa.me/971501234567?text={wa_text}")


def render_home_feature_tile(column: Any, icon: str, title: str, description: str, button_label: str, button_key: str) -> bool:
    with column:
        st.markdown(
            f"""
            <div class='home-feature-card'>
                <div class='feature-icon'>{icon}</div>
                <b>{escape(title)}</b>
                <p>{escape(description)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return st.button(button_label, key=button_key, use_container_width=True)


def focus_library_category(category: str) -> None:
    st.session_state.home_category_filter = category
    for tab_idx in range(3):
        st.session_state[f"library_category_filter_{tab_idx}"] = category
    st.session_state.screen = "🧸 Library"


def render_home_page(selected_profile: Optional[sqlite3.Row], active_category: str, rec_rows: List[sqlite3.Row]) -> None:
    welcome_name = selected_profile["child_name"] if selected_profile else "little readers"
    all_rows = list_stories("all")
    category_counts = {category: sum(1 for row in all_rows if story_category_from_row(row) == category) for category in STORY_TYPES}
    story_of_the_day = get_story_of_the_day()
    featured_row = None
    if all_rows:
        day_index = int(datetime.now().strftime("%j")) % len(all_rows)
        featured_row = all_rows[day_index]
    latest_story = get_last_story()

    st.markdown(
        f"""
        <div class='story-hero'>
            <div class='mini-pill'>MAGICAL STORYBOOK ADVENTURE</div>
            <div class='story-hero-title'>Welcome to a magical world of stories</div>
            <div class='story-hero-subtitle'>Read, imagine, and grow with every tale. {escape(welcome_name)} can explore gentle bedtime journeys, playful adventures, and brain-boosting questions in one cozy reading space.</div>
            <div style='margin-top:0.85rem; color:#4338ca; font-weight:800;'>Featured today: {escape(story_of_the_day['title'])} • {escape(story_of_the_day['blurb'])}</div>
            <div class='story-hero-decor'>
                <span style='top:14px; right:20px;'>⭐</span>
                <span style='top:74px; right:84px;'>☁️</span>
                <span style='bottom:18px; right:32px;'>🦊</span>
                <span style='bottom:44px; right:112px;'>🐻</span>
                <span style='top:28px; left:74%;'>🎈</span>
                <span style='bottom:22px; left:58%;'>🪁</span>
                <span style='top:84px; left:68%;'>🌙</span>
                <span style='bottom:18px; left:42%;'>📚</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Explore Wonderloom")
    tile1, tile2, tile3, tile4 = st.columns(4)
    if render_home_feature_tile(
        tile1,
        "📖",
        "Featured Story",
        f"{story_of_the_day['title']} • {story_of_the_day['blurb']}",
        "Open Featured Story",
        "home_featured_story_tile",
    ):
        if featured_row:
            open_story_in_reader(featured_row["id"])
            st.rerun()
        st.session_state.screen = "🧸 Library"
        st.rerun()
    if render_home_feature_tile(
        tile2,
        "🗺️",
        "Adventure Stories",
        f"{category_counts.get('Adventure', 0)} adventures ready for brave explorers.",
        "Explore Adventure",
        "home_adventure_tile",
    ):
        focus_library_category("Adventure")
        st.rerun()
    if render_home_feature_tile(
        tile3,
        "🌙",
        "Bedtime Stories",
        f"{category_counts.get('Bedtime', 0)} calming tales for soft, sleepy reading.",
        "Explore Bedtime",
        "home_bedtime_tile",
    ):
        focus_library_category("Bedtime")
        st.rerun()
    if render_home_feature_tile(
        tile4,
        "✨",
        "Magical Stories",
        f"{category_counts.get('Magical', 0)} sparkling journeys filled with wonder.",
        "Explore Magical",
        "home_magical_tile",
    ):
        focus_library_category("Magical")
        st.rerun()

    brain_col, spacer_col = st.columns([1, 3])
    brain_button = "Continue to Quiz" if latest_story else "Create a Story"
    brain_text = "Open your latest story and continue reading toward quiz time." if latest_story else "Create a story first to unlock brain boost questions and quiz time."
    if render_home_feature_tile(
        brain_col,
        "🧠",
        "Brain Boost Questions",
        brain_text,
        brain_button,
        "home_brain_boost_tile",
    ):
        if latest_story:
            open_story_in_reader(latest_story["id"])
            st.rerun()
        st.session_state.screen = "✨ Create Story"
        st.rerun()

    st.markdown("#### Featured Story")
    featured_carousel()

    st.markdown(f"#### {active_category} Picks")
    if rec_rows:
        for row in rec_rows:
            c1, c2 = st.columns([2.4, 1])
            with c1:
                st.markdown(
                    f"""
                    <div class='panel'>
                        <b>{escape(row['title'])}</b><br>
                        <span style='font-size:0.9rem;'>Category: {escape(story_category_from_row(row))} • Reads: {row['read_count']} • Favorite: {'Yes' if row['favorite'] else 'No'}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c2:
                if st.button("Open Story 📖", key=f"home_reco_open_{row['id']}", use_container_width=True):
                    open_story_in_reader(row["id"])
                    st.rerun()
    else:
        st.info("No recommendations yet for this category.")


def home_screen() -> None:
    st.markdown("### 🏠 Home")
    profiles = get_profiles()

    selected_filter, profile_option_map = render_recommendation_filter(profiles)
    selected_profile = profile_option_map.get(selected_filter)

    if st.session_state.home_last_recommendation_filter != selected_filter:
        st.session_state.home_last_recommendation_filter = selected_filter
        recommended_categories = get_recommendation_seed_categories(selected_filter, profiles, profile_option_map)
        if recommended_categories:
            st.session_state.home_category_filter = recommended_categories[0]

    st.markdown("#### Categories")
    cat_cols = st.columns(len(STORY_TYPES))
    for idx, category in enumerate(STORY_TYPES):
        if cat_cols[idx].button(category, key=f"home_cat_{category}", use_container_width=True):
            st.session_state.home_category_filter = category

    active_category = st.session_state.home_category_filter
    rec_rows = get_home_recommendation_rows(
        selected_option=selected_filter,
        profiles=profiles,
        profile_option_map=profile_option_map,
        active_category=active_category,
        limit=4,
    )

    render_home_page(selected_profile, active_category, rec_rows)

    last_story = get_last_story()
    action1, action2, action3 = st.columns(3)
    if action1.button("✨ Create Story Now", key="home_create_story", use_container_width=True):
        st.session_state.screen = "✨ Create Story"
    if action2.button(
        "📚 Continue Last Story",
        key="continue_btn",
        use_container_width=True,
        disabled=last_story is None,
    ):
        if last_story:
            open_story_in_reader(last_story["id"])
            st.rerun()
    if action3.button("🌟 Add 5 Stories to Library", key="seed_library_btn", use_container_width=True):
        added = add_curated_library_stories(5)
        st.success(f"Added {added} new stories to Library.")

    if last_story:
        st.caption(f"Last story: {last_story['title']} • {last_story['story_type']} • {last_story['mode']}")
    else:
        st.caption("Create a first story to unlock quick continue reading.")

    with st.expander("Library Story Packs", expanded=False):
        h1, h2 = st.columns(2)
        if h1.button("Import 100 Story Pack", key="import_pack_one"):
            result = import_story_json_file("library_stories_100.json")
            if result["imported"] == 0 and result["skipped"] > 0:
                st.info(f"No new stories imported. {result['skipped']} titles already exist in your library.")
            else:
                st.success(f"Imported {result['imported']} stories, skipped {result['skipped']} duplicates.")
        if h2.button("Import Alternate 100 Pack", key="import_pack_two"):
            result = import_story_json_file("library_stories_100_variant2.json")
            if result["imported"] == 0 and result["skipped"] > 0:
                st.info(f"No new stories imported. {result['skipped']} titles already exist in your library.")
            else:
                st.success(f"Imported {result['imported']} stories, skipped {result['skipped']} duplicates.")

        h3, h4 = st.columns(2)
        if h3.button("Force Import 100 Pack", key="import_pack_one_force"):
            result = import_story_json_file("library_stories_100.json", allow_duplicate_titles=True)
            st.success(f"Force imported {result['imported']} stories ({result['forced']} received new titles).")
        if h4.button("Force Import Alternate 100", key="import_pack_two_force"):
            result = import_story_json_file("library_stories_100_variant2.json", allow_duplicate_titles=True)
            st.success(f"Force imported {result['imported']} stories ({result['forced']} received new titles).")

        if st.button("Import 140 Story Expansion", key="import_pack_three"):
            result = import_story_json_file("library_stories_140_wonder.json")
            if result["imported"] == 0 and result["skipped"] > 0:
                st.info(f"No new stories imported. {result['skipped']} titles already exist in your library.")
            else:
                st.success(f"Imported {result['imported']} stories, skipped {result['skipped']} duplicates.")

    if st.toggle("Soft Background Lullaby", value=False, key="kids_home_music_toggle"):
        render_music_track("Cozy Kids Lullaby")


def render_voice_tts(text: str) -> None:
    safe_text = json.dumps(text)
    html = f"""
    <div style='border-radius:16px;padding:12px;background:linear-gradient(120deg,#eef2ff,#fce7f3);border:1px solid #e9d5ff;'>
      <div style='font-weight:800;margin-bottom:8px;color:#4c1d95'>Narrator Voices</div>
      <select id='voiceStyle' style='padding:6px;border-radius:10px;border:1px solid #c4b5fd;margin-right:8px;'>
        <option>Female Storyteller</option>
        <option>Male Storyteller</option>
        <option>Fun Cartoon Voice</option>
      </select>
      <button onclick='playVoice()' style='padding:6px 10px;border:none;border-radius:999px;background:#7c3aed;color:white;font-weight:700'>Play</button>
      <button onclick='stopVoice()' style='padding:6px 10px;border:none;border-radius:999px;background:#dc2626;color:white;font-weight:700'>Stop</button>
      <div id='voiceState' style='margin-top:7px;font-size:0.85rem;color:#6d28d9'>Ready</div>
    </div>
    <script>
      const storyText = {safe_text};
      const synth = window.speechSynthesis;
      function pickVoice(style) {{
        const voices = synth.getVoices();
        if (!voices.length) return null;
        if (style.includes('Female')) {{
          return voices.find(v => /female|zira|samantha|victoria/i.test(v.name)) || voices[0];
        }}
        if (style.includes('Male')) {{
          return voices.find(v => /male|david|mark|alex/i.test(v.name)) || voices[0];
        }}
        return voices.find(v => /child|junior|google uk english female/i.test(v.name)) || voices[0];
      }}
      function playVoice() {{
        const style = document.getElementById('voiceStyle').value;
        synth.cancel();
        const u = new SpeechSynthesisUtterance(storyText);
        u.rate = style.includes('Cartoon') ? 1.08 : 0.92;
        u.pitch = style.includes('Cartoon') ? 1.35 : 1.0;
        const v = pickVoice(style);
        if (v) u.voice = v;
        document.getElementById('voiceState').textContent = 'Now speaking with ' + style;
        synth.speak(u);
      }}
      function stopVoice() {{ synth.cancel(); document.getElementById('voiceState').textContent = 'Stopped'; }}
    </script>
    """
    components.html(html, height=130, scrolling=False)


def render_quiz_panel(story: Dict[str, Any], story_id: int) -> None:
    questions = ensure_story_questions(story)
    memory_questions = questions.get("memory", [])
    understanding_questions = questions.get("understanding", [])
    thinking_questions = questions.get("thinking", [])
    best_score = int(get_setting(f"quiz_best_{story_id}", "0") or "0")
    total_attempts = int(get_setting("quiz_attempts_total", "0") or "0")
    total_points = int(get_setting("quiz_points_total", "0") or "0")
    total_possible = int(get_setting("quiz_possible_total", "0") or "0")
    overall_pct = int((100 * total_points / total_possible)) if total_possible > 0 else 0

    st.markdown("#### Brain Boost Quiz")
    st.caption("Recall, understand, and think beyond the page.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Best (This Story)", f"{best_score}/{len(memory_questions)}")
    m2.metric("Quiz Attempts", str(total_attempts))
    m3.metric("Total Points", str(total_points))
    m4.metric("Overall Accuracy", f"{overall_pct}%")

    if not memory_questions:
        st.info("This story does not have quiz questions yet. Generate a new story to unlock quiz mode.")
        return

    if st.session_state.quiz_score is not None and st.session_state.quiz_total is not None and st.session_state.quiz_story_id == story_id:
        score = st.session_state.quiz_score
        total = st.session_state.quiz_total
        message = choose_feedback_message(score, total, story.get("feedback_messages"))
        percent = int((100 * score / total)) if total else 0
        st.progress(score / total if total else 0, text=f"Latest score: {score}/{total} ({percent}%)")
        st.success(f"{message} • Latest score: {score}/{total} • Best score: {max(best_score, score)}/{total}")

        with st.expander("Review Answers", expanded=True):
            for idx, item in enumerate(memory_questions):
                selected = st.session_state.get(f"quiz_memory_{story_id}_{idx}")
                correct = item.get("answer")
                q = item.get("question", f"Memory question {idx + 1}")
                is_correct = selected == correct
                status = "Correct" if is_correct else "Try Again"
                st.markdown(f"**Q{idx + 1}. {q}**")
                st.caption(f"Your answer: {selected if selected else 'Not answered'}")
                st.caption(f"Correct answer: {correct} • {status}")

        b1, b2 = st.columns(2)
        if b1.button("Retake Quiz", key=f"retake_quiz_{story_id}"):
            st.session_state.quiz_active = True
            st.session_state.quiz_story_id = story_id
            st.session_state.quiz_score = None
            st.session_state.quiz_total = None
            for idx in range(len(memory_questions)):
                key = f"quiz_memory_{story_id}_{idx}"
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        if b2.button("Close Quiz", key=f"close_quiz_{story_id}"):
            st.session_state.quiz_active = False
            st.session_state.quiz_story_id = story_id
            st.rerun()

        with st.expander("Understanding Questions", expanded=False):
            for idx, item in enumerate(understanding_questions):
                st.markdown(f"**Q{idx + 1}. {item.get('question', '')}**")
                st.text_area("Your answer", key=f"quiz_understanding_{story_id}_{idx}", height=80)
                st.caption(f"Suggested answer: {item.get('answer', '')}")

        with st.expander("Thinking Questions", expanded=False):
            for idx, item in enumerate(thinking_questions):
                st.markdown(f"**Q{idx + 1}. {item.get('question', '')}**")
                st.text_area("Your idea", key=f"quiz_thinking_{story_id}_{idx}", height=80)
        return

    if not st.session_state.quiz_active or st.session_state.quiz_story_id != story_id:
        if st.button("Start Quiz", key=f"start_quiz_{story_id}"):
            st.session_state.quiz_active = True
            st.session_state.quiz_story_id = story_id
            st.session_state.quiz_score = None
            st.session_state.quiz_total = None
            st.rerun()
        return

    st.caption("Memory Round: choose the best answer for each question.")
    for idx, item in enumerate(memory_questions):
        options = item.get("options", [])
        if options and item.get("answer") in options:
            options = sorted(options, key=lambda _: random.random())
        st.radio(item.get("question", f"Memory question {idx + 1}"), options, key=f"quiz_memory_{story_id}_{idx}")

    submitted = st.button("Submit Quiz", key=f"submit_quiz_{story_id}")
    if submitted:
        unanswered = [idx + 1 for idx in range(len(memory_questions)) if st.session_state.get(f"quiz_memory_{story_id}_{idx}") is None]
        if unanswered:
            st.warning(f"Please answer all memory questions before submitting. Missing: {', '.join(map(str, unanswered))}")
            return

        score = 0
        for idx, item in enumerate(memory_questions):
            selected = st.session_state.get(f"quiz_memory_{story_id}_{idx}")
            if selected == item.get("answer"):
                score += 1
        total = len(memory_questions)
        st.session_state.quiz_score = score
        st.session_state.quiz_total = total
        set_setting(f"quiz_best_{story_id}", str(max(best_score, score)))
        set_setting("quiz_attempts_total", str(total_attempts + 1))
        set_setting("quiz_points_total", str(total_points + score))
        set_setting("quiz_possible_total", str(total_possible + total))
        st.rerun()


def render_scene_clip(scene_idx: int, scene: Dict[str, str], auto_scroll: bool, highlight_words: bool) -> None:
        text = scene["text"].replace("\"", "&quot;")
        dialogue = scene["dialogue"].replace("\n", "<br>")
        html = f"""
        <style>
            .scene-stage {{
                perspective: 1600px;
                padding: 10px 4px;
            }}
            .scene-book {{
                position: relative;
                transform-style: preserve-3d;
                animation: pageFlipIn .9s cubic-bezier(.2,.8,.2,1);
            }}
            .scene-wrap {{
                position: relative;
                border-radius: 24px;
                background: linear-gradient(135deg,#fff9e8,#eef2ff,#ecfeff);
                border: 1px solid rgba(255,255,255,0.95);
                padding: 18px 16px 16px 18px;
                box-shadow: 0 16px 30px rgba(48, 35, 98, 0.14);
                overflow: hidden;
            }}
            .scene-wrap:before {{
                content: '';
                position: absolute;
                inset: 0 auto 0 0;
                width: 14px;
                background: linear-gradient(180deg, rgba(255,255,255,.9), rgba(224,231,255,.95));
                box-shadow: inset -4px 0 10px rgba(99,102,241,.08);
            }}
            .page-curl {{
                position: absolute;
                top: 0;
                right: 0;
                width: 72px;
                height: 72px;
                background: linear-gradient(135deg, rgba(255,255,255,.2) 0%, rgba(255,255,255,.92) 55%, rgba(224,231,255,.98) 100%);
                clip-path: polygon(100% 0, 0 0, 100% 100%);
                box-shadow: -8px 8px 18px rgba(79,70,229,.08);
            }}
            .orb {{
                width: 16px;
                height: 16px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 7px;
                animation: bob 2.2s ease-in-out infinite;
            }}
            .content {{
                margin-top: 8px;
                max-height: 220px;
                overflow-y: auto;
                font-size: 1.05rem;
                line-height: 1.7;
                font-family: 'Nunito', sans-serif;
            }}
            .word {{ padding: 0 1px; border-radius: 4px; }}
            .hl {{ background: #fde68a; }}
            .page-footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 10px;
                color: #6d28d9;
                font-size: .88rem;
                font-weight: 700;
            }}
            @keyframes bob {{
                0%,100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-6px); }}
            }}
            @keyframes pageFlipIn {{
                0% {{ transform: rotateY(-78deg) translateX(-18px); opacity: 0; }}
                100% {{ transform: rotateY(0deg) translateX(0); opacity: 1; }}
            }}
        </style>
        <div class='scene-stage'>
            <div class='scene-book'>
                <div class='scene-wrap'>
                    <div class='page-curl'></div>
                    <div>
                        <span class='orb' style='background:#fb7185'></span>
                        <span class='orb' style='background:#60a5fa; animation-delay:-0.5s;'></span>
                        <span class='orb' style='background:#34d399; animation-delay:-1s;'></span>
                        <b>{scene['heading']}</b>
                    </div>
                    <div id='contentBox{scene_idx}' class='content'></div>
                    <div style='margin-top:8px; font-size:0.95rem; color:#4c1d95;'><b>Dialogue:</b><br>{dialogue}</div>
                    <div class='page-footer'>
                        <span>✨ Keep reading with the page buttons</span>
                        <span>Page {scene_idx + 1}</span>
                    </div>
                </div>
            </div>
        </div>
        <script>
            const source = `{text}`;
            const target = document.getElementById('contentBox{scene_idx}');
            const words = source.split(' ');
            target.innerHTML = words.map(w => `<span class='word'>${{w}}</span>`).join(' ');
            const spans = target.querySelectorAll('.word');
            let i = 0;
            const doHighlight = {str(highlight_words).lower()};
            const doScroll = {str(auto_scroll).lower()};
            if (doHighlight) {{
                const tick = setInterval(() => {{
                    if (i > 0) spans[i - 1].classList.remove('hl');
                    if (i >= spans.length) {{ clearInterval(tick); return; }}
                    spans[i].classList.add('hl');
                    if (doScroll) spans[i].scrollIntoView({{behavior:'smooth', block:'center'}});
                    i += 1;
                }}, 350);
            }}
        </script>
        """
        components.html(html, height=380, scrolling=False)


def render_page_turn_transition(next_scene_number: int) -> None:
        html = f"""
        <style>
            .page-turn-stage {{
                perspective: 1800px;
                padding: 8px 0 2px;
            }}
            .page-turn-book {{
                position: relative;
                height: 300px;
                border-radius: 24px;
                background: linear-gradient(135deg, #fefce8, #eef2ff, #fae8ff);
                box-shadow: 0 18px 34px rgba(48, 35, 98, 0.16);
                overflow: hidden;
            }}
            .page-turn-sheet {{
                position: absolute;
                inset: 0;
                transform-origin: left center;
                background: linear-gradient(135deg, #ffffff, #eef2ff 45%, #ddd6fe 100%);
                border-left: 10px solid rgba(196, 181, 253, 0.9);
                box-shadow: -12px 0 24px rgba(99, 102, 241, 0.12) inset;
                animation: turnPage .78s cubic-bezier(.22,.8,.2,1) forwards;
            }}
            .page-turn-copy {{
                position: absolute;
                inset: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                gap: 10px;
                color: #4c1d95;
                font-family: 'Quicksand', sans-serif;
                font-weight: 700;
                z-index: 2;
            }}
            .page-turn-copy strong {{
                font-size: 1.5rem;
            }}
            @keyframes turnPage {{
                0% {{ transform: rotateY(0deg); opacity: 1; }}
                35% {{ transform: rotateY(-32deg); opacity: 1; }}
                100% {{ transform: rotateY(-88deg) translateX(-14px); opacity: 0.9; }}
            }}
        </style>
        <div class='page-turn-stage'>
            <div class='page-turn-book'>
                <div class='page-turn-copy'>
                    <div>✨ Turning the page...</div>
                    <strong>Page {next_scene_number}</strong>
                </div>
                <div class='page-turn-sheet'></div>
            </div>
        </div>
        """
        components.html(html, height=320, scrolling=False)


def create_story_screen() -> None:
    st.markdown("### ✨ Create Story")

    profiles = get_profiles()
    profile_map = {f"{p['avatar']} {p['child_name']} ({p['age_group']})": p for p in profiles}

    with st.expander("Child Profile", expanded=True):
        c1, c2 = st.columns([1.4, 1])
        with c1:
            selected_profile_label = st.selectbox("Select existing profile", options=["None"] + list(profile_map.keys()))
        with c2:
            if st.button("Add New Profile"):
                st.session_state["show_new_profile"] = True

        if st.session_state.get("show_new_profile", False):
            np1, np2, np3, np4 = st.columns([1.2, 1, 0.8, 0.7])
            new_name = np1.text_input("Child name", key="new_profile_name")
            new_age = np2.selectbox("Age", AGE_GROUPS, key="new_profile_age")
            new_avatar = np3.selectbox("Avatar", ["⭐", "🦊", "🐻", "🦄", "🚀", "👑"], key="new_profile_avatar")
            if np4.button("Save", key="save_profile"):
                if new_name.strip():
                    create_profile(new_name.strip(), new_age, new_avatar)
                    st.success("Profile saved")
                    st.session_state["show_new_profile"] = False
                    st.rerun()

    selected_profile = None if selected_profile_label == "None" else profile_map[selected_profile_label]

    rec = get_recommendations(selected_profile["id"] if selected_profile else None)
    st.info(f"Recommended categories: {', '.join(rec)}")

    col1, col2, col3 = st.columns(3)
    with col1:
        child_name = st.text_input("Child name", value=selected_profile["child_name"] if selected_profile else "Lily")
        default_difficulty = difficulty_label_from_age(selected_profile["age_group"]) if selected_profile else "Medium (5-8)"
        difficulty_label = st.selectbox("Difficulty level", list(DIFFICULTY_OPTIONS.keys()), index=list(DIFFICULTY_OPTIONS.keys()).index(default_difficulty))
        age_group = DIFFICULTY_OPTIONS[difficulty_label]
        story_type = st.selectbox("Category", STORY_TYPES, key="custom_story_type_select")
        
        # Play sound when category changes
        previous_story_type = st.session_state.get("previous_story_type", None)
        if story_type != previous_story_type:
            if story_type in CATEGORY_SOUNDS:
                play_sound(CATEGORY_SOUNDS[story_type], f"{story_type}_sound")
            st.session_state.previous_story_type = story_type

    with col2:
        mode = st.radio("Story mode", STORY_MODES)
        # Play sound when mode changes
        previous_mode = st.session_state.get("previous_story_mode", None)
        if mode != previous_mode:
            if mode in MODE_SOUNDS:
                play_sound(MODE_SOUNDS[mode], f"{mode}_sound")
            st.session_state.previous_story_mode = mode
            
        moral = st.selectbox("Moral", MORAL_OPTIONS, key="custom_moral_select")
        # Play sound when moral changes
        previous_moral = st.session_state.get("previous_moral", None)
        if moral != previous_moral:
            if moral in MORAL_SOUNDS:
                play_sound(MORAL_SOUNDS[moral], f"{moral}_sound")
            st.session_state.previous_moral = moral
            
        location = st.selectbox("Location", LOCATION_OPTIONS, key="custom_location_select")
        # Play sound when location changes
        previous_location = st.session_state.get("previous_location", None)
        if location != previous_location:
            if location in LOCATION_SOUNDS:
                play_sound(LOCATION_SOUNDS[location], f"{location}_sound")
            st.session_state.previous_location = location

    with col3:
        characters = st.multiselect("Characters", CHARACTER_OPTIONS, default=["Animals", "Kids"])
        use_ai = st.toggle("Use AI provider")
        api_provider = st.selectbox("Provider", ["Local Magic Engine", "OpenAI", "Mistral"], disabled=not use_ai)

    voice_note = st.audio_input("Voice input option (optional): record custom guidance")
    if voice_note is not None:
        st.caption("Voice note recorded. You can transcribe this into prompt guidance.")

    with st.expander("Advanced AI Settings"):
        api_key = st.text_input("API key", type="password", disabled=not use_ai)
        model = st.text_input("Model", value="gpt-4o-mini", disabled=not use_ai)
        image_model = st.text_input("Image model", value="gpt-image-1", disabled=not use_ai)
        make_scene_images = st.toggle("Generate scene images", value=True)

    if voice_note is not None:
        t1, t2 = st.columns([1, 2])
        if t1.button("Transcribe Voice Note", disabled=not use_ai or api_provider != "OpenAI"):
            with st.spinner("Transcribing voice note..."):
                transcript = transcribe_voice_note_openai(api_key=api_key, audio_file=voice_note)
            if transcript:
                st.session_state.voice_guidance = transcript
                st.success("Voice note transcribed successfully.")
            else:
                st.warning("Could not transcribe the voice note. Check API key/provider.")
        if st.session_state.voice_guidance:
            t2.text_area("Voice guidance transcript", value=st.session_state.voice_guidance, height=100)

    max_scene_limit = int(get_setting("max_scenes", "6") or "6")
    difficulty = get_auto_difficulty(age_group, selected_profile["id"] if selected_profile else None)

    if st.button("Generate Premium Story", key="generate_story_btn"):
        if not characters:
            st.warning("Please select at least one character type.")
            return

        payload = {
            "child_name": child_name.strip() or "Lily",
            "age_group": age_group,
            "story_type": story_type,
            "mode": mode,
            "characters": characters,
            "location": location,
            "moral": moral,
            "difficulty": difficulty,
            "api_provider": api_provider if use_ai else "Local Magic Engine",
            "api_key": api_key if use_ai else "",
            "model": model if use_ai else "",
            "voice_guidance": st.session_state.voice_guidance,
        }

        with st.spinner("Crafting your magical story..."):
            story = generate_story(payload)

        if len(story["scenes"]) > max_scene_limit:
            story["scenes"] = story["scenes"][:max_scene_limit]
            story["story"] = "\n\n".join(scene.get("text", "") for scene in story["scenes"])
            story["full_text"] = "\n\n".join([f"{s['heading']}\n{s['text']}\n{s['dialogue']}" for s in story["scenes"]]) + f"\n\nMoral: {story['moral']}"

        if make_scene_images:
            with st.spinner("Painting scene illustrations..."):
                provider_for_images = api_provider if use_ai else "Local Magic Engine"
                key_for_images = api_key if use_ai else ""
                story = enrich_story_with_scene_images(story, provider_for_images, key_for_images, image_model if use_ai else "")

        sid = save_story(
            profile_id=selected_profile["id"] if selected_profile else None,
            payload=story,
            story_type=story_type,
            mode=mode,
            moral=moral,
            location=location,
            characters=characters,
        )
        open_story_in_reader(sid)
        st.success("Story created and saved to library.")
        st.rerun()


def story_player_screen() -> None:
    st.markdown("### 📚 Story Player")
    sid = st.session_state.active_story_id
    if sid is None:
        st.warning("Open a story from Library or create a new one.")
        return

    row = get_story(sid)
    if not row:
        st.error("Story not found.")
        return

    mark_read(sid)
    new_story_loaded = False
    if st.session_state.live_story_id != sid or st.session_state.live_story is None:
        loaded_story = json.loads(row["content_json"])
        normalized_story = normalize_story_payload(loaded_story)
        st.session_state.live_story = normalized_story
        st.session_state.live_story_id = sid
        new_story_loaded = True
        if loaded_story != normalized_story:
            conn = db()
            conn.execute(
                "UPDATE stories SET content_json=?, content_text=? WHERE id=?",
                (json.dumps(normalized_story), normalized_story.get("full_text", ""), sid),
            )
            conn.commit()
            conn.close()
    story = st.session_state.live_story
    sync_story_reader(story, reset_index=new_story_loaded or st.session_state.current_story is None)

    total_pages = max(1, int(st.session_state.get("total_pages", 0) or 0))
    current_page_index = min(max(0, st.session_state.get("current_page_index", 0)), total_pages - 1)

    if st.session_state.page_turning and st.session_state.page_turn_target is not None:
        target_page_index = min(max(0, int(st.session_state.page_turn_target)), total_pages - 1)
        if target_page_index != current_page_index:
            st.progress((current_page_index + 1) / total_pages, text=f"Turning to page {target_page_index + 1}...")
            render_page_turn_transition(target_page_index + 1)
            time.sleep(0.36)
            st.session_state.current_page_index = target_page_index
            if st.session_state.story_pages:
                target_page = st.session_state.story_pages[target_page_index]
                st.session_state.scene_index = int(target_page.get("scene_index", target_page_index))
            st.session_state.page_turning = False
            st.session_state.page_turn_target = None
            st.rerun()
        st.session_state.page_turning = False
        st.session_state.page_turn_target = None

    st.markdown(f"## {story['title']}")
    st.caption(story.get("subtitle", ""))

    top1, top2, top3 = st.columns(3)
    with top1:
        voice_style = st.selectbox("Narrator voice style", VOICE_STYLES, key="voice_style_select")
    with top2:
        music = st.selectbox("Background music", list(MUSIC_TRACKS.keys()))
    with top3:
        sfx = st.selectbox("Sound effect", ["None"] + list(SFX_TRACKS.keys()))

    render_music_track(music)
    if sfx != "None":
        st.audio(SFX_TRACKS[sfx], format="audio/ogg")

    total_pages = max(1, int(st.session_state.get("total_pages", 0) or 0))
    current_page_index = min(max(0, st.session_state.get("current_page_index", 0)), total_pages - 1)
    pages = st.session_state.get("story_pages", [])
    current_page = pages[current_page_index] if pages else split_story_into_pages(story)[0]
    current_scene_index = int(current_page.get("scene_index", current_page_index))

    st.progress((current_page_index + 1) / total_pages, text=f"Page {current_page_index + 1} of {total_pages}")
    render_story_page(current_page, current_page_index, total_pages)
    render_navigation(sid)

    st.markdown("#### Make Your Choice")
    ch1, ch2 = st.columns([1, 1])
    if ch1.button(current_page.get("choice_a", "Choice A"), key=f"choice_a_{sid}_{current_page_index}"):
        st.session_state.choices.append({"scene": current_page_index + 1, "choice": current_page.get("choice_a", "Choice A")})
        reaction = apply_branch_choice(story, current_scene_index, current_page.get("choice_a", "Choice A"))
        st.success(f"Character reaction: {reaction}")
        st.session_state.live_story = story
        sync_story_reader(story, reset_index=False)
    if ch2.button(current_page.get("choice_b", "Choice B"), key=f"choice_b_{sid}_{current_page_index}"):
        st.session_state.choices.append({"scene": current_page_index + 1, "choice": current_page.get("choice_b", "Choice B")})
        reaction = apply_branch_choice(story, current_scene_index, current_page.get("choice_b", "Choice B"))
        st.info(f"Character reaction: {reaction}")
        st.session_state.live_story = story
        sync_story_reader(story, reset_index=False)

    if current_page_index >= total_pages - 1:
        st.success(f"The End • Moral: {story['moral']}")
        render_quiz_panel(story, sid)
        recommendation = get_next_story_recommendation(sid, row["story_type"])
        if recommendation:
            st.markdown("#### Next Story Recommendation")
            st.markdown(
                f"""
                <div class='panel'>
                    <b>{recommendation['title']}</b><br>
                    <span style='font-size:0.9rem;'>Category: {recommendation['story_type']} • Mode: {recommendation['mode']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open Recommended Story", key=f"open_reco_{recommendation['id']}"):
                open_story_in_reader(recommendation["id"])
                st.rerun()

    with st.expander("Narration Studio", expanded=False):
        render_voice_tts(story["full_text"])
        st.caption(f"Selected voice style: {voice_style}")

    if st.session_state.choices:
        with st.expander("Your Interactive Path"):
            for item in st.session_state.choices:
                st.write(f"Scene {item['scene']}: {item['choice']}")

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        if st.button("Bookmark / Favorite", key="fav_story_btn"):
            toggle_favorite(sid)
            st.rerun()
    with d2:
        st.download_button("Download TXT", data=story["full_text"], file_name="story.txt", mime="text/plain")
    with d3:
        try:
            pdf_bytes = create_pdf(story)
        except RuntimeError:
            st.button("Download PDF", key="pdf_missing_btn", disabled=True, use_container_width=True)
            st.caption("PDF export is temporarily unavailable until the PDF package is installed.")
        else:
            st.download_button("Download PDF", data=pdf_bytes, file_name="story.pdf", mime="application/pdf")
    with d4:
        share_text = f"Read this magical story: {story['title']}"
        parent_email = get_setting("parent_email", "")
        mailto = f"mailto:{parent_email}?subject={APP_NAME}%20Share&body={share_text}"
        st.link_button("Share with Parent", mailto)


def library_screen() -> None:
    st.markdown("### 🧸 Library")

    tabs = st.tabs(["Saved Stories", "Favorites", "Recently Read"])
    filters = ["all", "favorites", "recent"]

    for tab_idx, (tab, filter_name) in enumerate(zip(tabs, filters)):
        with tab:
            selected_category = st.selectbox(
                "Category filter",
                ["All Categories"] + STORY_TYPES,
                key=f"library_category_filter_{tab_idx}",
            )
            rows = list_stories(filter_name)
            if selected_category != "All Categories":
                rows = [r for r in rows if story_category_from_row(r) == selected_category]
            if not rows:
                st.info("No stories in this section yet.")
                continue

            for row in rows:
                col1, col2, col3 = st.columns([2.2, 1.1, 1])
                with col1:
                    st.markdown(
                        f"""
                        <div class='panel'>
                            <b>{row['title']}</b><br>
                            <span style='font-size:0.85rem;'>Type: {row['story_type']} • Mode: {row['mode']} • Moral: {row['moral']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col2:
                    st.caption(f"Reads: {row['read_count']} | Favorite: {'Yes' if row['favorite'] else 'No'}")
                    st.caption(f"Created: {row['created_at']}")
                with col3:
                    if st.button("Open Story 📖", key=f"open_{filter_name}_{row['id']}"):
                        open_story_in_reader(row["id"])
                        st.rerun()
                    if st.button("Favorite ⭐", key=f"fav_{filter_name}_{row['id']}"):
                        toggle_favorite(row["id"])
                        st.rerun()


def parent_zone_screen() -> None:
    st.markdown("### 👨‍👩‍👧 Parent Zone")
    st.caption("Safe controls, customization, and insights.")

    s1, s2 = st.columns(2)
    with s1:
        parent_email = st.text_input("Parent email", value=get_setting("parent_email", ""))
        max_scenes = st.slider("Max scenes per story", min_value=3, max_value=8, value=int(get_setting("max_scenes", "6") or "6"))
    with s2:
        strict_mode = st.toggle("Strict child-safe wording", value=get_setting("strict_mode", "true") == "true")
        st.caption("When enabled, prompts stay extra gentle and age-safe.")

    if st.button("Save Parent Settings"):
        set_setting("parent_email", parent_email)
        set_setting("max_scenes", str(max_scenes))
        set_setting("strict_mode", "true" if strict_mode else "false")
        st.success("Parent settings saved.")

    st.markdown("#### Data Tools")
    if st.button("Upgrade Story JSON Schema", key="upgrade_story_schema_btn"):
        result = upgrade_story_json_schema()
        st.success(f"Schema upgrade complete. Scanned {result['scanned']} stories, upgraded {result['upgraded']} stories.")

    st.markdown("#### Library Import Tools")
    p1, p2 = st.columns(2)
    if p1.button("Load library_stories_100.json", key="parent_import_one"):
        result = import_story_json_file("library_stories_100.json")
        if result["imported"] == 0 and result["skipped"] > 0:
            st.info(f"No new stories imported. {result['skipped']} titles already exist in your library.")
        else:
            st.success(f"Imported {result['imported']} stories, skipped {result['skipped']} duplicates.")
    if p2.button("Load library_stories_100_variant2.json", key="parent_import_two"):
        result = import_story_json_file("library_stories_100_variant2.json")
        if result["imported"] == 0 and result["skipped"] > 0:
            st.info(f"No new stories imported. {result['skipped']} titles already exist in your library.")
        else:
            st.success(f"Imported {result['imported']} stories, skipped {result['skipped']} duplicates.")
    if st.button("Load library_stories_140_wonder.json", key="parent_import_three"):
        result = import_story_json_file("library_stories_140_wonder.json")
        if result["imported"] == 0 and result["skipped"] > 0:
            st.info(f"No new stories imported. {result['skipped']} titles already exist in your library.")
        else:
            st.success(f"Imported {result['imported']} stories, skipped {result['skipped']} duplicates.")

    p3, p4 = st.columns(2)
    if p3.button("Force Load 100.json", key="parent_import_one_force"):
        result = import_story_json_file("library_stories_100.json", allow_duplicate_titles=True)
        st.success(f"Force imported {result['imported']} stories ({result['forced']} received new titles).")
    if p4.button("Force Load 100_variant2.json", key="parent_import_two_force"):
        result = import_story_json_file("library_stories_100_variant2.json", allow_duplicate_titles=True)
        st.success(f"Force imported {result['imported']} stories ({result['forced']} received new titles).")

    st.markdown("#### Behavior Insights")
    rows = list_stories("all")
    if not rows:
        st.info("Insights appear after a few stories are created.")
        return

    type_counts: Dict[str, int] = {}
    for row in rows:
        type_counts[row["story_type"]] = type_counts.get(row["story_type"], 0) + 1

    st.bar_chart(type_counts)

    st.markdown("#### Quiz Insights")
    attempts = int(get_setting("quiz_attempts_total", "0") or "0")
    points = int(get_setting("quiz_points_total", "0") or "0")
    possible = int(get_setting("quiz_possible_total", "0") or "0")
    accuracy = int((100 * points / possible)) if possible > 0 else 0
    q1, q2, q3 = st.columns(3)
    q1.metric("Total Quiz Attempts", str(attempts))
    q2.metric("Points Earned", f"{points}/{possible}" if possible > 0 else "0/0")
    q3.metric("Average Accuracy", f"{accuracy}%")


def main() -> None:
    init_db()
    seed_library_if_empty()
    init_state()
    style_app(st.session_state.platform_mode)
    render_header(st.session_state.platform_mode)
    screen_nav()

    if st.session_state.platform_mode == "real_estate":
        if st.session_state.screen == "🏢 Home":
            real_estate_home_screen()
        elif st.session_state.screen == "🔍 Properties":
            real_estate_properties_screen()
        elif st.session_state.screen == "📈 Investments":
            real_estate_investments_screen()
        elif st.session_state.screen == "🤝 Contact":
            real_estate_contact_screen()
        return

    if st.session_state.screen == "🏠 Home":
        home_screen()
    elif st.session_state.screen == "✨ Create Story":
        create_story_screen()
    elif st.session_state.screen == "📚 Story Player":
        story_player_screen()
    elif st.session_state.screen == "🧸 Library":
        library_screen()
    elif st.session_state.screen == "👨‍👩‍👧 Parent Zone":
        parent_zone_screen()


if __name__ == "__main__":
    main()
