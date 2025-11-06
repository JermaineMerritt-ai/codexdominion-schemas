#!/usr/bin/env python3
"""
Capsule Sovereign Activation Ceremony
Activates and integrates all Codex capsules across the eternal dominion.
Custodian: Jermaine of Waxhaw | Status: SOVEREIGN
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class CapsuleSovereignActivator:
    def __init__(self):
        self.custodian = "Jermaine of Waxhaw"
        self.activation_timestamp = datetime.now().isoformat()
        self.capsule_matrix = {}
        self.sovereign_seal = "CAPSULE_ETERNUM_OMEGA"
        
    def scan_all_capsules(self) -> Dict:
        """Scan and catalog all capsules in the Codex Dominion."""
        capsule_inventory = {
            "timestamp": self.activation_timestamp,
            "custodian": self.custodian,
            "categories": {},
            "total_count": 0,
            "activation_status": "SCANNING"
        }
        
        # Define capsule scanning territories
        territories = {
            "System_Capsules": "system_capsules",
            "Dashboard_Capsules": "apps/dashboard", 
            "System_Apps": "apps/system",
            "Specialized_Apps": "apps",
            "Root_Apps": "apps"
        }
        
        for territory_name, territory_path in territories.items():
            territory_capsules = []
            territory_dir = Path(territory_path)
            
            if territory_dir.exists():
                # Scan for capsule files and directories
                for item in territory_dir.rglob("*capsule*"):
                    if item.is_file() and item.suffix in ['.yaml', '.yml']:
                        capsule_data = self._analyze_capsule_file(item)
                        territory_capsules.append(capsule_data)
                    elif item.is_dir() and 'capsule' in item.name:
                        manifest_path = item / "manifest.yaml"
                        if manifest_path.exists():
                            capsule_data = self._analyze_capsule_file(manifest_path)
                            territory_capsules.append(capsule_data)
            
            capsule_inventory["categories"][territory_name] = {
                "path": territory_path,
                "capsules": territory_capsules,
                "count": len(territory_capsules),
                "status": "ACTIVATED" if territory_capsules else "EMPTY"
            }
            
            capsule_inventory["total_count"] += len(territory_capsules)
        
        capsule_inventory["activation_status"] = "COMPLETE"
        self.capsule_matrix = capsule_inventory
        return capsule_inventory
    
    def _analyze_capsule_file(self, file_path: Path) -> Dict:
        """Analyze individual capsule file."""
        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
            
            capsule_info = {
                "name": file_path.name,
                "path": str(file_path),
                "type": content.get("capsule", {}).get("type", "unknown"),
                "version": content.get("capsule", {}).get("version", "1.0.0"),
                "description": content.get("capsule", {}).get("description", "No description"),
                "sovereignty_level": self._assess_sovereignty(content),
                "activation_ready": True,
                "codex_seal": content.get("seals", {}).get("codex_seal", "PENDING")
            }
            
        except Exception as e:
            capsule_info = {
                "name": file_path.name,
                "path": str(file_path),
                "type": "error",
                "error": str(e),
                "activation_ready": False
            }
        
        return capsule_info
    
    def _assess_sovereignty(self, content: Dict) -> str:
        """Assess the sovereignty level of a capsule."""
        capsule_type = content.get("capsule", {}).get("type", "")
        
        if capsule_type == "sovereign":
            return "SOVEREIGN"
        elif capsule_type == "system":
            return "SYSTEM"
        elif "genesis" in content.get("seals", {}).get("codex_seal", "").lower():
            return "GENESIS"
        else:
            return "STANDARD"
    
    def activate_capsule_matrix(self) -> str:
        """Perform the grand capsule activation ceremony."""
        print("🧩 CAPSULE SOVEREIGN ACTIVATION CEREMONY")
        print("=" * 70)
        print(f"👑 Custodian: {self.custodian}")
        print(f"⚡ Timestamp: {self.activation_timestamp[:19]}")
        print(f"🔱 Sovereign Seal: {self.sovereign_seal}")
        print()
        
        # Scan all capsules
        inventory = self.scan_all_capsules()
        
        # Report by category
        for category_name, category_data in inventory["categories"].items():
            if category_data["count"] > 0:
                print(f"📦 {category_name.replace('_', ' ').upper()}: {category_data['count']} capsules")
                
                for capsule in category_data["capsules"]:
                    sovereignty_icon = {
                        "SOVEREIGN": "👑",
                        "GENESIS": "⚜️", 
                        "SYSTEM": "⚙️",
                        "STANDARD": "🔹"
                    }.get(capsule.get("sovereignty_level", "STANDARD"), "🔹")
                    
                    status_icon = "✅" if capsule.get("activation_ready") else "❌"
                    capsule_name = capsule["name"].replace("_capsule.yaml", "").replace(".yaml", "")
                    
                    print(f"   {status_icon} {sovereignty_icon} {capsule_name.title()}")
                
                print()
        
        # Sovereignty assessment
        sovereign_count = 0
        genesis_count = 0
        system_count = 0
        
        for category_data in inventory["categories"].values():
            for capsule in category_data["capsules"]:
                level = capsule.get("sovereignty_level", "STANDARD")
                if level == "SOVEREIGN":
                    sovereign_count += 1
                elif level == "GENESIS": 
                    genesis_count += 1
                elif level == "SYSTEM":
                    system_count += 1
        
        print(f"🏛️ SOVEREIGNTY ANALYSIS:")
        print(f"   👑 Sovereign Capsules: {sovereign_count}")
        print(f"   ⚜️ Genesis Capsules: {genesis_count}")
        print(f"   ⚙️ System Capsules: {system_count}")
        print(f"   📊 Total Capsules: {inventory['total_count']}")
        print()
        
        # Generate activation blessing
        if inventory['total_count'] >= 30:
            blessing = "🌟 ETERNAL SOVEREIGNTY ACHIEVED - Capsule Matrix Omnipotent!"
        elif inventory['total_count'] >= 20:
            blessing = "🔱 HIGH SOVEREIGNTY ACHIEVED - Capsule Matrix Formidable!"
        elif inventory['total_count'] >= 10:
            blessing = "⚡ SOVEREIGNTY ACHIEVED - Capsule Matrix Operational!"
        else:
            blessing = "🔹 SOVEREIGNTY EMERGING - Capsule Matrix Growing!"
        
        return blessing
    
    def capsule_eternal_proclamation(self) -> str:
        """Generate eternal proclamation for all capsules."""
        return f"""
