# Life After the First Dispute Outcome: Pre-Arbitration & Arbitration by Scheme

**A merchant guide to the second dispute cycle**

---

## 1. Why this document exists

Most merchants understand the first round of a dispute: a chargeback arrives, you send
evidence, you win or you lose. What is far less well understood is what happens *after*
that first outcome — the **second dispute cycle**, made up of **pre-arbitration** and
**arbitration**.

This is where a large share of recoverable revenue is won or lost, for three reasons:

1. **The clocks are short.** The windows in cycle two are measured in 10–15 days, not 30–45.
2. **The action owner changes depending on the scheme and the dispute reason.** In most flows
   the *issuer* decides whether to escalate. In **Visa Allocation (fraud and authorization)
   disputes, the decision sits with you and your acquirer** — and you get only 10 days.
3. **Arbitration has a price tag.** The losing side pays the scheme's filing and review fees
   (typically **USD 400–800**, in addition to the disputed amount), so the final step is a
   commercial decision, not just an evidence decision.

Read section 2 for the plain-English version. Use sections 4–9 when you need the exact flow
for a specific scheme.

---

## 2. The one-minute summary

### 2a. Visa Collaboration, Mastercard, Discover / Diners

> 1. **Initial chargeback** — the cardholder's issuing bank initiates the dispute.
> 2. **Our representment** — we challenge the dispute with your evidence.
> 3. **Issuer rejection** — the issuing bank rejects the evidence, in what is called the
>    **"pre-arbitration"** stage.
> 4. **Formal rebuttal** — we formally escalate and challenge their rejection
>    (the **"pre-arbitration response"**).
> 5. **Final resolution** — the issuing bank must then either accept liability or take the
>    case to formal **arbitration** with the card scheme (e.g. Visa), where the losing party
>    incurs a fee (typically USD 400–800).

### 2b. Visa Allocation (fraud and authorization disputes)

> 1. **Initial chargeback** — the cardholder's issuing bank initiates the dispute.
> 2. **Our representment** — we challenge the dispute with your evidence, in what is called
>    raising the **"pre-arbitration"**.
> 3. **Issuer rejection** — the issuing bank rejects the evidence, in what is called the
>    **"pre-arbitration response"**.
> 4. **Final resolution** — the **merchant** must then either accept liability or take the
>    case to formal **arbitration** with the card scheme, where the losing party incurs a fee
>    (typically USD 400–800).

**The single most important difference:** in Allocation there is no "formal rebuttal" step
for you, because your pre-arbitration *was* the rebuttal. Once the issuer rejects it, the next
move is yours — escalate to arbitration or accept liability.

---

## 3. Who holds the next move — at a glance

### 3a. The decision owner, by scheme

| Scheme / flow | Dispute reasons covered | Who raises pre-arbitration | Who responds to it | **Who decides on arbitration** | Escalation window |
|---|---|---|---|---|---|
| **Visa — Allocation** | Fraud (10.x), Authorization (11.x) | **Merchant / acquirer** (this *is* the dispute response) | Issuer | **Merchant / acquirer** | **10 days** from issuer's rejection |
| **Visa — Collaboration** | Processing errors (12.x), Consumer disputes (13.x) | Issuer (after rejecting our dispute response) | **Merchant / acquirer** | Issuer | **10 days** from our pre-arb response |
| **Mastercard** | All reason codes | Issuer (after rejecting our second presentment) | **Merchant / acquirer** | Issuer | **15 days** from our pre-arb response |
| **Discover / Diners** | All reason codes | Issuer (after rejecting our representment) | **Merchant / acquirer** | Issuer | **10 days** from our pre-arb response |
| **American Express** | All reason codes | *n/a — no pre-arbitration / arbitration cycle* | *n/a* | **Amex itself adjudicates** | *n/a* |

**Rule of thumb:** *Allocation is the only flow where the ball ends up in the merchant's court.
Everywhere else, after our rebuttal, we wait on the issuer.*

### 3b. The complete map

Every path that can follow an initial dispute outcome, across all five scheme flows. Gold nodes are
the points where **you** must act; blue nodes are where the **issuer** acts. Visa Allocation is the
only lane whose final escalation decision is gold.

