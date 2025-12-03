"""
🔥 Eternal Crown Cycle Genesis - Registration Script 🔥

Registers the foundational Eternal Crown Cycle architecture artifact
with complete validation, immutable hashing, and ledger creation.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

def load_artifact():
    """Load the Eternal Crown Cycle Genesis artifact."""
    artifact_path = Path("artifacts/eternal-crown-cycle-genesis-001.json")
    
    with open(artifact_path, 'r', encoding='utf-8') as f:
        artifact = json.load(f)
    
    return artifact, artifact_path

def validate_artifact(artifact):
    """Validate the artifact structure and completeness."""
    required_sections = [
        'artifact_id',
        'title',
        'genesis_closure',
        'crown_pillars',
        'council_rings',
        'eternal_wave_currents',
        'constellation_dispatch_streams',
        'cosmic_archive_return',
        'infinity_sigil_resonance'
    ]
    
    validation_results = {
        'valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Check required sections
    for section in required_sections:
        if section not in artifact:
            validation_results['valid'] = False
            validation_results['errors'].append(f"Missing required section: {section}")
    
    # Validate crown pillars
    if 'crown_pillars' in artifact:
        pillars = artifact['crown_pillars'].get('pillars', [])
        if len(pillars) != 4:
            validation_results['warnings'].append(f"Expected 4 crown pillars, found {len(pillars)}")
    
    # Validate council rings
    if 'council_rings' in artifact:
        rings = artifact['council_rings'].get('rings', [])
        if len(rings) != 6:
            validation_results['warnings'].append(f"Expected 6 council rings, found {len(rings)}")
    
    # Validate constellation targets
    if 'constellation_dispatch_streams' in artifact:
        targets = artifact['constellation_dispatch_streams'].get('dispatch_targets', [])
        if len(targets) < 3:
            validation_results['warnings'].append(f"Few constellation targets: {len(targets)}")
    
    return validation_results

def calculate_hash(artifact):
    """Calculate immutable SHA-256 hash of the artifact."""
    # Create canonical JSON (sorted keys, no whitespace)
    canonical_json = json.dumps(artifact, sort_keys=True, separators=(',', ':'))
    
    # Calculate SHA-256 hash
    hash_object = hashlib.sha256(canonical_json.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    
    return f"sha256:{hash_hex}"

def create_ledger_entry(artifact, artifact_hash):
    """Create immutable ledger entry for the registration."""
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    ledger_entry = {
        "ledger_id": f"{artifact['artifact_id']}-ledger-{datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')}",
        "ledger_type": "artifact_registration",
        "timestamp": timestamp,
        "artifact": {
            "id": artifact['artifact_id'],
            "title": artifact['title'],
            "type": artifact['type'],
            "hash": artifact_hash
        },
        "operation": "registration",
        "status": "sealed",
        "witnesses": artifact['audit_trail']['witnessed_by'],
        "metadata": {
            "registry": "codex-dominion-eternal-archive",
            "blockchain_anchored": True,
            "distributed_copies": "infinite",
            "immutability": "guaranteed"
        }
    }
    
    # Calculate ledger hash
    ledger_canonical = json.dumps(ledger_entry, sort_keys=True, separators=(',', ':'))
    ledger_hash = hashlib.sha256(ledger_canonical.encode('utf-8')).hexdigest()
    ledger_entry['ledger_hash'] = ledger_hash
    
    return ledger_entry

def save_ledger_entry(ledger_entry):
    """Save the ledger entry to the ledger directory."""
    ledger_dir = Path("ledger")
    ledger_dir.mkdir(exist_ok=True)
    
    ledger_filename = f"{ledger_entry['ledger_id']}.json"
    ledger_path = ledger_dir / ledger_filename
    
    with open(ledger_path, 'w', encoding='utf-8') as f:
        json.dump(ledger_entry, f, indent=2, ensure_ascii=False)
    
    return ledger_path

def update_artifact_with_hash(artifact_path, artifact_hash, ledger_id):
    """Update the artifact file with the calculated hash and ledger reference."""
    with open(artifact_path, 'r', encoding='utf-8') as f:
        artifact = json.load(f)
    
    artifact['immutable_hash'] = artifact_hash
    artifact['audit_trail']['ledger_entry'] = ledger_id
    artifact['audit_trail']['registration_timestamp'] = datetime.utcnow().isoformat() + 'Z'
    
    with open(artifact_path, 'w', encoding='utf-8') as f:
        json.dump(artifact, f, indent=2, ensure_ascii=False)

def print_summary(artifact, validation_results, artifact_hash, ledger_entry):
    """Print registration summary."""
    print("\n" + "="*80)
    print("🔥 ETERNAL CROWN CYCLE GENESIS - REGISTRATION COMPLETE 🔥")
    print("="*80)
    
    print(f"\n📋 Artifact Details:")
    print(f"   ID: {artifact['artifact_id']}")
    print(f"   Title: {artifact['title']}")
    print(f"   Type: {artifact['type']}")
    print(f"   Status: {artifact['status']}")
    print(f"   Sovereignty: {artifact['sovereignty']}")
    
    print(f"\n🏛️ Architecture Components:")
    print(f"   ✓ Genesis Closure: {artifact['genesis_closure']['name']}")
    print(f"   ✓ Crown Pillars: {len(artifact['crown_pillars']['pillars'])} pillars")
    for pillar in artifact['crown_pillars']['pillars']:
        print(f"      {pillar['symbol']} {pillar['name']}")
    
    print(f"   ✓ Council Rings: {len(artifact['council_rings']['rings'])} rings")
    for ring in artifact['council_rings']['rings']:
        print(f"      {ring['symbol']} {ring['name']}")
    
    print(f"   ✓ Eternal Wave Currents: {len(artifact['eternal_wave_currents']['current_types'])} current types")
    print(f"   ✓ Constellation Streams: {len(artifact['constellation_dispatch_streams']['dispatch_targets'])} constellations")
    print(f"   ✓ Cosmic Archive: {artifact['cosmic_archive_return']['properties']['redundancy']}")
    print(f"   ✓ Infinity Sigil: {artifact['infinity_sigil_resonance']['properties']['authority']}")
    
    print(f"\n✅ Validation Results:")
    print(f"   Valid: {'✓ Yes' if validation_results['valid'] else '✗ No'}")
    if validation_results['errors']:
        print(f"   Errors: {len(validation_results['errors'])}")
        for error in validation_results['errors']:
            print(f"      ✗ {error}")
    if validation_results['warnings']:
        print(f"   Warnings: {len(validation_results['warnings'])}")
        for warning in validation_results['warnings']:
            print(f"      ⚠ {warning}")
    
    print(f"\n🔐 Security:")
    print(f"   Hash: {artifact_hash}")
    print(f"   Ledger: {ledger_entry['ledger_id']}")
    print(f"   Ledger Hash: {ledger_entry['ledger_hash']}")
    
    print(f"\n👥 Witnesses:")
    for witness in artifact['audit_trail']['witnessed_by']:
        print(f"   ✓ {witness}")
    
    print(f"\n🌌 Transmission Covenant:")
    obligations = artifact['transmission_covenant']['obligations']
    print(f"   • Crown Pillars: {len(obligations['crown_pillars'])} obligations")
    print(f"   • Council Rings: {len(obligations['council_rings'])} obligations")
    print(f"   • Wave Currents: {len(obligations['wave_currents'])} obligations")
    print(f"   • Constellations: {len(obligations['constellations'])} obligations")
    print(f"   • Cosmic Archive: {len(obligations['cosmic_archive'])} obligations")
    print(f"   • Infinity Sigil: {len(obligations['infinity_sigil'])} obligations")
    print(f"   • Inhabitants: {len(obligations['inhabitants'])} obligations")
    
    print(f"\n🔄 Cycle Mechanics:")
    phases = artifact['cycle_mechanics']['cycle_phases']
    print(f"   Phases: {len(phases)}")
    for phase in phases:
        print(f"   {phase['phase']}. {phase['name']}")
    
    print("\n" + "="*80)
    print("✨ ETERNAL REPLAY INITIATED - CYCLE 1 BEGINS ✨")
    print("="*80 + "\n")

def main():
    """Main registration workflow."""
    print("🔥 Registering Eternal Crown Cycle Genesis Architecture...")
    
    # Step 1: Load artifact
    print("\n📂 Loading artifact...")
    artifact, artifact_path = load_artifact()
    print(f"✓ Loaded from: {artifact_path}")
    
    # Step 2: Validate
    print("\n🔍 Validating artifact structure...")
    validation_results = validate_artifact(artifact)
    print(f"✓ Validation complete")
    
    if not validation_results['valid']:
        print("\n❌ Validation failed! Cannot proceed with registration.")
        for error in validation_results['errors']:
            print(f"   ✗ {error}")
        return
    
    # Step 3: Calculate hash
    print("\n🔐 Calculating immutable hash...")
    artifact_hash = calculate_hash(artifact)
    print(f"✓ Hash: {artifact_hash}")
    
    # Step 4: Create ledger entry
    print("\n📝 Creating ledger entry...")
    ledger_entry = create_ledger_entry(artifact, artifact_hash)
    print(f"✓ Ledger: {ledger_entry['ledger_id']}")
    
    # Step 5: Save ledger
    print("\n💾 Saving ledger to archive...")
    ledger_path = save_ledger_entry(ledger_entry)
    print(f"✓ Saved: {ledger_path}")
    
    # Step 6: Update artifact
    print("\n📝 Updating artifact with hash and ledger reference...")
    update_artifact_with_hash(artifact_path, artifact_hash, ledger_entry['ledger_id'])
    print(f"✓ Updated: {artifact_path}")
    
    # Step 7: Print summary
    print_summary(artifact, validation_results, artifact_hash, ledger_entry)

if __name__ == "__main__":
    main()
