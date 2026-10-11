from pathlib import Path

from cracklife.generator import generate_quest, load_journal_entries, save_journal_entry


def test_generate_quest_returns_expected_structure():
    quest = generate_quest(
        location_type="sidewalk",
        nature_focus="pollinators",
        duration=20,
        difficulty="easy",
    )

    assert quest["title"]
    assert len(quest["tasks"]) == 3
    assert quest["reflection"]
    assert quest["safety"]
    assert quest["source"] in {"ollama", "fallback"}


def test_journal_round_trip(tmp_path):
    journal_path = tmp_path / "journal.json"
    entry = {
        "title": "Patch of moss",
        "location": "Back alley",
        "notes": "Observed moss under a bench.",
        "nature_focus": "moss",
    }

    save_journal_entry(entry, journal_path)
    entries = load_journal_entries(journal_path)

    assert len(entries) == 1
    assert entries[0]["title"] == "Patch of moss"
