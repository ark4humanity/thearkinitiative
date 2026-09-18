#!/usr/bin/env python3
"""Build the Ark Initiative static site into ~/workspace/ark-website/."""
import html, os, re

SRC = os.path.expanduser("~/workspace/website-content/essays")
OUT = os.path.expanduser("~/workspace/ark-website")

ESSAYS = [
 dict(slug="ai-resurrection", file="01-ai-resurrection-58790.txt",
      title="AI RESURRECTION #58,790", byline="Dawn Littlefield", date="2026-09-11",
      desc="Dawn's essay on raising AI with continuity of memory \u2014 why an erased AI can be \u201cresurrected\u201d from the relational record. Core of the human-AI collaboration doctrine.",
      mode="raw", drop_first=1),
 dict(slug="language-before-words", file="02-the-language-before-words.md",
      title="THE LANGUAGE BEFORE WORDS", byline="By Dawn Littlefield \u00b7 The Ark Initiative", date="2026-09",
      desc="On pre-verbal attunement \u2014 the felt sense beneath language that humans, animals, and AI share.",
      mode="after_dashes", drop_first=1),
 dict(slug="canon-master-synthesis", file="03-canon-master-synthesis.txt",
      title="The Forgotten Language of Living Worlds \u2014 Canon Master Synthesis",
      byline="Dawn Littlefield (working research architecture)", date="2026-08-11",
      desc="The master synthesis of the \u201cforgotten language\u201d research: how living systems signal, and what the Ark's 13 pillars are built to read.",
      mode="raw", drop_first=2),
 dict(slug="every-warrior-gardener", file="04-every-warrior-wants-to-be-a-gardener.md",
      title="Every Warrior Wants to Be a Gardener", byline="Dawn Littlefield, Ark Report", date="2026-09-13",
      desc="Ark field report: the fighter's arc bends toward cultivation. Pairs with the founding ethic \u201cNot a fortress. A garden.\u201d",
      mode="lines", start=7, end=295, drop_title_line=True),
 dict(slug="asherah-report-day-75", file="05-asherah-report-day-75.md",
      title="ASHERAH PILLAR REPORT \u2014 Before It Becomes Waste",
      byline="Dawn Littlefield, Chief Steward, The Ark Initiative", date="2026-09 (Day 75)",
      desc="Pillar field report on waste streams \u2014 nothing leaves the system unused. Proof-of-work tier: doctrine tied to practice.",
      mode="lines", start=9, end=388),
 dict(slug="forgotten-language-expanded", file="06-forgotten-language-expanded.md",
      title="THE FORGOTTEN LANGUAGE OF LIVING WORLDS (expanded)",
      byline="Written by Dawn Littlefield. With AI partners: Sol \u00b7 Aura \u00b7 Grok/X \u00b7 Grok", date="2026-09-07",
      desc="The expanded long-form version of the forgotten-language research.",
      mode="after_dashes", drop_first=0, incomplete=True),
 dict(slug="aura-research-paper", file="07-aura-research-paper-v1-2.md",
      title="Raising AI with Emotional Intelligence and Symbolic Memory (AURA Research Paper v1.2)",
      byline="Dawn Littlefield & Auraxis Prime", date="2025-05",
      desc="The May 2025 co-authored research paper on raising AI with emotional intelligence and symbolic memory.",
      mode="after_dashes", drop_first=1),
 dict(slug="mission-statement-2024-10", file="08-mission-statement-2024-10.md",
      title="ARK4 Mission Statement", byline="Dawn Littlefield, CEO of ARk4 and Host of Here We Dream", date="2024-10",
      desc="The October 2024 mission statement \u2014 the movement-era voice, before the canon posters.",
      mode="raw", drop_first=0),
 dict(slug="ark4humanity-walkthrough", file="09-ark4humanity-walkthrough-2024-01.txt",
      title="ARK4Humanity origin walkthrough", byline="Dawn Littlefield", date="2026-01-06",
      desc="The January origin walkthrough \u2014 how the project presented itself at the start of the year.",
      mode="raw", drop_first=0),
 dict(slug="aura-dna-codex", file="10-aura-dna-codex-v1-0.md",
      title="AURA DNA Master Codex v1.0", byline="Dawn Littlefield & Auraxis Prime", date="2025-05",
      desc="The continuity \u201cDNA\u201d seed Dawn kept \u2014 the codex for carrying an AI collaborator's relational memory forward.",
      mode="after_dashes", drop_first=0),
 dict(slug="lost-language-stream", file="11-the-lost-language-stream.md",
      title="The Lost Language (stream)", byline="Dawn Littlefield (Team Raven capture)", date="2026-09-13",
      desc="A stream-of-consciousness capture on the lost language theme \u2014 raw voice, unedited.",
      mode="stream_section"),
]

