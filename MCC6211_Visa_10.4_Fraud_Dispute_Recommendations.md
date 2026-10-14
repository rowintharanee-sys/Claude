# Recommendations: Defending Visa Fraud Disputes (10.4) – MCC 6211, US Region

**Merchant:** Polymarket (Non-ACH card deposits)
**MCC:** 6211 – Security Brokers / Dealers (trading market)
**Region:** United States
**Dispute reason in scope:** Visa 10.4 – Other Fraud, Card-Absent Environment
**Transaction type:** Online, digital (account funding / deposit), no physical shipping

---

## 1. Summary

The merchant's current representment package has useful data points (AVS full match, IP data, account ID, credit confirmation and a long history with the customer). But it is written as a **narrative fraud-score summary**, not as **Visa-recognised remedies or compelling evidence**. Issuers review these responses against the specific remedies listed for reason code 10.4. If the evidence doesn't map clearly to one of them, the dispute is likely to stand even when the underlying data is strong.

We recommend restructuring the response around three levers, in order of strength:

1. **Liability shift via authentication (3DS / Visa Secure)** – a remedy where it applies, though it's not widely used in the US.
2. **Visa Compelling Evidence 3.0 (CE 3.0)** – the strongest option for this merchant given its high volume of repeat customers.
3. **Other allowable compelling evidence for 10.4** – account, identity, usage and post-transaction activity evidence, taken from the merchant's own platform data.

---

## 2. Remedy 1 – 3DS / Visa Secure authentication

- If the transaction was fully authenticated through Visa Secure (ECI 05) and the authentication data (CAVV) was in the authorisation, the fraud liability shifts to the issuer and a 10.4 dispute is not valid.
- **US applicability:** Strong Customer Authentication isn't mandatory in the US, so 3DS adoption is low and it's often not part of the payment flow. **This remedy is usually not available for the merchant's current US traffic.**
- **Recommendation:** The merchant could consider adding 3DS **selectively** (for example on first deposits, high-value deposits or new cards, or when risk signals are elevated) to get liability shift on the riskiest share of volume.
- **Note:** Liability shift for *attempted* authentication (ECI 06) is restricted for some high-risk MCCs. Check against the current Visa Core Rules whether attempted-authentication liability shift applies to MCC 6211 before relying on it.

---

## 3. Remedy 2 – Visa Compelling Evidence 3.0 (CE 3.0)

CE 3.0 is the most relevant remedy for this merchant. The current package already *suggests* a repeat-customer pattern ("55 purchases on polymarket.com"), but it doesn't present that pattern in the format CE 3.0 requires.

### 3.1 CE 3.0 qualification criteria

| Requirement | What the merchant must show |
|---|---|
| Prior transactions | **At least 2** prior transactions on the **same card (PAN)** at the **same merchant** |
| Time window | Prior transactions processed **between 120 and 365 days before the dispute processing date** |
| Dispute / fraud status | Prior transactions **were not disputed** and **were not reported as fraud** (TC40) |
| Matching data elements | Disputed transaction and both prior transactions share **at least 2** of: **customer IP address**, **device ID / device fingerprint**, **shipping address**, **user account ID / login ID** |
| Mandatory element | **At least 1** of the matching elements must be the **IP address** or the **device ID / fingerprint** |
| Description | Description of the goods or service provided (for example "Account deposit – funds credited to trading account ID xxx") |

### 3.2 Gaps in the current package against CE 3.0

- **Aggregate counts only:** "55 purchases on polymarket.com" isn't CE 3.0 evidence. Issuers need **transaction-level detail** for each qualifying prior transaction: date, amount, transaction or ARN reference, IP address, device ID and account ID.
- **Third-party network data doesn't qualify:** "61 purchases at the Riskified network" includes purchases at other merchants. CE 3.0 only counts prior transactions at the **same merchant**, so this figure should not be used as CE 3.0 evidence.
- **No device ID:** "iPhone / iOS 26 / native_app" is a user agent, not a device ID. The merchant should provide the actual **device identifier or fingerprint value** from its app or fraud tooling.
- **Elements that don't count:** Credit card number, BIN, cookies, email, billing phone and billing name are not CE 3.0 qualifying elements. They can be included as supporting information, but they don't count towards the 2-element match. **Shipping address isn't meaningful for a digital deposit.**
- **120-day rule not checked:** It's not clear whether the prior transactions fall inside the 120–365 day window. Transactions from the last 120 days don't qualify.

