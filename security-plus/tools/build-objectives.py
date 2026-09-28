#!/usr/bin/env python3
"""Turn the official SY0-701 objectives PDF into one checklist file per objective.

    python3 tools/build-objectives.py            # report only
    python3 tools/build-objectives.py --write    # (re)generate objectives/

Run it once to scaffold the study guide, and again only if CompTIA reissues the
PDF. **It will not overwrite notes** — files that already exist are left alone
unless --force is passed, so regenerating never destroys written work.

Why this exists rather than a hand-typed list: the exam is graded against the
objectives document, so the checklist has to be the objectives document. 797
terms typed by hand would be 797 chances to silently drop one.

Extraction notes, because the PDF fights back:
  * The objectives are laid out in three columns at x ≈ 59 / 237 / 415. Reading
    the page in raw order interleaves them, so words are grouped into lines by
    their y coordinate, then into columns by x, and each column is read top to
    bottom before moving right.
  * An objective's number sits alone in the left margin (x ≈ 31), level with its
    title — sometimes rounding to the same y as the title and sometimes not, so
    both forms are handled.
  * Bullet depth is carried by the glyph: • top level, − second, ◦ third.
  * The running header and footer repeat on every page and would otherwise be
    appended to whatever term ends the page.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PDF = HERE / "comptia-security-plus-sy0-701-exam-objectives.pdf"
OUT = HERE / "objectives"

BULLETS = {"•": 0, "−": 1, "◦": 2}
COLUMNS = (59.3, 237.2, 415.0)
HEADER = re.compile(r"^([1-5]\.[1-9])(?:\s+(\S.*))?$")
CHROME = re.compile(r"^(CompTIA Security\+ SY0-701|Exam Objectives Document|Copyright ©)")

DOMAINS = {
    "1": ("General Security Concepts", "12%"),
    "2": ("Threats, Vulnerabilities, and Mitigations", "22%"),
    "3": ("Security Architecture", "18%"),
    "4": ("Security Operations", "28%"),
    "5": ("Security Program Management and Oversight", "20%"),
}

STOPWORDS = {"a", "an", "and", "the", "of", "to", "in", "for", "with", "various", "common",
             "types", "given", "scenario", "explain", "summarize", "compare", "contrast",
             "importance", "purpose", "elements", "concepts", "processes", "associated",
             "different", "appropriate", "implement", "maintain", "apply", "use", "using",
             "modify", "analyze", "related", "activities", "strategies", "impact", "that"}


def unescape(text):
    for entity, char in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                         ("&quot;", '"'), ("&apos;", "'")):
        text = text.replace(entity, char)
    return text


def fragments(page):
    """Group a page's words into (y, x, text) runs, splitting on column gaps."""
    word = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="[\d.]+">(.*?)</word>')
    rows = {}
    for x0, y0, x1, text in word.findall(page):
        rows.setdefault(round(float(y0)), []).append((float(x0), float(x1), unescape(text)))

    out = []
    for y in sorted(rows):
        run = []
        for w in sorted(rows[y]):
            if run and w[0] - run[-1][1] > 18:          # a gap this wide is a column break
                out.append((y, run[0][0], " ".join(t for _, _, t in run)))
                run = []
            run.append(w)
        if run:
            out.append((y, run[0][0], " ".join(t for _, _, t in run)))
    # y > 60 drops the running page header; CHROME drops the footer block
    return [f for f in out if f[0] > 60 and not CHROME.match(f[2])]


