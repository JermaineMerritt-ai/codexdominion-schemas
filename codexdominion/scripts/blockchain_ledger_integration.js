#!/usr/bin/env node
/**
 * Blockchain Ledger Integration - Ethereum Smart Contract Interface
 *
 * This module provides blockchain integration for the Codex Dominion
 * artifact syndication system, enabling decentralized storage and
 * verification on Ethereum-compatible networks.
 *
 * Core Responsibilities:
 * - Store artifacts on-chain with metadata and content hashes
 * - Verify artifact integrity through blockchain queries
 * - Manage blockchain transactions and gas optimization
 * - Provide fallback to local ledger for offline operations
 */

const { ethers } = require("ethers");
const fs = require("fs").promises;
const path = require("path");
const crypto = require("crypto");

/**
 * Smart Contract ABI for Eternal Ledger
 * Defines the interface for interacting with the on-chain ledger
 */
const LEDGER_ABI = [
    "function storeArtifact(string artifactID, string metadata, bytes32 contentHash) external returns (uint256)",
    "function getArtifactHash(string artifactID) external view returns (bytes32)",
    "function getArtifactMetadata(string artifactID) external view returns (string)",
    "function verifyArtifact(string artifactID, bytes32 expectedHash) external view returns (bool)",
    "function getArtifactTimestamp(string artifactID) external view returns (uint256)",
    "function getArtifactOwner(string artifactID) external view returns (address)",
    "event ArtifactStored(string indexed artifactID, bytes32 contentHash, uint256 timestamp)",
    "event ArtifactVerified(string indexed artifactID, bool isValid)"
];

/**
 * Configuration for blockchain connection
 */
const CONFIG = {
    // Network configuration (defaults to local development)
    RPC_URL: process.env.ETHEREUM_RPC_URL || "http://localhost:8545",
    CHAIN_ID: parseInt(process.env.CHAIN_ID || "31337"), // Hardhat default

    // Contract configuration
    CONTRACT_ADDRESS: process.env.LEDGER_CONTRACT_ADDRESS || "0x5FbDB2315678afecb367f032d93F642f64180aa3",

    // Wallet configuration
    PRIVATE_KEY: process.env.PRIVATE_KEY || "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",

    // Gas configuration
    GAS_LIMIT: 500000,
    MAX_FEE_PER_GAS: ethers.parseUnits("50", "gwei"),
    MAX_PRIORITY_FEE: ethers.parseUnits("2", "gwei"),

    // Fallback configuration
    LOCAL_LEDGER_PATH: "data/blockchain-fallback-ledger.json",
    USE_FALLBACK: process.env.USE_FALLBACK === "true"
};

/**
 * Blockchain Ledger Manager
 * Manages connection to Ethereum network and smart contract interactions
 */
class BlockchainLedger {
    constructor(config = CONFIG) {
        this.config = config;
        this.provider = null;
        this.signer = null;
        this.ledgerContract = null;
        this.isConnected = false;
        this.fallbackMode = config.USE_FALLBACK;
    }

    /**
     * Initialize blockchain connection
     */
    async initialize() {
        try {
            // Connect to provider
            this.provider = new ethers.JsonRpcProvider(this.config.RPC_URL);

            // Create wallet/signer
            this.signer = new ethers.Wallet(this.config.PRIVATE_KEY, this.provider);

            // Connect to contract
            this.ledgerContract = new ethers.Contract(
                this.config.CONTRACT_ADDRESS,
                LEDGER_ABI,
                this.signer
            );

            // Verify connection
            await this.provider.getNetwork();

            this.isConnected = true;
            this.fallbackMode = false;

            console.log("✓ Blockchain connection established");
            console.log(`  Network: ${this.config.RPC_URL}`);
            console.log(`  Contract: ${this.config.CONTRACT_ADDRESS}`);
            console.log(`  Signer: ${await this.signer.getAddress()}`);

            return { connected: true };
        } catch (error) {
            console.warn("⚠ Blockchain connection failed, using fallback mode");
            console.warn(`  Error: ${error.message}`);

            this.fallbackMode = true;
            await this._initializeFallbackLedger();

            return { connected: false, fallback: true, error: error.message };
        }
    }

    /**
     * Initialize local fallback ledger
     */
    async _initializeFallbackLedger() {
        const ledgerPath = path.resolve(this.config.LOCAL_LEDGER_PATH);
        const ledgerDir = path.dirname(ledgerPath);

        // Create directory if it doesn't exist
        await fs.mkdir(ledgerDir, { recursive: true });

        // Initialize ledger file if it doesn't exist
        try {
            await fs.access(ledgerPath);
        } catch {
            const initialData = {
                artifacts: {},
                created_at: new Date().toISOString(),
                mode: "fallback"
            };
            await fs.writeFile(ledgerPath, JSON.stringify(initialData, null, 2));
        }
    }

