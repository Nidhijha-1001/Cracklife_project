# CrackLife: an AI field guide to the tiny ecosystems hiding in cities

This is a submission for the Hacktoberfest Open-Source AI Challenge: Week 1 — Touch Grass.

## What I built

CrackLife is a local-first AI field guide that helps people notice overlooked urban biodiversity. Instead of treating the city as empty space, the app turns a short walk into a guided urban nature quest: users choose a duration, location, difficulty, and ecology focus, then receive three concrete observation tasks plus a reflection prompt.

The app was designed to encourage people to pause, look up, and notice the small ecosystems already living in sidewalks, alley edges, rooftops, gardens, and neglected corners.

## Demo link

Local demo walkthrough: run the app with Streamlit and create a short urban biodiversity quest in under a minute. A short screen recording of the flow is recommended for the final DEV submission.

Demo command:

streamlit run app.py

## GitHub repository

Repository: https://github.com/your-username/CrackLife

Replace the placeholder above with the public repo URL before final submission.

## How I built it

I built CrackLife as a lightweight Python + Streamlit app with a local-first architecture.

The app includes:
- a responsive Streamlit interface
- configurable quest generation based on location, focus, time, and difficulty
- local OpenAI-compatible inference via Ollama when a model is available
- a transparent fallback prompt system when local inference is unavailable
- a local JSON field journal for recording observations

This matters because the project is not merely a chatbot. It is a practical field guide that helps turn a short walk into real observation and reflection.

## Why open innovation matters

Open innovation is central to this project because local open-weight models make it possible to run a helpful AI system without forcing users to depend on a proprietary cloud service. For a field guide, that means better privacy, stronger control over model behavior, and more flexibility to adapt the experience for different environments and use cases.

Instead of sending every observation to a remote service, CrackLife keeps the core experience local whenever possible. That is especially valuable for people walking outdoors in areas with weak connectivity or limited privacy expectations.

## The technical architecture

- Frontend: Streamlit
- Logic layer: Python
- Model runtime: Ollama + open-weight model (Gemma or Llama when installed locally)
- Storage: local JSON file for the journal
- Fallback behavior: structured, transparent prompt generation when the model is unavailable

## What makes it different

A generic AI app might generate nature-themed text. CrackLife does something more useful: it turns the city itself into a living observation site. It asks people to notice tiny habitats, like moss under a bench, weeds in a crack, or pollinators moving between flowers. The tool is targeted at the real world rather than the chat interface.

## Testing

I validated the core logic and journal behavior with a small Python test suite, including:
- quest generation returns the required structure
- journal entries save and load correctly

Known limitation: I was not able to verify a live Ollama inference run in this environment, so the application is built to work locally when a compatible model is installed and otherwise fall back gracefully.

## Known limitations and future improvements

Future improvements could include:
- image-based observation capture
- optional voice narration for guided walks
- location-aware habitat suggestions
- more advanced biodiversity classification powered by local models

## Prize categories

This project is strongest for the general challenge theme and especially fits the Best Use of Gemma category if a local Gemma model is used during runtime. It can also be positioned as a strong open-source AI project under the broader weekly challenge.

## Agent session

Optional: include a saved DevRelay agent session link here if you use one.

## Closing note

CrackLife is small, practical, and outdoors-first. It shows how open-source AI can be used not just for chat, but for helping people pay attention to the living systems around them.
