import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

DEFAULT_JOURNAL_PATH = Path(__file__).resolve().parents[1] / "journal.json"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def _title_case(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("_", " ").split())


def _fallback_quest(location_type: str, nature_focus: str, duration: int, difficulty: str) -> Dict[str, Any]:
    focus_label = _title_case(nature_focus)
    location_label = _title_case(location_type)
    task_theme = {
        "pollinators": "look for insects moving between flowers and leafy gaps",
        "moss": "look for moisture-loving patches on shaded walls and street edges",
        "weeds": "look for resilient plants pushing through cracks and curb edges",
        "birds": "listen for movement and watch for signs of nesting or feeding",
        "microhabitats": "look for tiny shelters made from leaves, cracks, and debris",
    }.get(nature_focus, "observe life hidden in the margins of the city")

    tasks = [
        {
            "title": "Scan the edges",
            "description": (
                f"Spend {duration // 3} minutes walking slowly around a {location_label.lower()} and look for "
                f"the first signs of {task_theme}. Notice where light, shade, and shelter change."
            ),
        },
        {
            "title": "Record the micro habitat",
            "description": (
                f"Choose one spot that feels overlooked. Describe the surface, moisture, and nearby plants or insects. "
                f"Ask: what makes this place useful to small life in a city?"
            ),
        },
        {
            "title": "Reflect before moving on",
            "description": (
                "Pause for a moment and note whether your attention changed after noticing small life. "
                "What would you look for next time at the same time of day?"
            ),
        },
    ]

    return {
        "title": f"{focus_label} Quest: Urban {location_label}",
        "tasks": tasks,
        "reflection": (
            f"How did a small {nature_focus.replace('_', ' ')} observation change the way you read the city? What else might be living in the margins you usually ignore?"
        ),
        "safety": "Stay on public paths, do not disturb nesting animals, and avoid handling wildlife or unknown plants.",
        "source": "fallback",
        "difficulty": difficulty,
        "duration_minutes": duration,
    }


def _read_installed_models() -> List[str]:
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if response.status_code != 200:
            return []
        payload = response.json()
        models = payload.get("models", [])
        return [m.get("name", "") for m in models if isinstance(m, dict)]
    except requests.RequestException:
        return []


def _call_ollama(location_type: str, nature_focus: str, duration: int, difficulty: str) -> Optional[Dict[str, Any]]:
    installed_models = _read_installed_models()
    if not installed_models:
        return None

    model_name = next((m for m in [OLLAMA_MODEL] + installed_models if m), None)
    if not model_name:
        return None

    prompt = (
        "You are a field guide for urban biodiversity. Generate a JSON object with exactly these keys: "
        "title, tasks, reflection, safety, source, difficulty, duration_minutes. "
        "tasks must be an array of exactly 3 objects with title and description fields. "
        "Keep the output valid JSON only and no markdown fences. "
        f"Location type: {location_type}. Nature focus: {nature_focus}. Duration minutes: {duration}. Difficulty: {difficulty}. "
        "Write a vivid but safe urban nature quest that encourages noticing overlooked life outdoors."
    )

    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 400},
        }
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        text = result.get("response", "")
        if not text:
            return None
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`\n ")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].lstrip()
        parsed = json.loads(cleaned)
        if not isinstance(parsed, dict):
            return None
        parsed.setdefault("source", "ollama")
        parsed.setdefault("difficulty", difficulty)
        parsed.setdefault("duration_minutes", duration)
        if not isinstance(parsed.get("tasks"), list) or len(parsed["tasks"]) != 3:
            raise ValueError("tasks must contain 3 entries")
        return parsed
    except (ValueError, TypeError, requests.RequestException, json.JSONDecodeError):
        return None


def generate_quest(
    location_type: str,
    nature_focus: str,
    duration: int = 20,
    difficulty: str = "easy",
) -> Dict[str, Any]:
    quest = _call_ollama(location_type, nature_focus, duration, difficulty)
    if quest is not None:
        return quest
    return _fallback_quest(location_type, nature_focus, duration, difficulty)


def load_journal_entries(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    target = Path(path) if path is not None else DEFAULT_JOURNAL_PATH
    if not target.exists():
        return []
    try:
        with target.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        return []
    return []


def save_journal_entry(entry: Dict[str, Any], path: Optional[Path] = None) -> List[Dict[str, Any]]:
    target = Path(path) if path is not None else DEFAULT_JOURNAL_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    entries = load_journal_entries(target)
    entries.append(entry)
    with target.open("w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2)
    return entries
