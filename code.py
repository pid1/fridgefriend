"""
FridgeFriend - A virtual pet for your fridge!
Tamagotchi-style companion for the Adafruit MagTag e-ink display.
"""

import time
import alarm
import board
import rtc
import socketpool
import wifi
import adafruit_ntp
from adafruit_magtag.magtag import MagTag

from dino import DinoSprite, is_night_time, ACTION_PLAY, ACTION_PET, ACTION_FEED, ACTION_SLEEP
from sounds import (
    play_sound,
    PLAY_SOUND,
    PET_SOUND,
    FEED_SOUND,
    SLEEP_SOUND,
)

# Button to action mapping
# MagTag buttons: A=D15, B=D14, C=D12, D=D11
# buttons[0]=A, buttons[1]=B, buttons[2]=C, buttons[3]=D
BUTTON_ACTIONS = {
    0: (ACTION_PLAY, PLAY_SOUND),   # D15 - Play
    1: (ACTION_PET, PET_SOUND),     # D14 - Pet
    2: (ACTION_FEED, FEED_SOUND),   # D12 - Feed
    3: (ACTION_SLEEP, SLEEP_SOUND), # D11 - Sleep
}

# Timing constants
ACTION_DISPLAY_DURATION = 5. # Seconds to show action sprite before sleep

def safe_refresh(display):
    """Safely refresh the e-ink display, waiting if necessary."""
    # Wait for display to be ready
    while display.time_to_refresh > 0:
        time.sleep(0.1)
    display.refresh()
    # Wait for refresh to complete
    while display.busy:
        time.sleep(0.1)

def sync_time(magtag):
    """Sync time from NTP via WiFi. Requires secrets.py with WiFi credentials."""
    try:
        print("Connecting to WiFi...")
        magtag.network.connect()

        print("Syncing time from NTP...")
        pool = socketpool.SocketPool(wifi.radio)

        # Get timezone offset from secrets (default to UTC-6 for Central)
        try:
            from secrets import secrets
            tz_offset = secrets.get("tz_offset_hours", -6)
        except (ImportError, KeyError):
            tz_offset = -6  # Default to Central Time

        ntp = adafruit_ntp.NTP(pool, tz_offset=tz_offset)
        rtc.RTC().datetime = ntp.datetime

        print(f"Time synced: {time.localtime()}")
        return True
    except Exception as e:
        print(f"Time sync failed: {e}")
        return False


def go_to_sleep(magtag):
    """Put the device into deep sleep, wake on any button press."""
    print("Going to deep sleep...")

    # Deinit peripherals to save power
    magtag.peripherals.deinit()

    # Create pin alarms for all 4 buttons
    pin_alarms = [
        alarm.pin.PinAlarm(pin=board.D15, value=False, pull=True),  # Button A
        alarm.pin.PinAlarm(pin=board.D14, value=False, pull=True),  # Button B
        alarm.pin.PinAlarm(pin=board.D12, value=False, pull=True),  # Button C
        alarm.pin.PinAlarm(pin=board.D11, value=False, pull=True),  # Button D
    ]

    # Deep sleep until a button is pressed
    alarm.exit_and_deep_sleep_until_alarms(*pin_alarms)

def main():

    # Initialize MagTag
    magtag = MagTag()

    # Get the display
    display = magtag.graphics.display

    # Initialize dinosaur sprite
    dino = DinoSprite(display)

    # Set up display
    display.root_group = dino.get_group()

    # Check if we woke from deep sleep and which button was pressed
    woke_from_button = None
    if alarm.wake_alarm:
        if isinstance(alarm.wake_alarm, alarm.pin.PinAlarm):
            pin = alarm.wake_alarm.pin
            if pin == board.D15:
                woke_from_button = 0
            elif pin == board.D14:
                woke_from_button = 1
            elif pin == board.D12:
                woke_from_button = 2
            elif pin == board.D11:
                woke_from_button = 3

    # Determine night mode
    night_mode = is_night_time()

    # If we woke from a button press, handle that action
    if woke_from_button is not None and woke_from_button in BUTTON_ACTIONS:
        action, sound = BUTTON_ACTIONS[woke_from_button]
        print(f"Woke from button {woke_from_button}: {action}")

        # Show action sprite
        dino.show_action(action)
        safe_refresh(display)

        # Light up NeoPixels and play sound
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill((100, 200, 100))  # Soft green
        play_sound(magtag, sound)
        magtag.peripherals.neopixel_disable = True

        # Hold action sprite briefly
        time.sleep(ACTION_DISPLAY_DURATION)

        # Return to idle
        dino.show_idle(night_mode)
        safe_refresh(display)
    else:
        # First boot or unknown wake - sync time and show idle
        print("FridgeFriend starting...")

        # Sync time on first boot
        sync_time(magtag)

        # Re-check night mode after time sync
        night_mode = is_night_time()
        print(f"Night mode: {night_mode}")

        dino.show_idle(night_mode)
        safe_refresh(display)

    print("FridgeFriend ready! Going to sleep...")

    # Go to deep sleep to save battery
    go_to_sleep(magtag)


# Run the main function
if __name__ == "__main__":
    main()
else:
    # CircuitPython runs code.py directly
    main()
