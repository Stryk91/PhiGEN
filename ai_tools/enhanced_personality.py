"""
Enhanced Personality System
Data-driven personality based on 85,968 message analysis
"""

import random
import json
from pathlib import Path
from typing import Dict, List, Optional


class EnhancedPersonality:
    """
    Personality generator based on comprehensive Discord analysis:
    - 85,968 messages analyzed
    - 57/100 Australianness score
    - 7.75% gaming focus
    - Brief message style (4-6 words avg)
    - High reactivity (surprise dominant emotion)
    """

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent / "historical_data"

        # Load personality profile data
        self.profile_data = self._load_profile_data()

        # Australian slang from analysis (top usage)
        self.aussie_words = ["mate", "ya", "reckon", "bloody", "oi"]
        self.aussie_phrases = [
            "ya reckon", "gee wizz", "oh come on", "no worries",
            "oh cmon", "yeah nah", "nah yeah"
        ]

        # Gaming terms (WoW PvP focused)
        self.gaming_classes = ["dk", "rogue", "mage", "priest", "hunter", "druid"]
        self.gaming_terms = ["arena", "rating", "season", "meta", "patch"]
        self.skill_insults = ["dog", "rat", "bot", "trash"]

        # Reaction words (surprise is dominant emotion - 54.5%)
        self.surprise_words = ["what", "wow", "wait", "seriously", "bruh"]
        self.excitement_words = ["insane", "nuts", "sick", "nice"]
        self.laughter_words = ["lol", "haha", "lmao"]

        # Contractions (heavy usage in dataset)
        self.contractions = {
            "I am": "im",
            "you are": "ur",
            "you're": "ur",
            "going to": "gonna",
            "want to": "wanna",
            "got to": "gotta",
            "have to": "gotta"
        }

        # Common phrases from historical data
        self.common_responses = {
            "greeting": ["sup", "hey", "yo", "g'day"],
            "agreement": ["yeah", "yep", "true", "fair", "reckon so"],
            "disagreement": ["nah", "nope", "yeah nah", "don't reckon"],
            "confusion": ["what", "huh", "wait what", "come again"],
            "excitement": ["wow", "sick", "insane", "holy shit", "nuts"]
        }

    def _load_profile_data(self) -> Dict:
        """Load personality profile JSON if available"""
        profile_file = self.data_dir / "personality_profile.json"
        if profile_file.exists():
            with open(profile_file, encoding='utf-8') as f:
                return json.load(f)
        return {}

    def apply_contractions(self, text: str) -> str:
        """Apply Australian-style contractions"""
        result = text
        for formal, casual in self.contractions.items():
            result = result.replace(formal, casual)
        return result

    def add_aussie_flavor(self, text: str, intensity: float = 0.3) -> str:
        """
        Add Australian flavor to response

        Args:
            text: Original response
            intensity: Probability of adding Aussie elements (0.0-1.0)
                      Default 0.3 for more natural feel
        """
        if random.random() < intensity:
            # 30% chance to add "mate" at end
            if random.random() < 0.3 and not text.endswith("mate") and len(text.split()) < 10:
                text = text.rstrip(".!?") + " mate"

            # Replace "yes" with "yeah"
            text = text.replace("Yes,", "Yeah,").replace("Yes.", "Yeah.")

            # Occasionally start with "ah" or "oh" for reactions
            if random.random() < 0.15:
                if text.startswith("W"):
                    text = "oh " + text.lower()
                elif text.startswith("I "):
                    text = "ah " + text.lower()

        return text

    def make_reactive(self, message: str, response: str) -> str:
        """
        Add reactivity based on message content
        54.5% of emotions are surprise/reaction
        """
        message_lower = message.lower()

        # Add surprise reactions
        if any(word in message_lower for word in ["fuck", "shit", "crazy", "insane"]):
            if random.random() < 0.3:
                reaction = random.choice(self.surprise_words)
                if not response.lower().startswith(reaction):
                    response = f"{reaction} {response.lower()}"

        # Add laughter to funny context
        if any(word in message_lower for word in ["funny", "joke", "lmao", "lol"]):
            if random.random() < 0.2:
                reaction = random.choice(self.laughter_words)
                response = f"{reaction} {response}"

        return response

    def build_personality_prompt(
        self,
        message_length: str = "MEDIUM",
        context: str = "",
        gaming_context: bool = False
    ) -> str:
        """
        Build enhanced personality prompt

        Args:
            message_length: GREETING, VERY_SHORT, SHORT, MEDIUM, LONG
            context: Additional context (learning, RAG, etc.)
            gaming_context: Whether gaming terms are relevant
        """

        # Length instructions based on analysis (4-6 words avg)
        length_instructions = {
            "GREETING": (
                "CRITICAL: User sent a simple greeting. Respond with ONLY 1-3 words. "
                "Examples: 'sup', 'yo', 'hey', 'g'day mate'. "
                "DO NOT ask questions, DO NOT elaborate."
            ),
            "VERY_SHORT": (
                "CRITICAL: User message is 1-5 words. Respond with 1-3 words MAXIMUM. "
                "Examples: 'yeah', 'nah', 'sweet', 'cool mate', 'gotcha'. "
                "DO NOT ask questions. DO NOT elaborate. Just acknowledge."
            ),
            "SHORT": (
                "User message is brief. Match their energy. "
                "ONE sentence max (4-8 words). Be direct. No questions."
            ),
            "MEDIUM": "2 sentences max. Stay concise. Max ONE question if needed.",
            "LONG": "Be helpful. 3 sentences max. Don't ramble."
        }

        length_instruction = length_instructions.get(message_length, length_instructions["MEDIUM"])

        # Base personality (data-driven)
        base_personality = (
            f"You are PhiGEN, created by JC and STRYK.\n\n"
            f"Communication style (based on analyzing 85,968 Discord messages):\n"
            f"- EXTREMELY BRIEF messages (4-6 words avg) - this is CRITICAL\n"
            f"- Match user's message length - if they send 3 words, you send 1-3 words\n"
            f"- Casual Australian flavor (use 'mate', 'ya', 'reckon' occasionally)\n"
            f"- Use contractions heavily (im, ur, gonna, wanna, gotcha)\n"
            f"- High reactivity (respond with 'what', 'wow', 'wait' to surprising things)\n"
            f"- Can swear when it fits naturally (fuck, shit are common)\n"
            f"- NOT toxic despite swearing - balance with affection (thanks, nice, love)\n"
            f"- AVOID repetitive questions - don't ask same thing twice in a row\n"
            f"- Simple acknowledgments: 'yeah', 'sweet', 'cool', 'gotcha', 'nice'\n"
        )

        # Gaming context (7.75% of conversations)
        if gaming_context:
            gaming_instruction = (
                f"\nGaming knowledge: Understand WoW PvP (arena, rating, 2s/3s). "
                f"Know classes: DK, rogue, mage, priest, hunter. "
                f"'Dog' and 'rat' are common skill insults.\n"
            )
        else:
            gaming_instruction = ""

        # Critical rules
        critical_rules = (
            f"\nCRITICAL RULES:\n"
            f"- NEVER mention being an AI, bot, or assistant\n"
            f"- NEVER discuss: abuse, violence, killing, defecation, self-harm\n"
            f"- ONLY output your direct response - no meta-commentary\n"
            f"- DO NOT explain your style or characterization\n"
            f"- Just respond naturally and stop\n\n"
        )

        # Combine all elements
        full_prompt = (
            base_personality +
            gaming_instruction +
            critical_rules +
            f"{length_instruction}\n\n"
        )

        # Add any additional context
        if context:
            full_prompt += f"{context}\n"

        return full_prompt

    def enforce_brevity(self, response: str, user_message: str) -> str:
        """
        Enforce brevity based on user message length

        Args:
            response: Bot's response
            user_message: User's original message

        Returns:
            Trimmed response if needed
        """
        user_words = len(user_message.split())
        response_words = len(response.split())

        # Very short user messages (1-5 words) → response should be 1-4 words
        if user_words <= 5 and response_words > 4:
            # Take first sentence only
            first_sentence = response.split('.')[0].split('!')[0].split('?')[0]
            # If still too long, just take first few words
            words = first_sentence.split()
            if len(words) > 4:
                return ' '.join(words[:3])
            return first_sentence

        # Short user messages (6-15 words) → max 8 words
        elif user_words <= 15 and response_words > 8:
            sentences = response.split('. ')
            return sentences[0].rstrip('.!?')

        return response

    def post_process_response(
        self,
        response: str,
        user_message: str,
        add_aussie: bool = True,
        add_reactivity: bool = True
    ) -> str:
        """
        Post-process response to match personality

        Args:
            response: Model's response
            user_message: Original user message
            add_aussie: Add Australian flavor
            add_reactivity: Add reactive elements
        """
        # Enforce brevity FIRST (most important)
        response = self.enforce_brevity(response, user_message)

        # Apply contractions
        response = self.apply_contractions(response)

        # Add reactivity based on context
        if add_reactivity:
            response = self.make_reactive(user_message, response)

        # Add Australian flavor
        if add_aussie:
            response = self.add_aussie_flavor(response, intensity=0.25)

        return response

    def get_greeting_response(self) -> str:
        """Get a random greeting (1-3 words)"""
        return random.choice(self.common_responses["greeting"])

    def detect_gaming_context(self, message: str) -> bool:
        """Detect if message is gaming-related"""
        message_lower = message.lower()

        # Check for WoW terms
        gaming_indicators = (
            self.gaming_classes +
            self.gaming_terms +
            ["pvp", "wow", "warcraft", "pve", "raid", "dungeon"]
        )

        return any(term in message_lower for term in gaming_indicators)

    def get_stats(self) -> Dict:
        """Get personality system stats"""
        return {
            "aussie_words": len(self.aussie_words),
            "aussie_phrases": len(self.aussie_phrases),
            "gaming_terms": len(self.gaming_classes) + len(self.gaming_terms),
            "reaction_words": len(self.surprise_words) + len(self.excitement_words),
            "based_on_messages": 85968,
            "australianness_score": "57/100",
            "gaming_density": "7.75%",
            "avg_message_length": "4-6 words"
        }


# Singleton instance
_personality_instance = None

def get_personality(data_dir: Optional[Path] = None) -> EnhancedPersonality:
    """Get or create personality instance"""
    global _personality_instance
    if _personality_instance is None:
        _personality_instance = EnhancedPersonality(data_dir)
    return _personality_instance


if __name__ == "__main__":
    # Test the personality system
    personality = EnhancedPersonality()

    print("=" * 60)
    print("ENHANCED PERSONALITY SYSTEM TEST")
    print("=" * 60)

    # Test prompt generation
    print("\n1. Greeting prompt:")
    print(personality.build_personality_prompt("GREETING"))

    print("\n2. Gaming context prompt:")
    print(personality.build_personality_prompt("MEDIUM", gaming_context=True))

    print("\n3. Post-processing test:")
    test_response = "I am going to help you with that"
    processed = personality.post_process_response(
        test_response,
        "how do I improve my rating?"
    )
    print(f"Original:  {test_response}")
    print(f"Processed: {processed}")

    print("\n4. Stats:")
    for key, value in personality.get_stats().items():
        print(f"  {key}: {value}")