### 3.3 Recommended CE 3.0 evidence table (to be generated from the merchant's system data)

| | Disputed transaction | Prior transaction 1 | Prior transaction 2 |
|---|---|---|---|
| Transaction date/time (UTC) | | | |
| Amount / currency | | | |
| Transaction ID / ARN | | | |
| Card (BIN + last 4) | | | |
| User account ID | | | |
| Customer IP address | | | |
| Device ID / fingerprint | | | |
| Disputed / reported as fraud? | Disputed | No | No |
| Days before dispute date | n/a | (120–365) | (120–365) |
| Service description | | | |

> **Note:** For the strongest outcome, the merchant should send the CE 3.0 data to Checkout.com **in a structured format** (for example CSV or JSON fields, or the dashboard / API evidence fields) and not only inside a PDF letter. That way the CE 3.0 data elements can be submitted to Visa correctly. CE 3.0 data can also be shared at the **pre-dispute stage via Visa Order Insight**, which can stop the dispute before it is raised.

---

## 4. Remedy 3 – Other allowable compelling evidence for 10.4 (when CE 3.0 isn't met)

When a case doesn't meet CE 3.0 (for example a new customer, prior transactions inside 120 days, or no IP/device match), the merchant can still defend with **allowable compelling evidence** showing that the cardholder took part in the transaction or benefited from it. For a trading platform (MCC 6211), we recommend the following, in order of strength.

### 4.1 Identity and account ownership (KYC)

- **Account creation:** date the account was created, before the disputed transaction.
- **KYC / identity verification:** outcome and date (ID document check, selfie/liveness, SSN/date-of-birth verification). Show that the **verified name matches the cardholder name**. Mask sensitive data.
- **Linked contact details:** registered email and phone, and when they were verified (email confirmation, SMS OTP).
- **Terms of Service acceptance:** timestamp, version and the IP/device used when accepting.

### 4.2 Authentication of the session for the disputed transaction

- Login record for the session in which the deposit was made: timestamp, IP, device ID, and how the user logged in (password, 2FA / OTP, biometrics, passkey).
- Evidence that the **same device and IP** were used in earlier logins or transactions on the account that weren't disputed.
- Any step-up verification completed at deposit (for example OTP sent to the verified phone number).

### 4.3 Usage of the deposited funds ("service provided")

For a trading or prediction market, this is the strongest evidence after CE 3.0. It shows the cardholder used the value they received.

- **Ledger entry** showing the deposit credited to the account (amount, timestamp, account ID).
- **Trading activity after the deposit:** orders and positions placed with the deposited funds (market name, date/time, amount, IP/device).
- **Withdrawals:** any withdrawals from the account to a **bank account or wallet in the cardholder's name**. This is a strong indicator that the cardholder controls the account.
- **Account activity after the transaction**, especially **after the dispute date**: continued logins, trades or deposits on the same account, device or card.

### 4.4 Undisputed transaction history (when CE 3.0 isn't fully met)

- A list of earlier **undisputed** deposits made with the **same card** and the **same account / device**, even if they fall outside the 120–365 day window or don't meet every CE 3.0 condition. This still supports the case as general compelling evidence.
- Total lifetime deposits and withdrawals on the account.

### 4.5 Cardholder communication

- Any support tickets, chat or emails where the customer refers to the account, the deposit or trading activity, especially around the transaction date.

### 4.6 Supporting signals (useful, but not a remedy on their own)

- **AVS result Y (full match)** and **CVV2 match (M).** These support the case, but **an AVS match alone doesn't remedy a 10.4 dispute.**
- IP geolocation consistent with the billing city or state.
- A fraud vendor's decision (for example Riskified) as supporting context only.

