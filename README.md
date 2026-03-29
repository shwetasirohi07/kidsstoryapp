# StorySpark Premium

StorySpark Premium is a professional-grade kids storytelling app built with Streamlit.
It combines interactive storytelling, parent-safe controls, audio narration, personalization, and a polished UI.

## Highlights

- Intelligent story generation with:
  - Child name and age group (3-5, 6-8, 9-12)
  - Story type (Adventure, Moral, Fantasy, Bedtime, Funny, Educational)
  - Story mode (Quick Story, Bedtime Story, Adventure Mode, Learn & Grow)
  - Characters, location, and moral selection
- Structured stories with beginning, conflict, resolution, dialogue, and clear moral
- Interactive choices per scene with tap-to-continue flow
- Interactive branching outcomes where choices dynamically alter upcoming scenes
- Story screens:
  - Home
  - Create Story
  - Story Player
  - Library (saved, favorites, recently read)
  - Parent Zone
- Voice and audio features:
  - Browser TTS narrator controls
  - Voice style selection (female, male, cartoon)
  - OpenAI voice-note transcription (speech-to-text)
  - Background music options
  - Sound effects
- Scene image generation:
  - AI-generated scene images (OpenAI Images API)
  - Automatic placeholder illustrations when AI image generation is unavailable
- Personalization:
  - Child profiles
  - Recommendation hints from reading behavior
  - Automatic difficulty adaptation
- Storage and sharing:
  - SQLite local storage
  - Save stories, favorites, reading history
  - Download TXT and PDF
  - Share with parent via email link
- Visual polish:
  - Gradient UI
  - Rounded cards/buttons
  - Sparkles and animated scene cards
  - Mobile-friendly responsive layout

## Tech Stack

- Python 3.10+
- Streamlit
- SQLite (local persistence)
- Requests (AI API calls)
- FPDF2 (PDF export)

## Optional AI Providers

The app supports these providers in the Story Creation screen:

- OpenAI
- Mistral
- Local Magic Engine fallback (default, no key required)

If API call fails or key is missing, the app automatically falls back to local generation.

## Run Locally

1. Create and activate virtual environment.

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Start the app.

```bash
streamlit run app.py
```

## Deployment (Streamlit Community Cloud)

1. Push this project to GitHub.
2. In Streamlit Community Cloud, create a new app from the repo.
3. Set entrypoint to `app.py`.
4. Add secrets if using AI APIs.

Example secrets:

```toml
OPENAI_API_KEY = "your_key_here"
MISTRAL_API_KEY = "your_key_here"
```

## Deployment (Render)

This repository already includes `Procfile` and `render.yaml`.

1. Connect repo in Render.
2. Ensure build command installs `requirements.txt`.
3. Start command should run Streamlit app.

Example start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## Notes

- Voice input recording is available in the creation flow and can be extended with speech-to-text APIs.
- Voice input transcription is supported with OpenAI audio transcription when API key is provided.
- All data is stored locally in `storyspark.db`.

## License

MIT
