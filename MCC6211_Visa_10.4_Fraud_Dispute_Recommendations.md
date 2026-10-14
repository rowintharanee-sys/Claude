4. Reason Code: FRAUD
(Visa 10.4 – Other Fraud – Card-Absent Environment)

While the merchant provides a detailed fraud summary for these disputes (AVS result, IP analysis, customer details and purchase history from their third-party fraud provider), the evidence is not structured against the remedies accepted by Visa for this reason code (sample below). In particular:

* Purchase history is shown only as totals (e.g. "Number of purchases in polymarket.com: 55") rather than the individual prior transactions the issuer can verify.

* Some data comes from the fraud provider's wider network (e.g. "Number of purchases at Riskified network: 61"). This covers purchases at other merchants, so it cannot be used to show the cardholder's history with Polymarket.

* The device information provided is a user agent (e.g. "iPhone / iOS 26 / native_app") rather than a unique Device ID / fingerprint.

* The IP analysis states that a cellular IP address geolocates to the cardholder's exact street address. Mobile IP addresses cannot normally be located to street level, so this statement may reduce the credibility of the response.

* An AVS full match (Y) supports the case, but on its own it is not a valid remedy for a fraud dispute.

* No evidence is provided of the customer's identity verification (KYC), how the customer logged in when making the deposit, or how the deposited funds were used.




Recommendation:
The merchant should structure the response around one of the following remedies, in order of strength:

* 3DS Authentication (Visa Secure): Transactions fully authenticated through 3DS (ECI 05) move fraud liability to the issuer, so the fraud dispute is not valid. We acknowledge that 3DS is not mandated in the US region and may not be part of your current payment flow, so this remedy may not be applicable to most of your transactions. However, you may consider applying 3DS selectively to higher-risk deposits (e.g. first deposit, new card, new device or high-value deposits) to benefit from the liability shift.

* Visa Compelling Evidence 3.0 (CE 3.0): Given the high number of repeat customers on your platform, this is the most effective remedy available. Where the following conditions are met, the issuer is not able to continue with the fraud dispute:

  - At least two (2) prior transactions on the same card, processed with Polymarket between 120 and 365 days before the dispute date.
  - The prior transactions must not have been disputed or reported as fraud.
  - The disputed transaction and the prior transactions must share at least two (2) of the following: Customer IP Address, Device ID / Device Fingerprint, Shipping Address, User Account ID / Login ID. At least one (1) of these must be the IP Address or Device ID.
  - A description of the service provided (e.g. "Deposit credited to account ID xxx").

  Please present this information at transaction level, i.e. date, amount, transaction ID / ARN, card BIN and last 4, IP address, Device ID and User Account ID for the disputed transaction and each prior transaction. Please also share the CE 3.0 data elements with us as structured data rather than only within the PDF, so they can be submitted to Visa in the required format.

Where the CE 3.0 conditions are not met (e.g. new customer, or prior transactions less than 120 days old), the merchant can still defend the dispute by providing compelling evidence that the cardholder took part in the transaction or benefited from it:

* Identity Verification (KYC): Screenshots from your internal platform showing the account creation date (before the disputed transaction), the KYC verification result and date, and that the verified name matches the cardholder name. Sensitive personal data should be masked.

* Login and Authentication Details: Login records for the session in which the deposit was made, showing the date and time, IP address, Device ID and the login method used (e.g. password, 2FA / OTP to the verified phone number or email, biometrics).

* Device and IP History: Evidence that the same Device ID and/or IP address was used in previous undisputed logins or transactions on the same account.

* Proof of Usage (Trading History): Activity logs showing the deposited funds were credited to the customer's wallet and then used to trade on prediction markets.

* Withdrawal History: Where applicable, evidence of withdrawals from the account to a bank account or wallet in the cardholder's name. This strongly indicates the cardholder controls the account.

* Account Activity After the Transaction: Evidence that the customer continued to use the account (logins, trades, further deposits) after the disputed transaction, and especially after the dispute was raised.

* Prior Undisputed Transactions: Where CE 3.0 is not fully met, a list of previous undisputed deposits made with the same card and the same account / device still supports the case.

* Customer Communication: Any emails, chats or support tickets where the customer refers to the account, the deposit or their trading activity.

* Cardholder Linkage: As in the section above, the customer's details (Name, Email Address, User/Wallet ID) must be clearly visible and consistent across the registration profile, the funding transaction and the activity logs.

* Supporting Information: AVS and CVV2 match results, IP address location matching the billing city/state, and the fraud provider's decision may be included as supporting information. However, they should not be the main basis of the defence.

Please note that all evidence should come from your own platform records (e.g. screenshots or system logs from your internal admin interface, clearly showing the User ID and timestamps), rather than only a written summary or third-party data. We also recommend starting the response with a short summary stating the remedy being claimed (CE 3.0 or compelling evidence), followed by the supporting evidence in the order listed above.