```mermaid
%%{init: {"flowchart": {"wrappingWidth": 340, "nodeSpacing": 45, "rankSpacing": 55, "htmlLabels": true}, "themeVariables": {"fontSize": "15px", "fontFamily": "Helvetica, Arial, sans-serif"}} }%%
flowchart TD
    START(["<b>Initial dispute raised by the issuer</b>"]) --> EVID["<b>We submit your evidence</b><br/>Visa: Dispute Response · Mastercard: Second Presentment<br/>Discover: Representment · Amex: Representment"]
    EVID --> FORK{"<b>Which scheme and<br/>reason code?</b>"}

    FORK -->|"Visa 10.x / 11.x"| AL1
    FORK -->|"Visa 12.x / 13.x"| CO1
    FORK -->|"Mastercard"| MC1
    FORK -->|"Discover / Diners"| DI1
    FORK -->|"American Express"| AX1

    subgraph AL["VISA ALLOCATION — fraud and authorization · MERCHANT holds the escalation right"]
        direction TB
        AL1["Our filing <b>is</b> the pre-arbitration<br/><i>no separate rebuttal stage</i>"] --> AL2{"Issuer reviews<br/>⏱ 30 days"}
        AL2 -->|Accepts| ALW["✅ <b>WIN</b><br/>no scheme fees"]
        AL2 -->|"Rejects — Pre-Arbitration Response"| AL3{"⚠️ <b>MERCHANT DECIDES</b><br/>⏱ 10 days"}
        AL3 -->|"Accept liability"| ALL["❌ <b>LOSS</b><br/>no scheme fees"]
        AL3 -->|"We file Arbitration"| ALA["⚖️ <b>Scheme ruling</b><br/>loser pays USD 400–800"]
    end

    subgraph CO["VISA COLLABORATION — processing and consumer disputes · ISSUER holds the escalation right"]
        direction TB
        CO1{"Issuer reviews<br/>⏱ 30 days"}
        CO1 -->|Accepts| COW["✅ <b>WIN</b>"]
        CO1 -->|"Rejects — raises Pre-Arbitration"| CO2["<b>We file the Pre-Arbitration Response</b><br/>your formal rebuttal · ⏱ 30 days"]
        CO2 --> CO3{"<b>ISSUER DECIDES</b><br/>⏱ 10 days"}
        CO3 -->|"Accepts liability"| COW2["✅ <b>WIN</b><br/>no scheme fees"]
        CO3 -->|"Issuer files Arbitration"| COA["⚖️ <b>Scheme ruling</b><br/>loser pays USD 400–800"]
    end

    subgraph MC["MASTERCARD — all reason codes · ISSUER holds the escalation right"]
        direction TB
        MC1{"Issuer reviews<br/>⏱ 45 days"}
        MC1 -->|Accepts| MCW["✅ <b>WIN</b>"]
        MC1 -->|"Rejects — raises Pre-Arbitration"| MC2["<b>We file the Pre-Arbitration Response</b><br/>⚠️ ⏱ only 10 days — silence = loss"]
        MC2 --> MC3{"<b>ISSUER DECIDES</b><br/>⏱ 15 days"}
        MC3 -->|"Accepts liability"| MCW2["✅ <b>WIN</b><br/>no scheme fees"]
        MC3 -->|"Issuer files Arbitration Case"| MCA["⚖️ <b>Scheme ruling</b><br/>loser pays USD 400–800"]
    end

    subgraph DI["DISCOVER / DINERS — all reason codes · ISSUER holds the escalation right"]
        direction TB
        DI1{"Issuer reviews<br/>⏱ 30 days"}
        DI1 -->|Accepts| DIW["✅ <b>WIN</b>"]
        DI1 -->|"Rejects — raises Pre-Arbitration"| DI2["<b>We file the Pre-Arbitration Response</b><br/>⏱ 30 days"]
        DI2 --> DI3{"<b>ISSUER DECIDES</b><br/>⏱ 10 days"}
        DI3 -->|"Accepts liability"| DIW2["✅ <b>WIN</b><br/>no scheme fees"]
        DI3 -->|"Issuer files Arbitration"| DIA["⚖️ <b>Scheme ruling</b><br/>loser pays USD 400–800"]
    end

    subgraph AX["AMERICAN EXPRESS — three-party network · NO second cycle exists"]
        direction TB
        AX1{"<b>Amex adjudicates</b><br/>its decision is final"}
        AX1 -->|"In your favour"| AXW["✅ <b>WIN</b>"]
        AX1 -->|"Against you"| AXL["❌ <b>LOSS</b><br/>no escalation route,<br/>no arbitration fees"]
    end

    style AL fill:#fdf6e3,stroke:#d9c48a
    style CO fill:#eef4fa,stroke:#a8c3dd
    style MC fill:#f3f0fa,stroke:#bdb2dd
    style DI fill:#edf6f0,stroke:#a9cdb6
    style AX fill:#f4f5f7,stroke:#c2c7d0
    classDef win fill:#1b7f4d,stroke:#0f5132,color:#ffffff
    classDef loss fill:#a4262c,stroke:#6e1a1e,color:#ffffff
    classDef arb fill:#5b3f9e,stroke:#3d2a6b,color:#ffffff
    classDef merchant fill:#b8860b,stroke:#7a5a07,color:#ffffff
    classDef issuer fill:#1f5f8b,stroke:#15405e,color:#ffffff
    classDef start fill:#333333,stroke:#111111,color:#ffffff

    class ALW,COW,COW2,MCW,MCW2,DIW,DIW2,AXW win
    class ALL,AXL loss
    class ALA,COA,MCA,DIA arb
    class AL3,AL1,CO2,MC2,DI2 merchant
    class AL2,CO1,CO3,MC1,MC3,DI1,DI3,AX1 issuer
    class START,EVID,FORK start
```

