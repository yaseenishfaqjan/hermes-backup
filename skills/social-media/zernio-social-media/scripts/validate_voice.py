#!/usr/bin/env python3
"""
Voice ID Validation Script
Ensures correct voice IDs are used for each channel
"""

import sys

# Official voice registry - NEVER change without explicit user confirmation
VOICE_REGISTRY = {
    "global-signal": {
        "voice_id": "auq43ws1oslv0tO4BDa7",
        "voice_name": "Brian",
        "provider": "elevenlabs",
        "description": "Professional, authoritative, calm"
    }
}

def validate_voice_id(channel: str, voice_id: str) -> bool:
    """
    Validate voice ID matches channel requirements
    
    Args:
        channel: Channel name (e.g., 'global-signal')
        voice_id: Voice ID to validate
        
    Returns:
        True if valid, raises AssertionError if invalid
    """
    if channel not in VOICE_REGISTRY:
        print(f"⚠️ Warning: No voice registry entry for channel '{channel}'")
        return True
    
    expected = VOICE_REGISTRY[channel]["voice_id"]
    
    assert voice_id == expected, f"""
    CRITICAL VOICE MISMATCH!
    
    Channel: {channel}
    Expected: {expected} ({VOICE_REGISTRY[channel]['voice_name']})
    Received: {voice_id}
    
    This voice ID is locked for {channel}. 
    Never substitute voices without explicit user approval.
    """
    
    print(f"✅ Voice validated: {channel} uses {VOICE_REGISTRY[channel]['voice_name']} ({voice_id})")
    return True

def get_voice_id(channel: str) -> str:
    """Get official voice ID for a channel"""
    if channel not in VOICE_REGISTRY:
        raise ValueError(f"No voice registered for channel '{channel}'")
    return VOICE_REGISTRY[channel]["voice_id"]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_voice.py <channel> <voice_id>")
        print("\nRegistered channels:")
        for ch, info in VOICE_REGISTRY.items():
            print(f"  {ch}: {info['voice_name']} ({info['voice_id']})")
        sys.exit(1)
    
    channel = sys.argv[1]
    voice_id = sys.argv[2]
    
    try:
        validate_voice_id(channel, voice_id)
    except AssertionError as e:
        print(e)
        sys.exit(1)
