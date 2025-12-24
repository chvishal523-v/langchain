from __future__ import annotations

import argparse
from pathlib import Path

from content_service import summarize, extract_bullets, rewrite_tone


def read_text(args) -> str:
    if args.text:
        return args.text.strip()

    if args.file:
        p = Path(args.file)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        return p.read_text(encoding="utf-8").strip()

    raise ValueError("Provide --text or --file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="content-assistant",
        description="Day 7: LangChain Content Assistant CLI (summarize / bullets / rewrite)"
    )

    parser.add_argument(
        "--provider",
        default="gemini",
        choices=["gemini", "mistral"],
        help="Which model provider to use (default: gemini)"
    )

    parser.add_argument(
        "--mode",
        default="balanced",
        choices=["deterministic", "balanced", "creative"],
        help="Temperature policy mode (default: balanced)"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summarize", help="Summarize text (3–4 sentences)")
    p_sum.add_argument("--text", help="Input text")
    p_sum.add_argument("--file", help="Path to a .txt file")

    p_bul = sub.add_parser("bullets", help="Extract 5 bullet points")
    p_bul.add_argument("--text", help="Input text")
    p_bul.add_argument("--file", help="Path to a .txt file")

    p_rew = sub.add_parser("rewrite", help="Rewrite in a chosen tone")
    p_rew.add_argument("--tone", required=True, help="Tone (e.g., professional, casual, funny)")
    p_rew.add_argument("--text", help="Input text")
    p_rew.add_argument("--file", help="Path to a .txt file")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    text = read_text(args)

    if args.command == "summarize":
        out = summarize(text=text, provider=args.provider, mode=args.mode)
    elif args.command == "bullets":
        out = extract_bullets(text=text, provider=args.provider, mode=args.mode)
    elif args.command == "rewrite":
        out = rewrite_tone(text=text, tone=args.tone, provider=args.provider, mode=args.mode)
    else:
        raise ValueError("Unknown command")

    print("\n===== OUTPUT =====\n")
    print(out)


if __name__ == "__main__":
    main()
