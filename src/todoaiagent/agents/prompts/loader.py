import os
from pathlib import Path

import yaml
from typing import Dict


from todoaiagent.config import LLMSettings


def load_prompt_yaml(path: str) -> Dict:
    file = Path(path)
    content = yaml.safe_load(file.read_text(encoding="utf-8"))
    return content


def build_todo_chat_messages(settings: LLMSettings) -> list[dict]:
    base = os.path.join(settings.prompt.prompt_dir, settings.prompt.system_prompt_file)
    doc = load_prompt_yaml(base)
    messages = []
    for m in doc.get("messages", []):
        # Todo: create logic to extract further linked files in the .yaml files for few shot examples
        # read raw text
        raw = ""
        if "content" in m:
            raw = m.get("content")

        messages.append({"role": m["role"], "content": raw})

    return messages