def parse():
    xml = subprocess.run(["pdftotext", "-bbox", str(PDF), "-"],
                         capture_output=True, text=True, check=True).stdout
    pages = re.findall(r'<page width="[\d.]+" height="[\d.]+">(.*?)</page>', xml, re.S)
    last = next(i for i, p in enumerate(pages) if "Acronym" in p and "List" in p)

    objectives = []
    for page in pages[:last]:
        frags = fragments(page)
        heads = [(f, HEADER.match(f[2])) for f in frags if f[1] < 45 and HEADER.match(f[2])]
        consumed = set()

        for (y, _, _), match in heads:
            title = match.group(2)
            if not title:                               # number alone: the title sits beside it
                beside = min((f for f in frags if 45 <= f[1] < 70 and abs(f[0] - y) <= 8),
                             key=lambda f: abs(f[0] - y), default=None)
                if beside:
                    title = beside[2]
                    consumed.add((beside[0], beside[1]))
            objectives.append({"id": match.group(1), "title": (title or "").strip(), "terms": []})

        edges = [f[0] for f, _ in heads] + [10 ** 6]
        bands = [(61, edges[0], None)]
        bands += [(heads[i][0][0], edges[i + 1], heads[i][1].group(1)) for i in range(len(heads))]

        for top, bottom, oid in bands:
            target = (next((o for o in reversed(objectives) if o["id"] == oid), None) if oid
                      else (objectives[-1] if objectives else None))
            if target is None:
                continue
            band = [f for f in frags if top <= f[0] < bottom
                    and (f[0], f[1]) not in consumed and not HEADER.match(f[2])]
            for column in range(3):
                in_column = [f for f in band
                             if min(range(3), key=lambda i: abs(f[1] - COLUMNS[i])) == column]
                for _, _, text in sorted(in_column):
                    if text[:1] in BULLETS:
                        target["terms"].append([BULLETS[text[0]], text[1:].strip()])
                    elif target["terms"]:
                        target["terms"][-1][1] += " " + text     # a wrapped line
    return objectives


def slug(objective):
    words = [w.strip(",.()/") for w in objective["title"].lower().split()]
    keep = [w for w in words if w and w not in STOPWORDS][:4]
    return f"{objective['id']}-" + "-".join(keep or ["objective"]) + ".md"


def render(objective, count):
    domain, weight = DOMAINS[objective["id"][0]]
    lines = [
        f"# {objective['id']} — {objective['title']}",
        "",
        f"**Domain {objective['id'][0]} — {domain}** · {weight} of the exam · "
        f"**{count} terms** from the official objectives.",
        "",
        "Every term below is quoted from the SY0-701 objectives document, version 7.0. "
        "Tick a box once the term can be explained without looking, and write the "
        "explanation underneath it.",
        "",
    ]
    for level, term in objective["terms"]:
        lines.append(f"{'  ' * level}- [ ] {'**' + term + '**' if level == 0 else term}")
    lines.append("")
    return "\n".join(lines)


def main():
    objectives = parse()
    total = sum(len(o["terms"]) for o in objectives)
    print(f"{len(objectives)} objectives, {total} terms")

    expected = [f"{d}.{n}" for d, count in (("1", 4), ("2", 5), ("3", 4), ("4", 9), ("5", 6))
                for n in range(1, count + 1)]
    missing = [e for e in expected if e not in [o["id"] for o in objectives]]
    if missing:
        sys.exit(f"missing objectives: {missing}")

    if "--write" not in sys.argv:
        for o in objectives:
            print(f"  {o['id']:4} {len(o['terms']):>3}  {o['title'][:60]}")
        return

    OUT.mkdir(exist_ok=True)
    index = ["# SY0-701 Objectives", "",
             "One file per objective, every term taken from the official objectives document "
             "(version 7.0, in this repo). Generated by `tools/build-objectives.py` — the exam "
             "is graded against this document, so the checklist is this document.", ""]
    for domain, (name, weight) in DOMAINS.items():
        index += [f"### {domain}.0 {name} — {weight}", ""]
        for o in [x for x in objectives if x["id"].startswith(domain)]:
            path = OUT / slug(o)
            if not path.exists() or "--force" in sys.argv:
                path.write_text(render(o, len(o["terms"])), encoding="utf-8")
            index.append(f"- [ ] [{o['id']} {o['title']}]({path.name}) — {len(o['terms'])} terms")
        index.append("")
    index += [f"**{len(objectives)} objectives, {total} terms total.**", ""]
    (OUT / "README.md").write_text("\n".join(index), encoding="utf-8")
    (OUT / ".objectives.json").write_text(json.dumps(objectives, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {len(objectives) + 1} files to {OUT}")


if __name__ == "__main__":
    main()
