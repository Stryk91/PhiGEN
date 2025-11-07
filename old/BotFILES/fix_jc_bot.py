import pathlib
content = pathlib.Path('jc_discord_bot.py').read_text()
content = content.replace("command_prefix='<@&1435809409543569510> '", "command_prefix=commands.when_mentioned")
pathlib.Path('jc_discord_bot.py').write_text(content)
print('✅ Fixed! Bot will respond to @mentions now')