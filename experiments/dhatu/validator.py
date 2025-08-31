#!/usr/bin/env python3
"""
Minimal Dhātu experiment harness:
- Loads inventory, toy corpus, and gold encodings
- Reports simple metrics: coverage and average length
"""
from __future__ import annotations
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def load_json(name: str):
    with open(os.path.join(HERE, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def list_sentences(corpus):
    for s in corpus["sentences"]:
        print(f"{s['id']:<10} [{s['lang']}] {s['text']}")

def compute_metrics(corpus, gold):
    total = len(corpus["sentences"])
    gold_ids = set(gold.keys())
    corpus_ids = {s["id"] for s in corpus["sentences"]}
    covered = len(corpus_ids & gold_ids)
    lengths = [len(gold[sid]) for sid in gold_ids if sid in corpus_ids]
    avg_len = sum(lengths)/len(lengths) if lengths else 0.0
    return {
        "sentences": total,
        "covered": covered,
        "coverage_rate": round(covered/total, 3) if total else 0.0,
        "avg_primitives_per_encoding": round(avg_len, 3)
    }

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true", help="List toy corpus sentences")
    p.add_argument("--metrics", action="store_true", help="Print simple metrics from gold encodings")
    args = p.parse_args(argv)

    corpus = load_json("toy_corpus.json")
    gold = load_json("gold_encodings.json")
    _inv = load_json("inventory_v0_1.json")  # reserved for future validation

    if args.list:
        list_sentences(corpus)
    if args.metrics:
        m = compute_metrics(corpus, gold)
        print(json.dumps(m, ensure_ascii=False, indent=2))
    if not args.list and not args.metrics:
        p.print_help()

if __name__ == "__main__":
    sys.exit(main())
