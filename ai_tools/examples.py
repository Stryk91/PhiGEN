"""
Example scripts showing how to use PhiGEN AI tools
"""

from ollama_client import OllamaClient
from code_reviewer import CodeReviewer
from log_analyzer import LogAnalyzer


def example_basic_generation():
    """Example 1: Basic text generation"""
    print("=" * 60)
    print("Example 1: Basic Text Generation")
    print("=" * 60)

    client = OllamaClient()

    prompt = "Explain Docker containers in 2 sentences"
    response = client.generate(prompt, temperature=0.7)

    print(f"Question: {prompt}")
    print(f"Answer: {response}\n")


def example_code_review():
    """Example 2: Review code"""
    print("=" * 60)
    print("Example 2: Code Review")
    print("=" * 60)

    code = """
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item.price
    return total
"""

    client = OllamaClient()
    system = "You are a code reviewer. Analyze for bugs and improvements."

    response = client.generate(
        f"Review this Python code:\n{code}",
        system=system,
        temperature=0.3
    )

    print(f"Code:\n{code}")
    print(f"Review:\n{response}\n")


def example_chat_conversation():
    """Example 3: Multi-turn conversation"""
    print("=" * 60)
    print("Example 3: Chat Conversation")
    print("=" * 60)

    client = OllamaClient()

    messages = [
        {"role": "user", "content": "What is Python?"},
    ]

    # First response
    response1 = client.chat(messages)
    print(f"User: {messages[0]['content']}")
    print(f"AI: {response1}\n")

    # Continue conversation
    messages.append({"role": "assistant", "content": response1})
    messages.append({"role": "user", "content": "Show me a simple example"})

    response2 = client.chat(messages)
    print(f"User: {messages[2]['content']}")
    print(f"AI: {response2}\n")


def example_code_reviewer_class():
    """Example 4: Using CodeReviewer class"""
    print("=" * 60)
    print("Example 4: CodeReviewer Class")
    print("=" * 60)

    reviewer = CodeReviewer()

    # Review a file (create a test file first)
    test_code = """
# test_example.py
def unsafe_function(user_input):
    # Potential SQL injection
    query = "SELECT * FROM users WHERE id = " + user_input
    return query
"""

    # Write test file
    with open("test_example.py", "w") as f:
        f.write(test_code)

    result = reviewer.review_file("test_example.py")

    if result['status'] == 'success':
        print(f"File: {result['file']}")
        print(f"Review:\n{result['review']}\n")

    # Cleanup
    import os
    os.remove("test_example.py")


def example_log_analyzer():
    """Example 5: Analyze logs"""
    print("=" * 60)
    print("Example 5: Log Analysis")
    print("=" * 60)

    # Create sample log
    sample_log = """
2025-01-07 10:30:45 INFO Starting application
2025-01-07 10:30:46 INFO Database connected
2025-01-07 10:31:00 WARNING Connection timeout, retrying...
2025-01-07 10:31:15 ERROR Failed to connect to external API
2025-01-07 10:31:15 ERROR Exception: Connection refused
2025-01-07 10:31:20 INFO Retry successful
"""

    # Write sample log
    with open("sample.log", "w") as f:
        f.write(sample_log)

    analyzer = LogAnalyzer()
    result = analyzer.analyze_file("sample.log", last_n_lines=20)

    if result['status'] == 'success':
        print(f"File: {result['file']}")
        print(f"Errors found: {result['errors_found']}")
        print(f"Warnings found: {result['warnings_found']}")
        print(f"\nAnalysis:\n{result['analysis']}\n")

    # Cleanup
    import os
    os.remove("sample.log")


def example_docker_log_analysis():
    """Example 6: Analyze Docker container logs"""
    print("=" * 60)
    print("Example 6: Docker Log Analysis")
    print("=" * 60)

    analyzer = LogAnalyzer()

    # Analyze phigen-dev container
    result = analyzer.analyze_docker_logs("phigen-dev", last_n_lines=50)

    if result.get('status') == 'success':
        print(f"Container: {result['container']}")
        print(f"\nAnalysis:\n{result['analysis']}\n")
    else:
        print(f"Status: {result.get('status')}")
        print(f"Note: Container may not be running\n")


def run_all_examples():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("PhiGEN AI Tools - Examples")
    print("=" * 60 + "\n")

    client = OllamaClient()

    if not client.is_available():
        print("❌ Error: Ollama is not available")
        print(f"Make sure Ollama is running at {client.host}")
        print("\nStart it with:")
        print("  docker-compose --profile ai up ollama -d")
        return

    print("✅ Ollama is available\n")

    try:
        example_basic_generation()
        input("Press Enter to continue...")

        example_code_review()
        input("Press Enter to continue...")

        example_chat_conversation()
        input("Press Enter to continue...")

        example_code_reviewer_class()
        input("Press Enter to continue...")

        example_log_analyzer()
        input("Press Enter to continue...")

        example_docker_log_analysis()

        print("=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nExamples interrupted.")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")


if __name__ == "__main__":
    run_all_examples()
