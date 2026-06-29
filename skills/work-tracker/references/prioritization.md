# Prioritization framework — the P-score

{{YOUR_NAME}} owns a head-of-product-scope role at {{COMPANY}}. The mandate is to deliver the highest-leverage product outcomes possible while keeping {{MANAGER}} (manager) and {{ENG_LEAD}} (engineering lead) in lockstep, protecting at-risk and high-value customers, and shaping the company's strategic narrative. This file is the brain that decides which deliverable surfaces in any given knock.

## The four lenses

Every candidate deliverable is scored HIGH / MED / LOW on four lenses. Score in the state file with a 4-letter code (`HHHH`, `HMLM`, etc.) plus a one-line rationale.

### Lens 1 -- Stakeholder Pull (who is waiting?)

| HIGH | MED | LOW |
|---|---|---|
| {{MANAGER}} explicit ask, {{ENG_LEAD}} explicit ask, board / investor request, paying customer with renewal risk in next 90 days, premium/concentration account, deal-blocking ask from active sales pipeline | Internal team blocked on {{YOUR_NAME}} (designer waiting on spec, eng blocked on PM clarity), key prospect, mid-tier customer, cross-functional partner coordination | Vendors, exploratory partner conversations, FYI threads, low-tier prospect, internal "nice to have" |

**Customer concentration weight:** any request from a top-5 ARR account or any account explicitly flagged as renewal-risk in the state file is a HIGH stakeholder pull regardless of who the messenger is.

### Lens 2 -- Strategic Fit (does it advance our bet?)

Read all roadmap-managed sources to score this:

- {{PLANNING_DOC}} (roadmap / quarterly priorities)
- The product backlog board (sort by priority score descending)
- Any governing scope-of-work doc ({{PLANNING_DOC}})
- The insights / customer-synthesis doc ({{PLANNING_DOC}})
- The market-scan doc (created by the recurring competitor scan -- see `market-pulse.md`)

| HIGH | MED | LOW |
|---|---|---|
| Contractually committed (top priority score), top-3 non-committed RICE epic, top-quartile backlog idea, an insight item explicitly named by {{MANAGER}} or {{ENG_LEAD}}, "where the puck is going" implication from the latest market scan | Mid-rank epic, supporting infrastructure for a top epic, insight item not yet rolled into an epic, customer-asked feature that aligns with roadmap direction | Off-roadmap, one-customer-one-time, pet feature without strategic anchor, polish on non-priority work |

If {{YOUR_NAME}} is working on something that is LOW on Strategic Fit but HIGH on Stakeholder Pull, surface it as a candidate to *delegate* or *defer* in a focus rec, not as a top-3 deliverable.

### Lens 3 -- Time Pressure (when does it matter?)

| HIGH | MED | LOW |
|---|---|---|
| Hard external deadline ≤7 days, deal-blocking, contractual scope-of-work gate, board/investor narrative deadline, customer presenting to their own committee in ≤7 days | Soft commitment ≤14 days, customer expecting "in next sprint," internal review milestone | No date, discretionary, "someday," "when you have time" |

### Lens 4 -- Leverage Multiplier (does completing this unlock more than itself?)

| HIGH | MED | LOW |
|---|---|---|
| Unblocks 2+ other people, generates validated learning fast (kills or confirms a hypothesis), builds defensible moat ({{PRODUCT}} / data network effects / proprietary insight), produces a board-narrative artifact, sets a precedent that compounds (template, framework, decision doc) | Modest unblock (1 person), polishes a top-priority feature, incremental learning, unlocks a single downstream task | Polish on non-priority work, rework that doesn't change outcome, work that benefits only {{YOUR_NAME}}, one-off |

## Scoring shorthand

Write the score as a 4-letter code in this order: **S**takeholder / **F**it / **P**ressure / **L**everage.

- `HHHH` -- top of stack, drop everything
- `HHHM` / `HMHH` / `HHMH` etc. -- top-3 candidate
- `HMMM` -- worth tracking, surface if no HIGH-pressure work competes
- `MMLL` or below -- log but don't surface in daily focus

A simple ranking heuristic: count the H's. 4H > 3H > 2H > 1H > 0H. Within a tier, break ties below.

## Auto-rules (override the score)

These bypass scoring entirely:

