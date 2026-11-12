import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency for YAML files
    yaml = None

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

STATE_PATH = BASE_DIR / "state.json"
PROBLEM_PATHS = [BASE_DIR / "problems.yml", BASE_DIR / "problems.yaml"]
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

DEFAULT_PROBLEMS = [
    {
        "title": "Reto inicial",
        "prompt": "Escribe un programa que imprima 'Hola, mundo!'",
        "hints": ["Usa print()", "No olvides el salto de línea"],
        "tags": ["principiante", "salida"],
    }
]


def load_problems() -> List[Dict[str, Any]]:
    for problems_path in PROBLEM_PATHS:
        if problems_path.exists():
            if yaml is None:
                raise RuntimeError("Instala pyyaml o elimina problems.yaml")

            with problems_path.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or []

            if not isinstance(data, list):
                raise TypeError("El archivo de problemas debe contener una lista")

            return data

    return DEFAULT_PROBLEMS


def init_state(n: int) -> Dict[str, Any]:
    order = list(range(n))
    random.shuffle(order)
    return {"order": order, "pos": 0, "last_post": None}


def load_state(n: int) -> Dict[str, Any]:
    if STATE_PATH.exists():
        with STATE_PATH.open("r", encoding="utf-8") as file:
            state = json.load(file)

        if "order" not in state or len(state["order"]) != n:
            return init_state(n)

        return state

    return init_state(n)


def save_state(state: Dict[str, Any]) -> None:
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def today_iso() -> str:
    return datetime.now().date().isoformat()


def select_today(problems: List[Dict[str, Any]], state: Dict[str, Any]) -> Dict[str, Any]:
    today = today_iso()
    if state.get("last_post") == today:
        pos = state.get("pos", 0)
        idx = state["order"][(pos - 1) % len(problems)]
        return problems[idx]

    pos = state.get("pos", 0)
    idx = state["order"][pos]
    problem = problems[idx]
    state["pos"] = (pos + 1) % len(problems)
    state["last_post"] = today
    return problem


def build_message(problem: Dict[str, Any]) -> Dict[str, Any]:
    title = problem.get("title", "Reto Python")
    prompt = problem.get("prompt", "")
    hints = problem.get("hints", [])
    tags = problem.get("tags", [])

    hints_md = "\n".join(f"• {hint}" for hint in hints) if hints else "—"
    tags_md = ", ".join(tags) if tags else "principiante"

    header = f":snake: *Reto Python del día:* *{title}*"
    body = f"{prompt}\n\n*Pistas:*\n{hints_md}\n\n*Etiquetas:* `{tags_md}`"

    return {
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": header}},
            {"type": "section", "text": {"type": "mrkdwn", "text": body}},
            {"type": "divider"},
        ]
    }


def post_to_slack(payload: Dict[str, Any]) -> None:
    if not BOT_TOKEN or not CHANNEL_ID:
        raise RuntimeError("Faltan SLACK_BOT_TOKEN o SLACK_CHANNEL_ID en .env")

    client = WebClient(token=BOT_TOKEN)
    try:
        client.chat_postMessage(channel=CHANNEL_ID, **payload)
    except SlackApiError as exc:
        response = getattr(exc, "response", None)
        data = getattr(response, "data", exc)
        raise RuntimeError(f"Error Slack: {data}") from exc


def main() -> None:
    problems = load_problems()
    state = load_state(len(problems))
    prob = select_today(problems, state)
    payload = build_message(prob)
    post_to_slack(payload)
    save_state(state)
    print("Publicado:", prob["title"])


if __name__ == "__main__":
    main()
