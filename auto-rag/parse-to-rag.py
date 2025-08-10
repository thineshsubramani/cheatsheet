#!/usr/bin/env python3
"""
Convert cheatsheet YAML files into RAG-friendly JSON chunks.
This will be used to advanced my cheat-cli.
"""

import yaml
import json
import hashlib
from pathlib import Path


def sha(text: str) -> str:
    """Generate short SHA256 hash for unique IDs."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def clean_aliases(aliases):
    """Normalize aliases: lowercase, deduplicate."""
    if not aliases:
        return []
    return sorted(set(a.strip().lower() for a in aliases if a.strip()))


def parse_yaml_commands(path: Path):
    """Parse a YAML cheatsheet into RAG-friendly chunks."""
    topic = path.stem  # e.g. linux.yaml → linux
    topic_parent = path.parent.name  # folder name (e.g. linux)
    entries = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(entries, list):
        return []

    chunks = []
    for entry in entries:
        group = entry.get("name", "").strip()
        aliases = clean_aliases(entry.get("alias", []))
        desc = entry.get("description", "").strip()
        syntax = entry.get("syntax", "")

        if not syntax or not group:
            continue

        # Syntax can be block string or inline
        if isinstance(syntax, str):
            lines = syntax.split("\n")
        else:
            continue  # skip malformed

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "#" in line:
                cmd, comment = line.split("#", 1)
                cmd, comment = cmd.strip(), comment.strip()
            else:
                cmd, comment = line, ""

            # Self-contained content for embeddings
            text_block = (
                f"Topic: {topic_parent}\n"
                f"Group: {group}\n"
                f"Command: {cmd}\n"
                f"Explanation: {comment}\n"
                f"Description: {desc}\n"
                f"Aliases: {', '.join(aliases)}\n"
                f"Source: topics/{topic_parent}/{topic}.yaml"
            )

            chunks.append({
                "id": sha(text_block + str(path)),
                "topic": topic_parent,
                "group": group,
                "aliases": aliases,
                "command": cmd,
                "comment": comment,
                "description": desc,
                "content": text_block,
                "tags": [topic_parent, group] + aliases,
                "source_file": f"topics/{topic_parent}/{topic}.yaml"
            })
    return chunks


def build_rag_dataset(root_dir: Path, output_file: Path):
    """Walk topics/ and convert all YAML files into a single JSON dataset."""
    all_chunks = []
    topics_dir = root_dir / "/home/thinesh40/development/go/custom_packages/cheatsheet/topics"

    for yaml_file in topics_dir.rglob("*.yaml"):
        chunks = parse_yaml_commands(yaml_file)
        all_chunks.extend(chunks)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed {len(all_chunks)} chunks from {topics_dir}")
    print(f"💾 Saved dataset to {output_file}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    output_path = repo_root / "rag_dataset.json"
    build_rag_dataset(repo_root, output_path)