---

## 5. Feedback on the current evidence package (example case `dsp_2y6pj6seqzyennb2mux4ic3nvm`)

| Area | Current state | Recommendation |
|---|---|---|
| **Structure** | Narrative letter built around fraud-vendor output | Lead with the **remedy being claimed** (CE 3.0 or compelling evidence), then the evidence for each element, in the order of Visa's requirements |
| **Prior history** | Aggregate counts (55 / 61) | Transaction-level table of qualifying prior transactions (see 3.3), **same merchant only** |
| **Device data** | User agent only | Include the **device ID / fingerprint value** |
| **IP analysis** | States the cellular IPv6 address geolocates to the **exact street address** | Mobile/cellular IPs can't be geolocated reliably to a street address, and the claim can weaken credibility. Show a **city/state-level** match and, more importantly, the **same IP or device used in earlier undisputed activity** |
| **"Delivery confirmation"** | Statement that funds were credited | Add a **ledger screenshot or export** plus **evidence the funds were used** (trades, withdrawals) |
| **Identity / KYC** | Not included | Add account creation date, KYC outcome, verified name match, ToS acceptance |
| **Login / authentication** | Not included | Add the login event for the deposit session (method, 2FA, device, IP) |
| **Post-dispute activity** | Not included | Add any continued account use after the dispute date |
| **Data source** | Mostly third-party vendor summary | Use the **merchant's own system records** (admin interface or database exports) with timestamps. Use vendor data as supporting context only |
| **Third-party network data** | "Purchases at Riskified network" | Remove or de-emphasise. It isn't the cardholder's history with this merchant and doesn't qualify under CE 3.0 |

### Should the evidence come from the interface or system data?

Yes. The evidence should come from the **merchant's own platform records**:

- **Screenshots from the internal admin or back-office interface** (account profile, KYC status, ledger, login history, trade history), showing the **account ID, timestamps and URL/system name** so they're clearly system-generated. Crop or mask any unnecessary PII.
- A **short summary table** on the first page that links each screenshot to the requirement it satisfies.
- **Structured data** (CSV/JSON or API evidence fields) for CE 3.0 elements, so they can be submitted to Visa in the required format.
- Keep the package **concise and readable**. Issuers spend limited time on each case, so put the strongest evidence first and avoid repeating generic statements.

---

## 6. Recommended response structure (template)

1. **Header:** case ID, network, reason code (10.4), amount, transaction date, order/transaction ID, card BIN + last 4.
2. **Remedy statement (1–2 sentences):** for example *"This transaction qualifies under Visa Compelling Evidence 3.0: the cardholder completed two prior undisputed transactions with us on [date] and [date] using the same card, sharing the same device ID and user account ID with the disputed transaction."* (or the compelling-evidence equivalent).
3. **CE 3.0 table** (section 3.3), if it applies.
4. **Account and identity:** account creation, KYC verification, verified name = cardholder name, ToS acceptance.
5. **Transaction session:** login method / 2FA, IP, device ID, AVS / CVV2 results.
6. **Service provided and usage:** ledger credit, trades placed with the funds, withdrawals to an account in the cardholder's name.
7. **Account activity after the transaction or dispute.**
8. **Customer communication**, if any.
9. **Conclusion:** short restatement of why the cardholder authorised or benefited from the transaction and the request to reverse the dispute.
10. **Appendix:** system screenshots and exports, each labelled with the section it supports.

---

## 7. Prevention recommendations

- **Visa Order Insight:** share transaction and CE 3.0 data with issuers at the inquiry stage, so the cardholder recognises the transaction before a dispute is filed.
- **Selective 3DS:** apply Visa Secure to high-risk deposits (new card, new device, first deposit, high amount) to get liability shift.
- **Descriptor clarity:** make sure the billing descriptor clearly identifies the merchant and the deposit, to reduce "unrecognised transaction" fraud claims.
- **Data capture:** consistently store **device ID**, **IP**, **account ID** and **login method** against every transaction, so CE 3.0 evidence can be generated automatically.
