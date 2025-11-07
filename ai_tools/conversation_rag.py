"""
Conversation RAG (Retrieval-Augmented Generation)
Semantic search over conversation history to find relevant examples
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConversationExample:
    """A single conversation exchange"""
    user_message: str
    bot_response: str
    timestamp: str
    reaction: Optional[str] = None  # GOOD, BAD, VERY_BAD
    author: str = "User"

    def get_quality_score(self) -> float:
        """Get numeric quality score for ranking"""
        if self.reaction == "GOOD":
            return 1.0
        elif self.reaction == "BAD":
            return -0.5
        elif self.reaction == "VERY_BAD":
            return -1.0
        return 0.0  # No reaction


class ConversationRAG:
    """RAG system for conversation history"""

    def __init__(self, log_file: Path, db_path: Path = None):
        self.log_file = log_file
        self.db_path = db_path or Path(__file__).parent / "chroma_db"
        self.collection = None
        self.embeddings_model = None

        # Lazy load ChromaDB and embeddings (only when needed)
        self._chroma_client = None

    def _init_chroma(self):
        """Initialize ChromaDB (lazy loading)"""
        if self._chroma_client is not None:
            return

        try:
            import chromadb
            from chromadb.config import Settings

            # Create persistent client
            self._chroma_client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            # Get or create collection
            self.collection = self._chroma_client.get_or_create_collection(
                name="conversations",
                metadata={"description": "Discord conversation history"}
            )

            logger.info(f"ChromaDB initialized with {self.collection.count()} examples")

        except ImportError:
            logger.error("ChromaDB not installed. Install with: pip install chromadb")
            raise

    def _init_embeddings(self):
        """Initialize embedding model (lazy loading)"""
        if self.embeddings_model is not None:
            return

        try:
            from sentence_transformers import SentenceTransformer

            # Use lightweight model (133MB, runs on CPU)
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer loaded: all-MiniLM-L6-v2")

        except ImportError:
            logger.error("sentence-transformers not installed. Install with: pip install sentence-transformers")
            raise

    def parse_conversation_log(self) -> List[ConversationExample]:
        """
        Parse conversation_full_log.txt into examples

        Format:
        User said at DD/MM HH:MMam/pm: message
        Bot said at DD/MM HH:MMam/pm: response [REACTION: GOOD]
        """
        if not self.log_file.exists():
            logger.warning(f"Log file not found: {self.log_file}")
            return []

        examples = []
        current_user_msg = None
        current_timestamp = None
        current_author = None

        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('==='):
                    continue

                # Parse: "Author said at DD/MM HH:MMam/pm: message [REACTION: TYPE]"
                # Handle optional leading quote
                cleaned_line = line.lstrip('"').strip()
                match = re.match(r'^(.+?) said at (.+?): (.+)$', cleaned_line)
                if not match:
                    continue

                author, timestamp, content = match.groups()

                # Extract reaction if present
                reaction = None
                reaction_match = re.search(r'\[REACTION: (\w+)\]', content)
                if reaction_match:
                    reaction = reaction_match.group(1)
                    content = re.sub(r'\s*\[REACTION: \w+\]', '', content).strip()

                # Detect if bot message
                is_bot = any(bot_name in author for bot_name in ['PhiGEN', 'Bot', 'APP'])

                if not is_bot:
                    # User message - store for pairing
                    current_user_msg = content
                    current_timestamp = timestamp
                    current_author = author
                else:
                    # Bot response - create example if we have a user message
                    if current_user_msg:
                        examples.append(ConversationExample(
                            user_message=current_user_msg,
                            bot_response=content,
                            timestamp=current_timestamp,
                            reaction=reaction,
                            author=current_author
                        ))
                        current_user_msg = None  # Reset

        logger.info(f"Parsed {len(examples)} conversation examples from log")
        return examples

    def index_conversations(self, force_rebuild: bool = False):
        """
        Index all conversations into ChromaDB

        Args:
            force_rebuild: If True, clear existing data and rebuild
        """
        self._init_chroma()
        self._init_embeddings()

        # Check if already indexed
        if not force_rebuild and self.collection.count() > 0:
            logger.info(f"Using existing index with {self.collection.count()} examples")
            return

        # Parse log file
        examples = self.parse_conversation_log()
        if not examples:
            logger.warning("No examples found to index")
            return

        # Clear existing if rebuilding
        if force_rebuild and self.collection.count() > 0:
            logger.info("Clearing existing index...")
            self._chroma_client.delete_collection("conversations")
            self.collection = self._chroma_client.create_collection(
                name="conversations",
                metadata={"description": "Discord conversation history"}
            )

        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []

        for i, example in enumerate(examples):
            # Combine user + bot for embedding (captures full context)
            combined_text = f"User: {example.user_message}\nBot: {example.bot_response}"

            documents.append(combined_text)
            metadatas.append({
                "user_message": example.user_message,
                "bot_response": example.bot_response,
                "timestamp": example.timestamp,
                "reaction": example.reaction or "NONE",
                "quality_score": example.get_quality_score(),
                "author": example.author
            })
            ids.append(f"conv_{i}")

        # Batch add to ChromaDB (handles embedding automatically with default model)
        # But we'll use our own embeddings for better control
        embeddings = self.embeddings_model.encode(documents, show_progress_bar=True).tolist()

        logger.info(f"Adding {len(documents)} examples to ChromaDB...")
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

        logger.info(f"✅ Indexed {len(examples)} conversations")

    def search_similar(self, query: str, top_k: int = 5,
                      min_quality: float = -0.5) -> List[Dict]:
        """
        Search for similar conversation examples

        Args:
            query: User's current message
            top_k: Number of results to return
            min_quality: Minimum quality score (-1.0 to 1.0)

        Returns:
            List of similar examples with metadata
        """
        self._init_chroma()
        self._init_embeddings()

        if self.collection.count() == 0:
            logger.warning("No examples indexed yet")
            return []

        # Embed the query
        query_embedding = self.embeddings_model.encode([query])[0].tolist()

        # Search (get more than top_k to filter by quality)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k * 3, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        # Filter by quality and re-rank
        filtered_results = []
        for i, metadata in enumerate(results['metadatas'][0]):
            quality_score = metadata.get('quality_score', 0.0)

            if quality_score >= min_quality:
                filtered_results.append({
                    'user_message': metadata['user_message'],
                    'bot_response': metadata['bot_response'],
                    'timestamp': metadata['timestamp'],
                    'reaction': metadata['reaction'],
                    'quality_score': quality_score,
                    'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                    'author': metadata.get('author', 'User')
                })

        # Sort by combined score (similarity + quality)
        filtered_results.sort(
            key=lambda x: x['similarity'] * 0.7 + (x['quality_score'] + 1) * 0.3,
            reverse=True
        )

        return filtered_results[:top_k]

    def build_rag_context(self, query: str, max_examples: int = 3) -> str:
        """
        Build RAG context string to inject into prompt

        Args:
            query: User's current message
            max_examples: Maximum examples to include

        Returns:
            Formatted context string
        """
        similar = self.search_similar(query, top_k=max_examples, min_quality=0.0)

        if not similar:
            return ""

        context_parts = [
            "=== RELEVANT PAST CONVERSATIONS ===",
            "(Use these as reference for style and approach)\n"
        ]

        for i, example in enumerate(similar, 1):
            reaction_emoji = {
                'GOOD': '✅',
                'BAD': '❌',
                'VERY_BAD': '💀',
                'NONE': ''
            }.get(example['reaction'], '')

            context_parts.append(f"Example {i} {reaction_emoji}:")
            context_parts.append(f"  User: {example['user_message'][:200]}")
            context_parts.append(f"  Bot: {example['bot_response'][:200]}")
            context_parts.append("")

        context_parts.append("=== END EXAMPLES ===\n")

        return "\n".join(context_parts)

    def get_stats(self) -> Dict:
        """Get RAG system statistics"""
        self._init_chroma()

        total = self.collection.count() if self.collection else 0

        if total == 0:
            return {
                "total_examples": 0,
                "good_examples": 0,
                "bad_examples": 0,
                "neutral_examples": 0
            }

        # Get all metadatas to calculate stats
        all_data = self.collection.get(include=["metadatas"])

        good = sum(1 for m in all_data['metadatas'] if m.get('reaction') == 'GOOD')
        bad = sum(1 for m in all_data['metadatas'] if m.get('reaction') in ['BAD', 'VERY_BAD'])
        neutral = total - good - bad

        return {
            "total_examples": total,
            "good_examples": good,
            "bad_examples": bad,
            "neutral_examples": neutral
        }


if __name__ == "__main__":
    # Test the RAG system
    import sys

    log_file = Path(__file__).parent / "conversation_full_log.txt"
    rag = ConversationRAG(log_file)

    print("Indexing conversations...")
    rag.index_conversations(force_rebuild=False)

    print("\nRAG Stats:")
    print(json.dumps(rag.get_stats(), indent=2))

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\nSearching for: {query}")
        results = rag.search_similar(query, top_k=3)

        for i, result in enumerate(results, 1):
            print(f"\n=== Result {i} (similarity: {result['similarity']:.2f}, quality: {result['quality_score']}) ===")
            print(f"User: {result['user_message'][:150]}")
            print(f"Bot: {result['bot_response'][:150]}")
            print(f"Reaction: {result['reaction']}")
