#!/usr/bin/env python3
"""Pesquisa SÓ LEITURA: answers.py <site> "consulta" [-d pasta/] [-t 8]
sites: devto tabnews huggingface hackaday instructables. Stdlib; só instructables usa patchright (venv do Scrapling).
Gera pasta/<site>-top.tsv (candidatos com score) e pasta/<site>-read.md (os -t primeiros lidos, com comentários)."""
import argparse, html, json, re, sys, time, urllib.parse as up, urllib.request as ur
from pathlib import Path

q = up.quote_plus
txt = lambda h: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()
row = lambda title, url, score=0, n=0, date="", **k: dict(title=title, url=url, score=score, n=n, date=date[:10], **k)

def get(url, raw=False):
    time.sleep(1)  # ponytail: espera fixa de 1s, sem retry/backoff
    with ur.urlopen(ur.Request(url, headers={"User-Agent": "Mozilla/5.0 (answers-cli; read-only)"}), timeout=30) as f:
        return f.read().decode() if raw else json.load(f)

def devto(Q, n):  # ponytail: a API oficial não tem busca de texto; 1 tag por palavra (máx 3)
    seen = {}
    for w in Q.lower().split()[:3]:
        for a in get(f"https://dev.to/api/articles?tag={q(w)}&top=365&per_page={n}"):
            seen[a["id"]] = row(a["title"], a["url"], a["public_reactions_count"], a["comments_count"], a["published_at"], id=a["id"])
    return list(seen.values())

def devto_read(r):
    return get(f"https://dev.to/api/articles/{r['id']}")["body_markdown"], [(0, (c.get("user") or {}).get("username", "?"), txt(c["body_html"])) for c in get(f"https://dev.to/api/comments?a_id={r['id']}")]

def tabnews(Q, n):  # ponytail: sem endpoint de busca; filtra o título nas 300 mais relevantes
    ws, rows = Q.lower().split(), []
    for p in range(1, 4):
        for c in get(f"https://www.tabnews.com.br/api/v1/contents?strategy=relevant&page={p}&per_page=100"):
            hit = sum(w in (c.get("title") or "").lower() for w in ws)
            if hit: rows.append(row(c["title"], f"https://www.tabnews.com.br/{c['owner_username']}/{c['slug']}", c["tabcoins"], c["children_deep_count"], c["published_at"], hit=hit, user=c["owner_username"], slug=c["slug"]))
    return rows

def tabnews_read(r):
    b = f"https://www.tabnews.com.br/api/v1/contents/{r['user']}/{r['slug']}"
    return get(b)["body"], [(c["tabcoins"], c["owner_username"], c["body"] or "") for c in get(b + "/children")]

def huggingface(Q, n):
    rows = []
    for k in ("models", "datasets", "spaces"):
        for m in get(f"https://huggingface.co/api/{k}?search={q(Q)}&sort=likes&direction=-1&limit={n}"):
            rows.append(row(f"[{k[:-1]}] {m['id']}", f"https://huggingface.co/{'' if k == 'models' else k + '/'}{m['id']}", m.get("likes", 0), m.get("downloads", 0), m.get("lastModified") or m.get("createdAt", ""), kind=k, id=m["id"]))
    for p in get(f"https://huggingface.co/api/papers/search?q={q(Q)}")[:n]:
        rows.append(row(f"[paper] {p['title']}", f"https://huggingface.co/papers/{p['paper']['id']}", p["paper"].get("upvotes", 0), p.get("numComments", 0), p.get("publishedAt", ""), kind="papers", id=p["paper"]["id"], body=p.get("summary", "")))
    return rows

def huggingface_read(r):  # n = downloads (models/datasets) ou comentários (papers)
    if r["kind"] == "papers": return r["body"], []
    path = ("" if r["kind"] == "models" else r["kind"] + "/") + r["id"]
    try: body = get(f"https://huggingface.co/{path}/raw/main/README.md", raw=True)
    except Exception: body = ""
    try: cs = [(0, d["author"]["name"], d["title"]) for d in get(f"https://huggingface.co/api/{r['kind']}/{r['id']}/discussions")["discussions"][:10]]
    except Exception: cs = []
    return body, cs