1. **Compliance / fiduciary trigger** -- anything touching audit, regulatory, fiduciary duty, or financial reporting accuracy goes to the top of the stack regardless of score. If your product is financial-adjacent, this risk is real.
2. **{{MANAGER}} explicit ask + named deadline** -- top of stack.
3. **Renewal-risk customer with renewal date ≤30 days** -- top of stack.
4. **Two-way door under 60 minutes** -- just do it. Do not spend a knock on it -- bundle into a focus rec as the "if you finish early" item.
5. **One-way door** (irreversible) -- never nudge. Escalate. The skill should surface it as "needs your decision before [date]" with the tradeoffs laid out, not as a "work on this" nudge.

## Tiebreakers (in order)

When two candidates score the same, apply in order:

1. **Closes a loop vs opens one** -- finishing > starting. A 2-hour task that ships beats a 2-hour task that begins something.
2. **Standing-elevating** -- artifacts that elevate {{YOUR_NAME}}'s standing as head of product (board narrative, market positioning, strategic frameworks, decision docs) > feature spec polish. Political capital compounds.
3. **Capacity-fit with the eng team** -- if the work depends on engineering {{ENG_LEAD}} cannot ship in the current quarter, demote it unless framing/positioning is the deliverable.
4. **Manager-visible** -- if {{MANAGER}} will see / ask about it within the week, weight up.
5. **Shortest path to a shippable artifact** -- early-stage companies die from indecision, not from imperfection.

## Head-of-product-at-a-startup considerations baked into the scoring

These shape *how* the lenses are weighted:

1. **Revenue protection ranks equal to manager ask.** Renewal risk and deal-blocking asks get HIGH stakeholder pull on par with {{MANAGER}}'s direct asks. At an early-stage company, churning a top-5 account is a company-survival event.

2. **Strategic moat is non-negotiable HIGH.** Anything that strengthens product defensibility, data network effects, or proprietary insight gets HIGH strategic fit even if it's not currently top of the RICE rank -- the rank captures next-quarter value, the moat captures next-fundraise value.

3. **Capacity reality demotes unfundable scope.** If the eng team cannot ship it in the current quarter (and it's not a fast-moving prototype), the deliverable becomes "frame it / scope it / position it" rather than "ship it." The work-tracker treats positioning work as the actual deliverable when shipping isn't yet on the table.

4. **Narrative leverage matters.** Artifacts that make {{MANAGER}} look credible externally (board decks, customer-facing one-pagers, investor updates, market-positioning docs) get a leverage bump because the political capital they create funds future product bets.

5. **Two-way doors fast / one-way doors deliberate.** Reversible decisions should be made in minutes, not days; irreversible decisions deserve days, not minutes. The skill nudges fast on the former and escalates the latter.

6. **Customer concentration weighting.** Premium or renewal-risk accounts get HIGH stakeholder pull on small asks where a mid-tier account would only get MED.

7. **Strategic-narrative test (weekly, not daily).** Once a week, the Sunday-evening or Monday-morning plan run asks: "do this week's top-3 deliverables ladder up to a story we can tell investors?" If three weeks pass with no narrative artifact in the top-3, surface that gap to {{YOUR_NAME}} explicitly.

8. **Saying no fast > saying yes slowly.** A clear "no, not now, here's why" is a top-tier deliverable. The skill surfaces these as candidate deliverables, not just feature/spec work.

## How the four lenses generate the daily top 3

After scoring all candidates:

1. Apply auto-rules. Anything triggered goes to the top, in trigger order.
2. Sort the rest by H-count (4H > 3H > 2H > 1H), then by tiebreakers above.
3. Take the top 3.
4. The morning focus rec leads with #1, mentions #2 as "if you finish early," and lists #3 as "next-up tomorrow" only if it's likely to slip without surfacing.
5. Knocks throughout the day target #1 and #2 -- briefings tied to them, nudges if they stall.

## When the framework gets it wrong

If {{YOUR_NAME}} overrides the recommendation 3+ times in a week (does something different from what the skill surfaced as #1), do not just retrain on the override -- *flag it explicitly* in the next morning rec:

> *"You've skipped my #1 three days running. Either I'm scoring something wrong or your real priority isn't in my state file. Want to walk through it?"*

The framework exists to be argued with, not blindly followed. {{YOUR_NAME}}'s correction is a signal that the lenses, the auto-rules, or the scored deliverables themselves need adjustment.

## State file integration

Each tracked deliverable in state gets these fields:

```
- **[Deliverable name]**
  - Anchor: [deadline / meeting / customer commitment]
  - Score: HHHH | rationale: "{{MANAGER}} asked, on roadmap top-3, due 5/14, unblocks customer committee"
  - Last activity: [date + what]
  - Notes: [context]
  - Nudges sent: [list]
```

The morning plan run re-scores every active deliverable. Scores are not sticky -- they reflect the world today.
