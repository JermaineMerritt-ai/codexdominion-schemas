// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title AuditConsentRing Smart Contract
 * @dev Implements on-chain audit logging and consent management
 * 
 * This smart contract provides immutable audit trails and consent tracking
 * for the Codex Dominion artifact syndication system on Ethereum-compatible
 * blockchains.
 * 
 * Core Features:
 * - Immutable action logging with event emission
 * - Access control and consent management
 * - Artifact revocation tracking
 * - GDPR/CCPA compliance metadata
 */

contract AuditConsentRing {
    
    // ============ Structs ============
    
    struct AuditEntry {
        address actor;
        string actionId;
        string actionType;
        string artifactId;
        uint256 timestamp;
        bytes32 contentHash;
    }
    
    struct ConsentRecord {
        address dataSubject;
        string purpose;
        bool granted;
        uint256 timestamp;
        uint256 expiresAt;
    }
    
    struct RevocationRecord {
        address revoker;
        string artifactId;
        string reason;
        uint256 timestamp;
        bool active;
    }
    
    // ============ State Variables ============
    
    address public owner;
    uint256 public totalActionsLogged;
    uint256 public totalConsents;
    uint256 public totalRevocations;
    
    // Mappings
    mapping(uint256 => AuditEntry) public auditTrail;
    mapping(address => uint256[]) public actorActions;
    mapping(string => uint256[]) public artifactActions;
    mapping(bytes32 => ConsentRecord) public consents;
    mapping(string => RevocationRecord) public revocations;
    mapping(address => mapping(string => bool)) public accessControl;
    
    // ============ Events ============
    
    event ActionLogged(
        address indexed actor,
        string actionId,
        string actionType,
        string artifactId,
        uint256 timestamp
    );
    
    event ConsentGranted(
        address indexed dataSubject,
        bytes32 indexed consentId,
        string purpose,
        uint256 expiresAt
    );
    
    event ConsentRevoked(
        address indexed dataSubject,
        bytes32 indexed consentId,
        uint256 timestamp
    );
    
    event AccessRevoked(
        address indexed revoker,
        string artifactId,
        string reason,
        uint256 timestamp
    );
    
    event AccessRestored(
        address indexed restorer,
        string artifactId,
        uint256 timestamp
    );
    
    // ============ Modifiers ============
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier validAddress(address _address) {
        require(_address != address(0), "Invalid address");
        _;
    }
    
    // ============ Constructor ============
    
    constructor() {
        owner = msg.sender;
        totalActionsLogged = 0;
        totalConsents = 0;
        totalRevocations = 0;
    }
    
    // ============ Audit Functions ============
    
    /**
     * @dev Log an action to the immutable audit trail
     * @param actionId Unique identifier for the action
     * @param actionType Type of action (create, access, modify, delete, etc.)
     * @param artifactId Identifier of the artifact involved
     * @param contentHash SHA256 hash of action content
     */
    function logAction(
        string memory actionId,
        string memory actionType,
        string memory artifactId,
        bytes32 contentHash
    ) public {
        uint256 entryIndex = totalActionsLogged;
        
        auditTrail[entryIndex] = AuditEntry({
            actor: msg.sender,
            actionId: actionId,
            actionType: actionType,
            artifactId: artifactId,
            timestamp: block.timestamp,
            contentHash: contentHash
        });
        
        // Index by actor
        actorActions[msg.sender].push(entryIndex);
        
        // Index by artifact
        if (bytes(artifactId).length > 0) {
            artifactActions[artifactId].push(entryIndex);
        }
        
        totalActionsLogged++;
        
        emit ActionLogged(
            msg.sender,
            actionId,
            actionType,
            artifactId,
            block.timestamp
        );
    }
    
    /**
     * @dev Get audit trail for a specific actor
     * @param actor Address of the actor
     * @return Array of entry indices
     */
    function getActorAuditTrail(address actor) 
        public 
        view 
        returns (uint256[] memory) 
    {
        return actorActions[actor];
    }
    
    /**
     * @dev Get audit trail for a specific artifact
     * @param artifactId Identifier of the artifact
     * @return Array of entry indices
     */
    function getArtifactAuditTrail(string memory artifactId) 
        public 
        view 
        returns (uint256[] memory) 
    {
        return artifactActions[artifactId];
    }
    
    /**
     * @dev Get specific audit entry
     * @param entryIndex Index of the audit entry
     * @return AuditEntry struct
     */
    function getAuditEntry(uint256 entryIndex) 
        public 
        view 
        returns (AuditEntry memory) 
    {
        require(entryIndex < totalActionsLogged, "Entry does not exist");
        return auditTrail[entryIndex];
    }
    
    // ============ Consent Functions ============
    
    /**
     * @dev Grant consent for data processing
     * @param purpose Purpose of data processing
     * @param durationDays Duration of consent in days
     * @return consentId Unique identifier for the consent
     */
    function grantConsent(
        string memory purpose,
        uint256 durationDays
    ) public returns (bytes32) {
        bytes32 consentId = keccak256(
            abi.encodePacked(msg.sender, purpose, block.timestamp)
        );
        
        uint256 expiresAt = block.timestamp + (durationDays * 1 days);
        
        consents[consentId] = ConsentRecord({
            dataSubject: msg.sender,
            purpose: purpose,
            granted: true,
            timestamp: block.timestamp,
            expiresAt: expiresAt
        });
        
        totalConsents++;
        
        emit ConsentGranted(msg.sender, consentId, purpose, expiresAt);
        
        return consentId;
    }
    
    /**
     * @dev Revoke previously granted consent
     * @param consentId Identifier of the consent to revoke
     */
    function revokeConsent(bytes32 consentId) public {
        ConsentRecord storage consent = consents[consentId];
        require(consent.dataSubject == msg.sender, "Not the consent owner");
        require(consent.granted, "Consent already revoked");
        
        consent.granted = false;
        
        emit ConsentRevoked(msg.sender, consentId, block.timestamp);
    }
    
    /**
     * @dev Check if consent is valid and active
     * @param consentId Identifier of the consent
     * @return bool indicating if consent is valid
     */
    function isConsentValid(bytes32 consentId) public view returns (bool) {
        ConsentRecord storage consent = consents[consentId];
        
        if (!consent.granted) {
            return false;
        }
        
        if (block.timestamp > consent.expiresAt) {
            return false;
        }
        
        return true;
    }
    
    // ============ Access Revocation Functions ============
    
    /**
     * @dev Revoke access to an artifact
     * @param artifactId Identifier of the artifact
     * @param reason Reason for revocation
     */
    function revokeAccess(
        string memory artifactId,
        string memory reason
    ) public {
        bytes32 revocationKey = keccak256(
            abi.encodePacked(artifactId, msg.sender)
        );
        
        revocations[artifactId] = RevocationRecord({
            revoker: msg.sender,
            artifactId: artifactId,
            reason: reason,
            timestamp: block.timestamp,
            active: true
        });
        
        accessControl[msg.sender][artifactId] = false;
        
        totalRevocations++;
        
        emit AccessRevoked(msg.sender, artifactId, reason, block.timestamp);
    }
    
    /**
     * @dev Restore previously revoked access
     * @param artifactId Identifier of the artifact
     */
    function restoreAccess(string memory artifactId) public {
        RevocationRecord storage revocation = revocations[artifactId];
        require(revocation.active, "No active revocation");
        require(
            revocation.revoker == msg.sender || msg.sender == owner,
            "Not authorized to restore"
        );
        
        revocation.active = false;
        accessControl[msg.sender][artifactId] = true;
        
        emit AccessRestored(msg.sender, artifactId, block.timestamp);
    }
    
    /**
     * @dev Check if access is revoked for an artifact
     * @param actor Address to check
     * @param artifactId Identifier of the artifact
     * @return bool indicating if access is revoked
     */
    function isAccessRevoked(address actor, string memory artifactId) 
        public 
        view 
        returns (bool) 
    {
        return !accessControl[actor][artifactId];
    }
    
    /**
     * @dev Get revocation record for an artifact
     * @param artifactId Identifier of the artifact
     * @return RevocationRecord struct
     */
    function getRevocationRecord(string memory artifactId) 
        public 
        view 
        returns (RevocationRecord memory) 
    {
        return revocations[artifactId];
    }
    
    // ============ Compliance Dashboard Functions ============
    
    /**
     * @dev Generate compliance statistics
     * @return Statistics about audit trail, consents, and revocations
     */
    function getComplianceStats() 
        public 
        view 
        returns (
            uint256 actionsLogged,
            uint256 consentsGranted,
            uint256 accessRevocations,
            uint256 blockNumber,
            uint256 timestamp
        ) 
    {
        return (
            totalActionsLogged,
            totalConsents,
            totalRevocations,
            block.number,
            block.timestamp
        );
    }
    
    /**
     * @dev Get actor statistics
     * @param actor Address of the actor
     * @return Number of actions by this actor
     */
    function getActorStats(address actor) 
        public 
        view 
        returns (uint256) 
    {
        return actorActions[actor].length;
    }
    
    /**
     * @dev Get artifact statistics
     * @param artifactId Identifier of the artifact
     * @return Number of actions for this artifact
     */
    function getArtifactStats(string memory artifactId) 
        public 
        view 
        returns (uint256) 
    {
        return artifactActions[artifactId].length;
    }
    
    // ============ Admin Functions ============
    
    /**
     * @dev Transfer ownership of the contract
     * @param newOwner Address of the new owner
     */
    function transferOwnership(address newOwner) 
        public 
        onlyOwner 
        validAddress(newOwner) 
    {
        owner = newOwner;
    }
    
    /**
     * @dev Emergency pause function (if needed for upgrades)
     * @notice This is a placeholder for future pause functionality
     */
    function pause() public onlyOwner {
        // Implement pause logic if needed
        // Consider using OpenZeppelin's Pausable contract
    }
    
    /**
     * @dev Get contract version
     * @return Version string
     */
    function version() public pure returns (string memory) {
        return "1.0.0";
    }
}