def hackaday(Q, n):  # sem score no site: a ordem é a relevância do WordPress
    return [row(txt(p["title"]["rendered"]), p["link"], date=p["date"], id=p["id"], body=txt(p["content"]["rendered"])) for p in get(f"https://hackaday.com/wp-json/wp/v2/posts?search={q(Q)}&per_page={n}&_fields=id,link,title,date,content")]

def hackaday_read(r):
    return r["body"], [(0, c["author_name"], txt(c["content"]["rendered"])) for c in get(f"https://hackaday.com/wp-json/wp/v2/comments?post={r['id']}&per_page=30")]

def render(url, js):
    from patchright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto(url, wait_until="networkidle"); out = pg.evaluate(js); b.close(); return out

LINKS = r"""() => [...new Set([...document.querySelectorAll('a[href]')].filter(a => /^https:\/\/www\.instructables\.com\/[^\/]+$/.test(a.href)).map(a => { let e = a; for (let i = 0; i < 6 && e && !/\nby [^\n]+\n[\d.,]+K?\n[\d.,]+K?\s*$/.test(e.innerText.trim()); i++) e = e.parentElement; return e && /\nby [^\n]+\n[\d.,]+K?\n[\d.,]+K?\s*$/.test(e.innerText.trim()) && e.innerText.length < 200 ? a.href + '\t' + e.innerText.trim().replace(/\n+/g, '\t') : null; }).filter(Boolean))]"""

def num(s):  # "9.5K" -> 9500
    try: return int(float(s.rstrip("Kk")) * (1000 if s[-1] in "Kk" else 1))
    except ValueError: return 0

def instructables(Q, n):  # ponytail: a busca deles é JS e a API exige chave, então renderiza a página e lê os cards (título, autor, favoritos, views); sem comentários
    rows = []
    for x in render(f"https://www.instructables.com/search/?q={q(Q)}&projects=all", LINKS)[:n]:
        u, t, _, *rest = x.split("\t") + [""] * 5
        rows.append(row(t, u, num(rest[0]), num(rest[1])))
    return rows

def instructables_read(r):
    return render(r["url"], "() => document.body.innerText"), []

SITES = dict(devto=(devto, devto_read), tabnews=(tabnews, tabnews_read), huggingface=(huggingface, huggingface_read), hackaday=(hackaday, hackaday_read), instructables=(instructables, instructables_read))
one = lambda s: str(s).replace("\t", " ").replace("\n", " ")

def main():
    if "--self-check" in sys.argv:
        assert txt("<b>a</b>  &amp; b\n") == "a & b" and row("t", "u", date="2026-11-08T10:00")["date"] == "2026-11-08" and len(SITES) == 5
        return print("ok")
    a = argparse.ArgumentParser(); a.add_argument("site", choices=SITES); a.add_argument("query"); a.add_argument("-d", default="."); a.add_argument("-t", type=int, default=8); a = a.parse_args()
    find, read = SITES[a.site]; d = Path(a.d); d.mkdir(parents=True, exist_ok=True)
    try: rows = sorted(find(a.query, 30), key=lambda r: (r.get("hit", 0), r["score"]), reverse=True)
    except Exception as e: sys.exit(f"ERRO: {a.site} falhou ({e})")
    if not rows: sys.exit(f"ERRO: 0 resultados em {a.site} para '{a.query}'")
    (d / f"{a.site}-top.tsv").write_text("score\tn\tdate\ttitle\turl\n" + "".join(f"{r['score']}\t{r['n']}\t{r['date']}\t{one(r['title'])}\t{r['url']}\n" for r in rows))
    out = []
    for r in rows[:a.t]:
        try: body, cs = read(r)
        except Exception as e: body, cs = f"(erro ao ler: {e})", []
        out.append(f"## {r['title']}\n{r['url']} · score {r['score']} · n {r['n']} · {r['date']}\n\n{body[:4000]}\n\n" + "".join(f"- **{u}** ({s}): {t[:500]}\n" for s, u, t in sorted(cs, key=lambda c: -c[0])[:8]))
    (d / f"{a.site}-read.md").write_text("\n".join(out))
    print(f"{len(rows)} candidatos, {len(out)} lidos -> {d}/{a.site}-top.tsv, {a.site}-read.md")

main()
