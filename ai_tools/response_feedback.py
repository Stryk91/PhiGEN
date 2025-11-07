"""
Response Quality Feedback System
Learns from user reactions to improve response quality
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResponseFeedbackTracker:
    """Tracks response quality based on user reactions"""

    def __init__(self, feedback_file: Path, log_file: Path):
        self.feedback_file = feedback_file
        self.log_file = log_file
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)

        # Reaction mappings
        self.GOOD_REACTIONS = ['✅', '✔️', '👍', '💚']
        self.BAD_REACTIONS = ['❌', '❎', '👎', '💔']
        self.VERY_BAD_REACTIONS = ['☠️', '💀', '🤮', '🤢']

        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Create files if they don't exist"""
        if not self.feedback_file.exists():
            initial_data = {
                "good_responses": [],
                "bad_responses": [],
                "very_bad_responses": [],
                "stats": {
                    "total_good": 0,
                    "total_bad": 0,
                    "total_very_bad": 0
                }
            }
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2)

        if not self.log_file.exists():
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"=== Conversation Log Started {datetime.now().strftime('%d/%m/%y %I:%M%p')} ===\n\n")

    def log_message(self, author: str, message: str, is_bot: bool = False, message_id: Optional[int] = None):
        """Log a message in simple chronological format"""
        timestamp = datetime.now().strftime('%d/%m %I:%M%p')

        # Format: "Author said at DD/MM HH:MMam/pm: message"
        log_line = f"{author} said at {timestamp}: {message}"

        # If bot message, add message ID for reaction tracking
        if is_bot and message_id:
            log_line += f" [MSG_ID:{message_id}]"

        log_line += "\n"

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)

    def add_reaction(self, message_id: int, reaction: str, bot_response: str):
        """Add a reaction to a bot response and update learning database"""
        # Determine reaction type
        if reaction in self.GOOD_REACTIONS:
            reaction_type = "GOOD"
            category = "good_responses"
        elif reaction in self.BAD_REACTIONS:
            reaction_type = "BAD"
            category = "bad_responses"
        elif reaction in self.VERY_BAD_REACTIONS:
            reaction_type = "VERY_BAD"
            category = "very_bad_responses"
        else:
            return  # Ignore other reactions

        logger.info(f"Reaction {reaction} ({reaction_type}) added to message {message_id}")

        # Update the log file with reaction
        self._update_log_with_reaction(message_id, reaction_type)

        # Update feedback database
        self._update_feedback_database(category, bot_response, reaction_type)

    def _update_log_with_reaction(self, message_id: int, reaction_type: str):
        """Update the log file to append reaction to the message"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Find the line with this message ID
            for i, line in enumerate(lines):
                if f"[MSG_ID:{message_id}]" in line:
                    # Remove the MSG_ID tag and add reaction
                    lines[i] = line.replace(f" [MSG_ID:{message_id}]", f" [REACTION: {reaction_type}]")
                    break

            # Write back
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        except Exception as e:
            logger.error(f"Error updating log with reaction: {e}")

    def _update_feedback_database(self, category: str, response: str, reaction_type: str):
        """Add response to the appropriate category in feedback database"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Add response if not already there (limit to 50 most recent)
            if response not in data[category]:
                data[category].append(response)
                # Keep only last 50
                if len(data[category]) > 50:
                    data[category] = data[category][-50:]

            # Update stats
            stat_key = f"total_{category.split('_')[0]}"  # e.g., "total_good"
            data["stats"][stat_key] = data["stats"].get(stat_key, 0) + 1

            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error updating feedback database: {e}")

    def get_bad_response_examples(self, limit: int = 5) -> List[str]:
        """Get examples of bad responses to avoid"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Prioritize very_bad over bad
            very_bad = data.get("very_bad_responses", [])[-limit:]
            remaining = limit - len(very_bad)

            if remaining > 0:
                bad = data.get("bad_responses", [])[-remaining:]
                return very_bad + bad

            return very_bad

        except Exception as e:
            logger.error(f"Error getting bad examples: {e}")
            return []

    def get_good_response_examples(self, limit: int = 5) -> List[str]:
        """Get examples of good responses to emulate"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return data.get("good_responses", [])[-limit:]

        except Exception as e:
            logger.error(f"Error getting good examples: {e}")
            return []

    def get_feedback_stats(self) -> Dict:
        """Get overall feedback statistics"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "total_good": data["stats"].get("total_good", 0),
                "total_bad": data["stats"].get("total_bad", 0),
                "total_very_bad": data["stats"].get("total_very_bad", 0),
                "good_examples_count": len(data.get("good_responses", [])),
                "bad_examples_count": len(data.get("bad_responses", [])),
                "very_bad_examples_count": len(data.get("very_bad_responses", []))
            }

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "total_good": 0,
                "total_bad": 0,
                "total_very_bad": 0,
                "good_examples_count": 0,
                "bad_examples_count": 0,
                "very_bad_examples_count": 0
            }

    def build_learning_context(self) -> str:
        """Build context string with good/bad examples for prompt injection"""
        bad_examples = self.get_bad_response_examples(limit=3)
        good_examples = self.get_good_response_examples(limit=3)

        context_parts = []

        if bad_examples:
            context_parts.append("[Previous responses that got NEGATIVE reactions - AVOID these patterns]")
            for i, example in enumerate(bad_examples, 1):
                # Truncate long examples
                truncated = example[:150] + "..." if len(example) > 150 else example
                context_parts.append(f"  Bad example {i}: \"{truncated}\"")

        if good_examples:
            context_parts.append("\n[Previous responses that got POSITIVE reactions - USE these patterns]")
            for i, example in enumerate(good_examples, 1):
                truncated = example[:150] + "..." if len(example) > 150 else example
                context_parts.append(f"  Good example {i}: \"{truncated}\"")

        if context_parts:
            return "\n".join(context_parts) + "\n"

        return ""

    def get_all_responses_by_quality(self) -> Dict[str, List[str]]:
        """Get all responses organized by quality"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "good": data.get("good_responses", []),
                "bad": data.get("bad_responses", []),
                "very_bad": data.get("very_bad_responses", [])
            }

        except Exception as e:
            logger.error(f"Error getting all responses: {e}")
            return {"good": [], "bad": [], "very_bad": []}
