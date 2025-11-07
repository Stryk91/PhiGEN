#!/usr/bin/env python3
"""
JC Discord System Launcher
Starts both the file watcher and Discord bot together
"""

import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def start_watcher():
    """Start the file watcher"""
    print("🔍 Starting Agent Feed Watcher...")
    watcher_script = SCRIPT_DIR / "jc_feed_watcher.py"
    return subprocess.Popen([sys.executable, str(watcher_script)])

def start_bot():
    """Start the Discord bot"""
    print("🤖 Starting JC Discord Bot...")
    bot_script = SCRIPT_DIR / "jc_discord_bot.py"
    return subprocess.Popen([sys.executable, str(bot_script)])

def main():
    print("="*60)
    print("🚀 JC Discord System Launcher")
    print("="*60)
    print()
    print("Starting all JC Discord components...")
    print()
    
    processes = []
    
    try:
        # Start watcher
        watcher_process = start_watcher()
        processes.append(("File Watcher", watcher_process))
        time.sleep(2)
        
        # Start bot
        bot_process = start_bot()
        processes.append(("Discord Bot", bot_process))
        time.sleep(2)
        
        print()
        print("="*60)
        print("✅ All JC Discord components running!")
        print("="*60)
        print()
        print("Active processes:")
        for name, proc in processes:
            print(f"  • {name}: PID {proc.pid}")
        print()
        print("Press Ctrl+C to stop all processes")
        print("="*60)
        print()
        
        # Wait for processes
        while True:
            time.sleep(1)
            
            # Check if any process died
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"⚠️ {name} stopped unexpectedly!")
    
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down JC Discord System...")
        
        # Terminate all processes
        for name, proc in processes:
            print(f"  Stopping {name}...")
            proc.terminate()
            proc.wait()
        
        print("✅ All processes stopped")

if __name__ == '__main__':
    main()