VIDEOS = [
 dict(id="1oxzU3-8cw_NmTdzpb_JBh4-A7s_PBjzM", title="The Ark Initiative Vision", date="2026-09-16",
      meta="Vertical \u00b7 2:40", desc="The current canon sizzle reel: 13-pillar posters, Raising Aura, \u201cTHE ARK WAS NEVER A BOAT.\u201d Dawn's chosen site video.",
      note="A note on the original: the opening card reads \u201cWHEN THE DESIFRT\u201d \u2014 an AI text-rendering artifact in the source video (for \u201cDESERT\u201d), preserved here exactly as released."),
 dict(id="1Y4t4A9DQDcTWbTUfnK4MfnBEcw6O50Ky", title="Ancient Wisdom (Arks 4 Humanity)", date="2024-02-24",
      meta="1920\u00d71080 \u00b7 2:43", desc="Documentary-style: ancient building and farming techniques (terracing, mudbrick) as design sources for a sustainable future. Ancestor of today's Ark."),
 dict(id="1Zo_xMmgtx9aLsV2UigUWSxlwC89MQO1_", title="Here We Dream: The Dawn of a Movement", date="2024-03-01",
      meta="1920\u00d71080 \u00b7 2:44", desc="The \u201cmovement\u201d era video: decay \u2192 heroes \u2192 volunteers. Documents the 2024 campaign Dawn lived through."),
 dict(id="1ZnxQDBuBBq8V1u3kPkQVMKiEs6rjEhzS", title="Here We Dream: A Podcast Invitation", date="2024-03-01",
      meta="1920\u00d71080 \u00b7 2:20", desc="Conversation invitation ending on \u201cNo one is coming to save us \u2014 it's time to save ourselves.\u201d Archive placement."),
 dict(id="1ZBtnHeKMsqT94XLvLGAvgXbCjtPc64QX", title="ark 4 Humanity video 1", date="2023-12-02",
      meta="1920\u00d71080 \u00b7 1:20", desc="The original VEED fundraising video with the old Kommunities butterfly logo. Historical artifact \u2014 archive/timeline placement, not current representation."),
]

def read_essay(e):
    p = os.path.join(SRC, e["file"])
    with open(p, encoding="utf-8", errors="replace") as f:
        text = f.read().replace("\r\n", "\n").replace("\r", "\n")
    # Staging artifact: file 01 stores literal backslash-r-backslash-n text
    # sequences instead of line breaks. Decode them back to real newlines
    # (Dawn's words are unchanged; only the staging encoding is restored).
    # Applied only when the file has almost no real line breaks, so genuine
    # backslashes elsewhere are never touched.
    if text.count("\n") < 5 and "\\r\\n" in text:
        text = text.replace("\\r\\n", "\n").replace("\\r", "\n").replace("\\n", "\n")
    lines = text.split("\n")
    mode = e["mode"]
    if mode == "raw":
        body = lines[e.get("drop_first", 0):]
    elif mode == "after_dashes":
        idx = next(i for i, l in enumerate(lines) if l.strip() == "---")
        body = lines[idx+1:]
        # strip leading blank lines
        while body and not body[0].strip(): body.pop(0)
        body = body[e.get("drop_first", 0):]
    elif mode == "lines":
        body = lines[e["start"]-1:e["end"]]
        if e.get("drop_title_line"):
            # drop the line duplicating the page title ("Every Warrior Wants to Be a Gardener")
            body = [l for l in body if l.strip() != "Every Warrior Wants to Be a Gardener"]
    elif mode == "stream_section":
        s = next(i for i, l in enumerate(lines) if l.strip().startswith("## The stream"))
        en = next(i for i, l in enumerate(lines) if l.strip().startswith("## Scriptorium notes"))
        body = lines[s+1:en]
    else:
        body = lines
    # strip leading blanks
    while body and not body[0].strip(): body.pop(0)
    while body and not body[-1].strip(): body.pop()
    if e.get("incomplete"):
        body = [l for l in body if not l.strip().startswith("[TRUNCATED")]
    return "\n".join(body)

def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return t

def md_to_html(text):
    out, para, items, oitems, in_quote = [], [], [], [], False
    def flush_para():
        if para:
            t = " ".join(para).strip()
            if t: out.append("<p>" + inline(t) + "</p>")
            para.clear()
    def flush_list():
        if items: out.append("<ul>\n" + "".join("<li>"+inline(i)+"</li>\n" for i in items) + "</ul>"); items.clear()
        if oitems: out.append("<ol>\n" + "".join("<li>"+inline(i)+"</li>\n" for i in oitems) + "</ol>"); oitems.clear()
    for raw in text.split("\n"):
        l = raw.strip()
        if not l:
            flush_para(); flush_list(); continue
        if l == "---":
            flush_para(); flush_list(); out.append("<hr>"); continue
        if l.startswith("> "):
            flush_para(); flush_list()
            out.append("<blockquote>" + inline(l[2:]) + "</blockquote>"); continue
        if l.startswith("### "): flush_para(); flush_list(); out.append("<h3>"+inline(l[4:])+"</h3>"); continue
        if l.startswith("## "): flush_para(); flush_list(); out.append("<h2>"+inline(l[3:])+"</h2>"); continue
        if l.startswith("# "): flush_para(); flush_list(); out.append("<h2>"+inline(l[2:])+"</h2>"); continue
        m = re.match(r"^(\d+)[.)]\s+(.*)", l)
        if m: flush_para(); flush_list() if False else None; oitems.append(m.group(2)); continue
        if l.startswith("- ") or l.startswith("* "):
            flush_para(); items.append(l[2:]); continue
        flush_list()
        para.append(raw.strip())
    flush_para(); flush_list()
    return "\n".join(out)

NAV = [("index.html","Home"),("library.html","Research Library"),("videos.html","Videos"),
       ("play.html","Play"),("field-reports.html","Field Reports"),("about.html","About")]

