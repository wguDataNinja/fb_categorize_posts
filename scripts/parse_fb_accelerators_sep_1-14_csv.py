#!/usr/bin/env python3
# /Users/buddy/Desktop/projects/fb_categorize_posts/scripts/parse_to_csv.py

import os, re, csv
from bs4 import BeautifulSoup

INPUT = "/Users/buddy/Desktop/projects/fb_categorize_posts/data/fb_accelerators_sep_1-14_raw.html"
OUTPUT_DIR = "//output"

# ---------- tiny utils ----------
def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def txt(el):
    return el.get_text(" ", strip=True) if el else ""

def oneline(s):
    return re.sub(r"\s+", " ", s or "").strip()

def uid_from(href):
    if not href: return None
    m = re.search(r'/user/(\d+)/', href) or re.search(r'profile\.php\?id=(\d+)', href)
    return m.group(1) if m else None

GENERIC = {"profile", "view profile", "view story"}
def clean_name(s):
    if not s: return ""
    s = re.sub(r',?\s*view story$', "", s, flags=re.I).strip()
    return "" if s.lower() in GENERIC else s

def is_profile_a(a):
    if not a: return False
    h = a.get("href", "")
    return h.startswith("/profile.php?id=") or (h.startswith("/groups/") and "/user/" in h)

# ---------- page-wide index ----------
def build_profile_index(soup):
    idx = {}  # uid -> best name
    for a in soup.select('a[href^="/groups/"][href*="/user/"], a[href^="/profile.php?id="]'):
        uid = uid_from(a.get("href",""))
        if not uid: continue
        name = clean_name(txt(a) or a.get("aria-label",""))
        if not name: continue
        if uid not in idx or len(name) > len(idx[uid]):
            idx[uid] = name
    return idx

# ---------- nearest header anchor ----------
def nearest_profile_anchor(msg, max_up=8, max_sib=12):
    # previous siblings (headers often immediately before the message)
    sib = getattr(msg, "previous_sibling", None); steps = 0
    while sib and steps < max_sib:
        steps += 1
        if getattr(sib, "select", None):
            a = next((x for x in sib.select('h2 a[href^="/"], [role="heading"] a[href^="/"], a[href^="/"]') if is_profile_a(x)), None)
            if a: return a
        sib = getattr(sib, "previous_sibling", None)
    # next siblings
    sib = getattr(msg, "next_sibling", None); steps = 0
    while sib and steps < max_sib:
        steps += 1
        if getattr(sib, "select", None):
            a = next((x for x in sib.select('h2 a[href^="/"], [role="heading"] a[href^="/"], a[href^="/"]') if is_profile_a(x)), None)
            if a: return a
        sib = getattr(sib, "next_sibling", None)
    # ancestors
    p = msg
    for _ in range(max_up):
        p = getattr(p, "parent", None)
        if not p or not getattr(p, "select", None): break
        a = next((x for x in p.select('h2 a[href^="/"], [role="heading"] a[href^="/"], a[href^="/"]') if is_profile_a(x)), None)
        if a: return a
    return None

# ---------- message text ----------
BAD = {"facebook","like","reply","share","view story","see more"}
def extract_message_text(msg_block, min_chars=40):
    cands = []
    for sel in ('[dir="auto"]', 'span[dir="auto"]', 'div[dir="auto"]', 'p'):
        for el in msg_block.select(sel):
            s = txt(el)
            if not s: continue
            sl = s.lower().strip()
            if sl in BAD or re.fullmatch(r'(reply|see more)', sl, flags=re.I): continue
            if len(s) < min_chars: continue
            cands.append(s)
    if not cands:
        s = txt(msg_block)
        if s and s.lower().strip() not in BAD and len(s) >= min_chars:
            cands = [s]
    if not cands: return ""
    s = max(cands, key=len)
    return re.sub(r'\s*…\s*See more\s*$', '', s, flags=re.I)

# ---------- main ----------
def extract_username_text_pairs(html):
    soup = BeautifulSoup(html, "lxml")
    names = build_profile_index(soup)
    rows = []
    seen = set()

    for msg in soup.select('div[data-ad-preview="message"], div[data-ad-comet-preview="message"]'):
        a = nearest_profile_anchor(msg)
        uid = uid_from(a.get("href","")) if a else None
        text = extract_message_text(msg)
        if not text or not uid:
            continue
        username = names.get(uid, "") or uid or ""
        key = (uid, text[:200])
        if key in seen:
            continue
        seen.add(key)
        rows.append({"username": oneline(username), "text": oneline(text)})
    return rows

def write_csv(rows, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["username","text"])
        for r in rows:
            w.writerow([r["username"], r["text"]])

def main():
    html = read_html(INPUT)
    rows = extract_username_text_pairs(html)
    base = os.path.splitext(os.path.basename(INPUT))[0]
    out_path = os.path.join(OUTPUT_DIR, f"{base}.csv")
    write_csv(rows, out_path)
    print(f"Wrote {len(rows)} rows to {out_path}")

if __name__ == "__main__":
    main()