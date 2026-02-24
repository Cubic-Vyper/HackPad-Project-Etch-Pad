import time
import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.holdtap import HoldTap
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.rapidfire import RapidFire
from kmk.modules import Module
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.extensions.media_keys import MediaKeys

# Small delay for USB stability
time.sleep(1.5)
print("=" * 50)
print("CUSTOM KEYBOARD - RESTORED ORIGINAL LAYOUT")
print("=" * 50)

keyboard = KMKKeyboard()

# RGB - FIXED: num_pixels=1 for built-in LED
rgb = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    hue_default=0,
    sat_default=255,
    val_default=50,
    animation_mode=AnimationModes.RAINBOW,
    animation_speed=2,
    rgb_order=(1, 0, 2),
)

# Layer RGB indicators - FIXED: Now inherits from Module
class LayerRGBMode(Module):
    def __init__(self, rgb):
        self.rgb = rgb
        self.current_layer = None
    
    def after_matrix_scan(self, keyboard):
        if keyboard.active_layers:
            new_layer = keyboard.active_layers[0]
        else:
            new_layer = 0

        if new_layer != self.current_layer:
            self.current_layer = new_layer
            self.update_rgb_mode()
    
    def update_rgb_mode(self):
        if self.current_layer == 0:
            # Layer 0: Rainbow
            self.rgb.animation_mode = AnimationModes.RAINBOW
        else:
            # Layer 1: Swirl
            self.rgb.animation_mode = AnimationModes.SWIRL
        self.rgb.show()

# Module instances
macros = Macros()
layers = Layers()
holdtap = HoldTap()
holdtap.tap_time = 1250  # 1.25 seconds
encoder_handler = EncoderHandler()
mouse_keys = MouseKeys()
rapidfire = RapidFire()
layer_rgb_mode = LayerRGBMode(rgb)

# IMPORTANT: Add RapidFire FIRST so KC.RF is available
keyboard.modules = [rapidfire, layers, holdtap, encoder_handler, macros, mouse_keys, layer_rgb_mode]
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)

# Custom keys - FIXED: All macros use KC.MACRO (not KC.Macro)
SPAM_E = KC.RF(
    KC.E, 
    timeout=200, 
    interval=100, 
    enable_interval_randomization=True, 
    randomization_magnitude=25, 
    toggle=True
)

SCREENSHOT = KC.MACRO(
    Press(KC.LWIN), 
    Press(KC.LSFT), 
    Tap(KC.S), 
    Release(KC.LSFT), 
    Release(KC.LWIN)
)

RICKROLL = KC.MACRO(
    # Open Run dialog
    Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 600,
    # Type cmd and press enter
    Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500,
    # Type the command
    Tap(KC.C), Tap(KC.U), Tap(KC.R), Tap(KC.L), Tap(KC.SPACE), Tap(KC.A), Tap(KC.S),
    Tap(KC.C), Tap(KC.I), Tap(KC.I), Tap(KC.DOT), Tap(KC.L), Tap(KC.I), Tap(KC.V), Tap(KC.E),
    Tap(KC.SLASH), Tap(KC.R), Tap(KC.I), Tap(KC.C), Tap(KC.K), Tap(KC.ENTER)
)

PARROT = KC.MACRO(
    # Open Run dialog
    Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 600,
    # Type cmd and press enter
    Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500,
    # Type the command
    Tap(KC.C), Tap(KC.U), Tap(KC.R), Tap(KC.L), Tap(KC.SPACE), Tap(KC.P), Tap(KC.A), Tap(KC.R), Tap(KC.R),
    Tap(KC.O), Tap(KC.T), Tap(KC.DOT), Tap(KC.L), Tap(KC.I), Tap(KC.V), Tap(KC.E), Tap(KC.ENTER)
)

HACK = KC.MACRO(
    # Open Run dialog
    Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 600,
    # Type cmd and press enter
    Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500,
    # Type the command
    Tap(KC.C), Tap(KC.O), Tap(KC.L), Tap(KC.O), Tap(KC.R), Tap(KC.SPACE), Tap(KC.N2),
    Tap(KC.ENTER), 600, Tap(KC.D), Tap(KC.I), Tap(KC.R), Tap(KC.SLASH), Tap(KC.S), Tap(KC.ENTER)
)

PASTE = KC.MACRO(
    Press(KC.LCTL), 
    Tap(KC.V), 
    Release(KC.LCTL)
)

# Define your pins here! - FIXED: Using safe pins
PINS = [board.D7, board.D8, board.D9, board.D10]  # Keys: D7, D8, D9, D10

# Tell kmk we are not using a key matrix
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# Encoder pins - FIXED: Using safe pins, NO A0!
encoder_handler.pins = (
    (board.D0, board.D1, board.D2),   # First encoder: D0(A), D1(B), D2(button)
    (board.D3, board.D4, board.D5),    # Second encoder: D3(A), D4(B), D5(button)
)

# Define encoder actions - EXACTLY as you wanted
encoder_handler.map = [
    # Layer 0 - Mouse control
    [
        (KC.MS_RIGHT, KC.MS_LEFT, KC.MB_LMB),  # First encoder: mouse right/left, left click
        (KC.MS_UP, KC.MS_DOWN, KC.MB_RMB),     # Second encoder: mouse up/down, right click
    ],
    # Layer 1 - Volume + RGB control
    [
        (KC.VOLU, KC.VOLD, KC.MUTE),           # First encoder: volume up/down, mute
        (KC.RGB_VAI, KC.RGB_VAD, HACK),        # Second encoder: RGB brightness, HACK macro
    ],
]

# Here you define the buttons corresponding to the pins - EXACTLY as you wanted
keyboard.keymap = [
    # Layer 0: Screenshot, Paste, Parrot, Space
    [
        KC.HT(SCREENSHOT, KC.TO(1)),           # Tap: Screenshot, Hold: Layer 1
        PASTE,                                   # Paste macro
        PARROT,                                  # Parrot macro
        KC.SPACE,                                # Space
    ],
    # Layer 1: Previous track, Play/Pause+Rickroll, Next track, Spam E
    [
        KC.HT(KC.MPRV, KC.TO(0)),               # Tap: Previous track, Hold: Layer 0
        KC.HT(KC.MPLY, RICKROLL),                # Tap: Play/Pause, Hold: Rickroll
        KC.MNXT,                                  # Next track
        SPAM_E,                                   # Spam E (RapidFire)
    ],
]

print("=" * 50)
print("✅ CUSTOM KEYBOARD READY!")
print("=" * 50)
print("LAYER 0 (Rainbow RGB):")
print("  Key 1: Tap=Screenshot, Hold=Layer 1")
print("  Key 2: Paste (Ctrl+V)")
print("  Key 3: Parrot macro")
print("  Key 4: Space")
print("  Encoder 1: Mouse left/right + left click")
print("  Encoder 2: Mouse up/down + right click")
print()
print("LAYER 1 (Swirl RGB):")
print("  Key 1: Tap=Previous track, Hold=Layer 0")
print("  Key 2: Tap=Play/Pause, Hold=Rickroll")
print("  Key 3: Next track")
print("  Key 4: Spam E (RapidFire)")
print("  Encoder 1: Volume up/down + mute")
print("  Encoder 2: RGB brightness + HACK macro")
print("=" * 50)

# Start kmk!
if __name__ == '__main__':
    keyboard.go()
