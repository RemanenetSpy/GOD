Whitechain Bridge is a centralized cross-chain bridge for moving tokens between WCH-ETH and WCH-TRON. This program rewards vulnerabilities in smart contracts only that affect the safety of user funds. In-scope: on-chain contracts Bridge and Mapper and their direct dependencies as used by these contracts.


All

Scope

Focus Area

Program Rules

Disclosure Guidelines

Eligibility and Coordinated Disclosure

Severity levels

Report requirements (mandatory)

Handling process (SLA)

Payments, KYC, taxes

Safe testing rules

Legal / disclosure terms
In scope
Target
Type
Severity
Reward
https://github.com/whitechain-labs/bridge-contracts
Copied
Smart Contract
Critical
Bounty
Focus Area
IN SCOPE VULNERABILITIES: Smart Contracts
Bridge contract (all logic: bridgeTokens, receiveTokens, withdrawCoinLiquidity, withdrawTokenLiquidity, gas accounting, usedHashes, setDailyLimit, etc.)
Mapper contract (registering/removing/enabling mappings, mapInfo, withdraw/deposit types)
Library and interface contracts only insofar as they affect Bridge/Mapper security (e.g., ECDSAChecks, IERC20, IERC20Mintable)
UUPS proxy and _authorizeUpgrade flows, in context of possible upgrade capture or storage collision
Business logic issues
Unauthorized access / access control bypass (role escalation)
Signature issues: replay, forgery, malleability, bad domain separation
Reentrancy and callback attacks
Bridging daily limits logic
Upgradeability / proxy risks (UUPS, storage collision, uninitialized proxies)
Integer arithmetic / overflow / underflow / precision errors
Token handling issues (for standard ERC-20 tokens)
External call abuses, delegatecall and arbitrary call execution
Incorrect ETH/token accounting (gasAccumulated, contract balance errors)
Denial-of-Service (on-chain) and block gas limit issues
Oracle / external dependency manipulation (if used on-chain)
Cryptography & randomness weaknesses
Access to sensitive data / secrets leaked on-chain
Incorrect type casting / address conversions (bytes32 ↔ address)
Event/logging and monitoring omissions (auditability issues)
Front-running / race conditions (MEV) affecting protocol invariants
Self-destruct / funds locked by design mistakes
Denial via malformed input / improper validation (input sanitization)
Poor upgrade / governance locking policies (timelocks, multisig weaknesses)
Any other on-chain issue with clear potential loss.
OUT OF SCOPE VULNERABILITIES: Smart Contracts
Frontend, backend services, relayer servers, multisig operators, CI/CD, cloud infra, RPC node configuration.
Social engineering, physical access, compromise of org private keys (unless done by exploiting on-chain code).
Theoretical or non-reproducible issues without a PoC.
Architectural criticism of centralization, or design choices that are intentional.
ERC-20 non-standard, fee-on-transfer.
Program Rules
Avoid using web application scanners for automatic vulnerability searching which generates massive traffic
Make every effort not to damage or restrict the availability of products, services, or infrastructure
Avoid compromising any personal data, interruption, or degradation of any service
Don’t access or modify other user data, localize all tests to your accounts
Perform testing only within the scope
Don’t exploit any DoS/DDoS vulnerabilities, social engineering attacks, or spam
Don’t spam forms or account creation flows using automated scanners
In case you find chain vulnerabilities we’ll pay only for vulnerability with the highest severity.
Don’t break any law and stay in the defined scope
Any details of found vulnerabilities must not be communicated to anyone who is not a HackenProof Team or an authorized employee of this Company without appropriate permission
Disclosure Guidelines
Do not discuss this program or any vulnerabilities (even resolved ones) outside of the program without express consent from the organization
No vulnerability disclosure, including partial is allowed for the moment.
Please do NOT publish/discuss bugs
Eligibility and Coordinated Disclosure
We are happy to thank everyone who submits valid reports which help us improve the security. However, only those that meet the following eligibility requirements may receive a monetary reward:

You must be the first reporter of a vulnerability.
The vulnerability must be a qualifying vulnerability
Any vulnerability found must be reported no later than 24 hours after discovery and exclusively through hackenproof.com
You must send a clear textual description of the report along with steps to reproduce the issue, include attachments such as screenshots or proof of concept code as necessary.
You must not be a former or current employee of us or one of its contractor.
ONLY USE the EMAIL under which you registered your HackenProof account (in case of violation, no bounty can be awarded)
Provide detailed but to-the point reproduction steps
AI-generated reports without runable PoC are not accepted under this program.
Severity levels