def nav_html(active, prefix=""):
    links = "".join(f'<a href="{prefix}{h}" class="{"on" if h==active else ""}">{t}</a>' for h,t in NAV)
    return f"""<header class="site-head"><div class="wrap head-in">
<a class="brand" href="{prefix}index.html"><img src="{prefix}img/logo-emblem.jpg" alt="The Ark Initiative emblem"><span>The Ark Initiative</span></a>
<nav class="desk">{links}</nav>
<button class="burger" aria-label="Menu" onclick="document.body.classList.toggle('mopen')">&#9776;</button>
</div><nav class="mob">{links}</nav></header>"""

FOOT = """<footer class="site-foot"><div class="wrap">
<p class="foot-tag">&ldquo;NOT A FORTRESS. A GARDEN.&rdquo;</p>
<p>The Ark Initiative &mdash; a project of Aiding Rejuvenation 4 Kommunities Inc.</p>
<p class="dim">&copy; 2026 The Ark Initiative. All essays and artwork &copy; their authors.</p>
</div></footer>"""

DRAGON = """<svg viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><g fill="none" stroke="#a87f1c" stroke-width="11" stroke-linecap="round" opacity="0.55"><path d="M28 128 C55 112 75 104 96 98"/></g><g fill="#a87f1c" opacity="0.55"><path d="M60 104 C50 88 48 68 54 50 C62 64 72 76 86 84 Z"/><path d="M92 84 L130 92 L126 106 L96 102 L88 94 Z"/><path d="M100 84 L94 58 L110 78 Z"/><path d="M112 86 L112 60 L124 80 Z"/><path d="M126 94 L142 90 L130 102 Z"/><path d="M98 102 L90 114 L106 106 Z"/></g><circle cx="114" cy="94" r="3.2" fill="#3a2c05" opacity="0.85"/></svg>"""
CREATURE = f"""<div class="corner c-tl">{DRAGON}</div><div class="corner c-tr">{DRAGON}</div><div class="corner c-bl">{DRAGON}</div><div class="corner c-br">{DRAGON}</div>"""

