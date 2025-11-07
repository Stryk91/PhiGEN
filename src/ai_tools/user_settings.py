"""
User Settings Manager
Per-user configuration for model, temperature, length, tone, profiles
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


# Preset mappings
TEMP_PRESETS = {
    "robot": 1,
    "focused": 25,
    "balanced": 50,
    "creative": 75,
    "wild": 100
}

LENGTH_PRESETS = {
    "brief": 10,
    "normal": 50,
    "detailed": 100
}

TONE_PRESETS = {
    "pro": "professional",
    "casual": "casual",
    "tech": "technical",
    "eli5": "explain_like_im_5",
    "aussie": "australian"
}

MODEL_ALIASES = {
    "p": "phi",
    "ms": "mistral",
    "g": "granite",
    "c": "claude",
    "v": "vision"
}


class UserSettingsManager:
    """Manages per-user settings and profiles"""

    def __init__(self, settings_file: Path):
        self.settings_file = settings_file
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create settings file if it doesn't exist"""
        if not self.settings_file.exists():
            initial_data = {
                "users": {},
                "default_settings": {
                    "model": "phi",
                    "temperature": 50,
                    "length": 50,
                    "tone": "casual",
                    "context_window": 15,
                    "personality": "phigen"
                }
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2)

    def _load_data(self) -> Dict:
        """Load all settings data"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return {"users": {}, "default_settings": {}}

    def _save_data(self, data: Dict):
        """Save all settings data"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving settings: {e}")

    def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        """Get settings for a user (creates default if not exists)"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str not in data["users"]:
            # Create default settings for new user
            data["users"][user_id_str] = {
                "settings": data["default_settings"].copy(),
                "profiles": {}
            }
            self._save_data(data)

        return data["users"][user_id_str]["settings"]

    def update_user_setting(self, user_id: int, key: str, value: Any):
        """Update a single setting for a user"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str not in data["users"]:
            data["users"][user_id_str] = {
                "settings": data["default_settings"].copy(),
                "profiles": {}
            }

        data["users"][user_id_str]["settings"][key] = value
        self._save_data(data)

    def update_user_settings(self, user_id: int, settings: Dict[str, Any]):
        """Update multiple settings for a user"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str not in data["users"]:
            data["users"][user_id_str] = {
                "settings": data["default_settings"].copy(),
                "profiles": {}
            }

        data["users"][user_id_str]["settings"].update(settings)
        self._save_data(data)

    def save_profile(self, user_id: int, profile_name: str):
        """Save current settings as a named profile"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str not in data["users"]:
            return False

        current_settings = data["users"][user_id_str]["settings"].copy()
        data["users"][user_id_str]["profiles"][profile_name] = current_settings
        self._save_data(data)
        return True

    def load_profile(self, user_id: int, profile_name: str) -> Optional[Dict[str, Any]]:
        """Load a named profile"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str not in data["users"]:
            return None

        profiles = data["users"][user_id_str].get("profiles", {})
        if profile_name not in profiles:
            return None

        # Load profile settings
        profile_settings = profiles[profile_name]
        data["users"][user_id_str]["settings"] = profile_settings.copy()
        self._save_data(data)
        return profile_settings

    def list_profiles(self, user_id: int) -> list:
        """List all profiles for a user"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str not in data["users"]:
            return []

        return list(data["users"][user_id_str].get("profiles", {}).keys())

    def delete_profile(self, user_id: int, profile_name: str) -> bool:
        """Delete a named profile"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str not in data["users"]:
            return False

        profiles = data["users"][user_id_str].get("profiles", {})
        if profile_name in profiles:
            del profiles[profile_name]
            self._save_data(data)
            return True

        return False

    def reset_user_settings(self, user_id: int):
        """Reset user to default settings"""
        data = self._load_data()
        user_id_str = str(user_id)

        if user_id_str in data["users"]:
            data["users"][user_id_str]["settings"] = data["default_settings"].copy()
            self._save_data(data)

    @staticmethod
    def resolve_model_alias(model: str) -> str:
        """Resolve model alias to full name"""
        return MODEL_ALIASES.get(model.lower(), model.lower())

    @staticmethod
    def resolve_temp_preset(preset: str) -> Optional[int]:
        """Resolve temperature preset to numeric value"""
        return TEMP_PRESETS.get(preset.lower())

    @staticmethod
    def resolve_length_preset(preset: str) -> Optional[int]:
        """Resolve length preset to numeric value"""
        return LENGTH_PRESETS.get(preset.lower())

    @staticmethod
    def resolve_tone_preset(preset: str) -> Optional[str]:
        """Resolve tone preset"""
        return TONE_PRESETS.get(preset.lower(), preset.lower())

    @staticmethod
    def get_all_presets() -> Dict[str, Dict]:
        """Get all available presets"""
        return {
            "temperature": TEMP_PRESETS,
            "length": LENGTH_PRESETS,
            "tone": TONE_PRESETS,
            "models": MODEL_ALIASES
        }
