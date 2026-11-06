# Disputes Team – Proposed Target Structure

## 1. Why change

The current structure is organised by **type of work** (analytics, core operations, new products, advisory). This creates a few problems that will get worse as Issuing launches:

- **No one owns the merchant end to end.** A merchant's chargebacks, queries, performance reviews and recovery cases are handled by different units, so knowledge is lost at each hand-off.
- **Recovery is split.** First-cycle representment sits in Core Operations, while second-cycle (pre-arbitration / arbitration) and Managed Recovery sit in Performance & Advisory. The highest-value skill (winning cases) is spread thin.
- **Issuing has no home.** It is currently grouped with APMs under "New Products", but at scale it is a different business: cardholder-facing, regulated timelines, and the opposite side of the dispute.
- **Queue-only roles cause boredom.** A team that only handles merchant queries or control reports has low variety and high attrition.

## 2. Design principles

1. **Own the merchant, not the task.** Operational teams are organised around merchant portfolios (pods) so each analyst sees the full lifecycle for their merchants.
2. **Concentrate expert skills.** Pre-arbitration, arbitration and scheme rules expertise sit in one place and serve both Acquiring and Issuing.
3. **Separate "run" from "improve".** Operations run the cases; a central Intelligence team measures, automates and controls.
4. **Build for Issuing now.** Issuing gets its own unit from launch, seeded with experienced acquiring staff.
5. **Variety by design.** Rotation and project time are built into roles, not left to chance.

## 3. Proposed structure

```
                         Head of Disputes
                                |
   ------------------------------------------------------------------
   |                |                    |               |          |
 Acquiring       Issuing          Recovery &        Merchant      Disputes
 Disputes        Disputes         Arbitration       Performance   Intelligence
 Operations      Operations       Centre            & Advisory    & Controls
 (Merchant pods) (new)            (shared)
```

### 3.1 Acquiring Disputes Operations – organised in merchant pods

Each pod owns a portfolio of merchants for **all first-cycle work**: case intake, evidence review, representment, and **the merchant's day-to-day dispute queries**.

| Pod | Scope |
|---|---|
| Strategic merchants | Top merchants by volume / revenue, named analysts per merchant |
| High-risk verticals | Gaming, trading, crypto, marketplaces (e.g. FanDuel, Polymarket), where scheme rules and evidence requirements are specialised |
| Mid-market & long tail | High volume, process- and automation-led |
| APMs & alternative payments | Specialist pod for non-card dispute flows |

- Merchant queries go to the pod that owns the merchant. This **removes the need for a stand-alone query team** and means the person answering knows the cases.
- Simple, repetitive work (intake, data checks, status queries) is handled by AI / automation first, with Associates handling exceptions.

### 3.2 Issuing Disputes Operations – new unit

Handles disputes raised **on behalf of Checkout.com's cardholders**: intake of cardholder claims, chargeback filing, fraud claims, and regulatory timelines (e.g. Reg E / Reg Z in the US).

- Separate from Acquiring because the customer, regulation and incentives are different.
- **Seeded with experienced acquiring analysts at launch.** Knowing how merchants defend a case makes issuing analysts better at filing one.
- Second-cycle issuing cases go to the Recovery & Arbitration Centre (3.3).

### 3.3 Recovery & Arbitration Centre – shared expert team

Owns **all second-cycle work**: pre-arbitration, arbitration and compliance cases, for both Acquiring and Issuing, including the **Managed Recovery Service**.

- Brings the most experienced case specialists into one team. This is where cases are won or lost and where the success-fee revenue is earned.
- Measured commercially: recovery rate, success-fee revenue, and arbitration fees absorbed.
- Decides when to escalate based on issuer data and previous rulings, supplied by Intelligence & Controls.
- **Conflict control:** where Checkout.com is both the acquirer and the issuer on the same case ("on-us"), the case is handled by separate individuals with clear separation of duties.

### 3.4 Merchant Performance & Advisory

Proactive and strategic. **It doesn't handle cases.**