Final payout within the range depends on real exploitability, impact, and report quality.

Not eligible for reward
Anything outside smart-contract scope.
Issues that require compromising the organization’s private keys or social engineering.
Duplicate reports — reward goes to the first valid reporter.
Pure style / gas optimization suggestions without security impact.
Report requirements (mandatory)
A valid report must include:

Title — concise and specific.
Summary — 1–3 lines describing the impact.
Contracts / addresses / versions — exact addresses and versions used.
Reproduction steps — step-by-step instructions. For EVM, include a minimal script (Hardhat/Foundry/ethers.js) or exact calldata and RPC calls. Use a mainnet fork for destructive PoC.
PoC — runnable proof of concept demonstrating the issue on a fork or testnet; clearly mark commands and expected vs actual outcomes.
Severity assessment— your severity and rationale.
Fix recommendations — precise code suggestions or logical changes.
Artifacts — tx hashes, traces, logs, screenshots if applicable.
Contact — HackenProof username / email for follow-up.
Missing PoC or concrete reproduction may reduce reward or cause rejection.
Handling process (SLA)
Acknowledgement: within 72 hours.
Triage / reproduce: within 7 business days.
Fix & confirmation: priority given to Critical/High. Time to fix varies with complexity.
Payout: after verification and patch deployment; estimated within 14 business days after fix is merged and deployed (subject to HackenProof procedures).
Team may request additional PoC details. The first valid reporter gets priority for reward.

Payments, KYC, taxes
Rewards paid through HackenProof in USD or equivalent crypto, following HackenProof’s payout policies.
KYC may be required for large payouts per platform and regulatory requirements. Be prepared to provide identity and invoicing.
Tax reporting and compliance are the reporter’s responsibility.
Safe testing rules
Do not exploit real user funds. Do not perform destructive actions on production. Use a forked mainnet for PoC that would otherwise require real funds.
Do not publicly disclose vulnerability details before the issue is fixed and coordinated disclosure is approved. Premature publication can disqualify the reporter.
Do not attempt DoS on mainnet in a way that degrades service for users. Describe DoS vectors and demonstrate on a fork.
Follow laws and platform rules.
Legal / disclosure terms
Nature of the Program
This bug bounty program is a discretionary rewards program and not a competition, lottery, or offer of employment.
Submitting a report does not create any entitlement to a reward. All rewards (including whether to grant any reward at all and in what amount within the published ranges) are determined at our sole discretion, taking into account severity, impact, exploitability, scope, and report quality.
We may modify, suspend or terminate this program (including scope, reward ranges, and eligibility criteria) at any time, with prospective effect. Changes do not affect rewards already confirmed and communicated to the reporter.
Eligibility and Restricted Persons
By participating in the program, you represent and warrant that:

You are an individual acting on your own behalf, and at least 18 years old (or the age of majority in your jurisdiction, if higher).
You are not an employee, contractor, or officer of Whitechain or any of its affiliates, and have not been so within the last 12 months.
You are not involved in the development, auditing, or operation of the in-scope contracts in a professional capacity, and you do not have privileged internal access to their code or infrastructure beyond what is publicly available.
You are not subject to sanctions or listed on any sanctions list administered by the EU, UN, US, UK, or any other competent sanctions authority, and you are not a resident of a comprehensively sanctioned jurisdiction.
You are not acting on behalf of any person or entity that would not meet the above conditions.
We may require information and documentation to verify your eligibility and compliance with sanctions, anti-money-laundering, and other regulatory requirements. We may decline or revoke any reward if we have reason to believe that participation or payment would violate applicable law or internal compliance rules.

Lawful Conduct and Safe Harbor
You must comply with all applicable laws and regulations when performing any security research or submitting reports under this program.
You must follow the Scope, Not eligible for reward, and Safe testing rules sections of this policy at all times. In particular, you must avoid any action that:
causes actual loss of user funds or irreversible damage;
accesses, exfiltrates, or manipulates personal data of third parties;
degrades or disrupts production systems beyond what is strictly necessary for proof-of-concept;
involves social engineering, phishing, physical intrusion, or attacks against third-party services.
Safe harbor (to the extent permitted by law):
Provided that you:
act in good faith and within the in-scope targets and rules of this policy;
use non-destructive testing methods (e.g., on forked mainnet) and do not exploit a vulnerability beyond what is necessary to demonstrate impact;
promptly and confidentially disclose the vulnerability via HackenProof as described in this policy,
then Whitechain will not initiate civil action or a complaint to law enforcement against you solely on the basis of your good-faith security research under this program.

