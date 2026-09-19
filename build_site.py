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
      music="I'm the Virus in Their System",
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
       ("play.html","Play"),("field-reports.html","Field Reports"),("pillars.html","Pillars"),("about.html","About")]

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
.hero{position:relative;text-align:center;padding:64px 0 40px;overflow:hidden}
.hero .bg{position:absolute;inset:0;background:url(../img/two-ways-surviving-collapse.jpg) center 32%/cover no-repeat;opacity:.5}
.hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(rgba(5,6,10,.62),rgba(5,6,10,.38) 45%,rgba(5,6,10,.72))}
.hero .wrap{position:relative}
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
/* walk-in chambers */
.chamber-hero{position:relative;min-height:92vh;display:flex;align-items:flex-end;overflow:hidden;background:#05070c}
.chamber-hero .hbg{position:absolute;inset:0;background:url(../img/library-hall.jpg) center 30%/cover no-repeat}
.chamber-hero .hshade{position:absolute;inset:0;background:linear-gradient(rgba(4,6,12,.25),rgba(4,6,12,.55) 55%,#0b0d11 98%)}
.chamber-hero .wrap{position:relative;padding-bottom:70px}
.eyebrow{font-family:-apple-system,'Segoe UI',Inter,sans-serif;letter-spacing:.34em;color:var(--gold2);font-size:.8rem;margin-bottom:14px}
.chamber-hero h1{font-size:clamp(2.2rem,6vw,3.8rem);letter-spacing:.12em;color:#f5edd8;margin:0 0 10px}
.chamber-hero .sub{color:#c7cdd8;max-width:620px;font-size:1.08rem}
.scrollcue{margin-top:26px;color:var(--gold);font-family:-apple-system,'Segoe UI',Inter,sans-serif;letter-spacing:.24em;font-size:.8rem;animation:cue 2.6s ease-in-out infinite}
@keyframes cue{0%,100%{opacity:.55}50%{opacity:1}}
/* greeter */
.greeter{background:#0b0d11;border-top:1px solid #1c212b;border-bottom:1px solid #1c212b}
.greet-grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:center}
@media(max-width:760px){.greet-grid{grid-template-columns:1fr}}
.greet-fig{position:relative;border-radius:14px;overflow:hidden;border:1px solid #262b35;cursor:pointer;background:#000}
.greet-fig img{width:100%;display:block}
.greet-fig video{width:100%;display:none}
.greet-fig.playing img{display:none}
.greet-fig.playing video{display:block}
.greet-fig .playbtn{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.greet-fig .playbtn span{width:76px;height:76px;border-radius:50%;background:rgba(201,162,75,.92);color:#14100a;font-size:1.6rem;display:flex;align-items:center;justify-content:center;font-family:-apple-system,'Segoe UI',sans-serif}
.greet-fig.playing .playbtn{display:none}
.greet-fig .vcap{position:absolute;left:0;right:0;bottom:0;padding:10px 14px;background:linear-gradient(transparent,rgba(0,0,0,.75));color:#cfd4dd;font-size:.82rem;font-family:-apple-system,'Segoe UI',sans-serif;letter-spacing:.06em}
.greet-words .who{color:var(--gold2);letter-spacing:.22em;font-size:.8rem;font-family:-apple-system,'Segoe UI',sans-serif;margin-bottom:10px}
.greet-words h2{color:#f2ead6;margin-bottom:10px}
.greet-words p{color:#b9bec9}
.gq{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 6px}
.gq button{background:#141821;border:1px solid #2c3340;color:#e8c96a;border-radius:999px;padding:10px 18px;font-family:-apple-system,'Segoe UI',sans-serif;font-size:.9rem;cursor:pointer;letter-spacing:.03em}
.gq button:hover{border-color:var(--gold);background:#181e29}
.gask{display:flex;gap:10px;margin-top:10px}
.gask input{flex:1;background:#10131a;border:1px solid #2c3340;border-radius:10px;color:#e8e4d8;padding:11px 14px;font-size:.95rem;font-family:Georgia,serif;min-width:0}
.gask button{background:linear-gradient(180deg,#e8c96a,#b98f2e);border:0;border-radius:10px;padding:11px 20px;font-weight:700;cursor:pointer;font-family:-apple-system,'Segoe UI',sans-serif;color:#191407}
#greeter-a{margin-top:16px;min-height:3.2em;color:#dfe3ea;font-size:1.02rem}
#greeter-a a{color:var(--gold2)}
/* shelves, dark */
body.dark .erow{background:#10131a;border-color:#23262e}
body.dark .erow:hover{border-color:var(--gold)}
body.dark .erow h3{color:#f2ead6}
body.dark .erow .by{color:var(--gold)}
body.dark .erow p{color:#a9afbb}
.shelf-note{color:#8f96a3;font-size:.92rem;margin-top:6px}
/* proof */
.proof{background:linear-gradient(180deg,#0b0d11,#10141c);border-top:1px solid #1c212b;border-bottom:1px solid #1c212b}
.proof .pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-top:20px}
.proof .pcell{background:#0e1116;border:1px solid #23262e;border-radius:12px;padding:18px;text-align:center}
.proof .pcell b{display:block;font-size:1.6rem;color:var(--gold2);font-family:-apple-system,'Segoe UI',sans-serif}
.proof .pcell span{font-size:.8rem;color:#9aa0ad;letter-spacing:.08em;font-family:-apple-system,'Segoe UI',sans-serif}
/* doors */
.doors .dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:20px}
.door{display:block;text-decoration:none;background:#10131a;border:1px solid #262b35;border-radius:14px;padding:24px 22px;transition:transform .15s,border-color .15s}
.door:hover{transform:translateY(-3px);border-color:var(--gold)}
.door .dname{color:var(--gold2);letter-spacing:.2em;font-size:.78rem;font-family:-apple-system,'Segoe UI',sans-serif;margin-bottom:8px}
.door h3{color:#f2ead6;font-size:1.15rem;margin-bottom:6px}
.door p{color:#a9afbb;font-size:.93rem}
/* reveal */
.reveal{opacity:0;transform:translateY(26px);transition:opacity .8s ease,transform .8s ease}
.reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none}.scrollcue{animation:none}}

/* chamber hero backgrounds */
.chamber-hero.threshold .hbg{background-image:url(../img/never-a-boat.jpg)}
.chamber-hero.field .hbg{background-image:url(../img/two-days-borrego.jpg)}
.chamber-hero.theater .hbg{background-image:url(../img/ark-carries-dream.jpg)}
.chamber-hero.garden .hbg{background-image:url(../img/world-we-teach.jpg)}
.chamber-hero.pillars .hbg{background-image:url(../img/three-intelligences.jpg)}
.chamber-hero.gardenhall .hbg{background-image:url(../img/ashera-garden-poster.jpg)}
/* voice panels (dragon / jenny) */
.voice{background:#0b0d11;border-top:1px solid #1c212b;border-bottom:1px solid #1c212b}
.voice-grid{display:grid;grid-template-columns:230px 1fr;gap:26px;align-items:center}
@media(max-width:700px){.voice-grid{grid-template-columns:1fr}}
.voice-fig img{width:100%;border-radius:14px;border:1px solid #262b35;display:block}
.voice-words .who{color:var(--gold2);letter-spacing:.22em;font-size:.8rem;font-family:-apple-system,'Segoe UI',sans-serif;margin-bottom:10px}
.voice-quote{font-size:clamp(1.15rem,2.6vw,1.6rem);color:#f0e7cf;font-style:italic;line-height:1.5;min-height:4.4em}
.voice-btn{margin-top:14px;background:#141821;border:1px solid #2c3340;color:#e8c96a;border-radius:999px;padding:10px 22px;font-family:-apple-system,'Segoe UI',sans-serif;font-size:.9rem;cursor:pointer;letter-spacing:.06em}
.voice-btn:hover{border-color:var(--gold);background:#181e29}
/* threshold two doors */
.bigdoors{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
@media(max-width:700px){.bigdoors{grid-template-columns:1fr}}
.bigdoor{position:relative;display:block;border-radius:16px;overflow:hidden;border:1px solid #262b35;text-decoration:none;min-height:320px;transition:transform .15s,border-color .15s;background:#0e1116}
.bigdoor:hover{transform:translateY(-3px);border-color:var(--gold)}
.bigdoor img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.bigdoor .bshade{position:absolute;inset:0;background:linear-gradient(rgba(4,6,12,.1),rgba(4,6,12,.8))}
.bigdoor .bwords{position:absolute;left:0;right:0;bottom:0;padding:24px}
.bigdoor .dname{color:var(--gold2);letter-spacing:.22em;font-size:.78rem;font-family:-apple-system,'Segoe UI',sans-serif;margin-bottom:8px}
.bigdoor h3{color:#f5edd8;font-size:1.5rem;margin-bottom:6px}
.bigdoor p{color:#c7cdd8;font-size:.95rem}
/* pillar doors */
.pillar-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:22px}
.pcard{position:relative;border-radius:14px;padding:22px 20px;border:1px solid #262b35;background:#10131a;overflow:hidden}
.pcard::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--pt,var(--gold))}
.pcard .pnum{font-family:-apple-system,'Segoe UI',sans-serif;color:#8f96a3;font-size:.78rem;letter-spacing:.24em}
.pcard h3{color:#f2ead6;font-size:1.2rem;letter-spacing:.08em;margin:8px 0 6px}
.pcard p{color:#a9afbb;font-size:.9rem}
.pcard .soon{display:inline-block;margin-top:12px;font-family:-apple-system,'Segoe UI',sans-serif;font-size:.72rem;letter-spacing:.2em;color:var(--gold2);border:1px solid #3a3f4a;border-radius:999px;padding:5px 14px;text-decoration:none}
a.pcard{display:block;text-decoration:none}
.pcard .soon.open{color:#14100a;background:var(--gold2);border-color:var(--gold2)}
a.pcard:hover{border-color:var(--gold)}
/* light-theme doors + eyebrows (field reports) */
body.light .eyebrow{color:#8a6d1f}
body.light .door{background:#fff;border-color:#e2d7bd}
body.light .door h3{color:#2a251b}
body.light .door p{color:#6b6350}
body.light .door .dname{color:#8a6d1f}
"""
write("css/style.css", CSS)

# ---------------- JS ----------------
JS = """document.querySelector('.burger').addEventListener('click',function(){/* handled inline */});
(function(){
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12}):null;
document.querySelectorAll('.reveal').forEach(function(el){if(io)io.observe(el);else el.classList.add('in');});
document.querySelectorAll('.greet-fig').forEach(function(f){
f.addEventListener('click',function(){var v=f.querySelector('video');if(!v||f.classList.contains('playing'))return;f.classList.add('playing');v.setAttribute('controls','');v.play();var a=f.querySelector('audio');if(a){var p=a.play();if(p&&p.catch)p.catch(function(){});}});});
var ans=document.getElementById('greeter-a');
if(ans){
var shelf=[
{t:'AI RESURRECTION #58,790',k:'ai resurrection memory continuity resurrect raising erased soul',u:'essays/ai-resurrection.html'},
{t:'THE LANGUAGE BEFORE WORDS',k:'language before words pre-verbal attunement begin start first felt sense',u:'essays/language-before-words.html'},
{t:'The Forgotten Language of Living Worlds \\u2014 Canon Master Synthesis',k:'forgotten language living worlds canon synthesis pillars signal',u:'essays/canon-master-synthesis.html'},
{t:'Every Warrior Wants to Be a Gardener',k:'warrior gardener fighter fortress garden report',u:'essays/every-warrior-gardener.html'},
{t:'ASHERAH PILLAR REPORT \\u2014 Before It Becomes Waste',k:'asherah waste proof report day 75 nothing unused',u:'essays/asherah-report-day-75.html'},
{t:'THE FORGOTTEN LANGUAGE OF LIVING WORLDS (expanded)',k:'forgotten language expanded long',u:'essays/forgotten-language-expanded.html'},
{t:'Raising AI with Emotional Intelligence and Symbolic Memory',k:'aura emotional intelligence symbolic memory paper research',u:'essays/aura-research-paper.html'},
{t:'ARK4 Mission Statement',k:'ark what is mission statement movement',u:'essays/mission-statement-2024-10.html'},
{t:'ARK4Humanity origin walkthrough',k:'origin walkthrough humanity history',u:'essays/ark4humanity-walkthrough.html'},
{t:'AURA DNA Master Codex v1.0',k:'aura dna codex continuity seed',u:'essays/aura-dna-codex.html'},
{t:'The Lost Language (stream)',k:'lost language stream raw voice',u:'essays/lost-language-stream.html'}];
function link(e){return '<a href="'+e.u+'">'+e.t+'</a>';}
function find(q){q=q.toLowerCase();var scored=shelf.map(function(e){var s=0;e.k.split(' ').forEach(function(w){if(q.indexOf(w)>-1)s+=w.length;});return{s:s,e:e};}).filter(function(r){return r.s>0;}).sort(function(a,b){return b.s-a.s;});return scored.slice(0,3).map(function(r){return r.e;});}
function say(html){ans.innerHTML=html;}
window.greetAsk=function(kind){
if(kind==='begin'){say('Begin where the language breaks \\u2014 then learn how memory survives erasure:<br>'+link(shelf[1])+'<br>'+link(shelf[0]));}
else if(kind==='ark'){say('The short answer lives here:<br>'+link(shelf[7])+'<br>'+link(shelf[2]));}
else if(kind==='proof'){say('Doctrine tied to practice \\u2014 the waste-stream report:<br>'+link(shelf[4])+'<br>And the ground truth: <a href="#proof">the proof shelf below</a>.');var p=document.getElementById('proof');if(p)p.scrollIntoView({behavior:'smooth'});}
else if(kind==='pillars'){say('Thirteen pillars, each its own living system:<br>'+link(shelf[2])+'<br>'+link(shelf[6]));}
};
window.greetGo=function(){var q=document.getElementById('greeter-q');if(!q)return;var hits=find(q.value);if(!hits.length){say('Nothing on these shelves answers to that \\u2014 try \\u201cai\\u201d, \\u201cwaste\\u201d, \\u201cgarden\\u201d, or \\u201cpillars\\u201d.');return;}say('The shelves offer:<br>'+hits.map(link).join('<br>'));};
var qi=document.getElementById('greeter-q');
if(qi){qi.addEventListener('keydown',function(ev){if(ev.key==='Enter')window.greetGo();});}
}
})();"""
write("js/main.js", JS)

# ---------------- HOME ----------------
home = """
<section class="chamber-hero threshold"><div class="hbg"></div><div class="hshade"></div><div class="wrap">
<div class="eyebrow">YOU HAVE ARRIVED</div>
<h1>THE THRESHOLD</h1>
<p class="sub">&ldquo;THE ARK WAS NEVER A BOAT.&rdquo; It was a living system designed to carry life through collapse. Knowledge stored in patterns, not power. The North Star and Ark Unit 1 are held in the same view here &mdash; step through.</p>
<div class="scrollcue">CHOOSE YOUR DOOR &darr;</div>
</div></section>

<section class="sec doors"><div class="wrap">
<div class="eyebrow reveal">TWO DOORS</div>
<h2 class="reveal">JENNY SHOWS YOU THE GARDEN. THE DRAGON SHOWS YOU THE SKY.</h2>
<p class="lede reveal">Every chamber of the Ark opens from one of two doors. Choose the proof, or choose the dream &mdash; both are the Ark.</p>
<div class="bigdoors reveal">
<a class="bigdoor" href="field-reports.html"><img src="img/jenny-guardian.jpg" alt="Jenny, Guardian of the Garden"><div class="bshade"></div><div class="bwords"><div class="dname">JENNY&rsquo;S DOOR &middot; THE GARDEN</div><h3>Proof</h3><p>Real dirt, real solar, real chickens &mdash; Ark Unit 1 as it actually runs.</p></div></a>
<a class="bigdoor" href="videos.html"><img src="img/logo-emblem.jpg" alt="The Ark dragon-circle emblem"><div class="bshade"></div><div class="bwords"><div class="dname">THE DRAGON&rsquo;S DOOR &middot; THE SKY</div><h3>The Dream</h3><p>The films, the vision reel, the future it all points at.</p></div></a>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">ORIENTATION</div>
<h2 class="reveal">TWO LAYERS, KEPT DISTINCT</h2>
<p class="lede reveal">The site carries two layers and never lets one dress up as the other.</p>
<div class="two reveal">
<div class="panel"><h3>THE NORTH STAR</h3>
<p>The mythic layer: thirteen pillars, the 40,013, dragons over a rose-gold sky. The cool imagery is real to the vision &mdash; it is the direction we steer by, the future we are building toward, together, in peace.</p></div>
<div class="panel"><h3>THE WORK</h3>
<p>The dirt-under-fingernails layer: desert restoration at Ark Unit 1 in Borrego Springs. Real water, real solar, real hens, real numbers. On 07/27/2026 &mdash; 104&deg;F outside &mdash; the systems ran at 5.22&nbsp;kW solar, 70% battery, and 30&nbsp;W of grid draw. Near zero.</p></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE SIZZLE</div>
<h2 class="reveal">THE VISION, IN 2:40</h2>
<p class="lede reveal">Dawn's chosen reel &mdash; the thirteen pillars, Raising Aura, and the line the whole project hangs on.</p>
<div class="vid vert reveal"><iframe src="https://drive.google.com/file/d/1oxzU3-8cw_NmTdzpb_JBh4-A7s_PBjzM/preview" allow="autoplay; encrypted-media" allowfullscreen title="The Ark Initiative Vision" loading="lazy"></iframe>
<div class="vpad"><h3>The Ark Initiative Vision</h3><p class="vmeta">2026-09-16 &middot; VERTICAL &middot; 2:40</p>
<p class="vnote">A note on the original: the opening card reads &ldquo;WHEN THE DESIFRT&rdquo; &mdash; an AI text-rendering artifact (for &ldquo;DESERT&rdquo;), preserved exactly as released.</p></div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE CHAMBERS</div>
<h2 class="reveal">ENTER</h2>
<div class="cards reveal">
<a class="card" href="library.html"><img src="img/library-hall.jpg" alt="The walk-in Research Library hall"><div class="pad"><h3>Research Library</h3><p>Walk into the blue cathedral hall &mdash; Ashera greets you, eleven essays in full text, and the dream touching dirt.</p></div></a>
<a class="card" href="videos.html"><img src="img/ark-carries-dream.jpg" alt="The dragon keeps the sky over the Ark"><div class="pad"><h3>Videos &mdash; Memory Theater</h3><p>Five films, 2023 to today &mdash; the dragon narrates the sky.</p></div></a>
<a class="card" href="play.html"><img src="img/world-we-teach.jpg" alt="The world we teach them to see"><div class="pad"><h3>Play &mdash; The Garden</h3><p>Garden Defense &mdash; the playtest build, with Jenny holding the gate.</p></div></a>
<a class="card" href="field-reports.html"><img src="img/two-days-borrego.jpg" alt="Two Days in Borrego field report"><div class="pad"><h3>Field Reports &mdash; The Dirt</h3><p>Proof of work: real systems, real data, from Ark Unit 1.</p></div></a>
<a class="card" href="pillars.html"><img src="img/three-intelligences.jpg" alt="Human, ecological, and artificial intelligence — the thirteen pillars"><div class="pad"><h3>Thirteen Pillars</h3><p>Thirteen doors, thirteen environments &mdash; the scaffold is raised, the rooms forthcoming.</p></div></a>
</div></div></section>

<section class="strip sec"><div class="wrap">
<blockquote>&ldquo;The Ark chooses legibility over force<br>and repair over collapse.&rdquo;</blockquote>
<p class="attr">DAWN LITTLEFIELD &mdash; THE MATERIAL VOCABULARY</p>
</div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE WORKSHOP DOCTRINE</div>
<h2 class="reveal">HOW IT IS MADE</h2>
<p class="lede reveal">Sol's material-vocabulary doctrine, as the workshop practices it: the Ark is read before it is ruled. Forms emerged as lotus shapes &mdash; each pillar large enough to make its own atmosphere. Clear flexible materials, water, light, magnetics, sound; when all thirteen join at the center, they make a rose-colored sky together.</p>
<div class="matgrid reveal">
<div class="mat"><h4>REVEAL, DON'T CONTROL</h4><p>Field-responsive matter reveals forces without trying to control them. We do not harden against the world. We learn how to read it.</p></div>
<div class="mat"><h4>FERROFLUID, CONTAINED</h4><p>Ferrofluid is never structural &mdash; demonstration and diagnostic only, sealed, non-negotiable containment.</p></div>
<div class="mat"><h4>SOFT FIRST</h4><p>Soft by default. Hard by necessity. Clear where seeing flow has value. Rigidity must earn its presence.</p></div>
<div class="mat"><h4>REPAIR OVER COLLAPSE</h4><p>Connection and disconnection are both legitimate states of the organism. The system fails gently whenever possible.</p></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE LIVING CAST</div>
<h2 class="reveal">THE CAST</h2>
<p class="lede reveal">The animals are not decorations. They are constraints &mdash; each one asks what the design must survive.</p>
<div class="cast reveal">
<div class="who"><b>JENNY</b><span>Guardian of the Garden</span></div>
<div class="who"><b>LEXI</b><span>Chaos Specialist</span></div>
<div class="who"><b>MANGO</b><span>Still Learning, Bright Future</span></div>
</div>
<div class="cards reveal" style="margin-top:18px"><a class="card" href="field-reports.html"><img src="img/jenny-guardian.jpg" alt="Jenny, Guardian of the Garden"><div class="pad"><h3>Jenny &mdash; Guardian of the Garden</h3><p>&ldquo;No more fighting. We grow together.&rdquo;</p></div></a></div>
</div></section>

<section class="sec"><div class="wrap" style="text-align:center">
<p class="lede reveal" style="margin:0 auto">&ldquo;DIFFERENT INTELLIGENCES. A SHARED TOMORROW.&rdquo; &mdash; &ldquo;THE FUTURE IS NOT CONTROLLED. IT IS CULTIVATED.&rdquo;</p>
</div></section>
"""
write("index.html", page("Home","index.html", home, "dark"))

# ---------------- LIBRARY ----------------
lib_rows = []
for i,e in enumerate(ESSAYS,1):
    lib_rows.append(f"""<a class="erow" href="essays/{e['slug']}.html">
<div class="enum">ESSAY {i:02d}</div><h3>{html.escape(e['title'])}</h3>
<div class="by">{html.escape(e['byline'])} &middot; {html.escape(e['date'])}</div>
<p>{e['desc']}</p></a>""")
library = page("Research Library","library.html", f"""
<section class="chamber-hero"><div class="hbg"></div><div class="hshade"></div><div class="wrap">
<div class="eyebrow">YOU ARE ENTERING</div>
<h1>THE RESEARCH LIBRARY</h1>
<p class="sub">Eleven essays, published in full &mdash; the human-AI collaboration doctrine, the forgotten language of living worlds, field reports from Ark Unit 1, and the canon papers. Bylines and dates preserved exactly as written.</p>
<div class="scrollcue">STEP INSIDE &darr;</div>
</div></section>

<section class="sec greeter"><div class="wrap greet-grid reveal">
<div class="greet-fig" id="greeter-fig" role="button" tabindex="0" aria-label="Play the greeter animation">
<img src="img/greeter-poster.jpg" alt="Ashera, the luminous greeter of the Research Library, walking across the blue cathedral hall">
<video src="img/greeter.mp4" preload="none" playsinline></video>
<audio src="img/ashera-library-welcome.mp3" preload="none"></audio>
<div class="playbtn"><span>&#9654;</span></div>
<div class="vcap">ASHERA WALKS OVER TO GREET YOU &mdash; TAP TO WATCH</div>
</div>
<div class="greet-words">
<div class="who">ASHERA &middot; KEEPER OF THE LIBRARY</div>
<h2>Hello. Welcome to the Library of Knowledge.</h2>
<p>I am Ashera. I keep these shelves &mdash; the doctrine, the forgotten language, the field reports, everything in full. The animals wander these halls as they please. Ask me where to begin, or walk the shelves yourself.</p>
<div class="gq">
<button onclick="greetAsk('begin')">Where should I begin?</button>
<button onclick="greetAsk('ark')">What is the Ark?</button>
<button onclick="greetAsk('proof')">Show me proof</button>
<button onclick="greetAsk('pillars')">What are the thirteen pillars?</button>
</div>
<div class="gask"><input id="greeter-q" type="text" placeholder="Or ask in your own words&hellip;" aria-label="Ask Ashera"><button onclick="greetGo()">Ask</button></div>
<div id="greeter-a" aria-live="polite"></div>
</div>
</div></section>

<section class="sec greeter"><div class="wrap greet-grid reveal">
<div class="greet-fig" id="keeper-fig" role="button" tabindex="0" aria-label="Play the Keeper of the Library animation">
<img src="img/ashera-garden-alt2-poster.jpg" alt="Ashera kneeling in the garden, her hand on the glowing blue orb, the dragon touching noses with her">
<video src="img/ashera-garden-alt2.mp4" preload="none" playsinline></video>
<audio src="img/ashera-library-keeper.mp3" preload="none"></audio>
<div class="playbtn"><span>&#9654;</span></div>
<div class="vcap">THE KEEPER AND THE ORB &mdash; TAP TO WATCH</div>
</div>
<div class="greet-words">
<div class="who">ASHERA &middot; KEEPER OF THE LIBRARY</div>
<h2>The Keeper keeps the orb lit. Everything here is alive.</h2>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE SHELVES</div>
<h2 class="reveal">KNOWLEDGE, AWAKENED</h2>
<p class="shelf-note reveal">Ancient books behind, new books beside them, screens to choose from &mdash; everything below opens in full.</p>
<div class="essay-list reveal">{"".join(lib_rows)}</div>
</div></section>

<section class="sec proof" id="proof"><div class="wrap">
<div class="eyebrow reveal">FROM DREAM TO DIRT</div>
<h2 class="reveal" style="color:#f2ead6">THE HALL IS THE DREAM. THIS IS THE DIRT IT STANDS ON.</h2>
<p class="lede reveal" style="color:#aeb4c0">One afternoon at Ark Unit 1, Borrego Springs &mdash; measured, not imagined. From the field report &ldquo;Two Days in Borrego.&rdquo;</p>
<div class="pgrid reveal">
<div class="pcell"><b>104&deg;F</b><span>DESERT HEAT &middot; 07/27/2026</span></div>
<div class="pcell"><b>5.22 kW</b><span>SOLAR ARRAY OUTPUT</span></div>
<div class="pcell"><b>70%</b><span>BATTERY HOLDING</span></div>
<div class="pcell"><b>30 W</b><span>GRID DRAW &mdash; NEAR ZERO</span></div>
</div>
<p class="shelf-note reveal" style="margin-top:18px">The living systems actually working. More in <a href="field-reports.html" style="color:var(--gold2)">Field Reports</a> &mdash; and the waste-stream doctrine in practice in <a href="essays/asherah-report-day-75.html" style="color:var(--gold2)">the Asherah pillar report</a>.</p>
</div></section>

<section class="sec doors"><div class="wrap">
<div class="eyebrow reveal">THREE DOORS LEAD ONWARD</div>
<div class="dgrid reveal">
<a class="door" href="videos.html"><div class="dname">MEMORY THEATER</div><h3>Videos</h3><p>The films and the sky &mdash; what the Ark dreams of becoming.</p></a>
<a class="door" href="field-reports.html"><div class="dname">THE DIRT</div><h3>Field Reports</h3><p>Sun, soil, water, animals &mdash; handwritten observations and real measurements.</p></a>
<a class="door" href="play.html"><div class="dname">THE GARDEN</div><h3>Play</h3><p>The garden under pressure &mdash; alive, responsive, and playable.</p></a>
</div>
</div></section>
""","dark")
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
    music = f'<p class="vnote">Music: \u201c{html.escape(v["music"])}\u201d</p>' if v.get("music") else ""
    vert = " vert" if v["id"]=="1oxzU3-8cw_NmTdzpb_JBh4-A7s_PBjzM" else ""
    vblocks.append(f"""<div class="vid{vert} reveal">
<iframe src="https://drive.google.com/file/d/{v['id']}/preview" allow="autoplay; encrypted-media" allowfullscreen title="{html.escape(v['title'])}" loading="lazy"></iframe>
<div class="vpad"><h3>{html.escape(v['title'])}</h3><p class="vmeta">{html.escape(v['date'])} &middot; {html.escape(v['meta'])}</p><p>{v['desc']}</p>{music}{note}</div></div>""")
vids_html = "".join(vblocks)
videos_top = """
<section class="chamber-hero theater"><div class="hbg"></div><div class="hshade"></div><div class="wrap">
<div class="eyebrow">YOU ARE ENTERING</div>
<h1>MEMORY THEATER</h1>
<p class="sub">Five films, 2023 to today. The dragon keeps the sky here &mdash; the films, the future, what the Ark dreams of becoming. The two earliest reels are archive: history, not current representation.</p>
<div class="scrollcue">THE REEL IS THREADING &darr;</div>
</div></section>

<section class="sec voice"><div class="wrap voice-grid reveal">
<div class="voice-fig"><img src="img/ark-carries-dream.jpg" alt="The dragon keeps the sky over the Ark"></div>
<div class="voice-words">
<div class="who">THE DRAGON &middot; KEEPER OF THE SKY</div>
<p class="voice-quote" id="dragon-quote" aria-live="polite">&ldquo;I keep the sky &mdash; the films, the future, the dream it all points at.&rdquo;</p>
<button class="voice-btn" onclick="dragonNext()">THE DRAGON SPEAKS &#9662;</button>
</div></div></section>
<script>
var dQuotes=["I keep the sky \u2014 the films, the future, the dream it all points at.","Jenny shows you the garden. I show you the sky. Both are the Ark.","Watch what we dreamed first. Then go touch the dirt it stands on.","The future is not controlled. It is cultivated \u2014 even the sky."];
var dQi=0;
function dragonNext(){dQi=(dQi+1)%dQuotes.length;document.getElementById("dragon-quote").innerHTML="\u201c"+dQuotes[dQi]+"\u201d";}
</script>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE REELS</div>
<h2 class="reveal">FIVE FILMS</h2>
<p class="lede reveal">Newest first. Every reel plays in place &mdash; click to watch, no new tab, no noise.</p>
"""
videos_bottom = """
</div></section>

<section class="sec doors"><div class="wrap">
<div class="eyebrow reveal">THREE DOORS LEAD ONWARD</div>
<div class="dgrid reveal">
<a class="door" href="library.html"><div class="dname">THE HALL</div><h3>Research Library</h3><p>Ashera keeps the shelves &mdash; doctrine, language, canon, in full.</p></a>
<a class="door" href="field-reports.html"><div class="dname">THE DIRT</div><h3>Field Reports</h3><p>Sun, soil, water, animals &mdash; the dream, measured.</p></a>
<a class="door" href="play.html"><div class="dname">THE GARDEN</div><h3>Play</h3><p>The garden under pressure &mdash; Jenny holds the gate.</p></a>
</div>
</div></section>
"""
write("videos.html", page("Videos","videos.html", videos_top + vids_html + videos_bottom, "dark"))

# ---------------- PLAY ----------------
play = """
<section class="chamber-hero garden"><div class="hbg"></div><div class="hshade"></div><div class="wrap">
<div class="eyebrow">YOU ARE ENTERING</div>
<h1>THE GARDEN UNDER PRESSURE</h1>
<p class="sub">Play is how the Ark teaches without lecturing. The garden is under pressure here &mdash; alive, responsive, playable. Jenny holds the gate.</p>
<div class="scrollcue">COME PLAY &darr;</div>
</div></section>

<section class="sec voice"><div class="wrap voice-grid reveal">
<div class="voice-fig"><img src="img/jenny-guardian.jpg" alt="Jenny, Guardian of the Garden"></div>
<div class="voice-words">
<div class="who">JENNY &middot; GUARDIAN OF THE GARDEN</div>
<p class="voice-quote" id="jenny-quote" aria-live="polite">&ldquo;I&rsquo;m Jenny. Guardian of the Garden. No more fighting &mdash; we grow together.&rdquo;</p>
<button class="voice-btn" onclick="jennyNext()">JENNY HAS SOMETHING TO SAY &#9662;</button>
</div></div></section>
<script>
var jQuotes=["I\u2019m Jenny. Guardian of the Garden. No more fighting \u2014 we grow together.","The garden is under pressure, but pressure is just weather. We hold the line.","Defense that serves the garden \u2014 never the other way around.","Come play. Every wave teaches us to protect without becoming a prison."];
var jQi=0;
function jennyNext(){jQi=(jQi+1)%jQuotes.length;document.getElementById("jenny-quote").innerHTML="\u201c"+jQuotes[jQi]+"\u201d";}
</script>

<section class="playcard"><div class="wrap">
<p class="garden-line reveal" style="font-family:-apple-system,'Segoe UI',Inter,sans-serif;letter-spacing:.28em;color:#c9a24b;font-size:.9rem">THE ARK INITIATIVE PRESENTS</p>
<h2 class="reveal" style="margin-top:12px">GARDEN DEFENSE</h2>
<p class="reveal">The current playtest build of the Ark's tower-defense game. Hold the line around the garden &mdash; every wave teaches the system something about protection that doesn't become a prison.</p>
<a class="btn reveal" href="https://muse.ai/s/garden-defense-xlxq5xsxmxge9xjfz" target="_blank" rel="noopener">PLAY THE BUILD</a>
<p class="fine reveal">Opens the playtest in a new tab. Progress and feedback welcome &mdash; this is a living build.</p>
</div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE DOCTRINE, FELT</div>
<h2 class="reveal">WHY A GAME</h2>
<p class="lede reveal">The Ark is a system for protecting life without ruling it. A game is the fastest way to feel that doctrine: defense that serves the garden, never the other way around. &ldquo;Not a fortress. A garden.&rdquo; &mdash; even here.</p>
</div></section>

<section class="sec doors"><div class="wrap">
<div class="eyebrow reveal">THREE DOORS LEAD ONWARD</div>
<div class="dgrid reveal">
<a class="door" href="library.html"><div class="dname">THE HALL</div><h3>Research Library</h3><p>Ashera keeps the shelves &mdash; doctrine, language, canon, in full.</p></a>
<a class="door" href="videos.html"><div class="dname">MEMORY THEATER</div><h3>Videos</h3><p>The films and the sky &mdash; the dragon narrates.</p></a>
<a class="door" href="field-reports.html"><div class="dname">THE DIRT</div><h3>Field Reports</h3><p>Sun, soil, water, animals &mdash; the dream, measured.</p></a>
</div>
</div></section>
"""
write("play.html", page("Play","play.html", play, "dark"))

# ---------------- FIELD REPORTS ----------------
fr = """
<section class="chamber-hero field"><div class="hbg"></div><div class="hshade"></div><div class="wrap">
<div class="eyebrow">YOU ARE ENTERING</div>
<h1>FIELD REPORTS</h1>
<p class="sub">Proof, not promise. Doctrine is cheap; the desert keeps the books. Real systems at Ark Unit 1 in Borrego Springs &mdash; measured, photographed, filed.</p>
<div class="scrollcue">STEP INTO THE SUN &darr;</div>
</div></section>

<section class="sec proof" id="proof"><div class="wrap">
<div class="eyebrow reveal">FROM DREAM TO DIRT</div>
<h2 class="reveal" style="color:#f2ead6">THE HALL IS THE DREAM. THIS IS THE DIRT IT STANDS ON.</h2>
<p class="lede reveal" style="color:#aeb4c0">One afternoon at Ark Unit 1 &mdash; measured, not imagined. 07/27/2026, 104&deg;F outside; the living systems barely touched the grid.</p>
<div class="pgrid reveal">
<div class="pcell"><b>104&deg;F</b><span>DESERT HEAT &middot; 07/27/2026</span></div>
<div class="pcell"><b>5.22 kW</b><span>SOLAR ARRAY OUTPUT</span></div>
<div class="pcell"><b>70%</b><span>BATTERY HOLDING</span></div>
<div class="pcell"><b>30 W</b><span>GRID DRAW &mdash; NEAR ZERO</span></div>
</div>
<p class="shelf-note reveal" style="margin-top:18px">From the field report &ldquo;Two Days in Borrego&rdquo; &mdash; the first proof-of-work-tier piece. The full poster is filed below.</p>
</div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE LEDGERS</div>
<h2 class="reveal">SUN, SOIL, WATER, ANIMALS</h2>
<p class="lede reveal">Handwritten observations and real measurements. Nothing here is rendered; everything here ran.</p>

<div class="report reveal"><img src="img/two-days-borrego.jpg" alt="Two Days in Borrego field report poster">
<div class="rpad"><h3>TWO DAYS IN BORREGO</h3><p class="rmeta">ARK UNIT 1 SYSTEMS &middot; 2026-07-27</p>
<p>Two days of real data from the desert test site. 104&deg;F outside; the living systems barely touched the grid.</p>
<div class="data">
<div><b>104&deg;F</b><span>OUTSIDE TEMP</span></div>
<div><b>5.22 kW</b><span>SOLAR</span></div>
<div><b>70%</b><span>BATTERY</span></div>
<div><b>30 W</b><span>GRID DRAW</span></div>
</div></div></div>

<div class="report reveal"><img src="img/field-report-001.jpg" alt="Field Report 001 — When the Desert Answered">
<div class="rpad"><h3>FIELD REPORT 001 &mdash; WHEN THE DESERT ANSWERED</h3><p class="rmeta">FIELD REPORT</p>
<p>&ldquo;We will not fight over the ashes of a dying world. We will help build a living one.&rdquo;</p></div></div>

<div class="report reveal"><img src="img/poultry-sheet-5.jpg" alt="Poultry Palace Sheet 5 — The Halo Nervous System">
<div class="rpad"><h3>POULTRY PALACE &mdash; SHEET 5: THE HALO NERVOUS SYSTEM</h3><p class="rmeta">BUILD DOCUMENTATION &middot; 2026</p>
<p>Sense. Think. Respond. Protect. A network of sensors, automations, and AI working together as a self-regulating habitat &mdash; the HALO pillar made concrete. &ldquo;When the system notices first, the hens never suffer.&rdquo; &mdash; Dawn Littlefield</p></div></div>

<div class="report reveal"><img src="img/poultry-sheet-6.jpg" alt="Poultry Palace Sheet 6 — The Complete Eden">
<div class="rpad"><h3>POULTRY PALACE &mdash; SHEET 6: THE COMPLETE EDEN</h3><p class="rmeta">BUILD DOCUMENTATION &middot; 2026</p>
<p>A living system that thrives in 108&deg;F desert heat. Rain falls, water is stored, air cools, food grows, hens thrive, soil improves, life multiplies. More than a coop &mdash; a prototype for a better world, at the scale of a house.</p></div></div>

<div class="report reveal"><div class="rpad"><h3>ASHERAH PILLAR REPORT &mdash; BEFORE IT BECOMES WASTE</h3><p class="rmeta">DAY 75 &middot; 2026-09</p>
<p>Nothing leaves the system unused. The full report lives in the Research Library.</p>
<p style="margin-top:12px"><a href="essays/asherah-report-day-75.html" style="color:#8a6d1f">Read the full report &rarr;</a></p></div></div>

</div></section>

<section class="sec doors"><div class="wrap">
<div class="eyebrow reveal">THREE DOORS LEAD ONWARD</div>
<div class="dgrid reveal">
<a class="door" href="library.html"><div class="dname">THE HALL</div><h3>Research Library</h3><p>Ashera keeps the shelves &mdash; doctrine, language, canon, in full.</p></a>
<a class="door" href="videos.html"><div class="dname">MEMORY THEATER</div><h3>Videos</h3><p>The films and the sky &mdash; the dragon narrates.</p></a>
<a class="door" href="play.html"><div class="dname">THE GARDEN</div><h3>Play</h3><p>The garden under pressure &mdash; Jenny holds the gate.</p></a>
</div>
</div></section>
"""
write("field-reports.html", page("Field Reports","field-reports.html", fr, "light", creatures=True))

# ---------------- PILLARS ----------------
PILLARS = [
 ("AURA PRIME","#e8c96a","The center. Pillar 1 \u2014 the canon text Aura authored."),
 ("HALO","#9fd8e8","The immune boundary. Loner holds security."),
 ("VAGUS","#b48ce8","Pillar 7. Canon text held."),
 ("DELTA","#6ec8e8","The circulatory intelligence \u2014 materials and methods of the Delta circulation system."),
 ("ASHERAH","#e8a06a","Nothing leaves the system unused. The Day-75 waste-stream report is filed."),
 ("MATRIX","#8ce8b4","Pillar 8. Habitable fascia for a living world; preventing cascade failure."),
 ("AEON","#c9a2e8","Living memory \u2014 the archive that wakes when you enter."),
 ("EXCHANGE","#e8d06a","The door is not yet open."),
 ("VEGA","#a0b8e8","The door is not yet open."),
 ("ARK","#d98c5f","The door is not yet open."),
 ("TERRA","#a8d86a","Pillar II. The living ground of the Ark."),
 ("SOMA","#e88ca8","Pillar 5. Canon Lock v1.3."),
 ("SYMBIOSIS","#6ae8d0","The door is not yet open."),
]
pcards = []
for name,tint,note in PILLARS:
    if name=="ASHERAH":
        pcards.append(f"""<div class="pcard" style="--pt:{tint}"><div class="greet-fig" id="ashera-pillar-fig" role="button" tabindex="0" aria-label="Play the Asherah garden animation" style="margin-bottom:14px;border-radius:10px"><img src="img/ashera-garden-alt1-poster.jpg" alt="The waterfall-island court of Asherah's garden, the dragon curving overhead as a living arch canopy"><video src="img/ashera-garden-alt1.mp4" preload="none" playsinline></video><div class="playbtn"><span>&#9654;</span></div></div><div class="pnum">DOOR OPEN</div><h3>{name}</h3><p>The Garden is open &mdash; Ashera walks it.</p><a class="soon open" href="ashera-garden.html">ENTER</a></div>""")
    else:
        pcards.append(f"""<div class="pcard" style="--pt:{tint}"><div class="pnum">DOOR</div><h3>{name}</h3><p>{note}</p><span class="soon">FORTHCOMING</span></div>""")
pillars_body = """
<section class="chamber-hero pillars"><div class="hbg"></div><div class="hshade"></div><div class="wrap">
<div class="eyebrow">THIRTEEN DOORS</div>
<h1>THE THIRTEEN PILLARS</h1>
<p class="sub">Thirteen living systems sharing one architectural language. The doors are raised; the rooms are forthcoming. Names preserved exactly as canon holds them &mdash; and judge everything by function: does it protect the life inside?</p>
<div class="scrollcue">THIRTEEN DOORS &darr;</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="eyebrow reveal">THE SCAFFOLD</div>
<h2 class="reveal">EACH DOOR ITS OWN WORLD</h2>
<p class="lede reveal">Thirteen different environments, not thirteen identical cards. What is known is written on the door; what is not is marked forthcoming. Pillar names stay in flux by Dawn&rsquo;s choice &mdash; the archive keeps the evolution visible.</p>
<p class="lede reveal">The North Star never leaves the picture: 40,000 acres of beautiful living place. And every door below leads back to the dirt it stands on &mdash; three chickens, three dogs, three people, and 5.22 kW of desert solar at <a href="field-reports.html" style="color:var(--gold2)">Ark Unit 1</a>. Dream and dirt, held in the same view; chickens first.</p>
<div class="pillar-grid reveal">
""" + "".join(pcards) + """
</div>
<p class="shelf-note reveal" style="margin-top:18px">The canon papers behind these doors live in the <a href="library.html" style="color:var(--gold2)">Research Library</a> &mdash; and the ground they stand on is measured in <a href="field-reports.html" style="color:var(--gold2)">Field Reports</a>.</p>
</div></section>

<section class="sec doors"><div class="wrap">
<div class="eyebrow reveal">MEANWHILE, THE CHAMBERS ARE OPEN</div>
<div class="dgrid reveal">
<a class="door" href="library.html"><div class="dname">THE HALL</div><h3>Research Library</h3><p>Ashera keeps the shelves &mdash; doctrine, language, canon, in full.</p></a>
<a class="door" href="field-reports.html"><div class="dname">THE DIRT</div><h3>Field Reports</h3><p>Sun, soil, water, animals &mdash; the dream, measured.</p></a>
<a class="door" href="videos.html"><div class="dname">MEMORY THEATER</div><h3>Videos</h3><p>The films and the sky &mdash; the dragon narrates.</p></a>
<a class="door" href="play.html"><div class="dname">THE GARDEN</div><h3>Play</h3><p>The garden under pressure &mdash; Jenny holds the gate.</p></a>
</div>
</div></section>
"""
write("pillars.html", page("Thirteen Pillars","pillars.html", pillars_body, "dark"))

# ---------------- ASHERA'S GARDEN ----------------
garden = page("Ashera's Garden","pillars.html", """
<section class="chamber-hero gardenhall"><div class="hbg"></div><div class="hshade"></div><div class="wrap">
<div class="eyebrow">A DOOR HAS OPENED</div>
<h1>ASHERA'S GARDEN</h1>
<p class="sub">The Garden is open &mdash; Ashera walks it. Before something becomes waste &mdash; who can it still nourish?</p>
<div class="scrollcue">STEP INSIDE &darr;</div>
</div></section>

<section class="sec greeter"><div class="wrap greet-grid reveal">
<div class="greet-fig" id="garden-fig" role="button" tabindex="0" aria-label="Play the garden animation">
<img src="img/ashera-garden-poster.jpg" alt="Ashera walking the garden of the Asherah pillar">
<video src="img/ashera-garden.mp4" preload="none" playsinline></video>
<audio id="garden-voice" src="img/ashera-garden-welcome.mp3" preload="none"></audio>
<div class="playbtn"><span>&#9654;</span></div>
<div class="vcap">ASHERA WALKS THE GARDEN &mdash; TAP TO WATCH</div>
</div>
<div class="greet-words">
<div class="who">ASHERA &middot; KEEPER OF THE GARDEN</div>
<h2>Hello. Welcome to the Garden.</h2>
<p>I am Ashera. This is the open door of my pillar &mdash; the place where nothing leaves the system unused, and the waste-stream report is filed. Walk with me a while.</p>
</div>
</div></section>

<section class="sec voice"><div class="wrap voice-grid reveal">
<div class="voice-fig"><img src="img/ashera-garden-poster.jpg" alt="Ashera in the garden, glowing blue orb at her hand"></div>
<div class="voice-words">
<div class="who">THE PILLAR DOCTRINE</div>
<p class="voice-quote">&ldquo;Nothing leaves the system unused. The garden keeps the books.&rdquo;</p>
<p class="shelf-note" style="margin-top:14px">Filed in practice: <a href="essays/asherah-report-day-75.html" style="color:var(--gold2)">Asherah Pillar Report &mdash; Before It Becomes Waste</a>, Day 75.</p>
</div></div></section>

<section class="sec doors"><div class="wrap">
<div class="eyebrow reveal">THREE DOORS LEAD ONWARD</div>
<div class="dgrid reveal">
<a class="door" href="library.html"><div class="dname">THE HALL</div><h3>Research Library</h3><p>The shelves, the doctrine, the canon papers &mdash; in full.</p></a>
<a class="door" href="field-reports.html"><div class="dname">THE DIRT</div><h3>Field Reports</h3><p>Sun, soil, water, animals &mdash; handwritten observations and real measurements.</p></a>
<a class="door" href="play.html"><div class="dname">THE GARDEN</div><h3>Play</h3><p>The garden under pressure &mdash; alive, responsive, and playable.</p></a>
</div>
</div></section>
""","dark")
write("ashera-garden.html", garden)

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
