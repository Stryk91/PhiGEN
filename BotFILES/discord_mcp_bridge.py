#!/usr/bin/env python3
"""
Discord MCP Bridge
Provides MCP-compatible HTTP endpoints to control the Discord bot
"""

import json
import asyncio
from flask import Flask, request, jsonify
from pathlib import Path
import os
from datetime import datetime, timezone

app = Flask(__name__)

# Configuration
AGENT_FEED_PATH = r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl'
BOTFILES_DIR = r'E:\PythonProjects\PhiGEN\BotFILES'
COMMAND_QUEUE = os.path.join(BOTFILES_DIR, 'mcp_command_queue.jsonl')
RESPONSE_LOG = os.path.join(BOTFILES_DIR, 'mcp_responses.jsonl')

# Ensure directories exist
Path(BOTFILES_DIR).mkdir(parents=True, exist_ok=True)

def log_command(command_data):
    """Log incoming MCP commands"""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command_data
    }
    with open(COMMAND_QUEUE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

def read_agent_feed(limit=10):
    """Read recent entries from agent feed"""
    try:
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')

        entries = []
        for line in lines:
            if line.strip():
                entries.append(json.loads(line))

        return entries[-limit:] if len(entries) > limit else entries
    except Exception as e:
        return {"error": str(e)}

def get_jc_status():
    """Get JC's latest activity"""
    try:
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')

        for line in reversed(lines):
            if line.strip():
                entry = json.loads(line)
                if entry.get('agent') == 'JC':
                    return entry

        return {"status": "no_activity", "message": "No JC entries found"}
    except Exception as e:
        return {"error": str(e)}

def assign_task_to_agent(agent, task, priority="MEDIUM"):
    """Assign a task to an agent via agent feed"""
    try:
        task_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": "MCP",
            "action": "task_assigned",
            "details": {
                "target_agent": agent,
                "task": task,
                "priority": priority.upper(),
                "assigned_via": "MCP"
            }
        }

        with open(AGENT_FEED_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(task_entry) + '\n')

        return {"success": True, "entry": task_entry}
    except Exception as e:
        return {"error": str(e)}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Discord MCP Bridge",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route('/mcp/tools', methods=['GET'])
def list_tools():
    """List available MCP tools"""
    tools = [
        {
            "name": "discord_send_message",
            "description": "Send a message to Discord via the bot",
            "parameters": {
                "message": {"type": "string", "required": True, "description": "Message content"},
                "channel": {"type": "string", "required": False, "description": "Channel name or ID"}
            }
        },
        {
            "name": "discord_check_jc_status",
            "description": "Check JC's latest status from agent feed",
            "parameters": {}
        },
        {
            "name": "discord_read_feed",
            "description": "Read recent agent feed entries",
            "parameters": {
                "limit": {"type": "integer", "required": False, "default": 10, "description": "Number of entries"}
            }
        },
        {
            "name": "discord_assign_task",
            "description": "Assign a task to an agent",
            "parameters": {
                "agent": {"type": "string", "required": True, "description": "Target agent (JC, DC, etc.)"},
                "task": {"type": "string", "required": True, "description": "Task description"},
                "priority": {"type": "string", "required": False, "default": "MEDIUM", "description": "Priority level"}
            }
        },
        {
            "name": "discord_list_botfiles",
            "description": "List files in BotFILES directory",
            "parameters": {}
        },
        {
            "name": "discord_read_botfile",
            "description": "Read a file from BotFILES directory",
            "parameters": {
                "filename": {"type": "string", "required": True, "description": "File to read"}
            }
        }
    ]
    return jsonify({"tools": tools})

@app.route('/mcp/execute', methods=['POST'])
def execute_tool():
    """Execute an MCP tool"""
    data = request.get_json()
    tool_name = data.get('tool')
    params = data.get('parameters', {})

    # Log the command
    log_command({"tool": tool_name, "params": params})

    # Route to appropriate handler
    if tool_name == "discord_send_message":
        message = params.get('message')
        channel = params.get('channel', 'default')

        # Queue the message for the bot to send
        command = {
            "type": "send_message",
            "message": message,
            "channel": channel,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        with open(COMMAND_QUEUE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(command) + '\n')

        return jsonify({
            "success": True,
            "result": f"Message queued for Discord: {message[:50]}..."
        })

    elif tool_name == "discord_check_jc_status":
        status = get_jc_status()
        return jsonify({"success": True, "result": status})

    elif tool_name == "discord_read_feed":
        limit = params.get('limit', 10)
        entries = read_agent_feed(limit)
        return jsonify({"success": True, "result": entries})

    elif tool_name == "discord_assign_task":
        agent = params.get('agent')
        task = params.get('task')
        priority = params.get('priority', 'MEDIUM')

        result = assign_task_to_agent(agent, task, priority)
        return jsonify({"success": True, "result": result})

    elif tool_name == "discord_list_botfiles":
        try:
            items = os.listdir(BOTFILES_DIR)
            files = []
            for item in items:
                item_path = os.path.join(BOTFILES_DIR, item)
                files.append({
                    "name": item,
                    "type": "directory" if os.path.isdir(item_path) else "file",
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None
                })
            return jsonify({"success": True, "result": files})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    elif tool_name == "discord_read_botfile":
        filename = params.get('filename')
        try:
            filepath = os.path.join(BOTFILES_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({"success": True, "result": content})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    else:
        return jsonify({
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }), 400

@app.route('/mcp/status', methods=['GET'])
def get_status():
    """Get MCP bridge status"""
    try:
        # Check if command queue exists
        queue_size = 0
        if os.path.exists(COMMAND_QUEUE):
            with open(COMMAND_QUEUE, 'r') as f:
                queue_size = len(f.readlines())

        # Check if agent feed exists
        feed_entries = 0
        if os.path.exists(AGENT_FEED_PATH):
            with open(AGENT_FEED_PATH, 'r') as f:
                feed_entries = len(f.readlines())

        return jsonify({
            "status": "running",
            "queue_size": queue_size,
            "feed_entries": feed_entries,
            "botfiles_dir": BOTFILES_DIR,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Discord MCP Bridge...")
    print(f"📁 BotFILES Directory: {BOTFILES_DIR}")
    print(f"📋 Agent Feed: {AGENT_FEED_PATH}")
    print(f"📡 Starting server on http://localhost:5000")

    app.run(host='0.0.0.0', port=5000, debug=True)
