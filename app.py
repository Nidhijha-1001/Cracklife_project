from pathlib import Path

import streamlit as st

from cracklife.generator import DEFAULT_JOURNAL_PATH, generate_quest, load_journal_entries, save_journal_entry

st.set_page_config(page_title="CrackLife", page_icon="🌿", layout="wide")

LOCATION_OPTIONS = [
    "sidewalk",
    "park",
    "roof terrace",
    "alley",
    "community garden",
    "neighbourhood corner",
]
NATURE_OPTIONS = [
    "pollinators",
    "moss",
    "weeds",
    "birds",
    "microhabitats",
]


def render_quest(quest: dict) -> None:
    st.subheader(quest.get("title", "Urban discovery quest"))
    st.caption(
        f"Source: {quest.get('source', 'fallback')} • {quest.get('duration_minutes', 20)} minutes • {quest.get('difficulty', 'easy')}"
    )

    for index, task in enumerate(quest.get("tasks", []), start=1):
        with st.container():
            st.markdown(f"### {index}. {task.get('title', 'Observation task')}")
            st.write(task.get("description", ""))

    st.markdown("### Reflection question")
    st.info(quest.get("reflection", "Take a moment to notice what changed."))

    st.markdown("### Safety instructions")
    st.warning(quest.get("safety", "Stay on public paths and do not disturb wildlife."))


st.title("CrackLife — AI field guide to overlooked urban biodiversity")
st.markdown(
    "Build outdoor observation quests that help people notice the tiny ecosystems hiding in plain sight. "
    "The app uses open-source local inference when available and stays transparent when it falls back."
)

with st.sidebar:
    st.header("Create a quest")
    duration = st.slider("Duration (minutes)", min_value=10, max_value=60, value=25, step=5)
    location_type = st.selectbox("Location type", options=LOCATION_OPTIONS)
    difficulty = st.selectbox("Difficulty", options=["easy", "medium", "hard"])
    nature_focus = st.selectbox("Nature focus", options=NATURE_OPTIONS)

    generate_clicked = st.button("Generate quest")

    st.markdown("---")
    st.markdown("### Open-source AI")
    st.write(
        "CrackLife centers on local open-weight models through Ollama, which keeps inference on your machine "
        "and reduces dependence on proprietary cloud services."
    )
    st.markdown("### Privacy")
    st.write("Your field journal is stored locally as a JSON file on this machine, not in a remote database.")

if generate_clicked:
    quest = generate_quest(
        location_type=location_type,
        nature_focus=nature_focus,
        duration=duration,
        difficulty=difficulty,
    )
    render_quest(quest)
else:
    default_quest = generate_quest(
        location_type="sidewalk",
        nature_focus="pollinators",
        duration=20,
        difficulty="easy",
    )
    render_quest(default_quest)

st.markdown("---")

st.header("Field journal")
with st.form("journal_form"):
    title = st.text_input("Observation title")
    location = st.text_input("Observation location")
    notes = st.text_area("What did you notice?")
    focus = st.selectbox("Nature focus", options=NATURE_OPTIONS, index=0)
    submitted = st.form_submit_button("Save observation")

    if submitted:
        entry = {
            "title": title or "Urban observation",
            "location": location or "Unknown location",
            "notes": notes or "No notes recorded yet.",
            "nature_focus": focus,
        }
        save_journal_entry(entry, DEFAULT_JOURNAL_PATH)
        st.success("Observation saved to the local field journal.")

entries = load_journal_entries(DEFAULT_JOURNAL_PATH)
if not entries:
    st.info("No observations recorded yet. Save your first nature note to begin your urban field journal.")
else:
    for entry in reversed(entries):
        with st.container():
            st.markdown(f"### {entry.get('title', 'Observation')}")
            st.caption(f"Location: {entry.get('location', 'Unspecified')} • Focus: {entry.get('nature_focus', 'urban life')}")
            st.write(entry.get("notes", ""))
            st.markdown("---")

st.markdown("---")
st.header("Why open innovation matters")
st.markdown(
    "Open models let people train, inspect, and run AI locally without surrendering privacy or getting blocked by a proprietary API. "
    "For a field guide, that matters because data stays on the device and the model can be adapted for local ecosystems, low-connectivity environments, and community-led science."
)