> A rendered, print-ready version of this map and of every per-scheme diagram below is in
> [`dispute-flow-diagrams.html`](./dispute-flow-diagrams.html) — open it in a browser, or print it
> to PDF to send on.

---

## 4. Terminology decoder

The same four things are called different names in each scheme. This table is the Rosetta
Stone for everything that follows.

| What is actually happening | Visa Allocation | Visa Collaboration | Mastercard | Discover / Diners |
|---|---|---|---|---|
| Issuer opens the dispute | Dispute | Dispute | First chargeback | Dispute / chargeback |
| We challenge it with your evidence | **Dispute response** (filed *as* a pre-arbitration) | **Dispute response** | **Second presentment** | **Representment / dispute response** |
| Issuer refuses to accept our evidence | **Pre-arbitration response** | **Pre-arbitration** | **Pre-arbitration (pre-arb case)** | **Pre-arbitration** |
| We formally rebut that refusal | *(no separate step)* | **Pre-arbitration response** | **Pre-arbitration response** | **Pre-arbitration response** |
| Scheme makes a binding ruling | **Arbitration** | **Arbitration** | **Arbitration case** | **Arbitration / dispute resolution** |

> **Watch out:** "pre-arbitration" means the *opposite direction of travel* in Visa Allocation
> versus every other flow. In Allocation **we** raise it; elsewhere the **issuer** raises it.
> This is the single biggest source of confusion when reading dispute case notes.

---

## 5. Visa — Allocation (fraud & authorization disputes)

Applies to Visa reason codes **10.x (fraud)** and **11.x (authorization)**. Visa *allocates*
liability up front based on data it already holds, which is why your evidence enters the flow
as a pre-arbitration rather than as a plain response.

### Flow

```mermaid
flowchart TD
    A["Issuer initiates dispute<br/>(Visa allocates liability to merchant)"] --> B
    B["<b>We file the Dispute Response</b><br/>= raising pre-arbitration<br/>(your evidence)"] --> C{"Issuer reviews"}
    C -->|Accepts| W["✅ Case closed in your favour<br/>Funds returned, no scheme fees"]
    C -->|"Rejects (Pre-Arbitration Response)"| D{"<b>MERCHANT DECIDES</b><br/>⏱ 10 days only"}
    D -->|Accept liability| L["❌ Chargeback stands<br/>No arbitration fees"]
    D -->|Escalate| E["We file <b>Arbitration</b> with Visa"]
    E --> F["Visa issues a binding ruling"]
    F --> G["Losing party pays the<br/>disputed amount + scheme fees<br/>(typically USD 400–800)"]

    classDef merchant fill:#b8860b,stroke:#7a5a07,color:#ffffff
    classDef issuer fill:#1f5f8b,stroke:#15405e,color:#ffffff
    classDef win fill:#1b7f4d,stroke:#0f5132,color:#ffffff
    classDef loss fill:#a4262c,stroke:#6e1a1e,color:#ffffff
    classDef arb fill:#5b3f9e,stroke:#3d2a6b,color:#ffffff
    classDef neutral fill:#eef1f5,stroke:#8a94a3,color:#1a1a1a
    class A,C issuer
    class B,D,E merchant
    class W win
    class L loss
    class F,G arb
```

