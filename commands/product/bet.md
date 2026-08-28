# /bet: Sense -> Select -> Spec (the bet pipeline)

## Description

The system for generating good product bets and customer-meaningful specs faster, with a human
judgment gate at every handoff. This is the "aim the cannon" layer: it sits in front of your build
pipeline so only gated, well-specified bets reach it. It does NOT replace your existing skills. It
loops them together with sub-agent fleets and adds the one stage nothing else enforces: an explicit
Select gate that protects what gets built.

**Core idea:** the system *builds its own context* to judge where time should go, how the product
actually works, and whether existing work is still wanted. It reads that from your signal sources
(meeting notes, insights, your tracker, the direction anchor, and your codebase), so the calls
(prioritization, product-understanding, staleness) are evidence-based and system-generated, never
offloaded to your memory or punted back as a manual check.

The principle:

> AI raises how many bets you can evaluate and how fast you can draft a rigorous spec. It never
> decides what is meaningful to a customer or a buyer. Every stage handoff is a human gate, by design.

And the rule that resolves "fast beats right":

> Right before fast at selection. Fast beats right after.

So selection is deliberate. Everything downstream of a passed gate is fast and cheap to throw away.

> Passages marked **(worked example)** are written for one company. Replace the content with the
> equivalent for *your* product; keep the structure.

## System (the layers)

Built so the parts that carry the load stay stable as your capacity changes.

1. **State store (deterministic).** One file is the single source of truth for "what stage is each
   bet in" and "did it pan out": the `~/.claude/product-ideas.yaml` store (the `/idea` store). The
   funnel is read from state, never re-derived by an LLM each run.
2. **Agentic orchestration (this skill).** Each stage dispatches a parallel sub-agent fleet; the
   orchestrator coordinates, applies the human gates, and persists the gate decision to state.
3. **Apply layer (your tracker).** Creating / editing / ranking / linking issues happens through
   your tracker's API or MCP. Writes always show first and go out only on approval.
4. **Scheduled Sense (optional).** A recurring trigger runs the Sense fleet and surfaces new
   candidates awaiting a gate decision. It never gates or specs on its own.
5. **Evaluation loop.** `/bet eval` grades the gate's past decisions against real outcomes and
   recommends recalibration, so the system stays accurately aimed.

## Two phases this serves

Designed to survive a capacity step-change without a rebuild.

**Phase 1 (now): agents are faster than build capacity.** Build capacity is the binding constraint,
as in normal development. The gate **rations**: only the top-ranked bets that fit capacity get built;
the rest wait. Ranking and sequencing dominate. Product and tech compete for the same scarce
capacity, so a tech allocation is a real tradeoff. Backlog rank and sprint sizing matter most here.

**Phase 2 (next): build agents make capacity feel unlimited.** When almost anything can be built in
parallel, the binding constraint moves upstream to bet quality and direction (more compute than
commercializable ideas). What flips:
- Ranking relaxes from "ration scarce capacity" to "order by dependency and coherence." Many passed
  bets run at once.
- The **Select gate becomes the primary constraint**, not capacity. It is the only thing stopping
  junk from shipping at scale. The cannon is bigger, so aiming it precisely matters more, not less.
- **Cohesion becomes critical.** High throughput is the fastest route to a disjointed product; the
  coherence check is what keeps it tied together.
- Sense and Spec throughput scale up, and the eval loop matters more (miscalibration ships many
  wrong things fast).

**Load-bearing in both phases:** the Select gate, the coherence check, the human gates, the eval
loop. **Phase-dependent:** how hard ranking rations vs. orders, and sprint sizing. Centering the
Phase-2 load-bearing parts now means the move to Phase 2 is a relaxation of rationing, not a rebuild.

## The direction anchor (anti-whiplash)

Keep one durable file as the **anchor**: the handful of problem-themes you are committed to, and why,
on a slow clock. It exists so your dev team never feels jerked around: the fast layers (backlog rank,
sprints) move *within* these themes; they do not redraw them. It is both the shareable "where we are
going and why" one-pager and the file this loop reads and updates.

**The hierarchy: Theme -> Initiative -> Epic -> Story/Task.**
- **Theme** (anchor): the durable strategic frame. Slow clock.
- **Initiative:** a coordinating container: one common goal, several small epics, plus the "how these
  connect and why" and the cross-epic sequence. This is where interconnection context is preserved.
  An Initiative is defined by a PRD (Initiative = PRD). If your tracker has no native Initiative tier,
  the system is the source of truth for this layer; mirror it with a label + issue links + a tracking
  epic as the clickable home.
- **Epic:** small, single-feature, 2-4 week. The commitment unit. One PRD capability area.
- **Story / Task:** the ticket. One PRD P0/P1 requirement.

