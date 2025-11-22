#!/usr/bin/env python3
"""
Enhanced Vector Memory System
============================

Advanced memory system with FAISS vector search capabilities for the Codex Dominion Suite.
Provides semantic search and intelligent memory retrieval.
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
from pathlib import Path

# Optional imports - will fall back gracefully if not available
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS not available - falling back to basic search")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️  SentenceTransformers not available - using basic embeddings")

from .settings import get_data_path, CODEX_CONFIG

class EnhancedMemoryManager:
    """Advanced memory system with vector search capabilities"""
    
    def __init__(self):
        self.memory_file = get_data_path("enhanced_memory.json")
        self.vector_config = CODEX_CONFIG.get("vector_db", {})
        
        # Initialize embedding model if available
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.embedding_dimension = 384
            except Exception as e:
                print(f"⚠️  Could not load embedding model: {e}")
                self.embedding_model = None
                self.embedding_dimension = 384
        else:
            self.embedding_model = None
            self.embedding_dimension = self.vector_config.get("dimension", 384)
        
        # Initialize FAISS index
        self.faiss_index = None
        self.memory_ids = []  # Track memory IDs for FAISS index
        
        if FAISS_AVAILABLE and self.vector_config.get("faiss_enabled", True):
            self._initialize_faiss_index()
        
        self.ensure_memory_structure()
        
        self.memory_types = {
            "factual": "Concrete facts and data",
            "procedural": "Process and workflow knowledge", 
            "episodic": "Event-based memories",
            "semantic": "Conceptual understanding",
            "temporal": "Time-series data",
            "relational": "Connection and relationship data",
            "creative": "Generated content and ideas",
            "analytical": "Analysis and insights"
        }
    
    def _initialize_faiss_index(self):
        """Initialize FAISS index for vector similarity search"""
        try:
            index_path = Path(self.vector_config.get("index_path", "faiss_index"))
            
            # Create FAISS index
            self.faiss_index = faiss.IndexFlatIP(self.embedding_dimension)  # Inner product for cosine similarity
            
            # Try to load existing index
            if index_path.exists():
                try:
                    self.faiss_index = faiss.read_index(str(index_path))
                    # Load corresponding memory IDs
                    ids_file = index_path.with_suffix('.ids')
                    if ids_file.exists():
                        with open(ids_file, 'r') as f:
                            self.memory_ids = json.load(f)
                    print(f"✅ Loaded existing FAISS index with {len(self.memory_ids)} memories")
                except Exception as e:
                    print(f"⚠️  Could not load existing index: {e}")
                    self.faiss_index = faiss.IndexFlatIP(self.embedding_dimension)
            
        except Exception as e:
            print(f"⚠️  FAISS initialization failed: {e}")
            self.faiss_index = None
    
    def _save_faiss_index(self):
        """Save FAISS index to disk"""
        if not self.faiss_index:
            return
            
        try:
            index_path = Path(self.vector_config.get("index_path", "faiss_index"))
            index_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.faiss_index, str(index_path))
            
            # Save memory IDs
            ids_file = index_path.with_suffix('.ids')
            with open(ids_file, 'w') as f:
                json.dump(self.memory_ids, f)
                
        except Exception as e:
            print(f"⚠️  Could not save FAISS index: {e}")
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding vector for text"""
        if self.embedding_model:
            try:
                embedding = self.embedding_model.encode(text, convert_to_numpy=True)
                # Normalize for cosine similarity
                embedding = embedding / np.linalg.norm(embedding)
                return embedding.astype(np.float32)
            except Exception as e:
                print(f"⚠️  Embedding generation failed: {e}")
        
        # Fallback: simple hash-based embedding (not ideal but functional)
        hash_value = hashlib.md5(text.encode()).hexdigest()
        # Convert hex to numbers and create pseudo-embedding
        pseudo_embedding = np.array([
            int(hash_value[i:i+2], 16) / 255.0 
            for i in range(0, min(len(hash_value), self.embedding_dimension * 2), 2)
        ], dtype=np.float32)
        
        # Pad or truncate to correct dimension
        if len(pseudo_embedding) < self.embedding_dimension:
            pseudo_embedding = np.pad(pseudo_embedding, (0, self.embedding_dimension - len(pseudo_embedding)))
        else:
            pseudo_embedding = pseudo_embedding[:self.embedding_dimension]
        
        return pseudo_embedding / np.linalg.norm(pseudo_embedding)
    
    def ensure_memory_structure(self):
        """Initialize memory storage structure"""
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                "memories": {},
                "embeddings": {},  # Store embeddings separately
                "indices": {
                    "by_type": {},
                    "by_tag": {},
                    "by_date": {},
                    "by_importance": {}
                },
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "2.0.0",
                    "total_memories": 0,
                    "vector_enabled": FAISS_AVAILABLE and self.vector_config.get("faiss_enabled", True)
                }
            }
            self._save_memory(data)
    
    def _load_memory(self) -> Dict:
        """Load memory data from storage"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"memories": {}, "embeddings": {}, "indices": {}, "metadata": {}}
    
    def _save_memory(self, data: Dict):
        """Save memory data to storage"""
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        data["metadata"]["total_memories"] = len(data.get("memories", {}))
        data["metadata"]["vector_enabled"] = bool(self.faiss_index)
        
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Save FAISS index if available
        if self.faiss_index:
            self._save_faiss_index()
    
    def _generate_memory_id(self, content: str, memory_type: str) -> str:
        """Generate unique memory ID based on content hash"""
        content_hash = hashlib.md5(f"{content}{memory_type}".encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"EMEM-{timestamp}-{content_hash}"
    
    def store_memory(self, 
                    content: str,
                    memory_type: str = "factual",
                    category: str = None,  # Added for compatibility
                    importance: int = 5,
                    tags: List[str] = None,
                    metadata: Dict = None) -> str:
        """Store new memory with vector embedding"""
        
        # Support both memory_type and category parameters for compatibility
        if category and not memory_type:
            memory_type = category
        
        data = self._load_memory()
        
        memory_id = self._generate_memory_id(content, memory_type)
        
        # Generate embedding
        embedding = self._generate_embedding(content)
        
        memory = {
            "id": memory_id,
            "content": content,
            "type": memory_type,
            "importance": max(1, min(10, importance)),
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "access_count": 0,
            "metadata": metadata or {},
            "connections": [],
            "embedding_vector": embedding.tolist()  # Store as list for JSON serialization
        }
        
        data["memories"][memory_id] = memory
        
        # Store embedding separately for efficiency
        data["embeddings"][memory_id] = embedding.tolist()
        
        # Add to FAISS index if available
        if self.faiss_index is not None:
            try:
                self.faiss_index.add(embedding.reshape(1, -1))
                self.memory_ids.append(memory_id)
            except Exception as e:
                print(f"⚠️  Could not add to FAISS index: {e}")
        
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
        
        # Date index
        date_key = memory["created"][:10]
        if date_key not in data["indices"]["by_date"]:
            data["indices"]["by_date"][date_key] = []
        data["indices"]["by_date"][date_key].append(memory_id)
        
        # Importance index
        importance = str(memory["importance"])
        if importance not in data["indices"]["by_importance"]:
            data["indices"]["by_importance"][importance] = []
        data["indices"]["by_importance"][importance].append(memory_id)
    
    def semantic_search(self, 
                       query: str, 
                       limit: int = 10,
                       similarity_threshold: float = None) -> List[Tuple[Dict, float]]:
        """Perform semantic search using vector similarity"""
        
        if not self.faiss_index or len(self.memory_ids) == 0:
            # Fall back to text search
            return [(mem, 0.5) for mem in self.search_memories(query, limit=limit)]
        
        if similarity_threshold is None:
            similarity_threshold = self.vector_config.get("similarity_threshold", 0.7)
        
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            
            # Search FAISS index
            scores, indices = self.faiss_index.search(
                query_embedding.reshape(1, -1), 
                min(limit * 2, len(self.memory_ids))  # Get more results to filter
            )
            
            # Retrieve matching memories
            data = self._load_memory()
            results = []
            
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.memory_ids) and score >= similarity_threshold:
                    memory_id = self.memory_ids[idx]
                    if memory_id in data["memories"]:
                        memory = data["memories"][memory_id]
                        # Update access tracking
                        memory["last_accessed"] = datetime.now().isoformat()
                        memory["access_count"] = memory.get("access_count", 0) + 1
                        results.append((memory, float(score)))
            
            # Save updated access info
            self._save_memory(data)
            
            return results[:limit]
            
        except Exception as e:
            print(f"⚠️  Semantic search failed: {e}")
            # Fall back to text search
            return [(mem, 0.5) for mem in self.search_memories(query, limit=limit)]
    
    def search_memories(self, 
                       query: str = None,
                       memory_type: str = None,
                       tags: List[str] = None,
                       importance_min: int = 1,
                       limit: int = 20,
                       use_semantic: bool = True) -> List[Dict]:
        """Enhanced search with optional semantic capabilities"""
        
        # If semantic search is available and requested, use it
        if use_semantic and query and self.faiss_index:
            semantic_results = self.semantic_search(query, limit)
            if semantic_results:
                return [memory for memory, score in semantic_results]
        
        # Fall back to traditional search
        data = self._load_memory()
        memories = list(data["memories"].values())
        
        # Apply filters
        if memory_type:
            memories = [m for m in memories if m.get("type") == memory_type]
        
        if tags:
            memories = [m for m in memories 
                       if any(tag in m.get("tags", []) for tag in tags)]
        
        if importance_min:
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
    
    def get_similar_memories(self, memory_id: str, limit: int = 5) -> List[Tuple[Dict, float]]:
        """Find memories similar to a given memory using vector search"""
        
        data = self._load_memory()
        if memory_id not in data["memories"]:
            return []
        
        target_memory = data["memories"][memory_id]
        target_content = target_memory["content"]
        
        # Use semantic search to find similar memories
        similar = self.semantic_search(target_content, limit + 1)  # +1 to exclude self
        
        # Filter out the target memory itself
        return [(mem, score) for mem, score in similar if mem["id"] != memory_id][:limit]
    
    def get_enhanced_analytics(self) -> Dict[str, Any]:
        """Get comprehensive analytics including vector search metrics"""
        
        data = self._load_memory()
        memories = data["memories"]
        
        analytics = {
            "total_memories": len(memories),
            "vector_enabled": bool(self.faiss_index),
            "embedding_model": "SentenceTransformers" if self.embedding_model else "Fallback",
            "types_distribution": {},
            "importance_distribution": {},
            "access_patterns": {},
            "recent_activity": [],
            "top_tags": {},
            "connection_network": {"nodes": 0, "edges": 0},
            "similarity_clusters": []
        }
        
        # Basic analytics
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
        
        # Vector search specific analytics
        if self.faiss_index:
            analytics["faiss_index_size"] = self.faiss_index.ntotal
            analytics["embedding_dimension"] = self.embedding_dimension
        
        return analytics
    
    def consolidate_and_cluster(self, similarity_threshold: float = 0.8) -> Dict[str, Any]:
        """Advanced consolidation using vector similarity clustering"""
        
        if not self.faiss_index:
            return {"error": "Vector search not available for clustering"}
        
        data = self._load_memory()
        memories = list(data["memories"].values())
        
        clusters = []
        processed = set()
        
        for memory in memories:
            if memory["id"] in processed:
                continue
            
            # Find similar memories
            similar = self.get_similar_memories(memory["id"], limit=20)
            
            # Create cluster if we have similar memories above threshold
            cluster_members = [memory]
            for sim_memory, score in similar:
                if score >= similarity_threshold and sim_memory["id"] not in processed:
                    cluster_members.append(sim_memory)
                    processed.add(sim_memory["id"])
            
            if len(cluster_members) > 1:
                clusters.append({
                    "cluster_id": f"CLUSTER-{len(clusters) + 1}",
                    "members": cluster_members,
                    "avg_importance": np.mean([m["importance"] for m in cluster_members]),
                    "dominant_type": max(set([m["type"] for m in cluster_members]), 
                                       key=[m["type"] for m in cluster_members].count)
                })
            
            processed.add(memory["id"])
        
        return {
            "clusters_found": len(clusters),
            "clustered_memories": sum(len(c["members"]) for c in clusters),
            "clusters": clusters[:10],  # Return top 10 clusters
            "consolidation_recommendations": [
                f"Cluster {c['cluster_id']}: {len(c['members'])} similar {c['dominant_type']} memories"
                for c in clusters[:5]
            ]
        }

# Alias for backward compatibility
EnhancedCodexMemory = EnhancedMemoryManager

# Global enhanced memory instance
try:
    enhanced_codex_memory = EnhancedMemoryManager()
except Exception as e:
    print(f"⚠️  Enhanced memory initialization failed: {e}")
    enhanced_codex_memory = None

if __name__ == "__main__":
    print("🧠 Enhanced Codex Memory with Vector Search initialized")
    
    if enhanced_codex_memory:
        # Test enhanced memory
        memory_id = enhanced_codex_memory.store_memory(
            "Advanced AI-powered vector search enables semantic memory retrieval",
            "factual",
            importance=9,
            tags=["ai", "vector_search", "enhancement"]
        )
        print(f"Stored enhanced memory: {memory_id}")
        
        # Test semantic search
        results = enhanced_codex_memory.semantic_search("AI memory search")
        print(f"Semantic search found {len(results)} results")
        
        # Show analytics
        analytics = enhanced_codex_memory.get_enhanced_analytics()
        print(f"Vector enabled: {analytics['vector_enabled']}")
        print(f"Embedding model: {analytics['embedding_model']}")
    else:
        print("❌ Enhanced memory not available")