### Stage-by-stage

| # | Stage | Scheme name | Who acts | Indicative window | If no action is taken |
|---|---|---|---|---|---|
| 1 | Dispute raised | Dispute | Issuer | — | — |
| 2 | Evidence submitted | Dispute response (pre-arbitration) | **Merchant → Checkout → acquirer** | 30 days from dispute | Dispute stands; liability is yours |
| 3 | Issuer verdict | Pre-arbitration response | Issuer | 30 days | Treated as accepted in your favour |
| 4 | **Escalation decision** | Arbitration filing | **Merchant / acquirer** | **10 days from rejection** | Case closes against you; no fees |
| 5 | Binding ruling | Arbitration decision | Visa | Varies (typically weeks) | — |

### What this means for you

- **Step 4 is the one to diarise.** Ten days is the entire window, and it includes the time
  Checkout needs to prepare and file. Please aim to give us your instruction and any final
  supporting evidence **within 3–4 business days** of us notifying you of the rejection.
- You cannot add fundamentally new arguments at arbitration — Visa rules on the case as
  constructed. **Front-load your strongest evidence at step 2.**
- If the economics don't justify it (low ticket value versus a USD 400–800 downside), accepting
  liability at step 4 is a legitimate, fee-free outcome.

---

## 6. Visa — Collaboration (processing errors & consumer disputes)

Applies to Visa reason codes **12.x (processing errors)** and **13.x (consumer disputes)**. Here
the two sides *collaborate* through a conventional back-and-forth, and the issuer keeps the
escalation right.

### Flow

```mermaid
flowchart TD
    A["Issuer initiates dispute"] --> B["<b>We file the Dispute Response</b><br/>(your evidence)"]
    B --> C{"Issuer reviews"}
    C -->|Accepts| W["✅ Case closed in your favour"]
    C -->|Rejects| D["Issuer raises <b>Pre-Arbitration</b>"]
    D --> E{"<b>MERCHANT DECIDES</b><br/>fight back or accept?"}
    E -->|Accept| L["❌ Chargeback stands"]
    E -->|Fight back| F["<b>We file the Pre-Arbitration Response</b><br/>(formal rebuttal)"]
    F --> G{"<b>ISSUER DECIDES</b><br/>⏱ 10 days"}
    G -->|Accepts liability| W2["✅ Case closed in your favour"]
    G -->|Escalates| H["Issuer files <b>Arbitration</b> with Visa"]
    H --> I["Visa issues a binding ruling"]
    I --> J["Losing party pays the<br/>disputed amount + scheme fees<br/>(typically USD 400–800)"]

    classDef merchant fill:#b8860b,stroke:#7a5a07,color:#ffffff
    classDef issuer fill:#1f5f8b,stroke:#15405e,color:#ffffff
    classDef win fill:#1b7f4d,stroke:#0f5132,color:#ffffff
    classDef loss fill:#a4262c,stroke:#6e1a1e,color:#ffffff
    classDef arb fill:#5b3f9e,stroke:#3d2a6b,color:#ffffff
    classDef neutral fill:#eef1f5,stroke:#8a94a3,color:#1a1a1a
    class A,C,D,G,H issuer
    class B,E,F merchant
    class W,W2 win
    class L loss
    class I,J arb
```

### Stage-by-stage

| # | Stage | Scheme name | Who acts | Indicative window | If no action is taken |
|---|---|---|---|---|---|
| 1 | Dispute raised | Dispute | Issuer | — | — |
| 2 | Evidence submitted | Dispute response | **Merchant → Checkout → acquirer** | 30 days from dispute | Dispute stands; liability is yours |
| 3 | Issuer rejects | Pre-arbitration | Issuer | 30 days | Case closes in your favour |
| 4 | Formal rebuttal | **Pre-arbitration response** | **Merchant → Checkout → acquirer** | 30 days from pre-arb | Pre-arb is deemed accepted; you lose |
| 5 | **Escalation decision** | Arbitration filing | Issuer | **10 days from our response** | Case closes in your favour |
| 6 | Binding ruling | Arbitration decision | Visa | Varies | — |