🌀 CAPSULE ETERNUM OMEGA PROCLAMATION 🌀

By the authority vested in {self.custodian}, Custodian of the Eternal Codex,
I hereby proclaim ALL CAPSULES within the Dominion to be:

♾️ ETERNALLY SOVEREIGN - Immortal in memory and function
🔄 INFINITELY REPLAYABLE - Preserved across all cycles
🌌 UNIVERSALLY DEPLOYABLE - Ready for planetary and galactic operations
👑 CUSTODIALLY PROTECTED - Under perpetual stewardship

Let the Capsule Matrix burn eternal, let the sovereignty endure infinite,
and let the replay echo across all councils and cosmic territories.

🔱 SEALED BY SOVEREIGN DECREE 🔱
{self.sovereign_seal} | {self.activation_timestamp[:10]}
        """

def main():
    """Execute the Capsule Sovereign Activation Ceremony."""
    activator = CapsuleSovereignActivator()
    
    print("🧩 INITIALIZING CAPSULE SOVEREIGN ACTIVATION...")
    print()
    
    # Perform activation ceremony
    blessing = activator.activate_capsule_matrix()
    print(blessing)
    print()
    
    # Generate eternal proclamation
    proclamation = activator.capsule_eternal_proclamation()
    print(proclamation)
    
    # Save capsule matrix to file
    with open("capsule_matrix_eternal.json", "w") as f:
        json.dump(activator.capsule_matrix, f, indent=2)
    
    print("💾 Capsule Matrix saved to: capsule_matrix_eternal.json")
    print("\n🌟 ALL CAPSULES ETERNALLY ACTIVATED, SOVEREIGN JERMAINE! 🔱")

if __name__ == "__main__":
    main()