#!/usr/bin/env python3
"""
Codex Memory
============

Advanced memory and knowledge management system for the Codex Dominion Suite.
Handles long-term storage, retrieval, and knowledge synthesis.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
from .settings import get_data_path, BRAND_FILE

class CodexMemory:
    """Intelligent memory system for knowledge retention and retrieval"""
    
    def __init__(self):
        self.memory_file = get_data_path("memory.json")
        self.ensure_memory_structure()
        
        self.memory_types = {
            "factual": "Concrete facts and data",
            "procedural": "Process and workflow knowledge", 
            "episodic": "Event-based memories",
            "semantic": "Conceptual understanding",
            "temporal": "Time-series data",
            "relational": "Connection and relationship data"
        }
    
    def ensure_memory_structure(self):
        """Initialize memory storage structure"""
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                "memories": {},
                "indices": {
                    "by_type": {},
                    "by_tag": {},
                    "by_date": {},
                    "by_importance": {}
                },
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0.0",
                    "total_memories": 0
                }
            }
            self._save_memory(data)
    
    def _load_memory(self) -> Dict:
        """Load memory data from storage"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"memories": {}, "indices": {}, "metadata": {}}
    
    def _save_memory(self, data: Dict):
        """Save memory data to storage"""
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        data["metadata"]["total_memories"] = len(data.get("memories", {}))
        
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def _generate_memory_id(self, content: str, memory_type: str) -> str:
        """Generate unique memory ID based on content hash"""
        content_hash = hashlib.md5(f"{content}{memory_type}".encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"MEM-{timestamp}-{content_hash}"
    
    def store_memory(self, 
                    content: str,
                    memory_type: str = "factual",
                    importance: int = 5,
                    tags: List[str] = None,
                    metadata: Dict = None) -> str:
        """Store new memory with contextual information"""
        
        data = self._load_memory()
        
        memory_id = self._generate_memory_id(content, memory_type)
        
        memory = {
            "id": memory_id,
            "content": content,
            "type": memory_type,
            "importance": max(1, min(10, importance)),  # Clamp between 1-10
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "access_count": 0,
            "metadata": metadata or {},
            "connections": []  # Links to related memories
        }
        
        data["memories"][memory_id] = memory
        
        # Update indices
        self._update_indices(data, memory)
        
        self._save_memory(data)
        return memory_id
    
    def _update_indices(self, data: Dict, memory: Dict):
        """Update search indices for efficient retrieval"""
        memory_id = memory["id"]
        
        # Type index
        memory_type = memory["type"]
        if memory_type not in data["indices"]["by_type"]:
            data["indices"]["by_type"][memory_type] = []
        data["indices"]["by_type"][memory_type].append(memory_id)
        
        # Tag index
        for tag in memory.get("tags", []):
            if tag not in data["indices"]["by_tag"]:
                data["indices"]["by_tag"][tag] = []
            data["indices"]["by_tag"][tag].append(memory_id)
        
        # Date index (by day)
        date_key = memory["created"][:10]  # YYYY-MM-DD
        if date_key not in data["indices"]["by_date"]:
            data["indices"]["by_date"][date_key] = []
        data["indices"]["by_date"][date_key].append(memory_id)
        
        # Importance index
        importance = str(memory["importance"])
        if importance not in data["indices"]["by_importance"]:
            data["indices"]["by_importance"][importance] = []
        data["indices"]["by_importance"][importance].append(memory_id)
    
    def retrieve_memory(self, memory_id: str) -> Optional[Dict]:
        """Retrieve specific memory and update access tracking"""
        data = self._load_memory()
        
        if memory_id in data["memories"]:
            memory = data["memories"][memory_id]
            memory["last_accessed"] = datetime.now().isoformat()
            memory["access_count"] = memory.get("access_count", 0) + 1
            
            data["memories"][memory_id] = memory
            self._save_memory(data)
            
            return memory
        
        return None
    
    def search_memories(self, 
                       query: str = None,
                       memory_type: str = None,
                       tags: List[str] = None,
                       importance_min: int = 1,
                       limit: int = 20) -> List[Dict]:
        """Search memories with multiple criteria"""
        
        data = self._load_memory()
        memories = list(data["memories"].values())
        
        # Filter by type
        if memory_type:
            memories = [m for m in memories if m.get("type") == memory_type]
        
        # Filter by tags
        if tags:
            memories = [m for m in memories 
                       if any(tag in m.get("tags", []) for tag in tags)]
        
        # Filter by importance
        memories = [m for m in memories 
                   if m.get("importance", 0) >= importance_min]
        
        # Text search in content
        if query:
            query_lower = query.lower()
            memories = [m for m in memories 
                       if query_lower in m.get("content", "").lower()]
        
        # Sort by importance and recency
        memories.sort(key=lambda x: (
            x.get("importance", 0),
            x.get("created", "")
        ), reverse=True)
        
        return memories[:limit]
    
    def create_connection(self, memory_id1: str, memory_id2: str, 
                         connection_type: str = "related") -> bool:
        """Create connection between memories"""
        data = self._load_memory()
        
        if memory_id1 in data["memories"] and memory_id2 in data["memories"]:
            # Add bidirectional connection
            connection = {
                "target": memory_id2,
                "type": connection_type,
                "created": datetime.now().isoformat()
            }
            
            data["memories"][memory_id1]["connections"].append(connection)
            
            reverse_connection = {
                "target": memory_id1,
                "type": connection_type,
                "created": datetime.now().isoformat()
            }
            
            data["memories"][memory_id2]["connections"].append(reverse_connection)
            
            self._save_memory(data)
            return True
        
        return False
    
    def get_related_memories(self, memory_id: str) -> List[Dict]:
        """Get memories connected to the specified memory"""
        memory = self.retrieve_memory(memory_id)
        if not memory:
            return []
        
        related_memories = []
        for connection in memory.get("connections", []):
            target_memory = self.retrieve_memory(connection["target"])
            if target_memory:
                target_memory["connection_type"] = connection["type"]
                related_memories.append(target_memory)
        
        return related_memories
    
    def consolidate_memories(self, days_old: int = 30) -> Dict[str, int]:
        """Consolidate old, low-importance memories"""
        data = self._load_memory()
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        consolidated = 0
        archived = 0
        
        for memory_id, memory in list(data["memories"].items()):
            created_date = datetime.fromisoformat(memory["created"])
            
            if (created_date < cutoff_date and 
                memory.get("importance", 0) < 3 and 
                memory.get("access_count", 0) < 2):
                
                # Archive low-importance, rarely accessed memories
                memory["archived"] = True
                memory["archived_date"] = datetime.now().isoformat()
                archived += 1
            
            elif (created_date < cutoff_date and 
                  memory.get("access_count", 0) > 10):
                
                # Consolidate frequently accessed memories
                memory["consolidated"] = True
                memory["importance"] = min(10, memory.get("importance", 5) + 1)
                consolidated += 1
        
        self._save_memory(data)
        
        return {
            "consolidated": consolidated,
            "archived": archived,
            "total_processed": len(data["memories"])
        }
    
    def get_memory_analytics(self) -> Dict[str, Any]:
        """Generate comprehensive memory analytics"""
        data = self._load_memory()
        memories = data["memories"]
        
        analytics = {
            "total_memories": len(memories),
            "types_distribution": {},
            "importance_distribution": {},
            "access_patterns": {},
            "recent_activity": [],
            "top_tags": {},
            "connection_network": {"nodes": 0, "edges": 0}
        }
        
        # Analyze distribution
        for memory in memories.values():
            # Type distribution
            mem_type = memory.get("type", "unknown")
            analytics["types_distribution"][mem_type] = \
                analytics["types_distribution"].get(mem_type, 0) + 1
            
            # Importance distribution
            importance = str(memory.get("importance", 0))
            analytics["importance_distribution"][importance] = \
                analytics["importance_distribution"].get(importance, 0) + 1
            
            # Tag frequency
            for tag in memory.get("tags", []):
                analytics["top_tags"][tag] = analytics["top_tags"].get(tag, 0) + 1
            
            # Connection count
            analytics["connection_network"]["edges"] += len(memory.get("connections", []))
        
        analytics["connection_network"]["nodes"] = len(memories)
        
        # Recent activity (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        for memory in memories.values():
            created_date = datetime.fromisoformat(memory["created"])
            if created_date > recent_cutoff:
                analytics["recent_activity"].append({
                    "id": memory["id"],
                    "type": memory["type"],
                    "importance": memory["importance"],
                    "created": memory["created"]
                })
        
        return analytics

# Global memory instance
codex_memory = CodexMemory()

def brand_voice():
    try:
        with open(BRAND_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Codex voice: sovereign, clear, luminous, human, invitational."

if __name__ == "__main__":
    print("🧠 Codex Memory initialized")
    
    # Test memory storage
    memory_id = codex_memory.store_memory(
        "Codex Suite successfully initialized with modular architecture",
        "factual",
        importance=8,
        tags=["initialization", "architecture", "success"]
    )
    print(f"Stored memory: {memory_id}")
    
    # Test retrieval
    retrieved = codex_memory.retrieve_memory(memory_id)
    if retrieved:
        print(f"Retrieved: {retrieved['content']}")