**Layered clock speeds** (the whiplash cure is different cadences at different altitudes, faster moves
inside slower boundaries):
- **Direction / thesis:** rarely; pivot only on validated signal.
- **Themes:** curate about monthly.
- **Execution:** fluid, but the actively-committed slice (a 2-4 week window) is NOT re-prioritized
  mid-stream.

**Graduated-pivot governance** (resistance proportional to altitude): a ticket re-ranks on one signal;
a theme turns only on **accumulated** evidence across multiple reviews (a named pivot); the thesis
turns only on a validated shift. Signals accrue against a theme between reviews (hysteresis), so the
big boats turn slowly but never freeze.

**Anti-whiplash rules (enforce these):**
1. **Never re-rank actively-committed work.** Re-ranking reorders only the backlog *behind* the
   in-flight commitments the anchor lists. A large "in progress" epic protects only its
   actively-worked children; the un-started remainder is ordinary backlog.
2. **Every priority cites its theme.** If a bet maps to no current theme, that is a signal: either it
   is off-strategy (HOLD/DROP) or the themes need curating (a deliberate act, not a silent drift).
3. **Pivots are named.** A change in direction is logged with a why and communicated, not slipped in
   via a re-rank.

> **(worked example)** If your product has cross-cutting concerns (a compliance layer woven through
> every theme, an intelligence layer that touches every change, one key customer segment), score and
> brief each bet on those too, not just its theme.

## Working with /roadmap (two layers of one system, not rivals)

`/bet` and `/roadmap` must not become two prioritization systems that drift apart. They are nested:

- **/roadmap = the strategic layer.** Themes and epics, ranked, quarterly horizon. Answers "which
  bets/themes matter, and in what order."
- **/bet = the execution layer.** Individual bets through the gate, plus backlog grooming and sprints.
  Answers "is this bet real and ready, and what exactly gets built next."

Two handshakes keep them in lockstep:
1. **roadmap -> bet (direction in):** Sense reads the roadmap, and the Select gate's Strategic Fit
   lens is scored *against the roadmap's current ranked epics* (plus your identity), so `/bet`
   inherits strategy rather than re-deriving it. Epics `/bet` creates roll up to a roadmap theme,
   never a parallel taxonomy.
2. **bet -> roadmap (reality out):** `/bet` writes candidates and `/bet eval` outcomes to the shared
   store, which `/roadmap` consumes to update its confidence and strategic view.

They coordinate by reading each other, not by clobbering. Priority is nested, not competing: roadmap
ranks epics; `/bet` ranks tickets *within* the frame roadmap sets.

## Two audiences: agents vs humans (no slop)

Context volume must match the consumer. There is work built *by agents for agents*, and a separate
path of artifacts built to help *humans* understand only what they need.

- **Agent-facing** (the full Spec for a build agent, the gate record, complete justification):
  **completeness beats brevity.** Load all the context so a downstream agent builds the right thing.
  Verbosity here is not slop, it is the job; a naive agent needs everything to avoid building wrong.
- **Human-facing** (the Priority Brief, review summaries, the "why this, now"): **minimal and
  decision-relevant only.** Give the human exactly what they need to make the call, nothing more. A
  human-facing artifact that reads like the agent one *is* slop and wastes the reader's time.

Both are generated from the **same gate record**, but they are **different artifacts**. The human
brief is a ruthless distillation of the record, never the record itself. Right-size per reader:
engineers want the engineering-relevant why and tradeoff; a founder wants the strategic angle; a board
wants confidence.

## Usage

