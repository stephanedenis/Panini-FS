#!/usr/bin/env python3
import os
import subprocess
import time
from datetime import datetime, timezone
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
RESEARCH_DIR = os.path.join(ROOT, 'RESEARCH')
OUTPUT_DIR = os.path.join(ROOT, 'docs', 'research')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'feed.xml')
SITE_URL = os.environ.get('SITE_URL', 'https://paninifs.org')

def run(cmd):
    return subprocess.check_output(cmd, cwd=ROOT, text=True)

def isoformat(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %z')

def main():
    if not os.path.isdir(RESEARCH_DIR):
        print('No RESEARCH/ directory; skipping RSS generation')
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Collect recent commits touching RESEARCH (last 30 days, max 50)
    try:
        if os.path.isdir(os.path.join(RESEARCH_DIR, '.git')):
            # Submodule: query inside RESEARCH
            log = subprocess.check_output([
                'git', '-C', RESEARCH_DIR, 'log', '--since=30 days ago', '--max-count=200',
                '--name-only', '--pretty=%H%x09%ct%x09%s'
            ], text=True)
        else:
            # In-tree folder
            log = run(['git', 'log', '--since=30 days ago', '--max-count=200', '--name-only', '--pretty=%H%x09%ct%x09%s', 'RESEARCH'])
    except subprocess.CalledProcessError:
        log = ''

    items = []
    current = None
    for line in log.splitlines():
        if '\t' in line and len(line.split('\t')) >= 3 and line.split('\t')[0].strip():
            sha, ts, subject = line.split('\t', 2)
            current = {
                'sha': sha.strip(),
                'ts': int(ts.strip()),
                'subject': subject.strip(),
                'files': []
            }
            items.append(current)
        elif line.strip().startswith('RESEARCH/') and current is not None:
            current['files'].append(line.strip())

    # Deduplicate by sha and limit
    seen = set()
    unique_items = []
    for it in items:
        if it['sha'] in seen:
            continue
        seen.add(it['sha'])
        unique_items.append(it)
        if len(unique_items) >= 50:
            break

    now_http = isoformat(time.time())
    rss_items = []
    for it in unique_items:
        title = escape(it['subject'] or 'Update in RESEARCH')
        pub_date = isoformat(it['ts'])
        # Link to research overview as landing; guid as commit sha
        link = f"{SITE_URL}/research/overview/"
        description = escape("\n".join(it['files']) if it['files'] else 'Changes in RESEARCH/')
        guid = it['sha']
        rss_items.append(f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{description}</description>
    </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>PaniniFS — RESEARCH updates</title>
    <link>{SITE_URL}/research/overview/</link>
    <description>Latest changes in RESEARCH/ (last 30 days)</description>
    <language>fr</language>
    <lastBuildDate>{now_http}</lastBuildDate>
    {''.join(rss_items)}
  </channel>
</rss>
"""

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(rss)
    print(f"Wrote RSS: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
