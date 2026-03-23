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
from kmk.extensions import Extension


time.sleep(1.5)

keyboard = KMKKeyboard()

# RGB
rgb = RGB(
    pixel_pin=board.D4 ,
    num_pixels=4,
    val_limit=100,
    hue_default=0,
    sat_default=255,
    val_default=50,
    animation_mode=AnimationModes.RAINBOW,
    animation_speed=5,
    rgb_order=(1, 0, 2),
)

# Layer RGB indicators
class LayerRGBMode(Extension):
    def __init__(self, rgb):
        self.rgb = rgb
        self.current_layer = None
    
    def on_runtime_enable(self, keyboard):
        return
    
    def on_runtime_disable(self, keyboard):
        return
    
    def during_bootup(self, keyboard):
        return
    
    def before_matrix_scan(self, keyboard):
        # Check for layer changes before scanning keys
        if keyboard.active_layers:
            new_layer = keyboard.active_layers[0]
        else:
            new_layer = 0

        if new_layer != self.current_layer:
            self.current_layer = new_layer
            self.update_rgb_mode()
    
    def after_matrix_scan(self, keyboard):
        # Also check after scanning to catch any changes
        pass
    
    def before_hid_send(self, keyboard):
        pass
    
    def after_hid_send(self, keyboard):
        pass
    
    def on_powersave_enable(self, keyboard):
        pass
    
    def on_powersave_disable(self, keyboard):
        pass
    
    def update_rgb_mode(self):
        if self.current_layer == 0:
            # Layer 0: Rainbow
            self.rgb.animation_mode = AnimationModes.RAINBOW
        else:
            # Layer 1: Swirl
            self.rgb.animation_mode = AnimationModes.SWIRL
        self.rgb.show()


# Modules
layer_rgb_mode = LayerRGBMode(rgb)
macros = Macros()
layers = Layers()
holdtap = HoldTap()
holdtap.tap_time = 1250  # 1.25 seconds
encoder_handler = EncoderHandler()
mouse_keys = MouseKeys()
rapidfire = RapidFire()



keyboard.modules = [rapidfire, layers, holdtap, encoder_handler, macros, mouse_keys, layer_rgb_mode]
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)
keyboard.extensions.append(layer_rgb_mode)

# Custom keys
SPAM_CLICK = KC.RF(
    KC.MB_LMB, 
    timeout=200, 
    interval=70, 
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
    Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 1500,
    # Type cmd and press enter
    Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500,
    # Type the command
    Tap(KC.C), Tap(KC.U), Tap(KC.R), Tap(KC.L), Tap(KC.SPACE), Tap(KC.A), Tap(KC.S),
    Tap(KC.C), Tap(KC.I), Tap(KC.I), Tap(KC.DOT), Tap(KC.L), Tap(KC.I), Tap(KC.V), Tap(KC.E),
    Tap(KC.SLASH), Tap(KC.R), Tap(KC.I), Tap(KC.C), Tap(KC.K), Tap(KC.ENTER), Tap(KC.F11)
)

PARROT = KC.MACRO(
    # Open Run dialog
    Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 1500,
    # Type cmd and press enter
    Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500,
    # Type the command
    Tap(KC.C), Tap(KC.U), Tap(KC.R), Tap(KC.L), Tap(KC.SPACE), Tap(KC.P), Tap(KC.A), Tap(KC.R), Tap(KC.R),
    Tap(KC.O), Tap(KC.T), Tap(KC.DOT), Tap(KC.L), Tap(KC.I), Tap(KC.V), Tap(KC.E), Tap(KC.ENTER)
)

HACK = KC.MACRO(
    # Open Run dialog
    Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 1500,
    # Type cmd and press enter
    Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500,
    # Type the command
    Tap(KC.C), Tap(KC.O), Tap(KC.L), Tap(KC.O), Tap(KC.R), Tap(KC.SPACE), Tap(KC.N2),
    Tap(KC.ENTER), 600, Tap(KC.D), Tap(KC.I), Tap(KC.R), Tap(KC.SLASH), Tap(KC.S), Tap(KC.ENTER), Tap(KC.F11)
)

PASTE = KC.MACRO(
    Press(KC.LCTL), 
    Tap(KC.V), 
    Release(KC.LCTL)
)

# Define pins
PINS = [board.D7, board.D8, board.D9, board.D10] 

# Tell kmk we are not using a key matrix
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# Encoder pins
encoder_handler.pins = (
    (board.D5, board.D6, board.D0),   # First encoder
    (board.D1, board.D2, board.D3),   # Second encoder
)


encoder_handler.encoder_debounce = 30  # Reduces duplicate signals

encoder_handler.divisor = 2 

# Define encoder actions 
encoder_handler.map = [
    # Layer 0 - Mouse control
    [
        (KC.MS_RIGHT, KC.MS_LEFT, KC.MB_LMB, 50), #scrol (KC.MW_UP, KC.MW_DN, KC.MB_LMB, 50),
        (KC.MS_UP, KC.MS_DOWN, KC.MB_RMB, 50),
    ],
    # Layer 1 - Volume + RGB control
    [
        (KC.VOLU, KC.VOLD, KC.MUTE),
        (KC.RGB_VAI, KC.RGB_VAD, HACK),
    ],
]

# define the button pins
keyboard.keymap =    [
    # Layer 0
    [
        KC.HT(SCREENSHOT, KC.TO(1)),           # Tap: Screenshot, Hold: Layer 1
        PASTE,                                   # Paste macro
        PARROT,                                  # Parrot macro
        KC.SPACE,                                # Space
    ],
    # Layer 1
    [
        KC.HT(KC.MPRV, KC.TO(0)),               # Tap: Previous track, Hold: Layer 0
        KC.HT(KC.MPLY, RICKROLL),                # Tap: Play/Pause, Hold: Rickroll
        KC.HT(KC.MNXT, KC.F11),                                  # Next track
        SPAM_CLICK,                                   # Spam left click
    ],
]

# Start kmk
if __name__ == '__main__':
    keyboard.go()