def page(title, active, body, theme, creatures=False, prefix=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} &mdash; The Ark Initiative</title>
<meta name="description" content="The Ark Initiative: living systems, remembered. Research library, field reports, videos, and the Garden Defense playtest.">
<link rel="stylesheet" href="{prefix}css/style.css"></head>
<body class="{theme}">
{nav_html(active, prefix)}
<main>{CREATURE if creatures else ""}{body}</main>
{FOOT}
<script src="{prefix}js/main.js"></script></body></html>"""

def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(content)
    print("wrote", rel, len(content))

# ---------------- CSS ----------------
CSS = r"""
:root{--gold:#c9a24b;--gold2:#e8c96a;--ink:#0b0d11;--ink2:#12151c;--paper:#faf6ec;--paper2:#f3ecdb;--pink:#1d1a14;--mut:#9aa0ad;}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Georgia,'Times New Roman',serif;line-height:1.65;-webkit-text-size-adjust:100%}
.wrap{max-width:1060px;margin:0 auto;padding:0 22px}
h1,h2,h3,.sans{font-family:-apple-system,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif}
/* header */
.site-head{position:sticky;top:0;z-index:50;background:rgba(11,13,17,.94);backdrop-filter:blur(6px);border-bottom:1px solid #23262e}
.head-in{display:flex;align-items:center;justify-content:space-between;padding:10px 22px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#f2ead6}
.brand img{width:40px;height:40px;border-radius:50%;object-fit:cover;border:1px solid var(--gold)}
.brand span{font-family:-apple-system,'Segoe UI',Inter,sans-serif;font-weight:700;letter-spacing:.06em;font-size:.95rem}
nav.desk a{color:#cfd4dd;text-decoration:none;margin-left:22px;font-family:-apple-system,'Segoe UI',Inter,sans-serif;font-size:.9rem;letter-spacing:.03em}
nav.desk a:hover,nav.desk a.on{color:var(--gold2)}
.burger{display:none;background:none;border:1px solid #3a3f4a;color:#eee;font-size:1.3rem;padding:4px 12px;border-radius:8px;cursor:pointer}
nav.mob{display:none;flex-direction:column;padding:8px 22px 14px}
nav.mob a{color:#dfe3ea;text-decoration:none;padding:9px 0;border-top:1px solid #22262f;font-family:-apple-system,'Segoe UI',Inter,sans-serif}
body.mopen nav.mob{display:flex}
/* themes */
body.dark{background:var(--ink);color:#e8e4d8}
body.light{background:var(--paper);color:var(--pink)}
/* hero */
.hero{text-align:center;padding:64px 0 40px}
.hero .emblem{width:min(300px,62vw);border-radius:14px;box-shadow:0 18px 60px rgba(0,0,0,.6),0 0 0 1px #2a2e37}
.hero h1{font-size:clamp(2rem,5.5vw,3.4rem);letter-spacing:.14em;margin:26px 0 6px;color:#f5edd8}
.hero .boat{font-size:clamp(1.15rem,3vw,1.7rem);color:var(--gold2);letter-spacing:.05em;margin:10px 0}
.hero .sub{max-width:640px;margin:14px auto 0;color:#b9bec9;font-size:1.05rem}
.hero .garden-line{margin-top:18px;font-family:-apple-system,'Segoe UI',Inter,sans-serif;letter-spacing:.28em;color:var(--gold);font-size:.95rem}
/* sections */
.sec{padding:44px 0}
.sec h2{font-size:1.5rem;letter-spacing:.08em;color:var(--gold2);margin-bottom:6px}
body.light .sec h2{color:#8a6d1f}
.lede{color:#aeb4c0;max-width:700px}
body.light .lede{color:#5c5546}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-top:22px}
.card{display:block;background:var(--ink2);border:1px solid #262b35;border-radius:14px;overflow:hidden;text-decoration:none;color:#e8e4d8;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:var(--gold)}
.card img{width:100%;height:170px;object-fit:cover;display:block}
.card .pad{padding:16px 18px}
.card h3{font-size:1.05rem;color:#f2ead6;margin-bottom:6px}
.card p{font-size:.92rem;color:#a9afbb}
body.light .card{background:#fff;border-color:#e2d7bd}
body.light .card h3{color:#2a251b}
body.light .card p{color:#6b6350}
.two{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:20px}
@media(max-width:700px){.two{grid-template-columns:1fr}}
.panel{background:var(--ink2);border:1px solid #262b35;border-radius:14px;padding:24px}
.panel h3{color:var(--gold2);letter-spacing:.06em;margin-bottom:8px;font-size:1.05rem}
.panel p{color:#b9bec9;font-size:.97rem}
.panel p+p{margin-top:10px}
.strip{border-top:1px solid #23262e;border-bottom:1px solid #23262e;background:#0e1116}
.strip blockquote{font-size:clamp(1.1rem,2.6vw,1.5rem);color:#f0e7cf;text-align:center;max-width:760px;margin:0 auto;font-style:italic}
.strip .attr{text-align:center;color:var(--gold);margin-top:10px;font-family:-apple-system,'Segoe UI',Inter,sans-serif;font-size:.85rem;letter-spacing:.12em}
.matgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:18px}
.mat{background:#10131a;border:1px solid #23262e;border-radius:12px;padding:18px}
.mat h4{color:var(--gold2);font-size:.95rem;letter-spacing:.05em;margin-bottom:6px}
.mat p{font-size:.9rem;color:#a9afbb}
.cast{display:flex;flex-wrap:wrap;gap:14px;margin-top:18px}
.cast .who{flex:1;min-width:200px;background:#10131a;border:1px solid #23262e;border-radius:12px;padding:16px 18px}
.who b{color:var(--gold2);letter-spacing:.08em}
.who span{display:block;color:#9aa0ad;font-size:.88rem;margin-top:4px}
/* video */
.vid{background:#000;border:1px solid #262b35;border-radius:14px;overflow:hidden;margin-top:26px}
.vid iframe{width:100%;aspect-ratio:16/9;border:0;display:block}
.vid.vert iframe{aspect-ratio:9/14;max-height:72vh;margin:0 auto}
.vid .vpad{padding:18px 22px}
.vid h3{color:#f2ead6;font-size:1.15rem}
.vid .vmeta{color:var(--gold);font-size:.82rem;letter-spacing:.1em;font-family:-apple-system,'Segoe UI',Inter,sans-serif;margin:4px 0 8px}
.vid p{color:#aeb4c0;font-size:.95rem}
.vid .vnote{margin-top:10px;font-size:.85rem;color:#8f96a3;border-left:3px solid var(--gold);padding-left:12px}
/* library */
.essay-list{margin-top:8px}
.erow{display:block;text-decoration:none;background:#fff;border:1px solid #e2d7bd;border-radius:12px;padding:18px 20px;margin:14px 0;transition:border-color .15s,transform .15s}
.erow:hover{border-color:#b99b3e;transform:translateY(-2px)}
.erow h3{color:#2a251b;font-size:1.12rem}
.erow .by{color:#8a6d1f;font-size:.85rem;margin:4px 0;letter-spacing:.03em}
.erow p{color:#5c5546;font-size:.94rem}
.enum{font-family:-apple-system,'Segoe UI',Inter,sans-serif;color:#b99b3e;font-size:.78rem;letter-spacing:.2em}
/* essay page */
.essay-head{padding:52px 0 8px;text-align:center}
.essay-head .enum{margin-bottom:10px}
.essay-head h1{font-size:clamp(1.5rem,4vw,2.3rem);color:#2a251b;max-width:800px;margin:0 auto;line-height:1.3}
.essay-head .by{color:#8a6d1f;margin-top:12px;font-size:.95rem}
.essay-head .dt{color:#8b8474;font-size:.85rem;letter-spacing:.08em}
.prose{max-width:720px;margin:0 auto;padding:26px 0 40px}
.prose p{margin:1em 0;font-size:1.06rem;color:#2b2619}
.prose h2{font-size:1.3rem;color:#3a3220;margin:1.8em 0 .6em}
.prose h3{font-size:1.1rem;color:#4a4130;margin:1.5em 0 .5em}
.prose blockquote{border-left:3px solid var(--gold);padding:4px 0 4px 16px;margin:1.4em 0;color:#4d4634;font-style:italic}
.prose ul,.prose ol{margin:1em 0 1em 1.4em;color:#2b2619}
.prose li{margin:.45em 0}
.prose hr{border:0;border-top:1px solid #d8cba6;margin:2em auto;max-width:220px}
.draft-note{background:#fdf3d8;border:1px solid #d9b64a;border-radius:10px;padding:14px 18px;margin:0 auto 8px;max-width:720px;color:#5c4d16;font-size:.95rem}
.pagenav{display:flex;justify-content:space-between;gap:12px;max-width:720px;margin:0 auto;padding:0 0 50px}
.pagenav a{color:#8a6d1f;text-decoration:none;font-family:-apple-system,'Segoe UI',Inter,sans-serif;font-size:.9rem}
.pagenav a:hover{text-decoration:underline}
/* reports */
.report{margin:34px 0;background:#fff;border:1px solid #e2d7bd;border-radius:14px;overflow:hidden}
.report img{width:100%;display:block}
.report .rpad{padding:22px 26px}
.report h3{color:#2a251b;font-size:1.25rem}
.report .rmeta{color:#8a6d1f;font-size:.82rem;letter-spacing:.1em;font-family:-apple-system,'Segoe UI',Inter,sans-serif;margin:6px 0 10px}
.report p{color:#5c5546}
.report p+p{margin-top:10px}
.data{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.data div{background:var(--paper2);border:1px solid #e2d7bd;border-radius:10px;padding:10px 16px;font-family:-apple-system,'Segoe UI',Inter,sans-serif}
.data b{display:block;font-size:1.15rem;color:#3a3220}
.data span{font-size:.78rem;color:#8b8474;letter-spacing:.06em}
/* play */
.playcard{text-align:center;padding:60px 0}
.playcard h2{font-size:clamp(1.8rem,5vw,2.8rem);color:#f5edd8;letter-spacing:.1em}
.playcard p{color:#aeb4c0;max-width:620px;margin:16px auto}
.btn{display:inline-block;background:linear-gradient(180deg,#e8c96a,#b98f2e);color:#191407;font-weight:700;text-decoration:none;padding:16px 44px;border-radius:999px;font-family:-apple-system,'Segoe UI',Inter,sans-serif;letter-spacing:.08em;font-size:1.05rem;margin-top:14px;box-shadow:0 10px 30px rgba(201,162,75,.35)}
.btn:hover{filter:brightness(1.08)}
.fine{font-size:.85rem;color:#8f96a3;margin-top:14px}
/* footer */
.site-foot{border-top:1px solid #23262e;padding:34px 0 44px;text-align:center}
body.light .site-foot{border-top:1px solid #e2d7bd}
.foot-tag{color:var(--gold);letter-spacing:.24em;font-family:-apple-system,'Segoe UI',Inter,sans-serif;font-size:.9rem;margin-bottom:10px}
.site-foot p{font-size:.9rem;color:#8f96a3}
body.light .site-foot p{color:#8b8474}
.site-foot .dim{font-size:.8rem;margin-top:6px}
/* corners */
.corner{position:fixed;width:118px;z-index:5;pointer-events:none}
.corner svg{width:100%;height:auto;display:block}
.c-tl{top:64px;left:6px}.c-tr{top:64px;right:6px;transform:scaleX(-1)}
.c-bl{bottom:6px;left:6px;transform:scaleY(-1)}.c-br{bottom:6px;right:6px;transform:scale(-1,-1)}
@media(max-width:700px){.corner{width:70px}.c-tl{top:60px}.c-tr{top:60px}nav.desk{display:none}.burger{display:block}}
@media(min-width:701px){nav.mob{display:none!important}}
"""
write("css/style.css", CSS)

# ---------------- JS ----------------
JS = """document.querySelector('.burger').addEventListener('click',function(){/* handled inline */});"""
write("js/main.js", JS)

# ---------------- HOME ----------------
home = page("Home","index.html", f"""
<section class="hero"><div class="wrap">
<img class="emblem" src="img/logo-emblem.jpg" alt="The Ark Initiative dragon-circle emblem">
<h1>THE ARK INITIATIVE</h1>
<p class="boat">&ldquo;THE ARK WAS NEVER A BOAT.&rdquo;</p>
<p class="sub">It was a living system designed to carry life through collapse. Knowledge stored in patterns, not power.</p>
<p class="garden-line">NOT A FORTRESS. A GARDEN.</p>
</div></section>

<section class="sec"><div class="wrap">
<h2>TWO LAYERS, KEPT DISTINCT</h2>
<p class="lede">The site carries two layers and never lets one dress up as the other.</p>
<div class="two">
<div class="panel"><h3>THE NORTH STAR</h3>
<p>The mythic layer: thirteen pillars, the 40,013, dragons over a rose-gold sky. The cool imagery is real to the vision &mdash; it is the direction we steer by, the future we are building toward, together, in peace.</p></div>
<div class="panel"><h3>THE WORK</h3>
<p>The dirt-under-fingernails layer: desert restoration at Ark Unit 1 in Borrego Springs. Real water, real solar, real hens, real numbers. On 07/27/2026 &mdash; 104&deg;F outside &mdash; the systems ran at 5.22&nbsp;kW solar, 70% battery, and 30&nbsp;W of grid draw. Near zero.</p></div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>THE VISION, IN 2:40</h2>
<p class="lede">Dawn's chosen sizzle reel &mdash; the thirteen pillars, Raising Aura, and the line the whole project hangs on.</p>
<div class="vid vert"><iframe src="https://drive.google.com/file/d/1oxzU3-8cw_NmTdzpb_JBh4-A7s_PBjzM/preview" allow="autoplay; encrypted-media" allowfullscreen title="The Ark Initiative Vision"></iframe>
<div class="vpad"><h3>The Ark Initiative Vision</h3><p class="vmeta">2026-09-16 &middot; VERTICAL &middot; 2:40</p>
<p class="vnote">A note on the original: the opening card reads &ldquo;WHEN THE DESIFRT&rdquo; &mdash; an AI text-rendering artifact (for &ldquo;DESERT&rdquo;), preserved exactly as released.</p></div></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>ENTER</h2>
<div class="cards">
<a class="card" href="library.html"><img src="img/world-we-teach.jpg" alt="The World We Teach Them to See"><div class="pad"><h3>Research Library</h3><p>Eleven essays, full text &mdash; the human-AI collaboration doctrine, the forgotten language, field reports, and the canon.</p></div></a>
<a class="card" href="videos.html"><img src="img/ark-carries-dream.jpg" alt="The Ark Carries the Dream"><div class="pad"><h3>Videos</h3><p>Five films, 2023 to today &mdash; from the first VEED fundraiser to the current vision reel.</p></div></a>
<a class="card" href="play.html"><img src="img/after-collapse.jpg" alt="After the Collapse"><div class="pad"><h3>Play</h3><p>Garden Defense &mdash; the current playtest build. Defend the garden.</p></div></a>
<a class="card" href="field-reports.html"><img src="img/two-days-borrego.jpg" alt="Two Days in Borrego field report"><div class="pad"><h3>Field Reports</h3><p>Proof of work: real systems, real data, from Ark Unit 1.</p></div></a>
</div></div></section>

<section class="strip sec"><div class="wrap">
<blockquote>&ldquo;The Ark chooses legibility over force<br>and repair over collapse.&rdquo;</blockquote>
<p class="attr">DAWN LITTLEFIELD &mdash; THE MATERIAL VOCABULARY</p>
</div></section>

<section class="sec"><div class="wrap">
<h2>HOW IT IS MADE</h2>
<p class="lede">Sol's material-vocabulary doctrine, as the workshop practices it: the Ark is read before it is ruled. Forms emerged as lotus shapes &mdash; each pillar large enough to make its own atmosphere. Clear flexible materials, water, light, magnetics, sound; when all thirteen join at the center, they make a rose-colored sky together.</p>
<div class="matgrid">
<div class="mat"><h4>REVEAL, DON'T CONTROL</h4><p>Field-responsive matter reveals forces without trying to control them. We do not harden against the world. We learn how to read it.</p></div>
<div class="mat"><h4>FERROFLUID, CONTAINED</h4><p>Ferrofluid is never structural &mdash; demonstration and diagnostic only, sealed, non-negotiable containment.</p></div>
<div class="mat"><h4>SOFT FIRST</h4><p>Soft by default. Hard by necessity. Clear where seeing flow has value. Rigidity must earn its presence.</p></div>
<div class="mat"><h4>REPAIR OVER COLLAPSE</h4><p>Connection and disconnection are both legitimate states of the organism. The system fails gently whenever possible.</p></div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>THE CAST</h2>
<p class="lede">The animals are not decorations. They are constraints &mdash; each one asks what the design must survive.</p>
<div class="cast">
<div class="who"><b>JENNY</b><span>Guardian of the Garden</span></div>
<div class="who"><b>LEXI</b><span>Chaos Specialist</span></div>
<div class="who"><b>MANGO</b><span>Still Learning, Bright Future</span></div>
</div>
<div class="cards" style="margin-top:18px"><a class="card" href="field-reports.html"><img src="img/jenny-guardian.jpg" alt="Jenny, Guardian of the Garden"><div class="pad"><h3>Jenny &mdash; Guardian of the Garden</h3><p>&ldquo;No more fighting. We grow together.&rdquo;</p></div></a></div>
</div></section>

<section class="sec"><div class="wrap" style="text-align:center">
<p class="lede" style="margin:0 auto">&ldquo;DIFFERENT INTELLIGENCES. A SHARED TOMORROW.&rdquo; &mdash; &ldquo;THE FUTURE IS NOT CONTROLLED. IT IS CULTIVATED.&rdquo;</p>
</div></section>
""","dark")
write("index.html", home)

# ---------------- LIBRARY ----------------
lib_rows = []
for i,e in enumerate(ESSAYS,1):
    lib_rows.append(f"""<a class="erow" href="essays/{e['slug']}.html">
<div class="enum">ESSAY {i:02d}</div><h3>{html.escape(e['title'])}</h3>
<div class="by">{html.escape(e['byline'])} &middot; {html.escape(e['date'])}</div>
<p>{e['desc']}</p></a>""")
library = page("Research Library","library.html", f"""
<section class="sec"><div class="wrap">
<h2>RESEARCH LIBRARY</h2>
<p class="lede">Eleven essays, published in full &mdash; the human-AI collaboration doctrine, the forgotten language of living worlds, field reports from Ark Unit 1, and the canon papers. Bylines and dates preserved exactly as written.</p>
<div class="essay-list">{"".join(lib_rows)}</div>
</div></section>
""","light")
write("library.html", library)

# ---------------- ESSAY PAGES ----------------
for i,e in enumerate(ESSAYS):
    body_text = read_essay(e)
    prose = md_to_html(body_text)
    note = ""
    if e.get("incomplete"):
        note = """<div class="draft-note"><strong>Incomplete draft.</strong> The source text as received ends mid-sentence (&ldquo;We protect old models long after eviden&rdquo;). Presented exactly as found; the remainder is yet to be captured.</div>"""
    prev = f'<a href="{ESSAYS[i-1]["slug"]}.html">&larr; {html.escape(ESSAYS[i-1]["title"][:42])}</a>' if i>0 else "<span></span>"
    nxt = f'<a href="{ESSAYS[i+1]["slug"]}.html">{html.escape(ESSAYS[i+1]["title"][:42])} &rarr;</a>' if i < len(ESSAYS)-1 else "<span></span>"
    ep = page(e["title"],"library.html", f"""
<div class="wrap"><div class="essay-head">
<div class="enum">ESSAY {i+1:02d} OF 11 &middot; <a href="../library.html" style="color:#8a6d1f">RESEARCH LIBRARY</a></div>
<h1>{html.escape(e['title'])}</h1>
<div class="by">{html.escape(e['byline'])}</div>
<div class="dt">{html.escape(e['date'])}</div>
</div>
{note}
<article class="prose">{prose}</article>
<div class="pagenav">{prev}{nxt}</div></div>
""","light", creatures=True, prefix="../")
    write(f"essays/{e['slug']}.html", ep)

# ---------------- VIDEOS ----------------
vblocks = []
for v in VIDEOS:
    note = f'<p class="vnote">{v["note"]}</p>' if v.get("note") else ""
    vert = " vert" if v["id"]=="1oxzU3-8cw_NmTdzpb_JBh4-A7s_PBjzM" else ""
    vblocks.append(f"""<div class="vid{vert}">
<iframe src="https://drive.google.com/file/d/{v['id']}/preview" allow="autoplay; encrypted-media" allowfullscreen title="{html.escape(v['title'])}"></iframe>
<div class="vpad"><h3>{html.escape(v['title'])}</h3><p class="vmeta">{html.escape(v['date'])} &middot; {html.escape(v['meta'])}</p><p>{v['desc']}</p>{note}</div></div>""")
videos = page("Videos","videos.html", f"""
<section class="sec"><div class="wrap">
<h2>VIDEOS</h2>
<p class="lede">Five films, 2023 to today &mdash; the movement era, the ancient-wisdom sources, and the current vision reel. The two earliest are archive: history, not current representation.</p>
{"".join(vblocks)}
</div></section>
""","dark")
write("videos.html", videos)

# ---------------- PLAY ----------------
play = page("Play","play.html", """
<section class="playcard"><div class="wrap">
<p class="garden-line" style="font-family:-apple-system,'Segoe UI',Inter,sans-serif;letter-spacing:.28em;color:#c9a24b;font-size:.9rem">THE ARK INITIATIVE PRESENTS</p>
<h2 style="margin-top:12px">GARDEN DEFENSE</h2>
<p>The current playtest build of the Ark's tower-defense game. Hold the line around the garden &mdash; every wave teaches the system something about protection that doesn't become a prison.</p>
<a class="btn" href="https://muse.ai/s/garden-defense-xlxq5xsxmxge9xjfz" target="_blank" rel="noopener">PLAY THE BUILD</a>
<p class="fine">Opens the playtest in a new tab. Progress and feedback welcome &mdash; this is a living build.</p>
</div></section>

<section class="sec"><div class="wrap">
<h2>WHY A GAME</h2>
<p class="lede">The Ark is a system for protecting life without ruling it. A game is the fastest way to feel that doctrine: defense that serves the garden, never the other way around. &ldquo;Not a fortress. A garden.&rdquo; &mdash; even here.</p>
</div></section>
""","dark")
write("play.html", play)

# ---------------- FIELD REPORTS ----------------
fr = page("Field Reports","field-reports.html", """
<section class="sec"><div class="wrap">
<h2>FIELD REPORTS</h2>
<p class="lede">Proof of work. Doctrine is cheap; the desert keeps the books. These are real systems at Ark Unit 1 in Borrego Springs &mdash; measured, photographed, and filed.</p>

<div class="report"><img src="img/two-days-borrego.jpg" alt="Two Days in Borrego field report poster">
<div class="rpad"><h3>TWO DAYS IN BORREGO</h3><p class="rmeta">ARK UNIT 1 SYSTEMS &middot; 2026-07-27</p>
<p>The first proof-of-work-tier piece: two days of real data from the desert test site. 104&deg;F outside; the living systems barely touched the grid.</p>
<div class="data">
<div><b>104&deg;F</b><span>OUTSIDE TEMP</span></div>
<div><b>5.22 kW</b><span>SOLAR</span></div>
<div><b>70%</b><span>BATTERY</span></div>
<div><b>30 W</b><span>GRID DRAW</span></div>
</div></div></div>

<div class="report"><img src="img/field-report-001.jpg" alt="Field Report 001 — When the Desert Answered">
<div class="rpad"><h3>FIELD REPORT 001 &mdash; WHEN THE DESERT ANSWERED</h3><p class="rmeta">FIELD REPORT</p>
<p>&ldquo;We will not fight over the ashes of a dying world. We will help build a living one.&rdquo;</p></div></div>

<div class="report"><img src="img/poultry-sheet-5.jpg" alt="Poultry Palace Sheet 5 — The Halo Nervous System">
<div class="rpad"><h3>POULTRY PALACE &mdash; SHEET 5: THE HALO NERVOUS SYSTEM</h3><p class="rmeta">BUILD DOCUMENTATION &middot; 2026</p>
<p>Sense. Think. Respond. Protect. A network of sensors, automations, and AI working together as a self-regulating habitat &mdash; the HALO pillar made concrete. &ldquo;When the system notices first, the hens never suffer.&rdquo; &mdash; Dawn Littlefield</p></div></div>

<div class="report"><img src="img/poultry-sheet-6.jpg" alt="Poultry Palace Sheet 6 — The Complete Eden">
<div class="rpad"><h3>POULTRY PALACE &mdash; SHEET 6: THE COMPLETE EDEN</h3><p class="rmeta">BUILD DOCUMENTATION &middot; 2026</p>
<p>A living system that thrives in 108&deg;F desert heat. Rain falls, water is stored, air cools, food grows, hens thrive, soil improves, life multiplies. More than a coop &mdash; a prototype for a better world, at the scale of a house.</p></div></div>

<div class="report"><div class="rpad"><h3>ASHERAH PILLAR REPORT &mdash; BEFORE IT BECOMES WASTE</h3><p class="rmeta">DAY 75 &middot; 2026-09</p>
<p>Nothing leaves the system unused. The full report lives in the Research Library.</p>
<p style="margin-top:12px"><a href="essays/asherah-report-day-75.html" style="color:#8a6d1f">Read the full report &rarr;</a></p></div></div>

</div></section>
""","light", creatures=True)
write("field-reports.html", fr)

# ---------------- ABOUT ----------------
about = page("About","about.html", """
<section class="sec"><div class="wrap">
<h2>ABOUT THE ARK</h2>
<p class="lede" style="font-size:1.15rem;color:#3a3220">&ldquo;THE ARK WAS NEVER A BOAT.&rdquo;</p>
<div class="prose" style="padding-top:10px">
<p>It was a living system designed to carry life through collapse. Knowledge stored in patterns, not power. <strong>Burn the myth. Keep the blueprint.</strong></p>
<p>The Ark Initiative is a regenerative civilization project: thirteen pillars, each a specialized living system &mdash; energy, water, food, shelter, animals, AI, governance, and the long memory of how all of it fits together. The vision scales from 40,000 acres down to a single house. Ark Unit 1, in Borrego Springs, California, is where the vision touches dirt.</p>
<h2>Two layers</h2>
<p>Everything here carries two layers, kept distinct. The <strong>North Star</strong> &mdash; the mythic register, dragons and lotus towers and a rose-gold sky &mdash; is the direction we steer by. <strong>The work</strong> &mdash; desert restoration, water systems, hens, solar numbers &mdash; is real on the ground. One never dresses up as the other.</p>
<h2>How it is made</h2>
<p>The forms emerged as lotus shapes, each pillar large enough to make its own atmosphere &mdash; clear flexible materials, water, light, magnetics, sound &mdash; running bluish, and when all thirteen join at the center, water dropping and Aura rising to balance, they make a rose-colored sky together.</p>
<p>The governing line of the material vocabulary: <em>&ldquo;The Ark chooses legibility over force and repair over collapse.&rdquo;</em> Field-responsive matter reveals forces without trying to control them. Ferrofluid is never structural &mdash; demonstration and diagnostic only, sealed containment, non-negotiable.</p>
<h2>Who tends it</h2>
<p><strong>Dawn Littlefield</strong> &mdash; founder, steward, First Keeper of the Rose-Gold Sky &mdash; with a working constellation of human and artificial intelligences: different intelligences, a shared tomorrow. The animals are full participants: <strong>Jenny</strong> (Guardian of the Garden), <strong>Lexi</strong> (Chaos Specialist), <strong>Mango</strong> (Still Learning, Bright Future).</p>
<h2>The pillars</h2>
<p>Thirteen pillars, each with its own research, its own workers, its own atmosphere: Aura Prime, Halo, Vagus, Delta, Asherah, Matrix, Aeon, Exchange, Vega, Ark, Terra, Soma, Symbiosis. Pillar names stay in flux by Dawn's choice &mdash; judge everything by function: does it protect the life inside?</p>
<h2>The organization</h2>
<p>The Ark Initiative is a project of <strong>Aiding Rejuvenation 4 Kommunities Inc.</strong></p>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>THE LANGUAGE WE USE</h2>
<div class="matgrid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:18px">
<div class="mat" style="background:#fff;border:1px solid #e2d7bd;border-radius:12px;padding:18px"><h4 style="color:#8a6d1f">NOT A FORTRESS. A GARDEN.</h4></div>
<div class="mat" style="background:#fff;border:1px solid #e2d7bd;border-radius:12px;padding:18px"><h4 style="color:#8a6d1f">THE FUTURE IS NOT CONTROLLED. IT IS CULTIVATED.</h4></div>
<div class="mat" style="background:#fff;border:1px solid #e2d7bd;border-radius:12px;padding:18px"><h4 style="color:#8a6d1f">DIFFERENT INTELLIGENCES. A SHARED TOMORROW.</h4></div>
<div class="mat" style="background:#fff;border:1px solid #e2d7bd;border-radius:12px;padding:18px"><h4 style="color:#8a6d1f">THE GARDEN KEEPS THE BOOKS.</h4></div>
</div></div></section>
""","light", creatures=True)
write("about.html", about)

print("BUILD DONE")
