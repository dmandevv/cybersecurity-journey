# Security+ SY0-701

Working through **every term** in the official CompTIA Security+ exam objectives, one at a time, and writing each one down in my own words.

**The source is in this repo:** [`comptia-security-plus-sy0-701-exam-objectives.pdf`](comptia-security-plus-sy0-701-exam-objectives.pdf) — SY0-701 V7, Document Version 7.0. The exam is graded against that document, so the checklist **is** that document: [`objectives/`](objectives/) holds one file per objective, generated from the PDF rather than typed out, because 797 terms typed by hand is 797 chances to quietly drop one.

## Test details

| | |
|---|---|
| Exam | **SY0-701** (V7) |
| Questions | Maximum of 90, multiple-choice and performance-based |
| Length | 90 minutes |
| Domains | 5 · **28 objectives** · **797 terms** |

**⚠️ Timing matters on this one.** SY0-701 retires **11 June 2027**, and its replacement SY0-801 goes live **17 November 2026**. Both exams certify the same thing for three years and employers do not distinguish between them, so the plan is to sit **SY0-701** — but everything here is written against the 701 objectives, and that window is the deadline.

**⚠️ The bulleted lists are explicitly not exhaustive.** CompTIA says so in the document: the exam may test things in an objective that are not listed under it. Complete coverage of this checklist is the floor, not the ceiling.

## Domains

| Domain | Weight | Objectives | Terms |
|---|---|---|---|
| 1 — General Security Concepts | 12% | 4 | 111 |
| 2 — Threats, Vulnerabilities, and Mitigations | 22% | 5 | 150 |
| 3 — Security Architecture | 18% | 4 | 128 |
| 4 — Security Operations | **28%** | 9 | 247 |
| 5 — Security Program Management and Oversight | 20% | 6 | 161 |

**Domain 4 is the largest**, and it is also the one the homelab exercises directly — alerting, monitoring, log sources, incident response, hardening. **Domain 5 is the second largest and the one nothing in the lab touches**: governance, risk, compliance, audits, vendor management. Expect that one to need deliberate reading rather than recognition.

## How a session runs

**Order is domain order**, 1.1 through 5.6, except where the homelab has already covered something — those get confirmed rather than taught.

**1. One term at a time.** The term is explained, then written into its objective file in my own words, then the box is ticked. A term is not done because it was read — it is done when it can be explained without looking.

**2. Check online for sources that can be used to explore the term and/or apply it to real world** User wants real world practice with the term: short course/lab online (MUST BE FREE), practicing using a command on personal PC

**3. Quizzes come at the end of each objective**, questions delivered one at a time, and at the end of each domain as a longer set. **Misses get written up in the objective file**, not just re-read: the miss pattern is the study plan.

**Mock exams come last**, in the weeks before test day, and only full 90-question timed ones. A mock taken early measures nothing except how much has not been covered yet.

**⚠️ No brain dumps.** CompTIA revokes certifications and bans candidates for using leaked exam questions, and says so on page 2 of the objectives document. Practice questions come from legitimate sources — Professor Messer, CertMaster, ExamCompass and similar — or they are written fresh.

## Layout

```
comptia-security-plus-sy0-701-exam-objectives.pdf   the source of truth
objectives/
├── README.md                     index and progress, one line per objective
├── 1.1-security-controls.md      every term, as a checklist, notes underneath
└── ...                           28 files
tools/build-objectives.py         regenerates the above from the PDF
progress.md						  Daily log and progress tracker
```

**`build-objectives.py` never overwrites notes** — it skips files that already exist unless forced. It exists so the structure is reproducible if CompTIA reissues the document, not to be run routinely.