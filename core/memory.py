"""
PRATIGHAT.AI Memory Engine

Manages persistent storage using SQLite for structured data and
ChromaDB for vector embeddings and long-term memory.
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from core.config import get_config


@dataclass
class MemoryEntry:
    """Structured memory entry"""
    id: Optional[int] = None
    timestamp: str = ""
    agent: str = ""
    task: str = ""
    data: Dict[str, Any] = None
    insights: List[str] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        if self.data is None:
            self.data = {}
        if self.insights is None:
            self.insights = []


class MemoryEngine:
    """
    Memory Engine for PRATIGHAT-AI
    
    Handles both structured data (SQLite) and vector embeddings (ChromaDB)
    for long-term memory, pattern recognition, and context recall.
    """
    
    def __init__(self):
        config = get_config()
        self.sqlite_path = config.sqlite_path
        self.chroma_path = config.chroma_path
        
        # Initialize SQLite
        self.conn = sqlite3.connect(self.sqlite_path, check_same_thread=False)
        self._init_sqlite_schema()
        
        # Initialize ChromaDB if available
        if CHROMADB_AVAILABLE:
            self.chroma_client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=self.chroma_path
            ))
            
            # Create collections
            self.scan_collection = self._get_or_create_collection("scans")
            self.reasoning_collection = self._get_or_create_collection("reasoning")
            self.pattern_collection = self._get_or_create_collection("patterns")
        else:
            self.chroma_client = None
            self.scan_collection = None
            self.reasoning_collection = None
            self.pattern_collection = None
    
    def _init_sqlite_schema(self) -> None:
        """Initialize SQLite database schema"""
        cursor = self.conn.cursor()
        
        # Memory entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent TEXT NOT NULL,
                task TEXT NOT NULL,
                data TEXT NOT NULL,
                insights TEXT NOT NULL
            )
        """)
        
        # Hosts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT UNIQUE NOT NULL,
                hostname TEXT,
                os_type TEXT,
                fingerprint TEXT,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL
            )
        """)
        
        # Services table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host_id INTEGER NOT NULL,
                port INTEGER NOT NULL,
                protocol TEXT NOT NULL,
                service TEXT,
                version TEXT,
                state TEXT,
                FOREIGN KEY (host_id) REFERENCES hosts(id)
            )
        """)
        
        # Attack chains table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attack_chains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                steps TEXT NOT NULL,
                probability REAL,
                impact REAL,
                created_at TEXT NOT NULL
            )
        """)
        
        # PoC templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS poc_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                template TEXT NOT NULL,
                safe BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
    
    def _get_or_create_collection(self, name: str):
        """Get or create a ChromaDB collection"""
        if not CHROMADB_AVAILABLE or not self.chroma_client:
            return None
        try:
            return self.chroma_client.get_collection(name)
        except:
            return self.chroma_client.create_collection(name)
    
    def store_entry(self, entry: MemoryEntry) -> int:
        """Store a memory entry in SQLite"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memory_entries (timestamp, agent, task, data, insights)
            VALUES (?, ?, ?, ?, ?)
        """, (
            entry.timestamp,
            entry.agent,
            entry.task,
            json.dumps(entry.data),
            json.dumps(entry.insights)
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_entries(
        self, 
        agent: Optional[str] = None, 
        task: Optional[str] = None,
        limit: int = 100
    ) -> List[MemoryEntry]:
        """Retrieve memory entries"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM memory_entries WHERE 1=1"
        params = []
        
        if agent:
            query += " AND agent = ?"
            params.append(agent)
        
        if task:
            query += " AND task = ?"
            params.append(task)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [
            MemoryEntry(
                id=row[0],
                timestamp=row[1],
                agent=row[2],
                task=row[3],
                data=json.loads(row[4]),
                insights=json.loads(row[5])
            )
            for row in rows
        ]
    
    def store_host(self, ip: str, hostname: str = "", os_type: str = "", 
                   fingerprint: str = "") -> int:
        """Store or update host information"""
        cursor = self.conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO hosts (ip, hostname, os_type, fingerprint, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(ip) DO UPDATE SET
                hostname = excluded.hostname,
                os_type = excluded.os_type,
                fingerprint = excluded.fingerprint,
                last_seen = excluded.last_seen
        """, (ip, hostname, os_type, fingerprint, timestamp, timestamp))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def store_service(self, host_id: int, port: int, protocol: str,
                     service: str = "", version: str = "", state: str = "open") -> int:
        """Store service information"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO services (host_id, port, protocol, service, version, state)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (host_id, port, protocol, service, version, state))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_host_by_ip(self, ip: str) -> Optional[Dict[str, Any]]:
        """Retrieve host information by IP"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM hosts WHERE ip = ?", (ip,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'ip': row[1],
            'hostname': row[2],
            'os_type': row[3],
            'fingerprint': row[4],
            'first_seen': row[5],
            'last_seen': row[6]
        }
    
    def vectorize_and_store(self, collection_name: str, text: str, 
                           metadata: Dict[str, Any], doc_id: str) -> None:
        """Store text with vector embedding in ChromaDB"""
        if not CHROMADB_AVAILABLE or not self.chroma_client:
            return  # Silently skip if ChromaDB not available
            
        collection = getattr(self, f"{collection_name}_collection", None)
        if not collection:
            collection = self._get_or_create_collection(collection_name)
        
        if collection:
            collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
    
    def semantic_search(self, collection_name: str, query: str, 
                       n_results: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search in ChromaDB"""
        if not CHROMADB_AVAILABLE or not self.chroma_client:
            return []  # Return empty if ChromaDB not available
            
        collection = getattr(self, f"{collection_name}_collection", None)
        if not collection:
            return []
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            return []
        
        return [
            {
                'document': doc,
                'metadata': meta,
                'id': doc_id
            }
            for doc, meta, doc_id in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['ids'][0]
            )
        ]
    
    def store_attack_chain(self, name: str, description: str, steps: List[str],
                          probability: float, impact: float) -> int:
        """Store attack chain prediction"""
        cursor = self.conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO attack_chains (name, description, steps, probability, impact, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, json.dumps(steps), probability, impact, timestamp))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_attack_chains(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve stored attack chains"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM attack_chains ORDER BY probability DESC LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        return [
            {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'steps': json.loads(row[3]),
                'probability': row[4],
                'impact': row[5],
                'created_at': row[6]
            }
            for row in rows
        ]
    
    def close(self) -> None:
        """Close database connections"""
        self.conn.close()


# Global memory engine instance
_memory_engine: Optional[MemoryEngine] = None


def get_memory_engine() -> MemoryEngine:
    """Get global memory engine instance"""
    global _memory_engine
    if _memory_engine is None:
        _memory_engine = MemoryEngine()
    return _memory_engine
