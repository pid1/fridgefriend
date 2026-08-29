# SPDX-FileCopyrightText: 2026 FridgeFriend
# SPDX-License-Identifier: MIT
"""
Sound definitions for FridgeFriend actions.
Each sound is a list of (frequency_hz, duration_seconds) tuples.
"""

# Musical note frequencies (Hz)
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523
D5 = 587
E5 = 659
F5 = 698
G5 = 784
A5 = 880

# Play sound: cheerful ascending chirps
PLAY_SOUND = [
    (C5, 0.1),
    (E5, 0.1),
    (G5, 0.15),
    (A5, 0.2),
]

# Pet sound: soft purring hum
PET_SOUND = [
    (C4, 0.15),
    (E4, 0.15),
    (C4, 0.15),
    (E4, 0.2),
]

# Feed sound: chomping rhythm
FEED_SOUND = [
    (G4, 0.08),
    (0, 0.05),  # silence
    (G4, 0.08),
    (0, 0.05),
    (G4, 0.08),
    (A4, 0.15),
]

# Sleep sound: gentle descending lullaby
SLEEP_SOUND = [
    (G4, 0.2),
    (E4, 0.2),
    (C4, 0.3),
]

# Wake up sound: gentle ascending
WAKE_SOUND = [
    (C4, 0.15),
    (E4, 0.15),
    (G4, 0.2),
]


def play_sound(magtag, sound_sequence):
    """Play a sequence of tones through the MagTag speaker."""
    for freq, duration in sound_sequence:
        if freq > 0:
            magtag.peripherals.play_tone(freq, duration)
        else:
            # Silence - just wait
            import time

            time.sleep(duration)