### What this means for you

- **Step 4 is your last chance to put evidence on the record.** Treat it as a second, stronger
  representment, not a formality.
- After step 4 you are waiting. **Most issuers do not escalate** — filing arbitration exposes
  them to the same fee risk, so a well-argued pre-arbitration response very often ends the case.
- If the issuer does escalate, no further evidence is requested from you; Visa rules on the file.

---

## 7. Mastercard

The sequence is identical in shape to Visa Collaboration. Only the **wording** and the **final
escalation window** differ.

### Flow

```mermaid
flowchart TD
    A["Issuer raises <b>First Chargeback</b>"] --> B["<b>We file the Second Presentment</b><br/>(your evidence)"]
    B --> C{"Issuer reviews"}
    C -->|Accepts| W["✅ Case closed in your favour"]
    C -->|Rejects| D["Issuer raises <b>Pre-Arbitration</b>"]
    D --> E{"<b>MERCHANT DECIDES</b><br/>fight back or accept?"}
    E -->|Accept| L["❌ Chargeback stands"]
    E -->|Fight back| F["<b>We file the Pre-Arbitration Response</b><br/>(formal rebuttal)"]
    F --> G{"<b>ISSUER DECIDES</b><br/>⏱ 15 days"}
    G -->|Accepts liability| W2["✅ Case closed in your favour"]
    G -->|Escalates| H["Issuer files an <b>Arbitration Case</b><br/>with Mastercard"]
    H --> I["Mastercard issues a binding ruling"]
    I --> J["Losing party pays the<br/>disputed amount + scheme fees<br/>(typically USD 400–800)"]

    classDef merchant fill:#b8860b,stroke:#7a5a07,color:#ffffff
    classDef issuer fill:#1f5f8b,stroke:#15405e,color:#ffffff
    classDef win fill:#1b7f4d,stroke:#0f5132,color:#ffffff
    classDef loss fill:#a4262c,stroke:#6e1a1e,color:#ffffff
    classDef arb fill:#5b3f9e,stroke:#3d2a6b,color:#ffffff
    classDef neutral fill:#eef1f5,stroke:#8a94a3,color:#1a1a1a
    class A,C,D,G,H issuer
    class B,E,F merchant
    class W,W2 win
    class L loss
    class I,J arb
```

### Stage-by-stage

| # | Stage | Scheme name | Who acts | Indicative window | If no action is taken |
|---|---|---|---|---|---|
| 1 | Dispute raised | First chargeback | Issuer | — | — |
| 2 | Evidence submitted | **Second presentment** | **Merchant → Checkout → acquirer** | 45 days from chargeback | Chargeback stands; liability is yours |
| 3 | Issuer rejects | **Pre-arbitration** | Issuer | 45 days from second presentment | Case closes in your favour |
| 4 | Formal rebuttal | **Pre-arbitration response** | **Merchant → Checkout → acquirer** | **10 days from pre-arb** — the tightest merchant-side clock in the Mastercard flow | Pre-arb is deemed accepted; you lose |
| 5 | **Escalation decision** | Arbitration case filing | Issuer | **15 days from our response** | Case closes in your favour |
| 6 | Binding ruling | Arbitration decision | Mastercard | Varies | — |

### What this means for you

- **Mastercard's merchant-side rebuttal window at step 4 is short.** Silence is read as
  agreement, so an unanswered pre-arbitration is an automatic loss. If you want to defend,
  tell us quickly — ideally within **2–3 business days** of our notification.
