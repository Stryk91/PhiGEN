"""
REST API Wrapper for Local AI Models
Provides HTTP endpoints for AI functionality
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Add ai_tools to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from ollama_client import OllamaClient
from code_reviewer import CodeReviewer
from log_analyzer import LogAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for browser access

# Initialize clients
client = OllamaClient(model=os.getenv("AI_MODEL", "granite-code:3b"))
code_reviewer = CodeReviewer()
log_analyzer = LogAnalyzer()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "ai_available": client.is_available(),
        "model": client.model
    })


@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Generate text from prompt

    Body:
        {
            "prompt": "Your question",
            "system": "Optional system message",
            "temperature": 0.7,
            "max_tokens": 500
        }
    """
    try:
        data = request.json
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({"error": "prompt is required"}), 400

        response = client.generate(
            prompt=prompt,
            system=data.get('system'),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens')
        )

        return jsonify({
            "response": response,
            "model": client.model
        })

    except Exception as e:
        logger.error(f"Error in generate: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat with conversation history

    Body:
        {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi!"}
            ]
        }
    """
    try:
        data = request.json
        messages = data.get('messages', [])

        if not messages:
            return jsonify({"error": "messages are required"}), 400

        response = client.chat(messages)

        return jsonify({
            "message": {
                "role": "assistant",
                "content": response
            },
            "model": client.model
        })

    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/review/code', methods=['POST'])
def review_code():
    """
    Review code snippet

    Body:
        {
            "code": "def my_func():\n    return x",
            "language": "python"
        }
    """
    try:
        data = request.json
        code = data.get('code')

        if not code:
            return jsonify({"error": "code is required"}), 400

        system = """You are a code reviewer. Analyze for bugs, security, and best practices."""
        response = client.generate(
            prompt=f"Review this code:\n\n```\n{code}\n```",
            system=system,
            temperature=0.3
        )

        return jsonify({
            "review": response,
            "model": client.model
        })

    except Exception as e:
        logger.error(f"Error in code review: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/review/file', methods=['POST'])
def review_file():
    """
    Review a file

    Body:
        {
            "filepath": "path/to/file.py"
        }
    """
    try:
        data = request.json
        filepath = data.get('filepath')

        if not filepath:
            return jsonify({"error": "filepath is required"}), 400

        result = code_reviewer.review_file(filepath)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in file review: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze/logs', methods=['POST'])
def analyze_logs():
    """
    Analyze log file

    Body:
        {
            "filepath": "path/to/logfile.log",
            "lines": 500
        }
    """
    try:
        data = request.json
        filepath = data.get('filepath')
        lines = data.get('lines', 500)

        if not filepath:
            return jsonify({"error": "filepath is required"}), 400

        result = log_analyzer.analyze_file(filepath, lines)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in log analysis: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze/docker', methods=['POST'])
def analyze_docker():
    """
    Analyze Docker container logs

    Body:
        {
            "container": "container_name",
            "lines": 200
        }
    """
    try:
        data = request.json
        container = data.get('container')
        lines = data.get('lines', 200)

        if not container:
            return jsonify({"error": "container is required"}), 400

        result = log_analyzer.analyze_docker_logs(container, lines)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in Docker log analysis: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/models', methods=['GET'])
def list_models():
    """List available models"""
    try:
        models = client.list_models()
        return jsonify({
            "models": models,
            "current": client.model
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/explain', methods=['POST'])
def explain():
    """
    Explain a technical concept

    Body:
        {
            "concept": "What is Docker?"
        }
    """
    try:
        data = request.json
        concept = data.get('concept')

        if not concept:
            return jsonify({"error": "concept is required"}), 400

        system = "Explain technical concepts clearly with examples."
        response = client.generate(
            prompt=f"Explain: {concept}",
            system=system,
            temperature=0.6
        )

        return jsonify({
            "explanation": response,
            "model": client.model
        })

    except Exception as e:
        logger.error(f"Error in explain: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        "name": "PhiGEN AI API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/api/generate": "Generate text (POST)",
            "/api/chat": "Chat with history (POST)",
            "/api/review/code": "Review code snippet (POST)",
            "/api/review/file": "Review file (POST)",
            "/api/analyze/logs": "Analyze logs (POST)",
            "/api/analyze/docker": "Analyze Docker logs (POST)",
            "/api/models": "List models (GET)",
            "/api/explain": "Explain concept (POST)"
        },
        "model": client.model,
        "ai_available": client.is_available()
    })


def main():
    """Run the API server"""
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")

    logger.info(f"Starting AI API server on {host}:{port}")
    logger.info(f"Using model: {client.model}")

    if not client.is_available():
        logger.warning(f"Ollama not available at {client.host}")

    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
