# CrackLife

CrackLife is a local-first AI field guide for noticing the tiny ecosystems hiding in cities. It turns a short walk into a structured, safe observation quest and keeps a private field journal on the user's machine.

## Challenge fit

Verified from the official Week 1 DEV challenge page:
- Challenge: Hacktoberfest Open-Source AI Challenge: Week 1 — Touch Grass
- Submissions due: October 11, 2026 at 11:59 PM PDT
- Theme: build with open-source AI and get people outside
- Judging emphasis: writing quality, relevance to the theme, creativity, technical execution, and optional partner technology use
- Prize structure: one overall winner plus featured and partner category prizes, per the challenge page

This project fits the theme directly because it uses local open-weight AI to generate short, safety-aware outdoor quests for urban biodiversity observation.

## Strongest realistic category

The strongest realistic fit is the Best Use of Gemma category because the project is built around running open-weight AI locally and making model choice matter for privacy and control. It also aligns with the general challenge theme and can be framed as a practical field guide for urban nature observation.

## Why this project is differentiated

Instead of a generic chatbot, CrackLife turns the AI into a guided, real-world discovery tool:
- prompts users for duration, location type, difficulty, and biodiversity focus
- generates three concrete observation tasks plus a reflection prompt
- encourages careful, respectful urban observation without disturbing wildlife
- saves a private journal locally so the experience remains useful after the walk ends

## Architecture

- Frontend: Streamlit UI
- Core logic: Python app with quest generation and journal persistence
- AI layer: Ollama with an open-weight model such as Gemma or Llama, if installed locally
- Fallback behavior: transparent heuristic prompts when an open model is unavailable
- Storage: local JSON journal in the project directory

## Open-source AI rationale

The app intentionally centers local open-weight inference rather than a closed cloud-only model:
- faster iteration for offline or low-connectivity use
- better privacy because the model runs on the user’s machine
- more control over model choice, cost, and behavior
- easier explanation of why open innovation matters for real-world field work

## Run locally

1. Open a terminal in this project directory.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Start the app.

Commands:

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py

If Ollama is installed and a model is available, the app will use it automatically. If not, it falls back to a structured local prompt generator and clearly labels that state.

## Local model setup

If you want to test with a local model on macOS:

1. Install Ollama from https://ollama.com
2. Pull a supported model, for example:

ollama pull llama3.2

Then start the app and set:

export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.2

The app will use that model when it is available.

## Testing

This project includes a small Python test suite covering:
- quest generation structure
- journal saving and retrieval

Run:

python -m pytest -q

## Demo plan

1. Open the app and select a short urban walk.
2. Create a quest for pollinators or moss along a sidewalk or alley.
3. Review the three tasks and reflection question.
4. Save an observation in the journal.
5. Explain in the final write-up how open-weight local AI kept the experience private and practical outdoors.

## Files in the repository

- app.py — Streamlit interface
- cracklife/generator.py — quest generation and journal logic
- tests/test_cracklife.py — validation checks
- README.md — setup and project overview
- DEV_SUBMISSION.md — article draft for the challenge post
- assets/cracklife-cover.svg — cover image draft
- requirements.txt — Python dependencies
- LICENSE — MIT license
- .gitignore — ignores local state and temporary files

## Git workflow

Commands to initialize a Git repository and publish later:

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-url>
git push -u origin main

## Submission guidance

This repo is structured to produce a strong DEV article with:
- a working demo
- local AI explanation
- real journal use
- honest testing and limitations

Use the article draft in DEV_SUBMISSION.md as the starting point for the final DEV post.