- The issuer then gets **15 days** (rather than Visa's 10) to decide on arbitration, so expect
  a slightly longer wait before the case closes.
- Mastercard requires the issuer to attempt pre-arbitration *before* arbitration. That is good
  news for you: it guarantees you a rebuttal opportunity you can use.

---

## 8. Discover / Diners Club

Discover (which also operates Diners Club) follows the same structure as Visa Collaboration,
including the **10-day** issuer escalation window. Discover acts as both network and, for many
cards, the issuer — so the "issuer" in the flow below may be Discover itself.

### Flow

```mermaid
flowchart TD
    A["Issuer initiates dispute"] --> B["<b>We file the Representment</b><br/>(your evidence)"]
    B --> C{"Issuer reviews"}
    C -->|Accepts| W["✅ Case closed in your favour"]
    C -->|Rejects| D["Issuer raises <b>Pre-Arbitration</b>"]
    D --> E{"<b>MERCHANT DECIDES</b><br/>fight back or accept?"}
    E -->|Accept| L["❌ Chargeback stands"]
    E -->|Fight back| F["<b>We file the Pre-Arbitration Response</b><br/>(formal rebuttal)"]
    F --> G{"<b>ISSUER DECIDES</b><br/>⏱ 10 days"}
    G -->|Accepts liability| W2["✅ Case closed in your favour"]
    G -->|Escalates| H["Issuer files <b>Arbitration</b><br/>with Discover"]
    H --> I["Discover issues a binding ruling"]
    I --> J["Losing party pays the<br/>disputed amount + scheme fees<br/>(typically USD 400–800)"]

    classDef merchant fill:#b8860b,stroke:#7a5a07,color:#ffffff
    classDef issuer fill:#1f5f8b,stroke:#15405e,color:#ffffff
    classDef win fill:#1b7f4d,stroke:#0f5132,color:#ffffff
    classDef loss fill:#a4262c,stroke:#6e1a1e,color:#ffffff
    classDef arb fill:#5b3f9e,stroke:#3d2a6b,color:#ffffff
    classDef neutral fill:#eef1f5,stroke:#8a94a3,color:#1a1a1a
    class A,C,D,G,H issuer
    class B,E,F merchant
    class W,W2 win
    class L loss
    class I,J arb
```

### Stage-by-stage

| # | Stage | Scheme name | Who acts | Indicative window | If no action is taken |
|---|---|---|---|---|---|
| 1 | Dispute raised | Dispute / chargeback | Issuer | — | — |
| 2 | Evidence submitted | Representment / dispute response | **Merchant → Checkout → acquirer** | 30 days from dispute | Dispute stands; liability is yours |
| 3 | Issuer rejects | Pre-arbitration | Issuer | 30 days | Case closes in your favour |
| 4 | Formal rebuttal | Pre-arbitration response | **Merchant → Checkout → acquirer** | 30 days from pre-arb | Pre-arb is deemed accepted; you lose |
| 5 | **Escalation decision** | Arbitration filing | Issuer | **10 days from our response** | Case closes in your favour |
| 6 | Binding ruling | Arbitration decision | Discover | Varies | — |

---

## 9. American Express (and other networks)

### American Express

Amex is a **three-party network**: it is the network *and* the issuer. There is therefore **no
pre-arbitration and no arbitration cycle** — no third party exists to arbitrate between.

```mermaid
flowchart TD
    A["Amex raises an <b>Inquiry</b><br/>(information request)"] --> B["We respond with your evidence"]
    B --> C{"Amex reviews"}
    C -->|Satisfied| W["✅ No chargeback raised"]
    C -->|Not satisfied| D["Amex raises a <b>Chargeback</b>"]
    D --> E["<b>We file the Representment</b><br/>(your evidence)"]
    E --> F{"<b>AMEX DECIDES</b><br/>— and that decision is final"}
    F -->|In your favour| W2["✅ Funds returned"]
    F -->|Against you| L["❌ Chargeback stands<br/>(may be re-raised as a final chargeback)"]

    classDef merchant fill:#b8860b,stroke:#7a5a07,color:#ffffff
    classDef issuer fill:#1f5f8b,stroke:#15405e,color:#ffffff
    classDef win fill:#1b7f4d,stroke:#0f5132,color:#ffffff
    classDef loss fill:#a4262c,stroke:#6e1a1e,color:#ffffff
    classDef arb fill:#5b3f9e,stroke:#3d2a6b,color:#ffffff
    classDef neutral fill:#eef1f5,stroke:#8a94a3,color:#1a1a1a
    class A,C,D,F issuer
    class B,E merchant
    class W,W2 win
    class L loss
```

| Stage | Who acts | Notes |
|---|---|---|
| Inquiry | **Merchant** | Answer it. A good inquiry response often prevents the chargeback entirely. |
| Chargeback | Amex | — |
| Representment | **Merchant → Checkout** | Typically 20 days. Your one substantive defence. |
| Final decision | Amex | **No escalation route, no arbitration fees.** |

**Practical consequence:** with Amex, everything rides on the quality of your first response.
There is no second cycle to fall back on.

### JCB, UnionPay and other networks

These generally follow a two-cycle structure broadly similar to Visa Collaboration (dispute →
representment → pre-arbitration/second chargeback → arbitration), but volumes are low and the
rules vary by region and acquiring arrangement. **If you receive one of these, raise it with your
Checkout contact and we will confirm the exact applicable windows case by case** rather than
assume the Visa/Mastercard timings apply.

---

## 10. Master comparison

| | **Visa Allocation** | **Visa Collaboration** | **Mastercard** | **Discover / Diners** | **Amex** |
|---|---|---|---|---|---|
| Dispute reasons | Fraud 10.x, Auth 11.x | Processing 12.x, Consumer 13.x | All | All | All |
| Our first defence is called | Dispute response (= pre-arb) | Dispute response | Second presentment | Representment | Representment |
| Issuer's rejection is called | Pre-arbitration response | Pre-arbitration | Pre-arbitration | Pre-arbitration | *n/a* |
| Do we get a formal rebuttal? | ❌ No separate step | ✅ Pre-arb response | ✅ Pre-arb response | ✅ Pre-arb response | ❌ |
| **Who can escalate to arbitration** | **Merchant / acquirer** | Issuer | Issuer | Issuer | *Nobody* |
| **Escalation window** | **10 days** | **10 days** | **15 days** | **10 days** | *n/a* |
| Number of merchant evidence submissions | 1 | 2 | 2 | 2 | 1 (+ inquiry) |
| Losing-party fee exposure | ✅ USD ~400–800 | ✅ USD ~400–800 | ✅ USD ~400–800 | ✅ USD ~400–800 | ❌ None |
| Ruling is final & binding | ✅ | ✅ | ✅ | ✅ | ✅ (Amex's own) |

---

## 11. The economics of arbitration

Arbitration is the only stage of the dispute lifecycle where **losing costs you more than the
transaction**. Before escalating — or before deciding how hard to fight a pre-arbitration —
weigh these up:

| Factor | Why it matters |
|---|---|
| **Disputed amount** | Below roughly USD 500–1,000, a USD 400–800 fee can exceed the value of winning. High-ticket cases are where arbitration pays. |
| **Strength of evidence** | Arbitration is decided on the written file against the scheme's rulebook, not on fairness. A clear rule breach by the issuer is a strong case; "the customer is being unreasonable" is not. |
| **Scheme rule compliance** | If your original transaction had a technical defect (missing 3DS, wrong MCC, late presentment), you are likely to lose regardless of the commercial merits. |
| **Precedent value** | A pattern of identical disputes from one issuer or one product line can justify escalating one case to establish a position. |
| **Who pays** | The **losing party** pays the scheme's filing and review fees. Fee levels are set by each scheme and change periodically — we will confirm the current figure for your case before filing. |

**The pre-arbitration stage is where most cases are actually won.** Accepting at pre-arbitration
is free for the issuer, so a rebuttal that makes their arbitration case look weak is often
enough to close the matter without anyone paying a fee. Put your effort there.

---

## 12. What we need from you, and when

| Trigger | What we need | Target turnaround |
|---|---|---|
| Dispute / chargeback notification | Full evidence pack (see below) | Within 7 calendar days |
| Pre-arbitration received (Visa Collaboration, Mastercard, Discover) | Your decision to defend, plus any new evidence | **2–3 business days** (Mastercard is tightest) |
| Pre-arbitration response rejected (**Visa Allocation only**) | Your instruction to file arbitration or accept liability | **3–4 business days** — the total window is 10 days |
| Arbitration filed by either side | Nothing further — the file is closed to new evidence | — |

### Evidence pack checklist

- Transaction record: amount, date, currency, authorization code, ARN
- Authentication data: 3DS result, AVS/CVV match, device and IP data
- Proof of delivery or service: tracking, signature, download/access logs, usage timestamps
- Customer records: account history, previous undisputed orders, login history
- Communications: emails, chat logs, support tickets, cancellation or refund correspondence
- Your terms: T&Cs accepted at checkout, refund/cancellation policy, subscription consent
- For subscriptions: sign-up record, billing schedule disclosure, cancellation path evidence

**Unresponded means lost.** Across every scheme except Amex, failing to answer within the window
is treated as accepting liability. A fast "no, we won't defend this one" is better than silence.

---

## 13. Quick decision guide

```mermaid
flowchart TD
    S["Our first defence was rejected"] --> Q1{"Which scheme<br/>and reason code?"}
    Q1 -->|"Visa 10.x / 11.x<br/>(Allocation)"| A1["⚠️ <b>The next move is yours.</b><br/>10 days to file arbitration<br/>or accept liability"]
    Q1 -->|"Visa 12.x / 13.x,<br/>Mastercard,<br/>Discover / Diners"| A2["You have a rebuttal:<br/>file the pre-arbitration response"]
    Q1 -->|"Amex"| A3["No further stage.<br/>Amex's decision is final"]
    A1 --> Q2{"Is the amount worth<br/>a USD 400–800 downside<br/>on a loss?"}
    Q2 -->|Yes, and evidence is strong| E1["Instruct us to escalate"]
    Q2 -->|No, or evidence is weak| E2["Accept liability — fee-free"]
    A2 --> Q3{"Do you have evidence<br/>that answers the issuer's<br/>specific objection?"}
    Q3 -->|Yes| E3["Send it within 2–3 business days"]
    Q3 -->|No| E4["Accept — avoids wasted effort"]
    E3 --> F["Then wait: the issuer has<br/>10 days (Visa / Discover)<br/>or 15 days (Mastercard)"]

    classDef merchant fill:#b8860b,stroke:#7a5a07,color:#ffffff
    classDef issuer fill:#1f5f8b,stroke:#15405e,color:#ffffff
    classDef win fill:#1b7f4d,stroke:#0f5132,color:#ffffff
    classDef loss fill:#a4262c,stroke:#6e1a1e,color:#ffffff
    classDef arb fill:#5b3f9e,stroke:#3d2a6b,color:#ffffff
    classDef neutral fill:#eef1f5,stroke:#8a94a3,color:#1a1a1a
    class S,Q1 neutral
    class A1,A2,Q2,Q3,E1,E3 merchant
    class A3,F issuer
    class E2,E4 loss
```

---

## 14. Glossary

| Term | Meaning |
|---|---|
| **Allocation** | Visa's flow for fraud and authorization disputes, where Visa assigns liability up front from data it already holds. |
| **Arbitration** | The scheme's binding ruling on a dispute, with the losing party paying the scheme's fees. |
| **Collaboration** | Visa's flow for processing-error and consumer disputes, resolved by evidence exchange between the parties. |
| **First chargeback** | Mastercard's term for the issuer's initial dispute. |
| **Pre-arbitration** | A formal pre-escalation step. In Visa Allocation it is *our* evidence filing; in every other flow it is the *issuer's* rejection of our evidence. |
| **Pre-arbitration response** | The reply to a pre-arbitration. In Visa Allocation this is the *issuer's* rejection; elsewhere it is *our* formal rebuttal. |
| **Representment / dispute response** | Our submission of your evidence against the initial dispute. |
| **Second presentment** | Mastercard's term for the representment. |
| **ARN** | Acquirer Reference Number — the unique identifier used to trace a transaction through a dispute. |

---

## 15. Important notes on this document

- **Timeframes are the operative windows in our dispute-handling process and reflect current
  scheme rules.** Card schemes revise their rulebooks (Visa and Mastercard typically twice a
  year), and some windows vary by region, reason code, and acquiring arrangement. Where a case
  is close to a deadline we will always confirm the exact date that applies.
- **Fee figures are indicative.** The USD 400–800 range covers typical scheme filing and review
  fees for the losing party. Current amounts are set by each scheme and will be confirmed before
  any arbitration filing.
- **All windows are calendar days unless stated otherwise**, and they run from the scheme's
  processing date — not from the date we notify you. This is why our internal turnaround targets
  in section 12 are shorter than the scheme windows.
- Please raise any case-specific questions with your Checkout account or disputes contact.

