#!/usr/bin/env python3
"""
Bulk image generation for all stories in the database.
Generates scene illustrations for stories without images.
"""
import sqlite3
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Import from app.py
import hashlib
import base64
import requests
from urllib.parse import quote_plus
from html import escape
import re

DB_PATH = "storyspark.db"
IMAGE_CACHE_DIR = Path(".image_cache")


def materialize_remote_image(image_url: str) -> Optional[str]:
    """Download and cache remote images locally."""
    if not image_url or not isinstance(image_url, str):
        return None
    
    url = str(image_url).strip()
    if url.startswith(".image_cache"):
        return url
    
    if url.startswith("/"):
        return url
        
    if not url.startswith("http"):
        return None
    
    try:
        IMAGE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        url_hash = hashlib.sha1(url.encode("utf-8")).hexdigest()
        cached_path = IMAGE_CACHE_DIR / f"{url_hash}.png"
        
        if cached_path.exists():
            return str(cached_path)
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        cached_path.write_bytes(response.content)
        return str(cached_path)
    except Exception as e:
        print(f"  Failed to download {url[:50]}... - {e}")
        return None


def generate_scene_image_url(scene_text: str, provider: str, api_key: str, model: str) -> str:
    """Generate image URL for a scene."""
    def instant_storybook_image_url(prompt_text: str) -> str:
        prompt_for_url = re.sub(r"\s+", " ", str(prompt_text or "Magical storybook scene")).strip()[:300]
        safe_prompt = quote_plus(
            (
                "Premium child-friendly painterly storybook illustration, lively characters, dynamic scene action, "
                "golden-hour cinematic light, richly colored environment, crisp details, clean linework, high clarity, no text. "
                + prompt_for_url
            )[:640]
        )
        seed = int(hashlib.sha1(str(prompt_text).encode("utf-8")).hexdigest()[:8], 16)
        return (
            f"https://image.pollinations.ai/prompt/{safe_prompt}"
            f"?width=1536&height=1024&seed={seed}&model=flux&enhance=true&nologo=true&safe=true"
        )

    if provider == "OpenAI" and api_key:
        try:
            prompt = (
                "Child-friendly storybook illustration, vibrant cinematic colors, soft but crisp lighting, "
                "high detail, sharp focus, no text. "
                f"Scene description: {scene_text}"
            )
            payload: Dict[str, Any] = {
                "model": model or "gpt-image-1",
                "prompt": prompt,
                "size": "1536x1024",
            }
            if (model or "gpt-image-1").startswith("gpt-image"):
                payload["quality"] = "high"
            res = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=45,
            )
            res.raise_for_status()
            body = res.json()
            if body.get("data"):
                first = body["data"][0] if body["data"] else {}
                if first.get("url"):
                    return str(first["url"])
                b64_image = str(first.get("b64_json", "")).strip()
                if b64_image:
                    IMAGE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    img_key = hashlib.sha1(f"{model}|{prompt}".encode("utf-8")).hexdigest()
                    img_path = IMAGE_CACHE_DIR / f"{img_key}.png"
                    if not img_path.exists():
                        img_path.write_bytes(base64.b64decode(b64_image))
                    return str(img_path)
        except Exception as e:
            print(f"  OpenAI error: {e}")
            pass

    return instant_storybook_image_url(scene_text)


def resolve_scene_image_asset(scene_text: str, provider: str, api_key: str, model: str) -> str:
    """Download and cache image asset."""
    primary_url = generate_scene_image_url(scene_text=scene_text, provider=provider, api_key=api_key, model=model)
    primary_asset = materialize_remote_image(primary_url)
    if primary_asset and Path(primary_asset).exists():
        return primary_asset

    for retry in range(1, 4):
        retry_prompt = f"{scene_text} cinematic composition variation {retry}, sharper details, richer colors"
        retry_url = generate_scene_image_url(scene_text=retry_prompt, provider=provider, api_key=api_key, model=model)
        retry_asset = materialize_remote_image(retry_url)
        if retry_asset and Path(retry_asset).exists():
            return retry_asset

    return primary_asset or primary_url


def clean_story_title(title: str, fallback: str = "") -> str:
    """Clean story title."""
    if not title:
        return fallback
    clean = str(title).strip()[:256]
    return clean or fallback


