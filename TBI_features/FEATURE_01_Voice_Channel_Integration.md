# Feature #1: Voice Channel Integration

**Status:** TBI (To Be Implemented)
**Priority:** Medium
**Complexity:** High
**Estimated Time:** 2-3 days

---

## Overview

Enable bot to join Discord voice channels, speak responses (TTS), and listen to commands (STT).

**Commands:**
```
!join-voice           # Bot joins voice channel
!leave-voice          # Bot leaves voice channel
!tts on/off           # Text-to-speech responses
!stt on/off           # Speech-to-text (listen mode)
!voice-model <name>   # Set voice personality
!ask-voice            # Push-to-talk voice question
```

---

## Implementation Details

### Tech Stack

- `discord.py[voice]` - Voice channel support
- `pyttsx3` - Text-to-speech (offline, free)
- `speech_recognition` - Speech-to-text
- `pyaudio` - Audio capture
- `ffmpeg` - Audio processing

### Architecture

```
Discord Voice Channel
        ↓
Voice Connection Manager
        ↓
   ┌────┴────┐
   ↓         ↓
STT Engine  TTS Engine
   ↓         ↓
AI Model ← → Response
```

---

## Core Components

### 1. Voice Manager (`voice_manager.py`)

```python
import discord
import asyncio
import pyttsx3
import speech_recognition as sr
from collections import deque

class VoiceManager:
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}  # guild_id: voice_client
        self.tts_enabled = {}    # guild_id: bool
        self.stt_enabled = {}    # guild_id: bool
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.audio_queue = deque()

    async def join_voice(self, ctx):
        """Join user's voice channel"""
        if not ctx.author.voice:
            await ctx.send("You're not in a voice channel!")
            return False

        channel = ctx.author.voice.channel

        # Already connected
        if ctx.guild.id in self.voice_clients:
            await ctx.send(f"Already in {channel.name}")
            return True

        # Connect
        voice_client = await channel.connect()
        self.voice_clients[ctx.guild.id] = voice_client

        # Default: TTS on, STT off
        self.tts_enabled[ctx.guild.id] = True
        self.stt_enabled[ctx.guild.id] = False

        await ctx.send(f"✅ Joined {channel.name} | TTS: ON | STT: OFF")
        return True

    async def leave_voice(self, ctx):
        """Leave voice channel"""
        if ctx.guild.id not in self.voice_clients:
            await ctx.send("Not in a voice channel!")
            return

        await self.voice_clients[ctx.guild.id].disconnect()
        del self.voice_clients[ctx.guild.id]

        await ctx.send("✅ Left voice channel")

    async def speak(self, guild_id: int, text: str):
        """Convert text to speech and play in voice channel"""
        if guild_id not in self.voice_clients:
            return

        if not self.tts_enabled.get(guild_id, False):
            return

        # Generate TTS audio
        audio_file = f"temp_tts_{guild_id}.mp3"
        self.tts_engine.save_to_file(text, audio_file)
        self.tts_engine.runAndWait()

        # Play in voice channel
        voice_client = self.voice_clients[guild_id]
        voice_client.play(discord.FFmpegPCMAudio(audio_file))

        # Cleanup after playing
        while voice_client.is_playing():
            await asyncio.sleep(0.1)

        import os
        os.remove(audio_file)

    async def listen(self, guild_id: int) -> str:
        """Listen for speech and convert to text"""
        if guild_id not in self.voice_clients:
            return None

        if not self.stt_enabled.get(guild_id, False):
            return None

        voice_client = self.voice_clients[guild_id]

        # Record audio from voice channel
        # (Complex: requires voice receiving, which discord.py doesn't fully support)
        # Alternative: Use push-to-talk command instead

        # For now, return None (STT from Discord voice is limited)
        return None
```

### 2. Voice Commands (`bot.py` integration)

```python
voice_manager = VoiceManager(bot)

@bot.command(name='join-voice')
async def join_voice(ctx):
    """Join your voice channel"""
    await voice_manager.join_voice(ctx)

@bot.command(name='leave-voice')
async def leave_voice(ctx):
    """Leave voice channel"""
    await voice_manager.leave_voice(ctx)

@bot.command(name='tts')
async def toggle_tts(ctx, state: str = None):
    """Toggle text-to-speech: !tts on/off"""
    guild_id = ctx.guild.id

    if state == 'on':
        voice_manager.tts_enabled[guild_id] = True
        await ctx.send("🔊 TTS enabled")
    elif state == 'off':
        voice_manager.tts_enabled[guild_id] = False
        await ctx.send("🔇 TTS disabled")
    else:
        current = voice_manager.tts_enabled.get(guild_id, False)
        status = "ON" if current else "OFF"
        await ctx.send(f"🔊 TTS is currently {status}")

@bot.command(name='stt')
async def toggle_stt(ctx, state: str = None):
    """Toggle speech-to-text: !stt on/off"""
    guild_id = ctx.guild.id

    if state == 'on':
        voice_manager.stt_enabled[guild_id] = True
        await ctx.send("🎤 STT enabled (experimental)")
    elif state == 'off':
        voice_manager.stt_enabled[guild_id] = False
        await ctx.send("🎤 STT disabled")
    else:
        current = voice_manager.stt_enabled.get(guild_id, False)
        status = "ON" if current else "OFF"
        await ctx.send(f"🎤 STT is currently {status}")

@bot.command(name='voice-model')
async def set_voice_model(ctx, voice_name: str = None):
    """Set TTS voice: !voice-model <name>"""
    if not voice_name:
        # List available voices
        voices = voice_manager.tts_engine.getProperty('voices')
        voice_list = "\n".join([f"- {v.name}" for v in voices[:5]])
        await ctx.send(f"**Available voices:**\n{voice_list}")
        return

    # Set voice
    voices = voice_manager.tts_engine.getProperty('voices')
    for voice in voices:
        if voice_name.lower() in voice.name.lower():
            voice_manager.tts_engine.setProperty('voice', voice.id)
            await ctx.send(f"✅ Voice set to: {voice.name}")
            return

    await ctx.send(f"❌ Voice '{voice_name}' not found")

# Auto-speak AI responses when in voice
@bot.event
async def on_message(message):
    # Process commands first
    await bot.process_commands(message)

    # If bot responds in text channel and is in voice, speak it
    if message.author == bot.user and message.guild:
        guild_id = message.guild.id
        if guild_id in voice_manager.voice_clients:
            # Speak response (async)
            asyncio.create_task(voice_manager.speak(guild_id, message.content))
```

