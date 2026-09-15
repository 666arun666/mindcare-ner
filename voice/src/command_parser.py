"""
MINDCARE NER — Voice Command & Intent Parser
SIH26003: Cognitive Support Platform

Enforces an allowlisted command pattern.
Unrestricted or arbitrary speech is NEVER executed directly against system services.
"""

from dataclasses import dataclass
from enum import Enum


class VoiceIntent(str, Enum):
    START_GAME = "START_GAME"
    SET_WATER_REMINDER = "SET_WATER_REMINDER"
    QUERY_NEXT_ACTIVITY = "QUERY_NEXT_ACTIVITY"
    CONFIRM_ACTION = "CONFIRM_ACTION"
    CANCEL_ACTION = "CANCEL_ACTION"
    UNKNOWN = "UNKNOWN"


@dataclass
class ParsedVoiceCommand:
    raw_transcript: str
    intent: VoiceIntent
    requires_confirmation: bool
    action_payload: dict | None
    response_prompt: str


# Strict allowlist of supported phrases (normalized lowercase)
ALLOWLIST_MAP = {
    "start memory game": VoiceIntent.START_GAME,
    "open today's game": VoiceIntent.START_GAME,
    "open todays game": VoiceIntent.START_GAME,
    "play memory game": VoiceIntent.START_GAME,
    "remind me to drink water": VoiceIntent.SET_WATER_REMINDER,
    "what is my next activity": VoiceIntent.QUERY_NEXT_ACTIVITY,
    "what is my next activity?": VoiceIntent.QUERY_NEXT_ACTIVITY,
    "yes": VoiceIntent.CONFIRM_ACTION,
    "confirm": VoiceIntent.CONFIRM_ACTION,
    "no": VoiceIntent.CANCEL_ACTION,
    "cancel": VoiceIntent.CANCEL_ACTION,
}


class VoiceCommandParser:
    """
    Parses and sanitizes speech transcripts against allowlisted voice intents.
    """

    def parse(self, transcript: str) -> ParsedVoiceCommand:
        """
        Parse raw speech transcript into a validated intent.
        """
        if not transcript or not transcript.strip():
            return ParsedVoiceCommand(
                raw_transcript="",
                intent=VoiceIntent.UNKNOWN,
                requires_confirmation=False,
                action_payload=None,
                response_prompt="I could not hear you clearly. Please try speaking again.",
            )

        cleaned = transcript.strip().lower()

        # Check direct allowlist match
        intent = ALLOWLIST_MAP.get(cleaned, VoiceIntent.UNKNOWN)

        # Fuzzy phrase checks for variations of allowlisted commands
        if intent == VoiceIntent.UNKNOWN:
            if "drink water" in cleaned or "water reminder" in cleaned:
                intent = VoiceIntent.SET_WATER_REMINDER
            elif "start" in cleaned and "game" in cleaned:
                intent = VoiceIntent.START_GAME
            elif "next activity" in cleaned:
                intent = VoiceIntent.QUERY_NEXT_ACTIVITY

        # Construct intent response
        if intent == VoiceIntent.START_GAME:
            return ParsedVoiceCommand(
                raw_transcript=transcript,
                intent=intent,
                requires_confirmation=False,
                action_payload={"game_type": "memory_match"},
                response_prompt="Opening today's memory game. Get ready!",
            )
        elif intent == VoiceIntent.SET_WATER_REMINDER:
            # Water reminder changes state, requires confirmation
            return ParsedVoiceCommand(
                raw_transcript=transcript,
                intent=intent,
                requires_confirmation=True,
                action_payload={"reminder_type": "water", "interval_minutes": 60},
                response_prompt="Would you like me to set a reminder to drink water every hour?",
            )
        elif intent == VoiceIntent.QUERY_NEXT_ACTIVITY:
            return ParsedVoiceCommand(
                raw_transcript=transcript,
                intent=intent,
                requires_confirmation=False,
                action_payload=None,
                response_prompt="Checking your daily schedule. Your next activity is afternoon rest at 2 PM.",
            )
        elif intent == VoiceIntent.CONFIRM_ACTION:
            return ParsedVoiceCommand(
                raw_transcript=transcript,
                intent=intent,
                requires_confirmation=False,
                action_payload=None,
                response_prompt="Confirmed. Updating your reminders.",
            )
        elif intent == VoiceIntent.CANCEL_ACTION:
            return ParsedVoiceCommand(
                raw_transcript=transcript,
                intent=intent,
                requires_confirmation=False,
                action_payload=None,
                response_prompt="Action cancelled.",
            )
        else:
            return ParsedVoiceCommand(
                raw_transcript=transcript,
                intent=VoiceIntent.UNKNOWN,
                requires_confirmation=False,
                action_payload=None,
                response_prompt=(
                    "I can only help with specific activities like starting your game, "
                    "setting a water reminder, or checking your next activity."
                ),
            )
