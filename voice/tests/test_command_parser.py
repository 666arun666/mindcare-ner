from voice.src.command_parser import VoiceCommandParser, VoiceIntent


def test_parse_start_memory_game():
    parser = VoiceCommandParser()
    cmd = parser.parse("Start memory game")
    assert cmd.intent == VoiceIntent.START_GAME
    assert not cmd.requires_confirmation
    assert cmd.action_payload == {"game_type": "memory_match"}


def test_parse_open_todays_game():
    parser = VoiceCommandParser()
    cmd = parser.parse("Open today's game")
    assert cmd.intent == VoiceIntent.START_GAME
    assert not cmd.requires_confirmation


def test_parse_water_reminder_requires_confirmation():
    parser = VoiceCommandParser()
    cmd = parser.parse("Remind me to drink water")
    assert cmd.intent == VoiceIntent.SET_WATER_REMINDER
    assert cmd.requires_confirmation
    assert cmd.action_payload["reminder_type"] == "water"


def test_parse_query_next_activity():
    parser = VoiceCommandParser()
    cmd = parser.parse("What is my next activity?")
    assert cmd.intent == VoiceIntent.QUERY_NEXT_ACTIVITY
    assert not cmd.requires_confirmation


def test_confirmation_and_cancellation():
    parser = VoiceCommandParser()
    yes_cmd = parser.parse("confirm")
    assert yes_cmd.intent == VoiceIntent.CONFIRM_ACTION

    no_cmd = parser.parse("cancel")
    assert no_cmd.intent == VoiceIntent.CANCEL_ACTION


def test_unsupported_or_invalid_commands():
    parser = VoiceCommandParser()
    # Unallowlisted command
    unknown_cmd = parser.parse("Delete all patient records from the database")
    assert unknown_cmd.intent == VoiceIntent.UNKNOWN
    assert unknown_cmd.action_payload is None
    assert "only help with specific activities" in unknown_cmd.response_prompt


def test_empty_or_whitespace_transcript():
    parser = VoiceCommandParser()
    empty_cmd = parser.parse("   ")
    assert empty_cmd.intent == VoiceIntent.UNKNOWN
    assert "could not hear you" in empty_cmd.response_prompt
