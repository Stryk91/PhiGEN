#!/usr/bin/env python3
"""
Interactive Knowledge Graph Explorer
Navigate conversation chains from the historical Discord data
"""

import json
import sys
from pathlib import Path
from typing import List, Optional


class GraphExplorer:
    def __init__(self, graph_file: Path):
        print(f"Loading knowledge graph from {graph_file}...")
        with open(graph_file, encoding='utf-8') as f:
            self.graph = json.load(f)
        print(f"✅ Loaded {len(self.graph):,} unique messages\n")

    def get_responses(self, message: str) -> List[str]:
        """Get all recorded responses to a message"""
        return self.graph.get(message, [])

    def trace_chain(self, start: str, length: int = 10) -> List[str]:
        """Trace a conversation chain"""
        chain = [start]
        current = start

        for _ in range(length - 1):
            responses = self.get_responses(current)
            if not responses:
                break
            current = responses[0]  # Take first response
            chain.append(current)

        return chain

    def find_message(self, keyword: str, limit: int = 20) -> List[str]:
        """Find messages containing keyword"""
        matches = [msg for msg in self.graph.keys() if keyword.lower() in msg.lower()]
        return matches[:limit]

    def get_stats(self, message: str) -> dict:
        """Get statistics for a message"""
        responses = self.get_responses(message)
        return {
            'message': message,
            'response_count': len(responses),
            'has_continuation': any(r in self.graph for r in responses)
        }

    def interactive(self):
        """Interactive explorer mode"""
        print("=" * 60)
        print("KNOWLEDGE GRAPH INTERACTIVE EXPLORER")
        print("=" * 60)
        print("\nCommands:")
        print("  search <keyword>     - Find messages containing keyword")
        print("  trace <message>      - Trace conversation chain")
        print("  responses <message>  - Show all responses to a message")
        print("  stats <message>      - Show message statistics")
        print("  quit / exit          - Exit explorer")
        print()

        while True:
            try:
                cmd = input("\n> ").strip()

                if not cmd:
                    continue

                if cmd.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                parts = cmd.split(' ', 1)
                action = parts[0].lower()

                if action == 'search':
                    if len(parts) < 2:
                        print("Usage: search <keyword>")
                        continue

                    keyword = parts[1]
                    matches = self.find_message(keyword)
                    print(f"\nFound {len(matches)} messages containing '{keyword}':")
                    for i, msg in enumerate(matches, 1):
                        truncated = msg[:70] + "..." if len(msg) > 70 else msg
                        print(f"  {i}. {truncated}")

                elif action == 'trace':
                    if len(parts) < 2:
                        print("Usage: trace <message>")
                        continue

                    message = parts[1]
                    if message not in self.graph:
                        print(f"Message not found: '{message}'")
                        continue

                    chain = self.trace_chain(message, 10)
                    print(f"\nConversation chain from '{message[:50]}...':")
                    for i, msg in enumerate(chain, 1):
                        truncated = msg[:70] + "..." if len(msg) > 70 else msg
                        print(f"  {i}. {truncated}")

                elif action == 'responses':
                    if len(parts) < 2:
                        print("Usage: responses <message>")
                        continue

                    message = parts[1]
                    responses = self.get_responses(message)

                    if not responses:
                        print(f"No responses found for: '{message}'")
                        continue

                    print(f"\n{len(responses)} responses to '{message[:50]}...':")
                    for i, resp in enumerate(responses[:20], 1):
                        truncated = resp[:70] + "..." if len(resp) > 70 else resp
                        print(f"  {i}. {truncated}")

                    if len(responses) > 20:
                        print(f"  ... and {len(responses) - 20} more")

                elif action == 'stats':
                    if len(parts) < 2:
                        print("Usage: stats <message>")
                        continue

                    message = parts[1]
                    stats = self.get_stats(message)
                    print(f"\nStatistics for: '{message[:50]}...'")
                    print(f"  Recorded responses: {stats['response_count']}")
                    print(f"  Has continuations: {stats['has_continuation']}")

                else:
                    print(f"Unknown command: {action}")
                    print("Type 'quit' to exit or try: search, trace, responses, stats")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    graph_file = Path(__file__).parent / "historical_data" / "knowledge_base_from_discord.json"

    if not graph_file.exists():
        print(f"❌ Graph file not found: {graph_file}")
        sys.exit(1)

    explorer = GraphExplorer(graph_file)

    # Command line mode
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'search' and len(sys.argv) > 2:
            keyword = ' '.join(sys.argv[2:])
            matches = explorer.find_message(keyword, 30)
            print(f"Found {len(matches)} messages:")
            for i, msg in enumerate(matches, 1):
                print(f"{i}. {msg[:100]}")

        elif command == 'trace' and len(sys.argv) > 2:
            message = ' '.join(sys.argv[2:])
            chain = explorer.trace_chain(message, 15)
            for i, msg in enumerate(chain, 1):
                print(f"{i}. {msg}")

        else:
            print("Usage:")
            print("  python explore_graph.py search <keyword>")
            print("  python explore_graph.py trace <message>")
            print("  python explore_graph.py   (interactive mode)")
    else:
        # Interactive mode
        explorer.interactive()


if __name__ == "__main__":
    main()
