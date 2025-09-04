#!/usr/bin/env python3
"""
Minimal Dhātu experiment harness:
- Loads inventory, toy corpus, and gold encodings
- Reports simple metrics: coverage and average length
- Typological sample support (child-directed-first): list languages and sources
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

def compute_child_metrics(lang_codes):
    """Compute coverage/avg length for child prompts using gold_encodings_child.json."""
    gold_path = os.path.join(HERE, "gold_encodings_child.json")
    if not os.path.exists(gold_path):
        raise FileNotFoundError(gold_path)
    # Handle empty or invalid JSON gracefully by treating as empty mapping
    gold: dict
    try:
        if os.path.getsize(gold_path) == 0:
            gold = {}
        else:
            with open(gold_path, "r", encoding="utf-8") as f:
                gold = json.load(f)
            if gold is None:
                gold = {}
    except json.JSONDecodeError:
        # Print a lightweight notice to stderr and continue with empty annotations
        print(f"[warn] gold_encodings_child.json is empty or invalid JSON; proceeding with empty annotations", file=sys.stderr)
        gold = {}
    from collections import defaultdict
    out = {}
    for lc in lang_codes:
        data = load_child_prompts(lc)
        ids = [it["id"] for it in data.get("items", [])]
        covered = [gid for gid in ids if gid in gold]
        lengths = [len(gold[gid]) for gid in covered]
        out[lc] = {
            "sentences": len(ids),
            "covered": len(covered),
            "coverage_rate": round(len(covered)/len(ids), 3) if ids else 0.0,
            "avg_primitives_per_encoding": round(sum(lengths)/len(lengths), 3) if lengths else 0.0
        }
    return out

def list_typological_sample(sample):
    print(f"Typological sample v{sample.get('version')} priority={sample.get('priority')}")
    for lang in sample.get("languages", []):
        name = lang.get("name")
        iso = lang.get("iso639_3")
        fam = lang.get("family")
        prof = ", ".join(lang.get("profile", []))
        print(f"- {name} ({iso}) :: {fam} :: {prof}")
        for src in lang.get("child_sources", []):
            print(f"    • {src['type']}: {src['name']} -> {src['url']}")

def load_child_prompts(lang_code: str):
    path = os.path.join(HERE, "prompts_child", f"{lang_code}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_child_prompts(lang_code: str):
    data = load_child_prompts(lang_code)
    print(f"Child prompts [{data.get('lang')}]: {len(data.get('items', []))} items")
    for it in data.get("items", []):
        ph = ",".join(it.get("phenomena", []))
        print(f"- {it['id']}: {it['text']}  [{ph}]")

def aggregate_phenomena(lang_codes):
    from collections import Counter
    cnt = Counter()
    for lc in lang_codes:
        data = load_child_prompts(lc)
        for it in data.get("items", []):
            for ph in it.get("phenomena", []):
                cnt[ph] += 1
    return cnt

def list_available_child_langs():
    base = os.path.join(HERE, "prompts_child")
    langs = []
    if os.path.isdir(base):
        for fn in os.listdir(base):
            if fn.endswith(".json") and fn not in ("schema.json",):
                langs.append(os.path.splitext(fn)[0])
    print("Available child prompt languages:", ", ".join(sorted(langs)))

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true", help="List toy corpus sentences")
    p.add_argument("--metrics", action="store_true", help="Print simple metrics from gold encodings")
    p.add_argument("--list-sample", action="store_true", help="List typological sample languages and child-directed sources")
    p.add_argument("--list-child", metavar="LANG", help="List child-directed prompts for a language code (fr|en|…)")
    p.add_argument("--list-child-langs", action="store_true", help="List available child prompt languages")
    p.add_argument("--phenomena", nargs="*", help="Aggregate phenomena counts across child prompts for LANG codes (default: all child languages)")
    p.add_argument("--child-metrics", nargs="*", help="Compute metrics for child prompts using gold_encodings_child.json (default: fr en)")
    args = p.parse_args(argv)

    corpus = load_json("toy_corpus.json")
    gold = load_json("gold_encodings.json")
    _inv = load_json("inventory_v0_1.json")  # reserved for future validation
    sample = load_json("typological_sample.json")

    if args.list:
        list_sentences(corpus)
    if args.metrics:
        m = compute_metrics(corpus, gold)
        print(json.dumps(m, ensure_ascii=False, indent=2))
    if args.list_sample:
        list_typological_sample(sample)
    if args.list_child:
        list_child_prompts(args.list_child)
    if args.list_child_langs:
        list_available_child_langs()
    if args.phenomena is not None:
        if args.phenomena:
            langs = args.phenomena
        else:
            base = os.path.join(HERE, "prompts_child")
            langs = [os.path.splitext(fn)[0] for fn in os.listdir(base) if fn.endswith('.json') and fn != 'schema.json']
        cnt = aggregate_phenomena(langs)
        print(json.dumps(cnt.most_common(), ensure_ascii=False, indent=2))
    if args.child_metrics is not None:
        langs = args.child_metrics if args.child_metrics else ["fr", "en"]
        print(json.dumps(compute_child_metrics(langs), ensure_ascii=False, indent=2))
    if not args.list and not args.metrics and not args.list_sample and not args.list_child and not args.list_child_langs and args.phenomena is None and args.child_metrics is None:
        p.print_help()

if __name__ == "__main__":
    sys.exit(main())
