"""
Conversation Analysis Tool
Analyze scraped Discord conversations for word frequency, topics, and patterns
"""

import re
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple
import json


class ConversationAnalyzer:
    """Analyze conversation patterns and word frequency"""

    def __init__(self, log_file: Path):
        self.log_file = log_file

        # Common words to filter out
        self.stopwords = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
            'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
            'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
            'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
            'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
            'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
            'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had',
            'were', 'said', 'did', 'having', 'may', 'might', 'am', 'being', 'going',
            # Discord/chat specific
            'lol', 'lmao', 'omg', 'wtf', 'idk', 'tbh', 'imo', 'yeah', 'yes', 'no',
            'ok', 'okay', 'thanks', 'thank', 'please', 'hey', 'hi', 'hello'
        }

    def parse_messages(self) -> List[Dict]:
        """Parse all messages from log file"""
        messages = []

        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('==='):
                    continue

                # Handle optional leading quote
                cleaned_line = line.lstrip('"').strip()
                match = re.match(r'^(.+?) said at (.+?): (.+)$', cleaned_line)
                if not match:
                    continue

                author, timestamp, content = match.groups()

                # Remove reaction tags
                content = re.sub(r'\s*\[REACTION: \w+\]', '', content).strip()

                # Skip empty messages
                if not content:
                    continue

                is_bot = any(bot_name in author for bot_name in ['PhiGEN', 'Bot', 'APP'])

                messages.append({
                    'author': author,
                    'timestamp': timestamp,
                    'content': content,
                    'is_bot': is_bot
                })

        return messages

    def extract_words(self, text: str) -> List[str]:
        """Extract meaningful words from text"""
        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)

        # Remove mentions and channels
        text = re.sub(r'<@!?\d+>', '', text)
        text = re.sub(r'<#\d+>', '', text)

        # Extract words (alphanumeric + apostrophes)
        words = re.findall(r"\b[a-z]+(?:'[a-z]+)?\b", text)

        # Filter stopwords and short words
        words = [w for w in words if w not in self.stopwords and len(w) > 2]

        return words

    def get_word_frequency(self, messages: List[Dict], user_only: bool = True,
                          top_n: int = 50) -> Counter:
        """Get word frequency from messages"""
        all_words = []

        for msg in messages:
            # Skip bot messages if user_only
            if user_only and msg['is_bot']:
                continue

            words = self.extract_words(msg['content'])
            all_words.extend(words)

        return Counter(all_words).most_common(top_n)

    def get_user_stats(self, messages: List[Dict]) -> Dict:
        """Get per-user statistics"""
        user_stats = {}

        for msg in messages:
            author = msg['author']
            if author not in user_stats:
                user_stats[author] = {
                    'message_count': 0,
                    'word_count': 0,
                    'avg_message_length': 0
                }

            user_stats[author]['message_count'] += 1
            words = len(msg['content'].split())
            user_stats[author]['word_count'] += words

        # Calculate averages
        for author, stats in user_stats.items():
            if stats['message_count'] > 0:
                stats['avg_message_length'] = stats['word_count'] / stats['message_count']

        return user_stats

    def get_topic_clusters(self, messages: List[Dict], min_frequency: int = 3) -> Dict[str, List[str]]:
        """Identify topic clusters based on word co-occurrence"""
        # Get frequent words
        word_freq = dict(self.get_word_frequency(messages, user_only=False, top_n=100))
        frequent_words = {w for w, c in word_freq.items() if c >= min_frequency}

        # Group by common themes (simple keyword matching)
        topics = {
            'technical': ['docker', 'code', 'python', 'bot', 'error', 'fix', 'install',
                         'run', 'command', 'script', 'file', 'api', 'server', 'port'],
            'ai_ml': ['model', 'training', 'neural', 'llm', 'claude', 'mistral', 'phi',
                     'granite', 'token', 'prompt', 'response', 'temperature'],
            'discord': ['channel', 'message', 'user', 'permission', 'role', 'server'],
            'general': []
        }

        # Classify frequent words into topics
        classified = set()
        for topic, keywords in topics.items():
            matched = []
            for word in frequent_words:
                if any(kw in word or word in kw for kw in keywords):
                    matched.append(word)
                    classified.add(word)
            topics[topic] = matched

        # Remaining words go to general
        topics['general'] = list(frequent_words - classified)

        return topics

    def analyze(self) -> Dict:
        """Run full analysis"""
        messages = self.parse_messages()

        if not messages:
            return {'error': 'No messages found'}

        user_messages = [m for m in messages if not m['is_bot']]
        bot_messages = [m for m in messages if m['is_bot']]

        analysis = {
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'bot_messages': len(bot_messages),
            'unique_users': len(set(m['author'] for m in user_messages)),
            'top_words_user': self.get_word_frequency(messages, user_only=True, top_n=30),
            'top_words_overall': self.get_word_frequency(messages, user_only=False, top_n=30),
            'user_stats': self.get_user_stats(messages),
            'topics': self.get_topic_clusters(messages)
        }

        return analysis

    def print_analysis(self, analysis: Dict):
        """Pretty print analysis results"""
        print("=" * 60)
        print("CONVERSATION ANALYSIS REPORT")
        print("=" * 60)

        if 'error' in analysis:
            print(f"❌ {analysis['error']}")
            return

        print(f"\n📊 OVERVIEW")
        print(f"  Total Messages:   {analysis['total_messages']:,}")
        print(f"  User Messages:    {analysis['user_messages']:,}")
        print(f"  Bot Messages:     {analysis['bot_messages']:,}")
        print(f"  Unique Users:     {analysis['unique_users']}")

        print(f"\n🔥 TOP 30 WORDS (USER MESSAGES)")
        for i, (word, count) in enumerate(analysis['top_words_user'][:30], 1):
            bar = '█' * (count // 10) if count >= 10 else '▪'
            print(f"  {i:2}. {word:15} {count:4} {bar}")

        print(f"\n💬 USER STATISTICS (Top 10)")
        sorted_users = sorted(
            analysis['user_stats'].items(),
            key=lambda x: x[1]['message_count'],
            reverse=True
        )[:10]

        for author, stats in sorted_users:
            print(f"  {author:20} {stats['message_count']:4} msgs, "
                  f"avg {stats['avg_message_length']:.1f} words/msg")

        print(f"\n🏷️  TOPIC CLUSTERS")
        for topic, words in analysis['topics'].items():
            if words:
                print(f"  {topic.upper():15} {len(words):2} words: {', '.join(words[:10])}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    log_file = Path(__file__).parent / "conversation_full_log.txt"

    if not log_file.exists():
        print(f"❌ Log file not found: {log_file}")
        exit(1)

    analyzer = ConversationAnalyzer(log_file)
    print("Analyzing conversations...")
    analysis = analyzer.analyze()
    analyzer.print_analysis(analysis)

    # Save to JSON
    output_file = Path(__file__).parent / "conversation_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        # Convert Counter objects to lists for JSON serialization
        json_safe = analysis.copy()
        json_safe['top_words_user'] = list(json_safe['top_words_user'])
        json_safe['top_words_overall'] = list(json_safe['top_words_overall'])
        json.dump(json_safe, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Analysis saved to: {output_file}")