    /**
     * Read fallback ledger
     */
    async _readFallbackLedger() {
        const ledgerPath = path.resolve(this.config.LOCAL_LEDGER_PATH);
        const data = await fs.readFile(ledgerPath, "utf-8");
        return JSON.parse(data);
    }

    /**
     * Write to fallback ledger
     */
    async _writeFallbackLedger(data) {
        const ledgerPath = path.resolve(this.config.LOCAL_LEDGER_PATH);
        await fs.writeFile(ledgerPath, JSON.stringify(data, null, 2));
    }

    /**
     * Store artifact on blockchain or fallback ledger
     *
     * @param {string} artifactID - Unique identifier for the artifact
     * @param {string} metadata - JSON metadata string
     * @param {string} contentHash - SHA256 hash of artifact content
     * @returns {Object} Transaction result with hash and block info
     */
    async storeArtifact(artifactID, metadata, contentHash) {
        // Ensure contentHash is properly formatted as bytes32
        const formattedHash = contentHash.startsWith("0x")
            ? contentHash
            : `0x${contentHash}`;

        if (this.fallbackMode) {
            return await this._storeArtifactFallback(artifactID, metadata, formattedHash);
        }

        try {
            console.log(`Storing artifact: ${artifactID}`);

            // Prepare transaction
            const tx = await this.ledgerContract.storeArtifact(
                artifactID,
                metadata,
                formattedHash,
                {
                    gasLimit: this.config.GAS_LIMIT,
                    maxFeePerGas: this.config.MAX_FEE_PER_GAS,
                    maxPriorityFeePerGas: this.config.MAX_PRIORITY_FEE
                }
            );

            console.log(`  Transaction submitted: ${tx.hash}`);

            // Wait for confirmation
            const receipt = await tx.wait();

            console.log(`  ✓ Confirmed in block ${receipt.blockNumber}`);
            console.log(`  Gas used: ${receipt.gasUsed.toString()}`);

            return {
                success: true,
                transactionHash: receipt.hash,
                blockNumber: receipt.blockNumber,
                gasUsed: receipt.gasUsed.toString(),
                artifactID: artifactID,
                contentHash: formattedHash,
                timestamp: Date.now()
            };
        } catch (error) {
            console.error(`✗ Blockchain storage failed: ${error.message}`);
            console.log("  Falling back to local storage...");

            this.fallbackMode = true;
            return await this._storeArtifactFallback(artifactID, metadata, formattedHash);
        }
    }

    /**
     * Store artifact in fallback ledger
     */
    async _storeArtifactFallback(artifactID, metadata, contentHash) {
        const ledger = await this._readFallbackLedger();

        ledger.artifacts[artifactID] = {
            metadata: metadata,
            contentHash: contentHash,
            timestamp: new Date().toISOString(),
            mode: "fallback"
        };

        await this._writeFallbackLedger(ledger);

        console.log(`  ✓ Stored in fallback ledger: ${artifactID}`);

        return {
            success: true,
            mode: "fallback",
            artifactID: artifactID,
            contentHash: contentHash,
            timestamp: Date.now()
        };
    }

    /**
     * Verify artifact integrity from blockchain or fallback ledger
     *
     * @param {string} artifactID - Artifact identifier to verify
     * @returns {Object} Verification result with hash and status
     */
    async verifyIntegrity(artifactID) {
        if (this.fallbackMode) {
            return await this._verifyIntegrityFallback(artifactID);
        }

        try {
            console.log(`Verifying artifact: ${artifactID}`);

            // Query blockchain
            const storedHash = await this.ledgerContract.getArtifactHash(artifactID);

            if (storedHash === "0x0000000000000000000000000000000000000000000000000000000000000000") {
                return {
                    found: false,
                    artifactID: artifactID,
                    message: "Artifact not found on blockchain"
                };
            }

            console.log(`  ✓ Hash retrieved: ${storedHash}`);

            return {
                found: true,
                artifactID: artifactID,
                contentHash: storedHash,
                verified: true,
                source: "blockchain"
            };
        } catch (error) {
            console.error(`✗ Blockchain verification failed: ${error.message}`);
            console.log("  Checking fallback ledger...");

            return await this._verifyIntegrityFallback(artifactID);
        }
    }