### 3. Advanced: Push-to-Talk STT (`ptt_stt.py`)

```python
# Since Discord voice receiving is limited, use push-to-talk approach

@bot.command(name='ask-voice')
async def ask_voice(ctx):
    """Hold to record voice question, AI responds in voice"""
    guild_id = ctx.guild.id

    if guild_id not in voice_manager.voice_clients:
        await ctx.send("❌ Bot not in voice channel! Use !join-voice first")
        return

    # Notify user to start speaking
    await ctx.send("🎤 Recording for 10 seconds... Speak now!")

    # Record from user's microphone (requires voice receiving)
    # Alternative: User uploads audio file
    await ctx.send("📎 Or attach audio file for transcription")

    # Wait for audio file attachment
    def check(m):
        return (m.author == ctx.author and
                m.channel == ctx.channel and
                len(m.attachments) > 0)

    try:
        msg = await bot.wait_for('message', check=check, timeout=60.0)
        audio_attachment = msg.attachments[0]

        # Download audio
        audio_file = f"temp_audio_{ctx.author.id}.wav"
        await audio_attachment.save(audio_file)

        # Transcribe
        with sr.AudioFile(audio_file) as source:
            audio = voice_manager.recognizer.record(source)
            text = voice_manager.recognizer.recognize_google(audio)

        await ctx.send(f"📝 Transcribed: `{text}`")

        # Query AI
        response = await router.query(text, {"model": "mistral", "provider": "ollama"})

        # Respond in voice
        await voice_manager.speak(guild_id, response.content)

        # Also send text
        await ctx.send(f"💬 {response.content}")

        # Cleanup
        import os
        os.remove(audio_file)

    except asyncio.TimeoutError:
        await ctx.send("❌ Timeout - no audio received")
```

---

## Dependencies

**requirements.txt additions:**
```
discord.py[voice]>=2.3.0
pyttsx3>=2.90
SpeechRecognition>=3.10.0
PyAudio>=0.2.13
ffmpeg-python>=0.2.0
```

**System dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg portaudio19-dev

# Windows
# Download FFmpeg: https://ffmpeg.org/download.html
# Add to PATH

# Install Python packages
pip install discord.py[voice] pyttsx3 SpeechRecognition PyAudio
```

---

## Usage Example

```
User: !join-voice
Bot: ✅ Joined General | TTS: ON | STT: OFF

User: !ai what's the weather today?
Bot: (text) "I don't have real-time weather data..."
Bot: (speaks in voice) "I don't have real-time weather data..."

User: !tts off
Bot: 🔇 TTS disabled

User: !ai hello
Bot: (text only) "Hello! How can I help?"

User: !voice-model
Bot: **Available voices:**
     - Microsoft David Desktop
     - Microsoft Zira Desktop
     - Microsoft Mark

User: !voice-model zira
Bot: ✅ Voice set to: Microsoft Zira Desktop

User: !ask-voice
Bot: 🎤 Recording for 10 seconds... Speak now!
User: (uploads audio file)
Bot: 📝 Transcribed: `how do I fix this bug`
Bot: 💬 Let me analyze that for you...
Bot: (speaks response in voice)
```

---

## Limitations & Workarounds

### Limitations

1. **Discord voice receiving** - Discord.py has limited support for receiving voice
2. **STT quality** - Google Speech Recognition requires internet
3. **Latency** - TTS generation adds 1-2s delay
4. **Audio quality** - TTS sounds robotic (can upgrade to ElevenLabs API)

### Workarounds

1. Use push-to-talk via audio file upload
2. Use premium TTS service (ElevenLabs, Azure TTS)
3. Implement voice receiving with `discord-ext-voice-recv` library

---

## Pros & Cons

### Pros
- Hands-free bot interaction
- Multi-tasking (code while talking to bot)
- Accessibility for typing-impaired users
- Natural conversation flow

### Cons
- Complex audio setup
- Latency issues
- Limited Discord voice receiving support
- Requires system audio dependencies

---

## Future Enhancements

- **Premium TTS** - ElevenLabs for natural voices
- **Real-time STT** - Continuous voice recognition
- **Voice commands** - "Hey PhiGEN, analyze this code"
- **Multi-language** - Support multiple languages
- **Voice effects** - Filters, pitch adjustment

---

**Created:** 2025-11-08
**Status:** Awaiting approval
