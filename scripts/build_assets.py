#!/usr/bin/env python3
"""Builds the SVG images in assets/light and assets/dark that README.md uses.

All the text in the images lives in this file. Edit it, then run:

    python3 scripts/build_assets.py

Standard library only. The images have transparent backgrounds; GitHub shows
the light or dark set to match the viewer's theme.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "assets"

SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
FAMILIES = {"serif": SERIF, "sans": SANS, "mono": MONO}

THEMES = {
    "light": {"ink": "#111111", "body": "#3D3D3D", "muted": "#737373", "rule": "#D9D9D9", "accent": "#C2410C"},
    "dark": {"ink": "#F0F0F0", "body": "#C9C9C9", "muted": "#8D8D8D", "rule": "#30363D", "accent": "#FB923C"},
}

W = 1200

# =============================================================== content

HERO = {
    "name": "Mayank Gupta",
    "topright": "GenAI Engineer  ·  Gandhinagar, India",
    # (text, accent) pieces per line; accent pieces are set in italic.
    "headline": [
        [("I build retrieval systems,", False)],
        [("agents and MCP servers", False)],
        [("that run in ", False), ("production.", True)],
    ],
    "facts": [
        ("NOW", "Building ctxbook, an open-source memory server for MCP clients"),
        ("BACKGROUND", "5+ years of Python: APIs, then ML, then GenAI"),
        ("OPEN TO", "Senior GenAI / AI Engineer roles, remote or hybrid"),
    ],
}

SECTIONS = {
    "about": ("01", "About", "Who I am"),
    "work": ("02", "Selected work", "Things I've built"),
    "stack": ("03", "Stack", "Tools I reach for"),
}

FEATURED = {
    "kicker": "01  ·  OPEN SOURCE  ·  IN DEVELOPMENT",
    "title": "ctxbook",
    "summary": "A local-first memory server that every MCP client shares. Tell Claude Code your project "
               "uses Postgres and Cursor knows it too. Move to MongoDB and the old fact is replaced, "
               "not duplicated.",
    "facts": [
        ("BUILT", "Fact history, hybrid keyword + semantic search, conflict handling, 6 MCP tools and a CLI"),
        ("NEXT", "One-command client setup, an evaluation suite, then v0.1 on PyPI"),
        ("STACK", "Python, FastMCP"),
    ],
    "link": "github.com/ms7199/ctxbook",
    "clients": ["Claude Code", "Cursor", "Claude Desktop"],
    "caption": "Fig. 1   Every client reads and writes the same memory.",
}

PROJECTS = [
    {
        "file": "project-hr.svg", "num": "02", "title": "HR Assistant", "kind": "CLIENT WORK", "linked": False,
        "description": "An assistant for HR teams that calls SharePoint, Confluence and Outlook as MCP tools, "
                       "so answers come from the source systems instead of a stale copy, with each tool "
                       "scoped to what it may touch.",
        "stack": ["LangChain", "MCP", "FastAPI", "AWS"],
    },
    {
        "file": "project-docubot.svg", "num": "03", "title": "docubot-slack", "kind": "OPEN SOURCE", "linked": True,
        "description": "A Slack bot that answers questions from your PDFs using RAG. It keeps conversation "
                       "context and reloads the knowledge base without a restart.",
        "stack": ["Groq · Llama 3.3", "Pinecone", "Hugging Face", "Slack API"],
    },
    {
        "file": "project-memory.svg", "num": "04", "title": "Memory Assistant", "kind": "PROJECT", "linked": False,
        "description": "Long- and short-term memory for a chat assistant. Memories are scored, pruned and "
                       "recalled semantically, so it remembers users without its context growing forever.",
        "stack": ["LangChain", "Groq", "Pinecone", "MongoDB", "Next.js"],
    },
]

STACK = [
    ("LLMS & AGENTS", ["OpenAI, Groq", "LangChain", "LangGraph", "MCP / FastMCP", "Guardrails", "Hugging Face"]),
    ("RETRIEVAL & ML", ["Pinecone, FAISS", "Hybrid search", "Sentence-Transformers", "PyTorch, scikit-learn",
                        "Transformers, spaCy", "MLflow"]),
    ("BACKEND", ["Python", "FastAPI, Django REST", "Node.js, Express", "Celery, Redis", "PostgreSQL, MongoDB",
                 "JWT / OAuth2"]),
    ("CLOUD", ["AWS: EC2, Lambda, S3", "Azure", "Docker", "CI/CD", "DynamoDB"]),
]

CONTACT = {
    "line1": "Building something with LLMs?",
    "line2": "Let's talk.",
    "email": "guptamayank7199@gmail.com",
    "footer_left": "© 2026 Mayank Gupta",
    "footer_right": "Gandhinagar, India  ·  Remote or hybrid",
}

# ========================================================== text metrics

_W = {" ": 278, ".": 278, ",": 278, "·": 278, "-": 333, "/": 278, ":": 278, ";": 278, "(": 333, ")": 333,
      "&": 667, "+": 584, "'": 191, "@": 1015, "_": 556, "!": 278, "?": 556, "©": 737}
_W.update(zip("abcdefghijklmnopqrstuvwxyz",
              [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
               556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
              [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
               722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({d: 556 for d in "0123456789"})


def width(s, size, family="sans", weight=400, spacing=0.0):
    """Estimated rendered width, used for wrapping and placement (errs wide)."""
    gaps = spacing * max(len(s) - 1, 0)
    if family == "mono":
        return len(s) * size * 0.6 + gaps
    em = sum(_W.get(c, 600) for c in s) / 1000
    factor = {"serif": 1.12, "sans": 1.04}[family] * (1.05 if weight >= 600 else 1.0)
    return em * size * factor + gaps


def wrap(s, size, max_w, family="sans"):
    lines, line = [], ""
    for word in s.split():
        candidate = f"{line} {word}".strip()
        if line and width(candidate, size, family) > max_w:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines

# =========================================================== svg helpers


def _attrs(x, y, size, family, weight, anchor, spacing, italic, s=""):
    a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-family="{FAMILIES[family]}"',
         f'font-size="{size:g}"', f'font-weight="{weight}"']
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if spacing:
        a.append(f'letter-spacing="{spacing}"')
    if italic:
        a.append('font-style="italic"')
    if "  " in s:
        a.append('style="white-space:pre"')
    return " ".join(a)


def t(x, y, s, size, fill, family="sans", weight=400, anchor="start", spacing=0, italic=False):
    return f'<text {_attrs(x, y, size, family, weight, anchor, spacing, italic, s)} fill="{fill}">{escape(s)}</text>'


def spans(x, y, parts, size, P, family="serif", spacing=-0.5):
    """One line made of (text, accent) pieces; accent pieces are italic and coloured."""
    inner = ""
    for s, accent in parts:
        style = f' fill="{P["accent"]}" font-style="italic"' if accent else f' fill="{P["ink"]}"'
        inner += f"<tspan{style}>{escape(s)}</tspan>"
    return f'<text {_attrs(x, y, size, family, 400, "start", spacing, False)}>{inner}</text>'


def rule(y, color, x=0, w=W):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="1" fill="{color}"/>'


def write(theme, name, h, body, label, defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h:.0f}" viewBox="0 0 {W} {h:.0f}" '
           f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
           f'{f"<defs>{defs}</defs>" if defs else ""}{body}</svg>\n')
    (ROOT / theme / name).write_text(svg, encoding="utf-8")

# ================================================================ pieces


def hero(P):
    b = [t(0, 30, HERO["name"], 20, P["ink"], "sans", 600),
         t(W, 30, HERO["topright"], 15, P["muted"], "mono", anchor="end"),
         rule(54, P["rule"])]

    # Headline: largest size (max 64) at which every line fits the left column.
    col = 780
    widest = max(width("".join(s for s, _ in parts), 1, "serif") for parts in HERO["headline"])
    size = min(64, int(col / widest))
    x, fy = 880, 118
    last_baseline = fy
    for label, value in HERO["facts"]:
        b.append(t(x, fy, label, 14, P["muted"], "mono", spacing=1.5))
        lines = wrap(value, 19, W - x)
        for i, line in enumerate(lines):
            b.append(t(x, fy + 30 + i * 27, line, 19, P["body"]))
        last_baseline = fy + 30 + (len(lines) - 1) * 27
        fy += 30 + len(lines) * 27 + 26

    n = len(HERO["headline"])
    facts_mid = (fy - (fy - 118) - 11 + last_baseline + 5) / 2
    y = facts_mid - (n - 1) * size * 0.6 + size * 0.25
    for parts in HERO["headline"]:
        b.append(spans(0, y, parts, size, P))
        y += size * 1.2
    h = max(y, fy) + 10
    b.insert(3, f'<rect x="840" y="92" width="1" height="{h - 110:.0f}" fill="{P["rule"]}"/>')
    label = f'{HERO["name"]}, {HERO["topright"].replace("  ", " ")}. ' + \
        " ".join("".join(s for s, _ in p) for p in HERO["headline"]) + " " + \
        " ".join(f"{k.title()}: {v}." for k, v in HERO["facts"])
    return "hero.svg", h, "".join(b), label, ""


def section(P, key):
    num, title, note = SECTIONS[key]
    b = [rule(10, P["rule"]),
         t(0, 72, f"({num})", 16, P["muted"], "mono"),
         t(84, 74, title, 46, P["ink"], "serif", spacing=-0.5),
         t(W, 72, note, 15, P["muted"], "mono", anchor="end")]
    return f"section-{key}.svg", 104, "".join(b), f"{num} {title}", ""


def featured(P):
    f = FEATURED
    ink, muted, body = P["ink"], P["muted"], P["body"]
    b = [t(0, 40, f["kicker"], 14, P["accent"], "mono", spacing=1.5),
         t(0, 108, f["title"], 58, ink, "serif", spacing=-0.5)]
    y = 160
    for line in wrap(f["summary"], 21, 540):
        b.append(t(0, y, line, 21, body))
        y += 32
    y += 14
    for label, value in f["facts"]:
        b.append(rule(y, P["rule"], 0, 560))
        lines = wrap(value, 18, 440)
        for i, line in enumerate(lines):
            b.append(t(110, y + 32 + i * 27, line, 18, body))
        b.append(t(0, y + 32, label, 13, muted, "mono", spacing=1.5))
        y += 32 + (len(lines) - 1) * 27 + 20
    b.append(rule(y, P["rule"], 0, 560))
    link = f["link"] + "  ↗"
    b.append(t(0, y + 48, link, 16, P["accent"], "mono"))
    b.append(rule(y + 55, P["accent"], 0, width(link, 16, "mono")))
    left_end = y + 70

    # Fig. 1: line drawing of clients -> ctxbook -> local store
    fx, fw = 650, 550
    cx = fx + fw / 2
    bw, bh, gap = 160, 48, 15
    bx0 = fx + (fw - (bw * 3 + gap * 2)) / 2
    stroke = f'fill="none" stroke="{ink}" stroke-width="1.5"'
    mids = []
    for i, name in enumerate(f["clients"]):
        bx = bx0 + i * (bw + gap)
        mid = bx + bw / 2
        mids.append(mid)
        b.append(f'<rect x="{bx:.1f}" y="40" width="{bw}" height="{bh}" {stroke}/>')
        b.append(t(mid, 70, name, 17, ink, "sans", anchor="middle"))
        b.append(f'<path d="M{mid:.1f} {40 + bh} V140" {stroke}/>')
    b.append(f'<path d="M{mids[0]:.1f} 140 H{mids[-1]:.1f}" {stroke}/>')
    b.append(f'<path d="M{cx:.1f} 140 V188" {stroke} marker-end="url(#arrow)"/>')
    b.append(t(cx + 10, 170, "MCP", 12, muted, "mono", spacing=1))
    b.append(f'<rect x="{cx - 120:.1f}" y="192" width="240" height="72" {stroke}/>')
    b.append(f'<rect x="{cx - 114:.1f}" y="198" width="228" height="60" fill="none" stroke="{P["rule"]}"/>')
    b.append(t(cx, 228, f["title"], 24, ink, "serif", anchor="middle"))
    b.append(t(cx, 250, "MCP server", 13, muted, "mono", anchor="middle"))
    b.append(f'<path d="M{cx:.1f} 268 V312" {stroke} marker-start="url(#arrow)" marker-end="url(#arrow)"/>')
    top, bottom = 330, 404
    b.append(f'<path d="M{cx - 120:.1f} {top} V{bottom} A120 14 0 0 0 {cx + 120:.1f} {bottom} V{top}" {stroke}/>')
    b.append(f'<ellipse cx="{cx:.1f}" cy="{top}" rx="120" ry="14" {stroke}/>')
    b.append(t(cx, 374, "Local store", 17, ink, "sans", anchor="middle"))
    b.append(t(cx, 396, "facts · history · search", 12, muted, "mono", anchor="middle"))
    b.append(t(fx, 470, f["caption"], 17, muted, "serif", italic=True))

    defs = (f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M0 1 9 5 0 9" fill="none" stroke="{ink}" stroke-width="1.5"/></marker>')
    h = max(left_end, 490)
    label = f'{f["title"]}: {f["summary"]} ' + " ".join(f"{k.title()}: {v}." for k, v in f["facts"])
    return "project-ctxbook.svg", h, "".join(b), label, defs


def project(P, p, last):
    desc = wrap(p["description"], 19, 420)
    rows = max(len(desc), len(p["stack"]), 3)
    h = 56 + rows * 28 + 24
    b = [rule(0, P["rule"]),
         t(0, 54, p["num"], 16, P["muted"], "mono"),
         t(84, 58, p["title"], 34, P["ink"], "serif", spacing=-0.3),
         t(84, 92, p["kind"], 13, P["muted"], "mono", spacing=1.5)]
    if p["linked"]:
        b.append(t(84 + width(p["title"], 34, "serif") + 6, 56, "↗", 24, P["accent"]))
    for i, line in enumerate(desc):
        b.append(t(480, 54 + i * 28, line, 19, P["body"]))
    for i, item in enumerate(p["stack"]):
        b.append(t(W, 54 + i * 28, item, 14, P["muted"], "mono", anchor="end"))
    if last:
        b.append(rule(h - 1, P["rule"]))
    return p["file"], h, "".join(b), f'{p["title"]} ({p["kind"].lower()}): {p["description"]}', ""


def stack(P):
    colw = W / len(STACK)
    rows = max(len(items) for _, items in STACK)
    b = []
    for i, (label, items) in enumerate(STACK):
        x = i * colw
        b.append(t(x, 24, label, 14, P["muted"], "mono", spacing=1.5))
        for j, item in enumerate(items):
            b.append(t(x, 70 + j * 34, item, 20, P["body"]))
    h = 70 + (rows - 1) * 34 + 20
    label = " ".join(f'{label.title()}: {", ".join(items)}.' for label, items in STACK)
    return "stack.svg", h, "".join(b), label, ""


def contact(P):
    c = CONTACT
    b = [rule(10, P["rule"]),
         t(0, 112, c["line1"], 62, P["ink"], "serif", spacing=-0.5),
         spans(0, 188, [(c["line2"], True)], 62, P),
         t(0, 258, c["email"], 22, P["ink"], "mono"),
         rule(266, P["accent"], 0, width(c["email"], 22, "mono")),
         f'<rect x="0" y="267" width="{width(c["email"], 22, "mono"):.1f}" height="1" fill="{P["accent"]}"/>',
         rule(310, P["rule"]),
         t(0, 344, c["footer_left"], 14, P["muted"], "mono"),
         t(W, 344, c["footer_right"], 14, P["muted"], "mono", anchor="end")]
    return "contact.svg", 360, "".join(b), f'{c["line1"]} {c["line2"]} {c["email"]}', ""


def main():
    for theme, P in THEMES.items():
        (ROOT / theme).mkdir(parents=True, exist_ok=True)
        pieces = [hero(P), featured(P), stack(P), contact(P)]
        pieces += [section(P, key) for key in SECTIONS]
        pieces += [project(P, p, last=False) for p in PROJECTS]
        for name, h, body, label, defs in pieces:
            write(theme, name, h, body, label, defs)
        print(f"assets/{theme}/: {', '.join(p[0] for p in pieces)}")


if __name__ == "__main__":
    main()
