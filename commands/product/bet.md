# /bet — Sense -> Select -> Spec (the bet pipeline)

## Description

The system for generating good product bets and customer-meaningful specs faster, with a human
judgment gate at every handoff. It does NOT replace your existing skills. It loops them together
and adds the one stage you don't have: an explicit Select gate that protects what gets built.

The principle:

> AI raises how many bets we can evaluate and how fast we can draft a rigorous spec. It never
> decides what is meaningful to a customer or a buyer. Every stage handoff is a human gate, by design.

And the rule that resolves "fast beats right":

> Right before fast at selection. Fast beats right after.

So selection is deliberate (this skill is strict here). Everything downstream of a passed gate is
fast and cheap to throw away.

> The hard gates below are written as a worked example for one company. **Replace them with the
> 3-5 tests that define what is meaningful for *your* product** (your buyer-confidence test, your
> revenue-wedge test, your ICP, your "won't build" list). Keep the structure; swap the content.

## Usage

- `/bet` — show the pipeline funnel (Sensed -> Selected -> Spec'd) and what needs your decision
- `/bet sense` — gather candidate bets from all signal sources into one ranked, deduped list
- `/bet select [id | all]` — run the Select gate on a candidate (or all un-gated candidates); produce PASS / HOLD / DROP verdicts for your approval
- `/bet spec [id]` — draft a board-ready spec for a PASSED bet, inheriting your standards, routed to the right destination
- `/bet run` — the full loop: sense, then select, then (on your approval) spec the top passed bets

Plain language works too. Describe what you want ("what should we build next", "is the
cross-account work-matching bet ready to spec") and the skill picks the right stage.

## Candidate store

Bets ride on the existing **`~/.claude/product-ideas.yaml`** (the `/idea` store). This skill does
not create a parallel state file. It adds one block per idea, written only at the Select stage:

```yaml
  gate:
    verdict: pass | hold | drop
    lenses: "HHMH"            # Stakeholder / Fit / Pressure / Leverage (from prioritization.md)
    hard_gates:
      validation: { status: pass | hold, calls_validated: 2, calls_needed: 3 }
      buyer_confidence: pass | fail   # does this make a buyer more confident?
      hard_wedge: hard_dollar | soft_only   # hard dollar (revenue/compliance) vs soft value
      icp_fit: pass | weak | fail     # fits your defined ICP
      identity_check: pass | fail      # not on the "won't build" list
    track: demoable | core            # core requires validation = pass
    route: directory | board | tracker
    rationale: "one line"
    gated_on: "YYYY-MM-DD"
```

---

## Stage 1: Sense (delegate, don't rebuild)

Goal: assemble ONE deduped, ranked list of candidate bets from signal we already collect. This
stage raises the volume of candidates, not builds.

Pull from all of these in parallel, then dedupe by problem (not by wording):

| Source | How | What to take |
|---|---|---|
| Product ideas backlog | read `~/.claude/product-ideas.yaml` | all `captured` / `scoped` ideas |
| Meeting notes | run `/idea sweep` (last 14 days) | net-new ideas with verbatim customer quotes |
| Customer feedback | your {{SYNTHESIS_DOC}} (`/insights` output, doc `{{DOC_ID}}`) | INS-xxx items tagged `feature_request`, `prd_signal`, high priority |
| Market | your market-scan doc (`{{DOC_ID}}`, latest entry) | "actionable implications" and roadmap hooks |
| Product usage | usage / conversation logs (note as a gap if access is pending) | recurring asks / friction once available |
| Delivery context | work-tracker state `~/.claude/projects/<your-project>/memory/work-tracker_state.md` | high-score deliverables not yet a tracked bet |

Steps:
1. Gather candidates from every available source. State which sources were live and which were skipped (e.g. usage logs pending).
2. Dedupe into distinct bets. Merge duplicates, keep the strongest evidence (quote + source) for each.
3. For genuinely new bets not yet in the backlog, capture them via the `/idea add` schema (so they persist with source attribution and a 4-lens score).
4. Present the candidate list, ranked by the 4-lens composite, with a one-line "why now" each.

Human gate: {{YOUR_NAME}} decides which candidates are real and worth gating. Do not auto-promote.

---

## Stage 2: Select (the gate — this is the new IP)

Goal: a candidate earns capacity ONLY after it clears the gate. AI scores and recommends.
{{YOUR_NAME}} approves. This stage is deliberate on purpose.

For each candidate, run two layers:

### Layer A — the 4-lens P-score (reuse, don't reinvent)

Score Stakeholder Pull / Strategic Fit / Time Pressure / Leverage Multiplier per
`~/.claude/skills/work-tracker/references/prioritization.md` (HIGH / MED / LOW, 4-letter code).
Apply that file's auto-rules and tiebreakers. This gives the ranking.

### Layer B — the hard gates (the part nothing else enforces)

A bet must clear these to PASS. Each is a judgment; surface the evidence, let {{YOUR_NAME}} decide.

> The five tests below are an example. Replace them with your own. The pattern: a validation
> gate, a value test, a revenue/wedge test, an ICP-fit test, and an identity/"won't build" test.

1. **Validation (don't build in the dark).** Has the shared problem been validated across 3 to 5 customer calls? Count the calls with evidence. If not met, the bet can be PASS for a **demoable** build but is **HOLD for core build** until validation lands. Name exactly what validation is missing.
2. **Buyer-confidence test.** Does this make a buyer (or decision-maker) more confident in their decisions or in the product? If no, it does not pass.
3. **Hard-wedge test.** Does it hit a hard dollar (revenue, a compliance event, a financing event) or only soft value (relationship, NPS)? Label it `hard_dollar` / `soft_only`. Soft-only bets are not disqualified, but they cannot be sold on the wedge and rank lower.
4. **ICP fit.** Does it serve your defined ideal-customer profile? `pass` / `weak` / `fail`.
5. **Identity non-goals check.** Reject anything on your "won't build" list (the things you have explicitly decided are out of scope for the product).

### Verdict

- **PASS** — clears the value test + identity, with a named track. `track: core` requires validation = pass; otherwise `track: demoable`.
- **HOLD** — promising but missing validation or evidence. State precisely what is needed to convert it (e.g. "2 more customer calls confirming the pain").
- **DROP** — fails the value test or identity, or is soft-only with no path to a wedge. State which gate failed.

Then assign **route** (define your own destinations):
intelligence/analytics-layer items -> a feature directory doc (`{{DOC_ID}}`);
app epics/ideas -> your roadmap board (via `/roadmap`);
discrete bugs/stories -> your issue tracker.

Present verdicts as a table (candidate, lenses, hard-gate results, verdict, track, route,
one-line rationale). On {{YOUR_NAME}}'s approval, write the `gate` block back to
`product-ideas.yaml`. Update status: PASS -> `scoped`, HOLD stays `captured` with a note,
DROP -> archived via `/idea drop`.

Human gate: nothing reaches Spec without an approved PASS. **The failure mode to watch first: a
bet skipping the gate to keep a demo on schedule. Refuse to spec an un-gated bet; surface it instead.**

---

## Stage 3: Spec (delegate to /prd, wrap with your standards)

Goal: turn a PASSED bet into a rigorous, customer-meaningful spec, fast. Faster does NOT mean
looser: agents execute requirements literally, so a vague spec ships the wrong thing at full speed.

Steps:
1. Run `/prd [bet title] from [the source meetings on the bet]`. This already enforces the PRD template, runs framing and doc-review passes (Engineer / Designer / Customer PM / QA), and pulls meeting-notes + Insights.
2. **Inject your standards as the contract** (add to / verify in the draft before save). Replace these with your own; examples:
   - A **Value-Verification** section: "what makes this meaningful to the buyer, measurably" (the explicit success test, not a vibe).
   - **Show your work**: the spec must be able to surface its reasoning/sources, not assert.
   - **Domain-specific compliance constraints** (e.g. if you operate in a regulated space, encode the constraint here).
   - **Product requirements only**: no schema, enum values, API contracts, indexing, or migration detail. The dev team owns the how.
   - **Formatting house rules** for any tracker output (e.g. ASCII-only dashes: use `--` and `->`).
3. **Route the output** per the bet's `route`:
   - `directory` -> append an entry to your feature directory doc (`{{DOC_ID}}`), correct section, directory entry format. Show the entry to {{YOUR_NAME}} before writing.
   - `tracker` -> the `/prd` issue-tracker path: Epic per capability, Story per P0/P1 in Given/When/Then, `(DRAFT)` prefix, unassigned, your standard review label, full writeup shown to {{YOUR_NAME}} before push.
   - `board` -> leave the PRD as the artifact and let `/roadmap` / `/roadmap-edit` place it on the board.
4. Update `product-ideas.yaml`: status -> `in_prd`, `related.prd_url` -> the PRD doc URL.

Human gate: {{YOUR_NAME}} owns whether the requirement is right and meaningful (the "80% job" of
alignment and justification). Never push a tracker or directory write without showing it first.

---

## /bet run (the full loop)

1. Stage 1 Sense -> present ranked candidates.
2. Pause for {{YOUR_NAME}} to mark which to gate.
3. Stage 2 Select on those -> present verdicts table.
4. Pause for {{YOUR_NAME}} to approve PASS / HOLD / DROP.
5. For approved PASS bets, Stage 3 Spec the top N (ask how many) -> present each draft / routed entry for approval before any external write.

Never collapse the three pauses into one. The gates are the product.

## Guidelines

- Sense and Spec delegate to existing skills. The Select gate is the only place this skill adds new judgment. Keep it that way; do not duplicate `/idea`, `/prd`, `/roadmap`, or `/insights` logic.
- Always state which Sense sources were live vs skipped.
- Score with the existing 4-lens framework; do not invent a new scoring scale.
- Two-track dev: `demoable` bets can move without full validation; `core` builds require validation = pass. Enforce this in the gate.
- Reuse your standing schedule, don't add a new cron: `/idea sweep`, `/roadmap market-scan`, and the work-tracker daily plan already feed Sense. `/bet sense` aggregates their outputs on demand.
- Everything customer-facing or external (tracker, directory, emails) follows the standing message-send guardrail: show, wait for approval, then write.
