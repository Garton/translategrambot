#!/usr/bin/env python3
"""
Script to get all available Helsinki-NLP/opus-mt translation pairs using huggingface_hub
"""

import json
from typing import Dict, List

from huggingface_hub import HfApi


def get_opus_mt_pairs() -> List[Dict]:
    """Fetch all Helsinki-NLP/opus-mt models from Hugging Face Hub."""

    api = HfApi()

    try:
        # Get all models from Helsinki-NLP organization
        print("Fetching all models from Helsinki-NLP organization...")
        models = api.list_models(author="Helsinki-NLP")

        # Filter for opus-mt models
        opus_models = []
        for model in models:
            if model.modelId.startswith("Helsinki-NLP/opus-mt"):
                opus_models.append(
                    {
                        "model_id": model.modelId,
                        "language_pair": model.modelId.replace(
                            "Helsinki-NLP/opus-mt-", ""
                        ),
                        "downloads": getattr(model, "downloads", 0),
                        "likes": getattr(model, "likes", 0),
                        "last_modified": str(getattr(model, "lastModified", "")),
                    }
                )

        print(f"Found {len(opus_models)} opus-mt models")
        return opus_models

    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def parse_language_pairs(models: List[Dict]) -> List[str]:
    """Parse language pairs from model IDs."""
    pairs = []

    for model in models:
        pair = model["language_pair"]
        # Handle different naming conventions
        if "-" in pair:
            # Format: "en-ru" or "en-ru-en"
            parts = pair.split("-")
            if len(parts) >= 2:
                source = parts[0]
                target = parts[1]
                pairs.append(f"{source}-{target}")

    return sorted(list(set(pairs)))


def main():
    print("Fetching Helsinki-NLP/opus-mt models using huggingface_hub...")
    models = get_opus_mt_pairs()

    if not models:
        print("No models found or error occurred.")
        return

    print(f"Found {len(models)} opus-mt models")

    # Get unique language pairs
    pairs = parse_language_pairs(models)
    print(f"Found {len(pairs)} unique language pairs:")

    for pair in pairs:
        print(f"  {pair}")

    # Save to file
    with open("opus_mt_pairs_hf.json", "w", encoding="utf-8") as f:
        json.dump({"models": models, "pairs": pairs}, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to opus_mt_pairs_hf.json")

    # Show Russian language pairs
    print("\nRussian language pairs:")
    sorted_models = sorted(models, key=lambda x: x["language_pair"], reverse=True)
    for model in filter(lambda x: x["language_pair"].startswith("ru-"), sorted_models):
        print(f"  {model['model_id']} - {model['downloads']} downloads")

    # Show most popular models
    print("\nMost downloaded models:")
    sorted_by_downloads = sorted(models, key=lambda x: x["downloads"], reverse=True)
    for model in sorted_by_downloads[:10]:
        print(f"  {model['model_id']} - {model['downloads']} downloads")


if __name__ == "__main__":
    main()
