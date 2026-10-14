4. Reason Code: FRAUD

While the merchant provides a detailed fraud summary for these disputes (AVS result, IP analysis, customer details and purchase history from their third-party fraud provider), the evidence does not clearly demonstrate that the cardholder participated in or benefited from the transaction (sample below). In particular:

* Purchase history is shown only as totals (e.g. "Number of purchases in polymarket.com: 55") rather than the individual prior transactions the issuer can verify.

* Some data comes from the fraud provider's wider network (e.g. "Number of purchases at Riskified network: 61"). This covers purchases at other merchants, so it cannot be used to show the cardholder's history with Polymarket.

* The device information provided is a user agent (e.g. "iPhone / iOS 26 / native_app") rather than a unique Device ID / fingerprint.

* The IP analysis states that a cellular IP address geolocates to the cardholder's exact street address. Mobile IP addresses cannot normally be located to street level, so this statement may reduce the credibility of the response.

* An AVS full match (Y) supports the case, but on its own it is not a valid remedy for a fraud dispute.

* No evidence is provided of the customer's identity verification (KYC), how the customer logged in when making the deposit, or how the deposited funds were used.




Recommendation:

Outside of the remedies above, card schemes allow merchants to provide compelling evidence in an attempt to recover funds. This evidence should demonstrate that the cardholder participated in the transaction or benefited from it:

* Identity Verification (KYC): Screenshots from your internal platform showing the account creation date (before the disputed transaction), the KYC verification result and date, and that the verified name matches the cardholder name. Sensitive personal data should be masked.

* Login and Authentication Details: Login records for the session in which the deposit was made, showing the date and time, IP address, Device ID and the login method used (e.g. password, 2FA / OTP to the verified phone number or email, biometrics).

* IP Address and Device History: A timeline from your platform records showing the IP address and Device ID used at account registration / KYC, at previous undisputed logins and deposits, and at the disputed transaction. This shows that the same customer has consistently accessed the account over time, rather than a new or unknown user. Please note:
  - The comparison is strongest when it covers several points in time (registration, previous undisputed activity and the disputed transaction), rather than registration and the disputed transaction only.
  - Mobile IP addresses change frequently, so a different IP address does not by itself indicate fraud. Where the IP address differs, the IP address should be shown together with the Device ID, and the IP address location should be shown at city/state level and matched to the cardholder's billing address.
  - Each entry should clearly show the date and time, User ID, IP address and Device ID, taken directly from your system logs.

* Proof of Usage (Trading History): Activity logs showing the deposited funds were credited to the customer's wallet and then used to trade on prediction markets.

* Withdrawal History: Where applicable, evidence of withdrawals from the account to a bank account or wallet in the cardholder's name. This strongly indicates the cardholder controls the account.

* Account Activity After the Transaction: Evidence that the customer continued to use the account (logins, trades, further deposits) after the disputed transaction, and especially after the dispute was raised.

* Prior Undisputed Transactions: A list of previous undisputed deposits made with the same card and the same account / device, showing the date, amount and transaction ID of each one, rather than a total count.

* Customer Communication: Any emails, chats or support tickets where the customer refers to the account, the deposit or their trading activity.

* Cardholder Linkage: As in the section above, the customer's details (Name, Email Address, User/Wallet ID) must be clearly visible and consistent across the registration profile, the funding transaction and the activity logs.

* Supporting Information: AVS and CVV2 match results and the fraud provider's decision may be included as supporting information. However, they should not be the main basis of the defence.

Please note that all evidence should come from your own platform records (e.g. screenshots or system logs from your internal admin interface, clearly showing the User ID and timestamps), rather than only a written summary or third-party data. We also recommend starting the response with a short summary of why the transaction is not fraudulent, followed by the supporting evidence in the order listed above.