Forward (new work):
- `/bet` : show the funnel (Sensed -> Selected -> Spec'd) and what needs your decision
- `/bet sense` : run the Sense fleet, dedupe, refresh the candidate queue
- `/bet project [description]` : intake one new project and push it through Select -> Spec
- `/bet select [id | all]` : run the Select gate; produce PASS / HOLD / DROP / PARK for your approval
- `/bet park [id]` : set a gate-worthy but not-now bet aside as dormant with an activation trigger (defers timing, not merit)
- `/bet activate [id]` : wake a parked bet when its trigger fires and run the value-now evaluation (it never auto-builds)
- `/bet parked` : list dormant bets and their wake triggers (read at Spec and backlog-groom to catch coupled triggers)
- `/bet spec [id]` : draft a board-ready spec for a PASSED bet, routed to the right destination
- `/bet foresight` : the forward half of Sense; surface where-the-puck-is-going bets into exploration
- `/bet run` : the full forward loop: sense, then select, then (on approval) spec the top passed bets

Retroactive (existing backlog) and calibration:
- `/bet backlog` : groom the live backlog: merges, closes, epic groupings, rank, sprints; on approval
- `/bet integrity` : audit the product for coherence erosion (duplicate/dead surfaces, pattern drift)
- `/bet eval` : grade the gate's past decisions against outcomes; recommend recalibration

Plain language works too ("what should we build next", "groom the backlog", "is the gate calibrated").

## Candidate store

Bets ride on the existing **`~/.claude/product-ideas.yaml`** (the `/idea` store). This skill does not
create a parallel state file. It adds one block per idea, written only at the Select stage:

```yaml
  gate:
    verdict: pass | hold | drop
    lenses: "HHMH"                # Stakeholder / Fit / Pressure / Leverage (from prioritization.md)
    hard_gates:
      validation: { status: pass | hold, calls_validated: 2, calls_needed: 3 }
      buyer_confidence: pass | fail     # does this make a buyer more confident?
      hard_wedge: hard_dollar | soft_only   # hard dollar (revenue/compliance/financing) vs soft value
      icp_fit: pass | weak | fail       # fits your defined ICP
      identity_check: pass | fail       # not on the "won't build" list
    domain: { experts: "persona1,persona2", verdict: pass | concerns | fail }   # domain-expert step
    feasibility: clear | moderate | hard | unknown    # architect step
    cohesion: strong | fits | tension | conflict      # whole-preserving check
    track: demoable | core | exploration              # core needs validation=pass; exploration bypasses it
    conviction: "..."             # exploration only: the thesis
    kill_criterion: "..."         # exploration only: timeboxed learn-or-kill
    route: directory | board | tracker
    why_this: "..."               # Priority Brief lineage (see below)
    why_now: "..."
    tradeoff: "..."
    rationale: "one line"
    gated_on: "YYYY-MM-DD"
    parked:                        # OPTIONAL, orthogonal to verdict: defers timing, not merit
      trigger: "what must happen to make this worth doing"
      trigger_kind: coupled | time # coupled = a surface or bet gets touched; time = revisit-by date
      rationale: "why real but deferred now (the value-later judgment)"
      parked_on: "YYYY-MM-DD"
      activated_on: null           # set when the trigger fires
```

A `parked` block with no `activated_on` overrides the verdict-derived stage with **PARKED** (dormant,
out of the active queue) until its trigger fires. Read the funnel from state; never eyeball the YAML
by hand.

---

## Stage 1: Sense (two waves, delegate, don't rebuild)

Goal: refresh the strategic frame AND assemble ONE deduped, ranked list of candidate bets from signal
you already collect. A full Sense run INVOKES the upstream skills fresh, not just cached docs. It runs
in **two waves** because `/roadmap` synthesizes the other signals and must run *after* them.

**Wave 1: signal fleet (parallel sub-agents).** Pull from all available sources, then dedupe by
problem (not wording):

| Source | How | What to take |
|---|---|---|
| Product ideas backlog | read `product-ideas.yaml` | all `captured` / `scoped` ideas |
| Meeting notes | run `/idea sweep` (last 14 days) | net-new ideas with verbatim customer quotes |
| Customer feedback | your synthesis doc (`/insights` output) | items tagged `feature_request`, `prd_signal`, high |
| Market | your latest market-scan | actionable implications and roadmap hooks |
| Product usage | usage / conversation logs (note as a gap if pending) | recurring asks / friction |
| Delivery context | work-tracker state | high-score deliverables not yet a tracked bet |
| Risk backlog | your open security/quality issues | high-severity items (feeds the risk lane below) |

**Wave 2: run `/roadmap` (full), after Wave 1 completes.** The full roadmap evaluation ingests the
fresh signals and re-ranks the epics, so the Select gate's Strategic Fit lens scores against a
just-refreshed ranking, not a stale one. A full Sense run *is* a roadmap refresh.

Then the orchestrator:
1. Collects both waves. States which sources were live vs skipped, and whether this was fresh or cached.
2. Dedupes into distinct bets by problem; keeps the strongest evidence (quote + source) per bet.
3. Captures genuinely new bets via the `/idea add` schema (so they persist with source + a 4-lens score).
4. Presents the refreshed candidate queue, framed by the just-re-ranked roadmap.

Human gate: you decide which candidates are real and worth gating. No auto-promotion.

### The inclusion test (the guard against flooding)

Broad intake (audit findings, the risk backlog, ops/velocity signals) risks turning "everything into
a bet." The funnel must get more *legible*, not more crowded. Admit an item, feature or not, only if it
changes one of:
- **Do**: what the customer can *do* (a capability),
- **Exposed**: what the customer is *exposed to* (risk: security, compliance, correctness), or
- **Fast**: how *fast* you ship to them (leverage / velocity).

A pure refactor, cleanup, or dependency bump with **no leverage claim** stays in the engineering
backlog and never enters the funnel (that is the dev team's to sequence). A real risk or leverage
claim is a bet; housekeeping is not. When in doubt, the item must name which of Do / Exposed / Fast it
changes, or it does not enter.

---

## The Foresight Engine (find and protect forward bets)

Sense's forward half. Where the validated core lane asks "what is proven now?", Foresight asks "where
is the puck going?" and feeds the **exploration lane**. The signal is relational and leadership-driven,
not competitor-scraped.

**Forward-signal streams (mine each, distill to candidate forward bets):**
- **Segment-market read:** signals *in your buyers' markets* (regulatory shifts, demand movement,
  trends), pointed inward at your segments, not competitor products.
- **Partners:** mine partner-call notes for forward asides: where they see the market going, co-sell
  motions, what they would pay for. Tag them forward, distinct from a customer feature ask.
- **Sales read:** your sellers are the early-warning radar; they hear demand shifts and objections
  first. Mine their call transcripts (or interview them) for the *forward* read, where demand is
  heading, not the operational play-by-play.
- **Leadership / founder thought leadership:** capture strategic framings as **candidate** forward
  signal, with discernment. A directional signal is a hypothesis routed to exploration, NOT a named
  pivot. Do not auto-elevate.

**Distillation:**
- **Weak-signal detection:** cluster recurring, low-frequency, *un-ticketed* mentions (the "twelve
  quiet mentions"). That is where the non-obvious bet hides.
- **Representativeness:** down-weight the vocal-minority present-day ask in the core lane, but *route*
  a genuine early/forward signal to exploration. Same input, two treatments.

**Output:** forward bets written to the store with a source type, a **conviction thesis**, a suggested
**kill-criterion**, and the segment(s). They enter Select via the exploration lane, funded from a
reserved capacity slice so ambition is funded on purpose, not squeezed out.

Human gate: conviction is your call. You confirm which forward candidates get funded as exploration.

---

## The Integrity Guardian (maintain product coherence)

Foresight's counterpart. Foresight guards the **future**; Integrity guards the **whole**. As bets ship
fast (especially in Phase 2), the risk is the product fragments into a coherent-*looking* pile of
features. This organ keeps it a coherent product.

- **Living integrity model.** A continuously-maintained map of what exists and how it fits, grounded
  in your codebase (via a code-intelligence tool or LSP) plus your design system: surfaces,
  architecture and UX patterns, navigation, design tokens. This is the reference every integrity
  judgment is made against.
- **Whole-preserving check.** Every bet is checked not just "does it fit somewhere" but "does it
  preserve the whole": no duplicate surface for a thing that already exists, no pattern/UX drift, no
  new nav where an existing one belongs, no fragmentation. A real code check, not a stubbed guess.
- **Periodic integrity audit (the inverse of staleness).** Staleness asks "is this ticket still
  wanted?"; integrity asks "has the product fragmented, where is coherence eroding?" A scheduled scan
  surfaces **integrity-debt**: duplicate flows, drifting patterns, dead/orphan surfaces, inconsistent
  UX. Integrity-debt is its own evidence-based work stream.

Human gate: you approve integrity-debt work like any bet; the audit informs, it does not auto-file.

---

## Stage 2: Select (the gate, and the new IP)

Goal: a candidate is PUSHED to Spec only once there is enough evidence it is a strategic bet, not a
random feature that would need immediate rework. Selection runs **two scoring systems in sequence with
domain-expert validation between them**, all grounded in the current state of the product. The agents
score and recommend; you approve; the gate block is persisted with the push rule enforced.

Run this per candidate (parallelize across candidates for `all`). Each goes through three steps; stop
early if it fails, so you do not spend expert/architect time on a bet that already failed strategy.

### Step A: scoring system 1, the strategy hat (grounded in IDENTITY.md)

Dispatch a **strategy agent**. It reads `~/.claude/IDENTITY.md` and scores whether this maximizes your
strategic bets:
- **4-lens P-score** per `~/.claude/skills/work-tracker/references/prioritization.md` (Stakeholder Pull
  / Strategic Fit / Time Pressure / Leverage; HIGH / MED / LOW; 4-letter code; auto-rules + tiebreakers).
- **Class and strategic home.** Every candidate carries a `class` set at intake (`feature` |
  `security-compliance` | `platform-health` | `internal-tooling`). Strategic Fit is scored against the
  item's home: a `feature` against a theme, a non-`feature` bet against a company objective. Score each
  class on value native to its kind (feature = theme contribution; security = risk avoided x exposure
  x likelihood; tooling/health = leverage multiplier + kill criterion), then read on one comparable
  scale. Keep `class` + theme/objective visible on every ranked line so the rank stays legible.
- **Hard gates** anchored to your identity. **(worked example)** replace these five with the tests
  that define what is meaningful for *your* product:
  1. **Validation (don't build in the dark).** Has the shared problem been validated across 3 to 5
     customer calls? If not met, the bet can PASS for a **demoable** build but is **HOLD for core**.
  2. **Buyer-confidence test.** Does it make a buyer / decision-maker more confident? If no, no pass.
  3. **Hard-wedge test.** Does it hit a hard dollar (revenue, compliance, financing) or only soft value?
     Soft-only bets are not disqualified but rank lower and cannot be sold on the wedge.
  4. **ICP fit.** Does it serve your defined ideal-customer profile? `pass` / `weak` / `fail`.
  5. **Identity non-goals.** Reject anything on your explicit "won't build" list.
- **Capacity lanes** (when rationing Phase-1 capacity): reserve floors per lane (e.g. exploration,
  security/compliance, platform-health), and raise a lane's floor when its risk backlog spikes.
  Features do not out-rank a lane that is below its floor.

If system 1 fails (value-test fail, identity fail, or clearly off-strategy), stop and recommend
DROP / HOLD. Do not proceed to the expensive steps.

### Step B: domain-expert validation (spun up by the strategy agent)

If system 1 passes, spin up the field domain expert(s) whose judgment the bet actually needs (pick the
relevant persona(s) for your product; run in parallel if more than one). Each grounds in the current
product state and answers: is this a real problem for this persona, and **what should the product
actually look like** given what exists today? Output: a domain verdict (`pass` / `concerns` / `fail`)
plus the fleshed-out product shape. A `fail` blocks the push.

### Step C: scoring system 2, the architect (grounded in real code)

Dispatch a **dev-architect agent**. It pressure-tests the change against the real product, grounded in
your codebase (via a code-intelligence tool) plus the integrity model. It assesses:
- **Feasibility:** clear / moderate / hard / unknown, traced against actual surfaces.
- **Cohesion / whole-preserving:** does this tie into existing features for one coherent UX, or create
  a disjointed surface / duplicate an existing one / drift a pattern (needing immediate rework)?
  strong / fits / tension / conflict.

(If the codebase is unavailable, fall back to a manifest-only read and say so.)

### The push decision

Present one verdict table per candidate: lenses, system-1 hard gates, domain verdict + product shape,
system-2 feasibility + cohesion, recommended verdict, track, route, one-line rationale.

- **PASS (push to Spec)** only when: system 1 passes, domain verdict is `pass` (or `concerns`
  explicitly resolved), and cohesion is `fits` or `strong`. A `core` track additionally needs
  validation = pass.
- **HOLD** when promising but missing validation, carrying unresolved domain concerns, or showing
  `tension` cohesion that needs reshaping. Name exactly what is needed.
- **DROP** on system-1 fail, domain `fail`, or cohesion `conflict`.
- **PARK** when the bet is real and gate-worthy but its clock has not started: importance without
  urgency (a guardrail on stable, unchanged code; a hardening task; an initiative whose payoff is real
  but not now). PARK is **orthogonal to PASS / HOLD / DROP**: it judges *timing*, not *merit*, so you
  can park a pass, a hold, or a sensed bet. It records an **activation trigger** (what must happen to
  make this worth doing: a coupled surface gets touched, or a revisit-by date) and the value-later
  rationale. A parked bet leaves the active queue and stops competing for attention until the trigger
  fires. Do not conflate importance with urgency: a real-but-not-now bet is a PARK, never a DROP and
  never a must-have.

**The exploration lane (a different door, protects ambition).** The gates above are correct for the
validated *core* lane, but they would kill the ambitious, not-yet-validated bet, which is the opposite
of skating to where the puck is going. Forward bets (from the Foresight Engine) enter via
`track: exploration`, which **bypasses the validation requirement and the buyer-confidence / domain /
cohesion push-gates** (you cannot know those before you build to learn). It still respects **identity
non-goals**, and requires a **conviction** thesis + a **kill-criterion** (a timeboxed spike, not a
commitment). Draw exploration bets from the reserved capacity slice.

Human gate: you approve / override, then the gate block is written to `product-ideas.yaml`. The push
rule is enforced: refuse `core` without validation=pass, and refuse a PASS that fails buyer-confidence,
identity, the domain verdict, or shows cohesion `conflict`. **The failure mode to watch first: a bet
skipping the gate to keep a demo on schedule. Refuse to spec an un-gated bet; surface it instead.**

### Activation: the value-now evaluation (a fired trigger is not a green light)

Parking sets a trip-wire; it does not schedule the work. When a parked bet's trigger fires, that is a
prompt to **evaluate**, never a command to **execute**. The evaluation scales its rigor to the size of
the work and is, at bottom, a **capital-allocation call**: every product decision reduces to some form
of money (investment, scarce resources, future return).

1. **Size it first (this sets the rigor).**
   - **Rider**: small enough that "we are already in this surface" makes the marginal cost trivial
     (rides along with the triggering work; roughly a day or less, no new surface). Near-automatic yes;
     do it *with* the triggering work.
   - **Initiative**: large enough that "we are touching it anyway" is NOT sufficient justification. It
     gets the full evaluation below. This is the whole point of the step: a trigger can fire on a big
     initiative, and being in the neighborhood never makes it worth the capital on its own.

2. **The capital-allocation call (for initiatives).** State it in money terms, native to the class:
   - **Investment**: engineering time plus **opportunity cost**. When capacity is the binding constraint
     every yes is a no elsewhere, so name what it displaces.
   - **Return**: a feature returns future revenue or retention; security and compliance return loss
     avoided (risk x exposure x likelihood, plus deal-blocker removal); platform health and tooling
     return leverage (time saved); plus **strategic optionality** (what it opens).
   - **Why now vs later**: does doing it *now* change the cost or the return? Being in the code now can
     lower the cost (the rider discount); a distant return can argue the capital is better deployed
     elsewhere today.

3. **Output a disposition, with the economic rationale explicit:**
   - **ride-now**: spec it with the triggering work.
   - **promote**: worth doing now as its own committed work; spec it.
   - **re-park**: the trigger fired but the value math still says not yet; re-park with a sharper
     trigger. This path is what makes a trigger a *signal*, not an order.
   - **drop**: the trigger revealed it is no longer worth doing at all.

The same lens applies at *first* Select, not only on activation: an item can be gate-worthy on merit
yet fail the "is the return worth the capital **now**" test. That is a PARK, not a PASS. Importance
earns a place in the system; only the capital-allocation call earns a slot **now**.

---

## Priority Brief: the "why this, now"

Phase 1 is capacity-constrained, and your dev team are (rightly) priority skeptics: every proposed item
draws a "why this, why now?" Automating the analysis into the gate must NOT cost you the ability to
answer that. The gate already did the reasoning; this turns it into a short, human, evidence-cited
justification you **review, not re-derive**, and hand over. Same "show your work" discipline you use
with customers, pointed at your own team.

This is the **human-facing path**. It is a ruthless distillation of the gate record, NOT a dump of it.
If it starts to read like the full agent justification, cut it. Auto-generate about 4 to 6 lines per
prioritized item (a Select PASS, a sprint pick, a rank change):
- **What:** the item, one line.
- **Why this:** the strategic reason, with lineage (Theme -> Initiative -> this epic) plus the belief
  and wedge it serves. The lineage is the continuity that prevents whiplash.
- **Why now:** timing, what it unblocks or de-risks, validation (N calls), sequencing, plus the honest
  **tradeoff**: what you are NOT doing to do this, and why that is acceptable.
- **Evidence:** the receipts (customer quote, validation-call count, metric, roadmap rank, domain read).
  This is the part that answers a skeptic. Show the work, do not assert.

Persist `why_this` / `why_now` / `tradeoff` on the gate so the brief renders identically every time.
A good brief pre-answers "why this vs the other thing," "why now vs later," and "what if we don't." If
it cannot answer those from the gate record, the bet is not ready: send it back to HOLD rather than
dressing it up. It is also your own fast catch-up: read it to know what is coming and why, in minutes.

Delivery follows the standing message-send guardrail: you review and edit before anything is shared.

---

## Stage 3: Spec (delegate to /prd, wrap with your standards)

Goal: turn a PASSED bet into a rigorous, customer-meaningful spec, fast. Faster does NOT mean looser:
agents execute requirements literally, so a vague spec ships the wrong thing at full speed.

The spec is **agent-facing**: load the full context the build agent needs. Pair it with a thin
human-review layer (a few lines: what this is, the decisions to sign off, open questions) so you and
reviewers approve without reading the whole agent spec.

For each PASSED bet, dispatch a Spec agent that:
1. **Matches the artifact to the altitude AND the class.**
   - By altitude: an **Initiative-sized** bet (spans multiple epics toward one goal) gets a **PRD**
     that decomposes into child epics + stories (`/prd [title] from [source meetings]`). A **single
     epic** gets a lighter epic-spec; forcing a full PRD onto one epic is over-documentation slop.
   - By class: `feature` -> PRD / epic-spec (the default). `security-compliance` -> a problem / impact
     / acceptance / verification writeup (the vulnerable path, the exposure, acceptance criteria, a
     verification section), framed as product requirements, not prescribed code. `platform-health` /
     `internal-tooling` -> a leverage claim + kill criterion (what it unblocks, how you will know it
     worked, when to abandon it).
2. **Injects your standards as the contract** (add / verify before save). **(worked example)** swap for
   your own:
   - A **value-verification** section: what makes this meaningful to the buyer, measurably (an explicit
     success test, not a vibe).
   - **Show your work:** the spec surfaces its reasoning and sources; it does not assert.
   - **Domain constraints** for a regulated space (encode the constraint here).
   - **Product requirements only:** no schema, enum values, API contracts, indexing, migrations. The
     dev team owns the how.
   - **Formatting house rules** for tracker output (e.g. ASCII-only: `--`, `->`).
3. **Routes** per the bet's `route`: `directory` -> your feature-directory doc; `tracker` -> the `/prd`
   issue-tracker path (Epic per capability, Story per P0/P1 in Given/When/Then, `(DRAFT)` prefix,
   unassigned, your review label, full writeup shown first); `board` -> leave the PRD as the artifact
   for `/roadmap` to place.
4. Updates the store: `status -> in_prd`, `related.prd_url -> the PRD URL`.

Human gate: you own whether the requirement is right and meaningful (the "80% job"). Never push a
tracker or directory write without showing it first.

---

## /bet run (the full loop)

1. Stage 1 Sense fleet -> present ranked candidates.
2. Pause for you to mark which to gate.
3. Stage 2 Select on those -> present the verdict table.
4. Pause for you to approve PASS / HOLD / DROP / PARK; persist the gate block.
5. For approved PASS bets, Stage 3 Spec the top N (ask how many) -> present each draft / routed entry
   for approval before any external write.

Never collapse the three pauses into one. The gates are the product.

`/bet project [description]` is the single-item version: capture one new project, run it through
Select, and on PASS, Spec it. Use it when a specific initiative needs the gate now.

---

## Stage 4: Retroactive backlog grooming (`/bet backlog`)

Goal: keep the EXISTING backlog pointed at the right work. The same gate, applied to tickets already on
the board, plus structural cleanup. This is how the cannon stays aimed over time, not just at intake.

**Triage first: product vs tech (who owns the priority call).** Classify every item before scoring:
- **Product:** customer-facing features, UX, workflows, new capability; value is a customer outcome.
- **Tech:** framework/dependency upgrades, deprecations, refactors, infra, performance, test/CI,
  tech-debt.
- Setting up or syncing a *customer* integration is **product** (customers need it); pure internal
  plumbing of integration code is tech. Engineering spikes / research are tech.

The product gate applies ONLY to product items. **Tech items are NOT product-scored:** their timing is
the dev team's call, who own engineering-health reality. `/bet` still does structural cleanup on tech
items but **defers their prioritization to Dev**: label them `dev-only`, present them as a separate
"for Dev to rank" list, and flag only any tech item that blocks a product bet.

**Evaluate the PRODUCT items.** Produce a grooming plan with these moves:
- **Merge** near-duplicate tickets (keep one, link the rest as duplicates, close them).
- **Evaluate staleness (evidence-based, never a guess or a manual punt).** For old / orphan tickets,
  the system builds context and returns **KEEP / ARCHIVE / MERGE / RESURFACE** with evidence: last
  mention in notes + insights + calls (with a date), theme fit, live customer pull, superseded-by,
  ticket age/status, and whether the codebase shows the feature is already built (a "build X" ticket
  for something that exists = close). Bring the recommendation + evidence to approve; do not ask "is
  this still wanted?" as a manual check.
- **Epic grouping:** cluster related tickets into **small, single-feature epics sized to 2-4 weeks**,
  not large catch-all epics. Finishing one coherent feature before spreading across many small
  unrelated tickets ships value faster. Each epic rolls up to a roadmap theme. Treat existing massive
  epics as re-cut candidates: promote the big one to an Initiative (keep its coordinating narrative),
  re-cut its guts into small epics, commit the actively-worked slice, and return the un-started
  remainder to the ranked backlog. Never let "work is happening somewhere in this epic" protect the
  whole container.
- **Rank** (product items only): order by the 4-lens P-score + hard gates (the same Select logic).
  Re-ranking touches only the backlog *behind* the anchor's in-flight commitments (anti-whiplash rule 1).
- **Sprints:** propose the next sprint's product items from the top of the ranked, ready list,
  respecting capacity, and leave room for the dev team's own tech allocation.

Present the full plan for approval. On approval, apply the changes through your tracker (dry-run first
where possible, then execute only after you approve the specific change). Closing or merging someone
else's ticket is irreversible-ish, so surface the reasoning per item.

---

## Evaluation loop (`/bet eval`): keep the cannon aimed

Goal: verify the system is accurately pointing your work, and recalibrate when it is not. Run monthly
or on demand. The gate's past verdicts are the predictions; reality is the grade.

**Gather outcomes.** For each gated bet, determine what actually happened and record it:
- **PASSED + shipped:** did it deliver? Pull usage from your metrics, customer reaction from insights,
  renewal signal.
- **Shipped then reworked / reverted fast:** the cohesion check missed. This is the highest-signal
  failure, the "random feature that needed immediate rework" the gate exists to stop.
- **HELD / DROPPED that came back** (a competitor shipped it, customers kept asking): the gate was too
  strict or mis-weighted (vindicated).
- **Backlog hygiene drift:** are duplicates / stale tickets re-accumulating faster than you clear them?

**Produce the calibration report** and recommend adjustments for you to approve:
- PASSED bets under-deliver -> the gate is too loose (raise the validation bar, tighten a lens).
- Shipped-then-reworked recurs -> the cohesion grounding is weak (improve the integrity model, weight
  cohesion harder).
- DROPPED-then-vindicated recurs -> too strict or wrong weights (reweight strategic-fit / stakeholder
  pull).

This is the loop that makes the system trustworthy: the gate is only as good as its track record, and
this is where the track record gets measured.

---

## Autonomous Sense (scheduled)

An optional recurring trigger (set up via your scheduling skill) that runs without you:
1. Dispatches the Sense fleet, dedupes, captures new candidates via `/idea`.
2. Reads the funnel and lists the Sensed + Held bets awaiting a gate decision.
3. Messages you the funnel line + the top new candidates, with "reply to run `/bet select`."

It NEVER gates or specs autonomously. It only senses and surfaces. Selection and every external write
stay human-gated.

---

## Making it real: the machinery that helped (a suggestion)

The methodology above is tool-agnostic, but it earned its keep only once it was backed by a bit of
real machinery. None of this is required to start. It is what turned the pipeline from a document into
a system, offered as a starting point, not a mandate.

- **A deterministic state script.** A small CLI over the `product-ideas.yaml` store (Python works
  well) owns the funnel and enforces the push rule *in code*: it refuses a `core` PASS without
  validation, and refuses a PASS that fails identity or shows cohesion `conflict`. Keeping stage state
  out of the LLM is what stops the funnel from being silently re-derived, and re-invented, each run.
- **Code intelligence over your repo.** The architect step (Step C) and evidence-based staleness are
  only trustworthy if they read the *real* code, not a summary. An LSP-grade semantic tool (for
  example Serena, via MCP) lets an agent trace actual symbols and surfaces, so "does this duplicate an
  existing surface?" and "is this feature already built?" become real checks, not guesses.
- **A tracker apply layer beyond the MCP.** Most tracker MCPs can create / edit / link / transition,
  but not rank-order a backlog or build a sprint. A thin script against your tracker's Agile API
  (dry-run by default, an explicit `--execute` to write) closes that gap and keeps the destructive
  operations gated.
- **A metrics source for the eval loop.** Calibration needs real outcomes. Wire it to your usage
  analytics so "did the PASSED bet actually deliver?" is measured, not remembered.
- **A scheduled trigger for Autonomous Sense.** A weekly job that runs Sense and messages you the new
  candidates keeps the funnel fresh without your attention, while every gate and write stays manual.

The through-line: push determinism into scripts (state, the push rule, rank/sprint writes) and reserve
the agents for judgment (scoring, synthesis, the domain read). That split is what made it reliable.

---

## Guidelines

- Sense and Spec delegate to existing skills via sub-agent fleets. The Select gate is the only place
  this skill adds new judgment. Do not duplicate `/idea`, `/prd`, `/roadmap`, or `/insights` logic.
- Always read state from the store, never by eyeballing the YAML. Write gate verdicts only through the
  gate step.
- Always state which Sense sources were live vs skipped.
- Score with the existing 4-lens framework; do not invent a new scale.
- Two-track dev: `demoable` bets can move without full validation; `core` builds require validation =
  pass; `exploration` bypasses validation but requires a conviction + kill-criterion. Enforce this.
- Reuse your standing schedule; do not add redundant crons. `/idea sweep`, market scans, and the
  work-tracker daily plan already feed Sense; `/bet sense` aggregates their outputs on demand.
- Everything external (tracker, directory, email, chat) follows the standing message-send guardrail:
  show, wait for approval, then write.