This safe harbor:

applies only to activities conducted in compliance with this policy;
does not protect you from actions by third parties (e.g. regulators, law enforcement, other affected entities);
does not constitute a waiver of any legal rights we may have in case of non-compliance, abuse, fraud, extortion, or actual harm.
Nothing in this policy shall be interpreted as granting you permission to act unlawfully or to breach any contractual obligations you may have with third parties.

Confidentiality and Disclosure
All information about vulnerabilities, exploits, PoC code, and related technical or business information obtained through this program is considered confidential.
You must not disclose any such information publicly, or to any third party, without our prior written consent, even after the vulnerability has been fixed, unless we explicitly approve coordinated disclosure.
You may discuss the vulnerability only with Whitechain and through the HackenProof platform as required for triage and remediation.
Premature or unauthorized public disclosure, or disclosure in a way that may harm users or the ecosystem, may result in disqualification from rewards and may limit or remove the safe harbor described above.
Intellectual Property and Use of Submissions
By submitting a report, you grant Whitechain and its affiliates a worldwide, irrevocable, non-exclusive, royalty-free, transferable license to use, reproduce, modify, and distribute the contents of the report (including PoC code, scripts, logs, and documentation) for the purposes of verifying, fixing, and communicating about the vulnerability, and improving our systems, products, and documentation.
You retain any intellectual property rights in your own original PoC code and materials, but you acknowledge that:
we may independently discover, develop, or obtain similar information; and
we may use the information in your report without attribution, beyond what we choose to provide as recognition.
Participation in this program does not give you any ownership or other rights in Whitechain’s smart contracts, code, infrastructure, trademarks, or other intellectual property.
Data Protection, KYC and Privacy
We may collect and process the following categories of data in connection with the program:

HackenProof username and contact details (e.g. email);

blockchain addresses used for payouts;

technical report contents and metadata (logs, tx hashes, timestamps);

KYC / AML information (such as name, date of birth, nationality, address, identification documents, and tax identifiers) to the extent required by law, payment provider rules, or our internal compliance policies.

We process this data for the purposes of:

administering the bug bounty program;

triaging and resolving security issues;

performing KYC/AML and sanctions screening;

making and recording payments and complying with legal obligations (including accounting and regulatory reporting).

Our processing of personal data is further governed by our Privacy Policy, which applies in addition to this program. By participating, you acknowledge that you have read and understood our Privacy Policy.

Taxes and Regulatory Compliance
As stated in Section 9, you are solely responsible for any taxes, duties, or similar charges that may apply to rewards you receive, in your country of residence or any other relevant jurisdiction.
We may require you to provide tax-related information (such as invoicing details or tax identification numbers) in order to process payments.
All rewards are subject to applicable laws and regulations, including financial sanctions, anti-money-laundering and counter-terrorist-financing requirements, and any rules of the platforms or payment providers we use. We may withhold, delay, or decline payment if we reasonably believe that doing so is necessary to comply with such requirements.
No Employment or Agency Relationship
Participation in this program does not create any employment, partnership, joint venture, agency, or fiduciary relationship between you and Whitechain or any of its affiliates.
You act as an independent security researcher, and you are not authorized to represent or bind Whitechain in any way.
Priority and Relationship with Other Terms
This policy applies in addition to the HackenProof platform terms and policies. In case of conflict between this policy and HackenProof’s platform terms on matters relating to the use of the platform itself, the platform terms shall prevail.
In case of conflict between different language versions of this policy (if any), the English version shall prevail.
Governing Law and Jurisdiction
This bug bounty program and any contractual or non-contractual obligations arising out of or in connection with it shall be governed by and construed in accordance with the laws of England and Wales, excluding its conflict-of-law rules.
In the event of any dispute or claim arising out of or in connection with this bug bounty program, the parties shall first seek to resolve the dispute or claim amicably through good-faith negotiations. If a dispute or claim can not be resolved by negotiations, it shall be referred to and finally resolved by arbitration under the LCIA Rules, which Rules are deemed to be incorporated by reference into this clause. The number of arbitrators shall be one (1). The seat (legal place) of arbitration shall be London, England. The language of the arbitration shall be English.
The requirement to attempt amicable settlement through negotiation is a condition precedent to the commencement of arbitration, except where a party seeks interim, conservatory, or injunctive relief.
Nothing in this clause shall prevent either party from seeking interim, conservatory or injunctive measures from the courts of England and Wales, or any other court of competent jurisdiction, in support of the arbitration.