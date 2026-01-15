"""
Dinosaur sprite management for FridgeFriend.
Handles loading, displaying, and animating the chibi dino.
"""

import time
import displayio
import terminalio
from adafruit_display_text import label

# Action types
ACTION_PLAY = "play"
ACTION_PET = "pet"
ACTION_FEED = "feed"
ACTION_SLEEP = "sleep"

# Sprite file paths
SPRITE_PATHS = {
    "idle_day": "/sprites/idle_day.bmp",
    "idle_night": "/sprites/idle_night.bmp",
    ACTION_PLAY: "/sprites/play.bmp",
    ACTION_PET: "/sprites/pet.bmp",
    ACTION_FEED: "/sprites/feed.bmp",
    ACTION_SLEEP: "/sprites/sleep.bmp",
}

class DinoSprite:
    """Manages the dinosaur sprite display and animations."""

    def __init__(self, display):
        """
        Initialize the DinoSprite.

        Args:
            display: The MagTag display object
        """
        self.display = display
        self.display_width = display.width
        self.display_height = display.height

        # Create the display group
        self.group = displayio.Group()

        # Current state
        self.current_sprite_name = None
        self._tile_grid = None

        # Calculate center position for 64x64 sprite
        self.sprite_x = (self.display_width - 64) // 2
        self.sprite_y = (self.display_height - 64) // 2 - 10  # Shift up for labels

        # Set up white background
        self._setup_background()

        # Add button labels
        self._setup_labels()

    def _setup_background(self):
        """Create a white background for the display."""
        # Create a simple white background bitmap
        bg_bitmap = displayio.Bitmap(self.display_width, self.display_height, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0xFFFFFF  # White
        bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        self.group.append(bg_sprite)

    def _setup_labels(self):
        """Add button labels at the bottom of the display."""
        # Button labels: Play, Pet, Feed, Sleep (left to right)
        # MagTag display is 296x128, buttons are evenly spaced
        button_labels = ["PLAY", "PET", "FEED", "SLEEP"]
        label_y = self.display_height - 8  # Near bottom

        # Calculate x positions for 4 evenly spaced labels
        # Display width is 296, divide into 4 sections
        section_width = self.display_width // 4

        for i, text in enumerate(button_labels):
            # Center each label in its section
            label_x = (section_width * i) + (section_width // 2)
            btn_label = label.Label(
                terminalio.FONT,
                text=text,
                color=0x000000,
                anchor_point=(0.5, 0.5),
                anchored_position=(label_x, label_y)
            )
            self.group.append(btn_label)

    def _load_sprite(self, sprite_name):
        """
        Load a sprite bitmap from file.

        Args:
            sprite_name: Key from SPRITE_PATHS dict

        Returns:
            TileGrid with the loaded sprite
        """
        if sprite_name not in SPRITE_PATHS:
            raise ValueError(f"Unknown sprite: {sprite_name}")

        filepath = SPRITE_PATHS[sprite_name]
        bitmap = displayio.OnDiskBitmap(filepath)
        tile_grid = displayio.TileGrid(
            bitmap,
            pixel_shader=bitmap.pixel_shader,
            x=self.sprite_x,
            y=self.sprite_y
        )
        return tile_grid

    def _set_sprite(self, sprite_name):
        """
        Set the currently displayed sprite.

        Args:
            sprite_name: Key from SPRITE_PATHS dict
        """
        if sprite_name == self.current_sprite_name:
            return

        # Remove old sprite if exists
        if self._tile_grid is not None:
            self.group.remove(self._tile_grid)

        # Load and add new sprite
        self._tile_grid = self._load_sprite(sprite_name)
        self.group.append(self._tile_grid)
        self.current_sprite_name = sprite_name

    def show_idle(self, is_night=False):
        """
        Show the idle sprite.

        Args:
            is_night: If True, show sleepy/night sprite
        """
        sprite_name = "idle_night" if is_night else "idle_day"
        self._set_sprite(sprite_name)

    def show_action(self, action_type):
        """
        Show an action sprite.

        Args:
            action_type: One of ACTION_PLAY, ACTION_PET, ACTION_FEED, ACTION_SLEEP
        """
        if action_type in SPRITE_PATHS:
            self._set_sprite(action_type)

    def get_group(self):
        """Return the displayio Group for this sprite."""
        return self.group


def is_night_time():
    """
    Check if it's currently night time (6PM - 6AM).

    Returns:
        bool: True if between 6PM and 6AM
    """
    current_time = time.localtime()
    hour = current_time.tm_hour
    # Night is 6PM (18:00) to 6AM (06:00)
    return hour >= 18 or hour < 6
