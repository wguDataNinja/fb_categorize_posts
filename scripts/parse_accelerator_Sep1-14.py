#!/usr/bin/env python3
# scripts/parse_long.py
import re, json, argparse, sys
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from bs4 import BeautifulSoup

def read_html(p):
    with open(p, "r", encoding="utf-8") as f: return f.read()
def txt(el):
    return el.get_text(" ", strip=True) if el else None

def uid_from(h):
    if not h: return None
    m = re.search(r'/user/(\d+)/', h) or re.search(r'profile\.php\?id=(\d+)', h)
    return m.group(1) if m else None

# page-wide name index (uid -> best name)
GENERIC = {"profile","view profile","view story"}
def clean_name(s):
    if not s: return ""
    s = re.sub(r',?\s*view story$', '', s, flags=re.I).strip()
    return "" if s.lower() in GENERIC else s
def build_profile_index(soup):
    idx={}
    for a in soup.select('a[href^="/groups/"][href*="/user/"], a[href^="/profile.php?id="]'):
        uid = uid_from(a.get("href",""))
        if not uid: continue
        name = clean_name(txt(a) or a.get("aria-label",""))
        if not name: continue
        if uid not in idx or len(name) > len(idx[uid]): idx[uid] = name
    return idx

# story cleanup (optional; often missing in saved HTML)
KEEP_Q = {"story_fbid","id"}
def simplify_story(href):
    if not href: return None
    href = re.sub(r"^https?://[^/]+", "", href)
    u = urlparse(href)
    q = {k:v for k,v in parse_qsl(u.query, keep_blank_values=True) if k in KEEP_Q and v}
    return re.sub(r'[?&]+$', '', urlunparse(u._replace(query=urlencode(q, doseq=True))))

BAD = {"facebook","like","reply","share","view story","see more"}
def extract_message_text(msg_block, min_chars):
    cands=[]
    for sel in ('[dir="auto"]','span[dir="auto"]','div[dir="auto"]','p'):
        for el in msg_block.select(sel):
            s=txt(el)
            if not s: continue
            sl=s.lower().strip()
            if sl in BAD or re.fullmatch(r'(reply|see more)', sl, flags=re.I): continue
            if len(s) < min_chars: continue
            cands.append(s)
    if not cands:
        s=txt(msg_block)
        if s and s.lower().strip() not in BAD and len(s)>=min_chars: cands=[s]
    if not cands: return None
    return re.sub(r'\s*…\s*See more\s*$', '', max(cands, key=len), flags=re.I)

def is_profile_a(a):
    h=a.get("href","")
    return h.startswith("/profile.php?id=") or (h.startswith("/groups/") and "/user/" in h)

def find_uid_near(msg, max_up=8, max_sib=12):
    # scan nearby siblings first (headers are usually next/prev), then ancestors
    # prev siblings
    sib=getattr(msg,'previous_sibling',None); steps=0
    while sib and steps<max_sib:
        steps+=1
        if getattr(sib,'select',None):
            a=next((x for x in sib.select('a[href^="/"]') if is_profile_a(x)), None)
            if a: return uid_from(a.get("href",""))
        sib=getattr(sib,'previous_sibling',None)
    # next siblings
    sib=getattr(msg,'next_sibling',None); steps=0
    while sib and steps<max_sib:
        steps+=1
        if getattr(sib,'select',None):
            a=next((x for x in sib.select('a[href^="/"]') if is_profile_a(x)), None)
            if a: return uid_from(a.get("href",""))
        sib=getattr(sib,'next_sibling',None)
    # ancestors (and their early children)
    p=msg
    for _ in range(max_up):
        p=getattr(p,"parent",None)
        if not p or not getattr(p,'select',None): break
        a=next((x for x in p.select('h2 a[href^="/"], [role="heading"] a[href^="/"], a[href^="/"]') if is_profile_a(x)), None)
        if a: return uid_from(a.get("href",""))
    return None

def find_story_near(scope):
    for a in scope.select('a[href*="/posts/"], a[href*="/stories/"]'):
        h=a.get("href","")
        if "comment_id=" in h: continue
        return simplify_story(h)
    p=scope
    for _ in range(3):
        p=getattr(p,"parent",None)
        if not p: break
        for a in p.select('a[href*="/posts/"], a[href*="/stories/"]'):
            h=a.get("href","")
            if "comment_id=" in h: continue
            return simplify_story(h)
    return None

def extract_posts(html, min_chars):
    soup = BeautifulSoup(html, "lxml")
    name_idx = build_profile_index(soup)

    counters = {"msg_blocks":0,"no_uid":0,"no_text":0,"with_story":0,"deduped":0}
    posts=[]

    for msg in soup.select('div[data-ad-preview="message"], div[data-ad-comet-preview="message"]'):
        counters["msg_blocks"] += 1
        uid = find_uid_near(msg)
        if not uid:
            counters["no_uid"] += 1
            continue  # treat as non-post (comments often lack nearby header)
        text = extract_message_text(msg, min_chars=min_chars)
        if not text:
            counters["no_text"] += 1
            continue
        author = name_idx.get(uid, "")
        story = find_story_near(msg)
        if story: counters["with_story"] += 1
        posts.append({"story": story, "author": author, "uid": uid, "text": text})

    # de-dupe
    seen=set(); out=[]
    for p in posts:
        key=(p["uid"], (p["text"] or "")[:200], p["story"] or "")
        if key in seen:
            counters["deduped"] += 1
            continue
        seen.add(key); out.append(p)

    return {"posts_ct": len(out), "posts": out, "inspect": counters}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html_path", nargs="?", default="/Users/buddy/Desktop/projects/fb_categorize_posts/data/fb_accelerators_sep_1-14_raw.html")
    ap.add_argument("--out", default="-")
    ap.add_argument("--min-chars", type=int, default=80, help="minimum message length to treat as a post")
    args = ap.parse_args()

    html = read_html(args.html_path)
    data = extract_posts(html, min_chars=args.min_chars)
    js = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out=="-" or args.out=="/dev/stdout": sys.stdout.write(js+"\n")
    else:
        with open(args.out,"w",encoding="utf-8") as f: f.write(js+"\n")

if __name__ == "__main__":
    main()