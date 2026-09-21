# Daily Routine

**The working guide for the whole journey** — what to work on each day, and where every track currently stands. Moved here from the Network+ repo on 2026-09-17: it had grown to cover the homelab, simulated labs and parked SOC-analyst work, which made it the journey's routine rather than one exam's.

Training sources, rankings and free-tier notes live in **[practice-resources.md](https://github.com/dmandevv/soc-python-network-plus/blob/main/practice-resources.md)** — this file only says **what to work on and where each track stands.**

Claude follows this file to pick up where things left off, and updates *Where things stand* as blocks are completed. **The homelab's position is tracked privately**, in the homelab repo's `progress.md`.

## The shape of a day

**The blocks are a continuous loop, not a daily reset.** Work down the list in order; a day ends wherever it ends, and the next session picks up at the **next** block. After block 3 it wraps to block 1.

```
  1  Certification  →  2  Simulated lab  →  3  Homelab
  ↑                                                  │
  └──────────────────────────────────────────────────┘
```

| Block | Track | Currently |
|---|---|---|
| **1** | **Certification** — one objective section of the current exam | **Network+** — the walkthrough in [soc-python-network-plus/objectives](https://github.com/dmandevv/soc-python-network-plus/tree/main/objectives) |
| **2** | **Simulated lab** — one scenario, built and verified | **Packet Tracer** — queue below |
| **3** | **Homelab — 2 hours**, built problem-first | The build itself, which **doubles as Domain 5 practice** |

**The blocks are defined by role, not by tool,** so the structure outlives each exam. Block 1 follows the journey's step order — Network+ now, then Security+, then CCDL1 — and block 2 moves from Packet Tracer to Containerlab once Network+ is behind it.

**Built 2026-09-10 around one goal: mostly hands-on learning.** **Restructured 2026-09-18 to three blocks:** troubleshooting practice folded into the homelab, because **a real build generates authentic faults without anything being deliberately broken.**

**⚠️ The homelab is last on purpose.** It needs no discipline and would happily consume a whole day. **Blocks 1 and 2 are the ones that only happen if they come first.**

- **The lab does not open until 1 and 2 are done in the current pass.** Short blocks are fine; skipped ones are not.
- **The three-day skip trigger applies to blocks 1 and 2.** Avoidance is not the lab's problem.
- **⚠️ The lab now counts as Domain 5 practice, which makes "lab time is study time" an easy rationalisation.** It isn't. Blocks 1 and 2 are unchanged.

**⚠️ Do not restart at block 1 each session.** The *Where things stand* table below records where the last session stopped — start at the block **after** it.

## Where things stand

**Last session ended after block 3** (2026-09-21). **Resume at block 1.**

**Block 3 built the SIEM and it is ingesting.** The long stretch of it was a Domain 5 troubleshooting exercise in its own right — a log pipeline that ran cleanly end to end while producing events no rule could ever match, because one parser wanted a different timestamp format. **Found by testing line variants against the running system rather than reading documentation**, which is the same method that settled the DoH question.

**⚠️ Only Domain 5 remains** — five objectives and **24% of the exam**, the largest single domain. It pairs directly with block 3, which practises exactly this material.

| Track | Position | Next |
|---|---|---|
| **1 · Certification — Network+** | **5.1 complete** 2026-09-19 — the seven-step methodology, quiz **16/19** (one question void). **21 of 25 objectives done.** ⚠️ All three misses were **step-boundary confusions** — test vs verify, implement vs prevent | **5.2 — cabling and physical interface issues.** Then 5.3 through 5.5 |
| **2 · Simulated lab — Packet Tracer** | **7 scenarios done** — STP, double tagging, OSPF, EtherChannel/LACP, HSRP, DHCP relay, IPv6/SLAAC. NAT scrapped | **Scenario 8 — VLSM and summarisation** |
| **3 · Homelab** | Tracked privately | See `progress.md` in the homelab repo |

## Block 2 — Packet Tracer scenario queue

**One scenario per entry, each finishable within two blocks**, drawn from the N10-009 objectives and chosen for things the homelab cannot demonstrate — redundancy, dynamic routing, and failure behaviour need more devices than one switch provides.

**⚠️ Exam practice, not homelab modelling.** Each scenario gets its own `.pkt` file. Mixing the two is what made the NAT attempt confusing.

**Findings are written into the matching objective file** in the Network+ repo.

| # | Scenario | Objective | Status |
|---|---|---|---|
| **1** | ~~NAT and PAT~~ | 2.1 | **Scrapped** — the 3560 cannot translate |
| **2** | **Spanning Tree** | 2.2 | ✅ **Complete.** 9 lost pings on PVST+, **zero on RSTP** |
| **2b** | **VLAN double tagging** | 4.2 | ✅ **Complete.** Untagged native hop observed and closed. Attack itself not reproducible in Packet Tracer |
| **3** | **OSPF, single area** | 2.1 | ✅ **Complete.** Adjacencies, AD vs metric, the 100 Mbps reference-bandwidth trap, and **asymmetric routing produced by a one-sided cost change**. Link-failure reconvergence not measured |
| **4** | **EtherChannel / LACP** | 2.2 | ✅ **Complete.** Blocked port removed from STP's view, **zero loss on member failure** vs 9 pings on PVST+, `src-mac` hashing and the single-flow ceiling. **LACP proven blind to VLAN mismatch — CDP caught it.** Two PT fidelity limits recorded |
| **5** | **First-hop redundancy (HSRP)** | 2.1 | ✅ **Complete 2026-09-13.** Virtual MAC as the real mechanism, preempt, 8–10 lost pings vs zero on EtherChannel. **Reproduced the blackhole — a router staying active for a subnet it can no longer route out of.** Tracking unsupported in PT |
| **6** | **DHCP relay** | 3.4 | ✅ **Complete 2026-09-18.** Started with both clients failing — a router not forwarding broadcasts is the whole problem. **`giaddr` proven to be what selects the pool**, by deleting one pool and watching a working relay path produce nothing. `giaddr` vs option 3 distinguished, with HSRP as the case where they differ. `ip helper-address` relays eight UDP services, not one. Findings in `objectives/3.4-ipv4-ipv6-services.md` |
| **7** | **IPv6 and SLAAC** | 1.7 / 3.4 | ✅ **Complete 2026-09-19.** Started broken on the missing `ipv6 unicast-routing`. **Default gateway is the router's link-local, and the reason is renumbering.** EUI-64 both directions, solicited-node multicast as ARP's replacement, DAD succeeding by silence, M/O flags. **DHCPv6 assigns randomly, not sequentially — sequential would discard IPv6's 2⁶⁴ scan resistance.** Dual-stack means separate firewall rule sets, which is how IPv6 silently bypasses IPv4 controls. Findings in `objectives/3.4-ipv4-ipv6-services.md` |
| **8** | **VLSM and summarisation.** Three sites, one block, subnet by hand then summarise | 1.7 | Queued |
| **9** | **Wireless channel planning.** Three APs, non-overlapping channels, co-channel interference | 2.3 | Queued |
| **10** | **QoS.** Voice prioritised over bulk traffic across a congested link | 2.1 | Queued |

## Block 3 — Homelab, built problem-first

**The build is the troubleshooting practice.** Network+ Domain 5 is 24% of the exam and the one domain that can't be learned by reading — and a real build produces genuine faults continuously, without anything being broken on purpose.

**How the block runs — problem-first, not procedure-first.** Claude states **the goal**, **the constraints**, **candidate tools** with one line each on what they are for, and **the success criterion** up front. **Then it is yours to work out.** Claude reviews a plan before it runs, answers questions, and explains commands when asked.

**Ask for a bigger hint when you want one:** *"nudge"* names the layer or component · *"narrow"* names the mechanism or config area · *"command"* gives the syntax, explained.

**Claude interrupts unasked only for** anything irreversible or destructive, a secret about to be exposed, a factual error that would cost an hour, or a silent-failure trap.

**⚠️ Nothing is broken deliberately.** Fault injection into this lab was considered and rejected — it is a working system carrying a live site, log collection and an IDS, not a training target.

### What a build will not teach

**Recorded now so it is a list rather than a guess later.** These Domain 5 areas get little or no exercise from building, and need external practice — simulator activities, capture files, or question practice — before the exam:

| Area | Why the lab misses it |
|---|---|
| **Fibre and optical faults** | No fibre until the Phase 4 SFP+ backbone |
| **PoE** — power budget, incorrect standard | No powered devices yet |
| **Physical media and terminations** — crosstalk, attenuation, TX/RX transposed, bad terminations | Four short factory patch cables |
| **Physical tools** — toner and probe, cable tester, visual fault locator | Hardware not owned, and possibly never |
| **Wireless troubleshooting** — interference, channel overlap, coverage, roaming, disassociation | No access point until Phase 4 |
| **Cisco `show` command syntax** | RouterOS is a different CLI. **Covered in block 2 instead** |

**When the homelab reaches a stable state, this table becomes block 3's replacement queue.**

## Parked tracks

**Not deleted — parked with their position, so they can be resumed.**

| Track | Position when parked | Why |
|---|---|---|
| **TryHackMe** | TShark room complete. SOC Fundamentals turned out to be premium | Parked 2026-09-10. **Nmap Live Host Discovery** (`nmap01`) is the next room if it returns. Use [tryhackme.com/free-rooms](https://tryhackme.com/free-rooms) — third-party free-room lists are stale |
| **Packet analysis** | **3 complete** — *First to Last*, *Easy as 123*, *Lumma in the Room-ah!* (all answers correct). Tradecraft in [analysis-lessons.md](https://github.com/dmandevv/soc-python-network-plus/blob/main/analysis-lessons.md) | Parked 2026-09-10. Next would be ***It's a trap!*** (2025-06-13). **This is the SOC-analyst track rather than the exam track** — worth restarting after the exam |

## Progression triggers

| When | Change |
|---|---|
| **Network+ objectives finish** | Block 1 becomes Network+ practice exams |
| **Network+ passed** | Block 1 moves to **Security+**. The parked SOC-analyst tracks become candidates to return |
| **The Packet Tracer queue empties** | Block 2 becomes **Containerlab** |
| **A block in 1–2 is skipped three days running** | Replace it. A track being avoided is not being learned |
| **The homelab reaches a stable state** | Block 3 becomes external Domain 5 practice, from the gap table above |

## Why the lab comes last

It previously competed with these hours and lost, which is the wrong way round. **Simulated work was a rehearsal for the lab; the lab is the thing itself** — and so it's the reward the other three blocks earn.