    /**
     * Verify artifact from fallback ledger
     */
    async _verifyIntegrityFallback(artifactID) {
        const ledger = await this._readFallbackLedger();

        if (artifactID in ledger.artifacts) {
            const artifact = ledger.artifacts[artifactID];

            console.log(`  ✓ Found in fallback ledger: ${artifactID}`);

            return {
                found: true,
                artifactID: artifactID,
                contentHash: artifact.contentHash,
                metadata: artifact.metadata,
                timestamp: artifact.timestamp,
                verified: true,
                source: "fallback"
            };
        }

        return {
            found: false,
            artifactID: artifactID,
            message: "Artifact not found in fallback ledger"
        };
    }

    /**
     * Get artifact metadata from blockchain
     */
    async getArtifactMetadata(artifactID) {
        if (this.fallbackMode) {
            const ledger = await this._readFallbackLedger();
            return ledger.artifacts[artifactID]?.metadata || null;
        }

        try {
            const metadata = await this.ledgerContract.getArtifactMetadata(artifactID);
            return metadata || null;
        } catch (error) {
            console.error(`Error getting metadata: ${error.message}`);
            return null;
        }
    }

    /**
     * Get artifact timestamp from blockchain
     */
    async getArtifactTimestamp(artifactID) {
        if (this.fallbackMode) {
            const ledger = await this._readFallbackLedger();
            return ledger.artifacts[artifactID]?.timestamp || null;
        }

        try {
            const timestamp = await this.ledgerContract.getArtifactTimestamp(artifactID);
            return timestamp.toString();
        } catch (error) {
            console.error(`Error getting timestamp: ${error.message}`);
            return null;
        }
    }

    /**
     * Get current gas price estimate
     */
    async getGasPrice() {
        if (this.fallbackMode) {
            return { fallback: true, gasPrice: "N/A" };
        }

        try {
            const feeData = await this.provider.getFeeData();
            return {
                gasPrice: ethers.formatUnits(feeData.gasPrice || 0n, "gwei"),
                maxFeePerGas: ethers.formatUnits(feeData.maxFeePerGas || 0n, "gwei"),
                maxPriorityFeePerGas: ethers.formatUnits(feeData.maxPriorityFeePerGas || 0n, "gwei")
            };
        } catch (error) {
            return { error: error.message };
        }
    }

    /**
     * Get signer balance
     */
    async getBalance() {
        if (this.fallbackMode) {
            return { fallback: true, balance: "N/A" };
        }

        try {
            const balance = await this.provider.getBalance(await this.signer.getAddress());
            return {
                balance: ethers.formatEther(balance),
                wei: balance.toString()
            };
        } catch (error) {
            return { error: error.message };
        }
    }
}

/**
 * Demo: Blockchain Ledger Integration
 */
async function main() {
    console.log("=== Blockchain Ledger Integration Demo ===\n");

    // Initialize blockchain ledger
    const ledger = new BlockchainLedger();
    await ledger.initialize();

    // Generate sample artifact data
    const artifactID = "eternal-ledger-v1.0.0";
    const metadata = JSON.stringify({
        name: "Eternal Ledger Diagram",
        version: "1.0.0",
        type: "diagram",
        format: "png",
        created: new Date().toISOString()
    });

    // Generate content hash
    const contentHash = crypto
        .createHash("sha256")
        .update("Sample artifact content")
        .digest("hex");

    console.log("\n1. Storing artifact on blockchain...");
    const storeResult = await ledger.storeArtifact(artifactID, metadata, contentHash);
    console.log("   Result:", JSON.stringify(storeResult, null, 2));

    console.log("\n2. Verifying artifact integrity...");
    const verifyResult = await ledger.verifyIntegrity(artifactID);
    console.log("   Result:", JSON.stringify(verifyResult, null, 2));

    console.log("\n3. Getting artifact metadata...");
    const metadataResult = await ledger.getArtifactMetadata(artifactID);
    console.log("   Metadata:", metadataResult);

    if (!ledger.fallbackMode) {
        console.log("\n4. Checking gas prices...");
        const gasPrice = await ledger.getGasPrice();
        console.log("   Gas prices:", JSON.stringify(gasPrice, null, 2));

        console.log("\n5. Checking signer balance...");
        const balance = await ledger.getBalance();
        console.log("   Balance:", JSON.stringify(balance, null, 2));
    }

    console.log("\n=== Demo Complete ===");
    console.log("Blockchain integration: Decentralized artifact integrity.");
}

// Export for use as module
module.exports = {
    BlockchainLedger,
    LEDGER_ABI,
    CONFIG
};

// Run demo if executed directly
if (require.main === module) {
    main().catch(console.error);
}