- Performance reviews and recommendation reports for merchants (e.g. the fraud / service-not-received evidence reviews).
- Prevention: driving adoption of tools such as Visa CE 3.0, Order Insight, RDR / Ethoca / Verifi, and 3DS where relevant.
- Commercial owner of the Managed Recovery Service: selling it, onboarding merchants and reporting on it. The Recovery & Arbitration Centre delivers it.
- Escalation point for complex merchant concerns that go beyond a pod.

### 3.5 Disputes Intelligence & Controls

The "improve" engine for the whole department.

- Reporting, dashboards and KPIs.
- Control reports and quality assurance: case sampling, error tracking.
- AI and automation: evidence auto-assembly, case routing, query auto-responses.
- **Scheme rules centre of excellence:** tracks scheme rule changes, maintains playbooks, and runs training for all units.
- Issuer behaviour and win/loss analytics that feed representment and escalation strategy.

## 4. Roles and career paths

Replace the single ladder with **one shared grade structure and four specialist tracks**, so people can progress without becoming managers.

| Grade | Typical scope |
|---|---|
| Associate (replaces Coordinator) | Intake, data checks, automation exceptions, first-line queries |
| Analyst | Owns cases end to end within a pod |
| Senior Analyst / Specialist | Complex cases, pre-arbitration, mentoring, subject-matter owner |
| Lead | Leads a pod or a desk day to day |
| Manager | Owns a unit |
| Senior Manager / Head | Owns the department |

**Tracks** (from Analyst level upwards):

- **Operations:** case handling and pod leadership.
- **Recovery specialist:** arbitration and scheme rules expertise.
- **Advisory:** merchant-facing performance and strategy.
- **Data & automation:** analytics, controls and AI.

## 5. Preventing boredom and building skills

- **Rotation:** Associates and Analysts rotate between pods (or into Issuing) every 6–12 months, by choice and subject to performance.
- **Secondments:** strong Analysts spend time in the Recovery & Arbitration Centre or Advisory, which acts as a talent pipeline.
- **Project time (about 10–20%):** operations staff join Intelligence projects such as automation, playbooks and AI tooling, so routine work comes with improvement work.
- **Skills matrix:** a visible matrix (reason codes, schemes, APMs, issuing, arbitration) used for development plans and resourcing.

## 6. Key metrics by unit

| Unit | Primary metrics |
|---|---|
| Acquiring Operations | Representment rate, first-cycle win rate, SLA adherence, merchant query resolution time |
| Issuing Operations | Regulatory SLA compliance, filing accuracy, cardholder recovery rate |
| Recovery & Arbitration | Second-cycle win rate, success-fee revenue, net arbitration cost |
| Performance & Advisory | Merchant win-rate uplift, dispute-ratio reduction, Managed Recovery adoption |
| Intelligence & Controls | Automation rate, QA error rate, reporting accuracy, cost per case |

## 7. Phased transition

1. **Phase 1 (0–3 months):**
   - Create the Recovery & Arbitration Centre by consolidating second-cycle work and Managed Recovery.
   - Formalise Intelligence & Controls.
2. **Phase 2 (3–6 months, before Issuing scales):**
   - Stand up Issuing Operations with seconded acquiring staff and new hires.
   - Define Reg E / Reg Z processes and controls.
3. **Phase 3 (6–9 months):**
   - Move Acquiring Operations into merchant pods and route merchant queries to pods.
   - Introduce rotation and the new career tracks.

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Pods create uneven workloads | Intelligence monitors volume; a flexible "float" of analysts moves between pods |
| Loss of specialist depth in operations | Scheme rules centre of excellence plus playbooks; specialists embedded in the high-risk pod |
| Issuing launch pulls experienced staff out of acquiring | Phased secondments, with backfill hiring started in Phase 1 |
| On-us conflicts between Issuing and Acquiring | Separation of duties and an independent review for on-us arbitration |
| Change fatigue | Phased rollout, clear role mapping for each person, early communication |