def build_lively_scene_prompt(
    story_title: str,
    scene_heading: str,
    scene_text: str,
    scene_dialogue: str,
    base_prompt: str,
) -> str:
    """Build a rich image prompt from scene data."""
    parts = [base_prompt] if base_prompt else []
    if scene_heading:
        parts.append(f"Scene: {scene_heading}")
    if scene_text:
        parts.append(f"Setting: {scene_text[:200]}")
    if scene_dialogue:
        parts.append(f"Action: {scene_dialogue[:150]}")
    return " | ".join(parts)[:1000]


def enrich_story_with_scene_images(story: Dict[str, Any], provider: str, api_key: str, image_model: str) -> Dict[str, Any]:
    """Add images to all scenes in a story."""
    scenes = story.get("scenes", [])
    story_title = clean_story_title(story.get("title", "Magical Story"), "Magical Story")
    
    for idx, scene in enumerate(scenes):
        rich_prompt = build_lively_scene_prompt(
            story_title=story_title,
            scene_heading=str(scene.get("heading", "Story scene")),
            scene_text=str(scene.get("text", "")),
            scene_dialogue=str(scene.get("dialogue", "")),
            base_prompt=str(scene.get("image_prompt", "")),
        )
        scene["image_prompt"] = rich_prompt
        if not scene.get("image_url"):
            print(f"    Generating image for scene {idx + 1}/{len(scenes)}...")
            scene["image_url"] = resolve_scene_image_asset(rich_prompt, provider, api_key, image_model)
            time.sleep(0.5)  # Rate limiting
    
    return story


def get_image_settings() -> Dict[str, str]:
    """Get image provider settings from database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT key, value FROM settings WHERE key IN ('image_provider', 'image_openai_key', 'image_model')")
    settings = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    
    provider = settings.get("image_provider", "Local Magic Engine") or "Local Magic Engine"
    openai_key = settings.get("image_openai_key", "") or ""
    image_model = settings.get("image_model", "gpt-image-1") or "gpt-image-1"
    
    if provider != "OpenAI":
        openai_key = ""
    
    return {
        "provider": provider,
        "openai_key": openai_key,
        "image_model": image_model,
    }


def bulk_generate_images(skip_if_images: bool = True, limit: Optional[int] = None) -> None:
    """Bulk generate images for all stories."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get settings
    settings = get_image_settings()
    provider = settings["provider"]
    api_key = settings["openai_key"]
    image_model = settings["image_model"]
    
    print(f"Image Generation Settings:")
    print(f"  Provider: {provider}")
    print(f"  Model: {image_model}")
    print(f"  Skip if already has images: {skip_if_images}\n")
    
    # Get all stories
    cursor.execute("SELECT id, title, content_json FROM stories ORDER BY id")
    stories = cursor.fetchall()
    
    if limit:
        stories = stories[:limit]
    
    total = len(stories)
    generated_count = 0
    skipped_count = 0
    failed_count = 0
    
    print(f"Processing {total} stories...\n")
    
    for idx, (story_id, title, content_json) in enumerate(stories, 1):
        try:
            content = json.loads(content_json)
            
            # Check if already has images
            has_images = any(
                scene.get("image_url") and scene["image_url"].strip()
                for scene in content.get("scenes", [])
            )
            
            if has_images and skip_if_images:
                print(f"[{idx}/{total}] SKIP - {title} (already has images)")
                skipped_count += 1
                continue
            
            # Generate images
            print(f"[{idx}/{total}] Generating - {title}")
            content = enrich_story_with_scene_images(content, provider, api_key, image_model)
            
            # Save back to database
            cursor.execute("UPDATE stories SET content_json=? WHERE id=?", (json.dumps(content), story_id))
            conn.commit()
            
            generated_count += 1
            print(f"  ✓ Saved\n")
            
        except json.JSONDecodeError:
            print(f"[{idx}/{total}] ERROR - {title} (invalid JSON)\n")
            failed_count += 1
        except Exception as e:
            print(f"[{idx}/{total}] ERROR - {title} ({e})\n")
            failed_count += 1
    
    conn.close()
    
    print(f"\nBulk Generation Complete:")
    print(f"  Generated: {generated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total processed: {total}")


if __name__ == "__main__":
    skip_existing = True
    limit = None
    
    if len(sys.argv) > 1 and sys.argv[1] == "--overwrite":
        skip_existing = False
        print("Running with --overwrite: will regenerate even if images exist\n")
    
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
            print(f"Running with limit: {limit} stories\n")
        except:
            pass
    
    bulk_generate_images(skip_if_images=skip_existing, limit=limit)
