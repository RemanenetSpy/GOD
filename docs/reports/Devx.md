Is an innovative infrastructure of 50+ smart contracts for building and governing effective DAOs.


All

Scope

Focus Area

Program Rules

Disclosure Guidelines

Eligibility and Coordinated Disclosure
In scope
Target
Type
Severity
Reward
https://github.com/dexe-network/DeXe-Protocol/tree/master/contracts
Copied
Smart Contract
Critical
Bounty
Focus Area
How DEXE Protocol works: https://whitepaper.dexe.network/

Documentation can be found here: https://docs.dexe.network/

IN-SCOPE: SMART CONTRACT VULNERABILITIES
We are looking for evidence and reasons for incorrect behavior of the smart contract, which could cause unintended functionality:

Critical
Manipulation of governance voting result deviating from voted outcome and resulting in a direct change from intended effect of original results
Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield
Direct theft of any user NFTs, whether at-rest or in-motion, other than unclaimed royalties
Permanent freezing of funds
Permanent freezing of NFTs
Unauthorized minting of NFTs
Unintended alteration of what the NFT represents (e.g. token URI, payload, artistic content)
Protocol insolvency
High
Theft of unclaimed yield
Theft of unclaimed royalties
Permanent freezing of unclaimed yield
Permanent freezing of unclaimed royalties
Temporary freezing of funds
Temporary freezing NFTs
Medium
Unauthorized transaction
Smart contract unable to operate due to lack of token funds
Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)
OUT OF SCOPE: SMART CONTRACT VULNERABILITIES
Theoretical vulnerabilities without any proof or demonstration
Old compiler version
The compiler version is not locked
Vulnerabilities in imported contracts
Code style guide violations
Redundant code
Gas optimizations
Impacts requiring attacks that the reporter has already exploited themselves, leading to damage
Impacts caused by attacks requiring access to leaked keys/credentials
Impacts caused by attacks requiring access to privileged addresses (governance, strategist) except in such cases where the contracts are intended to have no privileged access to functions that make the attack possible
Impacts relying on attacks involving the depegging of an external stablecoin where the attacker does not directly cause the depegging due to a bug in code
Mentions of secrets, access tokens, API keys, private keys, etc. in Github will be considered out of scope without proof that they are in-use in production
Best practice recommendations
Feature requests
Impacts on test files and configuration files unless stated otherwise in the bug bounty program
Incorrect data supplied by third party oracles
Not to exclude oracle manipulation/flash loan attacks
Impacts requiring basic economic and governance attacks (e.g. 51% attack)
Lack of liquidity impacts
Impacts from Sybil attacks
Impacts involving centralization risks
We do not limit parameters of TokenSale proposal. Users may create proposals that will not ever end. The participation in such proposal will not give users rewards.
The project operates with NFTs that users may use to vote in DAOs. There is a possibility to hit an "unbounded loop" here. The protocol does not work with deflationary/rebasing tokens.
Lack of treasury tokens on DAO pool with voting rewards set. This will affect users who claim tokens.
DAOs created intentionally with exploitable ERC20/ERC721 tokens which as a result lead to exploitable DAOs
Malcreated DAOs, for example with 100% quorum that make them unusable
Finishing links in proposals description/DAO description
We are using SphereX on-chain protection, so some suspicious transactions may get reverted. This is expected behavior
Any issue that was described in the previous security audit reports. Previous security audit reports can be found here https://github.com/dexe-network/DeXe-Protocol/tree/master/audits
Prohibited Activities:
Any testing on mainnet or public testnet deployed code; all testing should be done on local-forks of either public testnet or mainnet
Any testing with pricing oracles or third-party smart contracts
Attempting phishing or other social engineering attacks against our employees and/or customers
Any testing with third-party systems and applications (e.g. browser extensions) as well as websites (e.g. SSO providers, advertising networks)
Any denial of service attacks that are executed against project assets
Automated testing of services that generates significant amounts of traffic
Public disclosure of an unpatched vulnerability in an embargoed bounty
Program Rules
General Terms
Each bounty for a potentially malicious transaction that can be reverted through the SphereX security system, whether it is qualified as Critical, High or Medium, will be estimated among the ranges of one level lower. But if a transaction can overcome our protection, and cause critical vulnerability it is rewarded as Critical.
Medium bounties are paid in stable, while high and critical bounties are paid in $DEXE.
Critical severity issues are paid with a 6-month linear vesting
Note that for critical smart contract bugs, the reward amount is 10% of the funds directly affected up to a maximum of USD 500 000 in $DEXE with a 6-month linear vesting schedule.
Low severity issues are "Out of scope" and are not eligible for a bounty
Note
Make every effort not to damage or restrict the availability of products, services, or infrastructure
Avoid compromising any personal data, interruption, or degradation of any service
Don’t access or modify other user data, localize all tests to your accounts
Perform testing only within the scope
Don’t exploit any DoS/DDoS vulnerabilities, social engineering attacks, or spam
Don’t spam forms or account creation flows using automated scanners
In case you find chain vulnerabilities we’ll pay only for vulnerability with the highest severity.
Don’t break any law and stay in the defined scope
Any details of found vulnerabilities must not be communicated to anyone who is not a HackenProof Team or an authorized employee of this Company without appropriate permission
In case that your finding is valid you might be asked for extra KYC verification to proceed with payments
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
ONLY USE the EMAIL under which you registered your HackerProof account (in case of violation, no bounty can be awarded)
Provide detailed but to-the point reproduction steps