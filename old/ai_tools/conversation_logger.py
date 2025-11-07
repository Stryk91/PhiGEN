"""
Conversation Logger
Logs Discord conversations to build context and learn communication patterns
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class ConversationLogger:
    """Logs and analyzes Discord conversations for contextual learning"""

    def __init__(self, log_file: Path):
        """
        Initialize conversation logger

        Args:
            log_file: Path to JSONL log file
        """
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log_message(self,
                   channel_id: int,
                   channel_name: str,
                   user_id: int,
                   user_name: str,
                   message: str,
                   bot_response: Optional[str] = None,
                   model_used: Optional[str] = None):
        """
        Log a conversation message

        Args:
            channel_id: Discord channel ID
            channel_name: Discord channel name
            user_id: User ID
            user_name: Username
            message: User's message
            bot_response: Bot's response (if any)
            model_used: Which AI model responded
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "channel_id": channel_id,
            "channel_name": channel_name,
            "user_id": user_id,
            "user_name": user_name,
            "message": message,
            "bot_response": bot_response,
            "model_used": model_used
        }

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Error logging conversation: {e}")

    def get_recent_context(self,
                          channel_id: Optional[int] = None,
                          limit: int = 50) -> List[Dict]:
        """
        Get recent conversation history

        Args:
            channel_id: Filter by specific channel (None = all channels)
            limit: Maximum number of messages to return

        Returns:
            List of conversation entries
        """
        if not self.log_file.exists():
            return []

        entries = []

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())

                        # Filter by channel if specified
                        if channel_id is None or entry.get('channel_id') == channel_id:
                            entries.append(entry)
                    except json.JSONDecodeError:
                        continue

            # Return most recent entries
            return entries[-limit:] if entries else []

        except Exception as e:
            logger.error(f"Error loading conversation history: {e}")
            return []

    def build_context_prompt(self,
                            channel_id: Optional[int] = None,
                            limit: int = 20) -> str:
        """
        Build a context prompt from recent conversations

        Args:
            channel_id: Filter by specific channel
            limit: Number of recent messages to include

        Returns:
            Context string to inject into prompts
        """
        recent = self.get_recent_context(channel_id, limit)

        if not recent:
            return ""

        # Build context from recent conversations
        context_lines = [
            "Recent conversation context (to understand communication style):"
        ]

        for entry in recent[-10:]:  # Use last 10 messages for context
            user_msg = entry.get('message', '')
            bot_resp = entry.get('bot_response', '')

            if user_msg:
                context_lines.append(f"User: {user_msg[:100]}")  # Limit length
            if bot_resp:
                context_lines.append(f"Bot: {bot_resp[:100]}")

        return "\n".join(context_lines)

    def analyze_patterns(self, limit: int = 1000) -> Dict:
        """
        Analyze conversation patterns to learn semantics and slang

        Args:
            limit: Number of recent messages to analyze

        Returns:
            Analysis dictionary with patterns, common words, etc.
        """
        recent = self.get_recent_context(limit=limit)

        if not recent:
            return {
                "total_messages": 0,
                "common_words": [],
                "active_users": [],
                "message_count": 0
            }

        # Extract all user messages
        all_messages = [entry.get('message', '') for entry in recent if entry.get('message')]

        # Count word frequency (simple tokenization)
        word_counts = Counter()
        for msg in all_messages:
            # Simple word extraction (lowercase, split by space)
            words = [w.lower().strip('.,!?;:"()[]{}') for w in msg.split()]
            # Filter out very short words and common stopwords
            words = [w for w in words if len(w) > 2 and w not in {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'has', 'had', 'was', 'were', 'been', 'have', 'will', 'with', 'this', 'that', 'from', 'they', 'what', 'when', 'where', 'who', 'why', 'how'}]
            word_counts.update(words)

        # Count active users
        user_counts = Counter(entry.get('user_name') for entry in recent if entry.get('user_name'))

        return {
            "total_messages": len(recent),
            "user_messages": len(all_messages),
            "common_words": word_counts.most_common(20),
            "active_users": user_counts.most_common(10),
            "message_count": len(all_messages)
        }

    def get_stats(self) -> Dict:
        """Get conversation logging statistics"""
        if not self.log_file.exists():
            return {
                "total_logged": 0,
                "file_size": 0
            }

        try:
            line_count = 0
            with open(self.log_file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)

            file_size = self.log_file.stat().st_size

            return {
                "total_logged": line_count,
                "file_size_kb": round(file_size / 1024, 2),
                "log_file": str(self.log_file)
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "total_logged": 0,
                "file_size_kb": 0,
                "error": str(e)
            }
