# You import all the IOs of your board
import board

# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.holdtap import HoldTap
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.rapidfire import RapidFire

# This is the main instance of your keyboard
keyboard = KMKKeyboard()

# RGB
rgb = RGB(
    pixel_pin=board.GP6,
    num_pixels=4,
    val_limit=100,
    hue_default=0,
    sat_default=255,
    val_default=50,
    animation_mode=AnimationModes.RAINBOW,
    animation_speed=2,
    rgb_order=(1, 0, 2),
)

#layer rgb indicators
class LayerRGBMode:
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
        return
    
    def update_rgb_mode(self):
        if self.current_layer == 0:
            # Layer 0: Rainbow
            self.rgb.animation_mode = AnimationModes.RAINBOW
        else:
            # Layer 1: Swirl
            self.rgb.animation_mode = AnimationModes.SWIRL
        self.rgb.show()

#Moudle instances here
macros = Macros()
layers = Layers()
holdtap = HoldTap()
holdtap.tap_time = 1250 # 1.25 seconds
encoder_handler = EncoderHandler()
mouse_keys = MouseKeys()
layer_rgb_mode = LayerRGBMode(rgb)

# Add the macro extension
keyboard.modules = [layer_rgb_mode, layers, holdtap, encoder_handler, macros, mouse_keys, RapidFire()]
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)

#Custom keys
SPAM_E = KC.RF(KC.E, timeout=200, interval=100, enable_interval_randomization=True, randomization_magnitude=25, toggle=True)
SCREENSHOT = KC.MACRO(Press(KC.LWIN), Press(KC.LSFT), Tap(KC.S), Release(KC.LSFT), Release(KC.LWIN))
RICKROLL =  KC.Macro(
        # Open Run dialog
        Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 600,  # wait 600 ms for run dialog to open

        #type cmd and press enter
        Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500, # wait 2.5 seconds for cmd to open
        
        #Type the command
        Tap(KC.C), Tap(KC.U), Tap(KC.R), Tap(KC.L), Tap(KC.SPACE), Tap(KC.A), Tap(KC.S),
        Tap(KC.C), Tap(KC.I), Tap(KC.I), Tap(KC.DOT), Tap(KC.L), Tap(KC.I), Tap(KC.V), Tap(KC.E),
        Tap(KC.SLASH), Tap(KC.R), Tap(KC.I), Tap(KC.C), Tap(KC.K), Tap(KC.ENTER),)
PARROT = KC.Macro(
        # Open Run dialog
        Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 600,  # wait 600 ms for run dialog to open

        #type cmd and press enter
        Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500, # wait 2.5 seconds for cmd to open
        
        #Type the command
        Tap(KC.C), Tap(KC.U), Tap(KC.R), Tap(KC.L), Tap(KC.SPACE), Tap(KC.P), Tap(KC.A), Tap(KC.R), Tap(KC.R),
        Tap(KC.O), Tap(KC.T), Tap(KC.DOT), Tap(KC.L), Tap(KC.I), Tap(KC.V), Tap(KC.E), Tap(KC.ENTER),)
HACK = KC.Macro(
        # Open Run dialog
        Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN), 600,  # wait 600 ms for run dialog to open
        #type cmd and press enter
        Tap(KC.C), Tap(KC.M), Tap(KC.D), Tap(KC.ENTER), 2500, # wait 2.5 seconds for cmd to open
        #Type the command
        Tap(KC.C), Tap(KC.O), Tap(KC.L), Tap(KC.O), Tap(KC.R), Tap(KC.SPACE), Tap(KC.N2),
        Tap(KC.ENTER), 600, Tap(KC.D), Tap(KC.I), Tap(KC.R), Tap(KC.SLASH), Tap(KC.S), Tap(KC.ENTER),)

# Define your pins here!
PINS = [board.GP1, board.GP2, board.GP4, board.GP3]

# Tell kmk we are not using a key matrix
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

#Enchoder pins
encoder_handler.pins = (
    (board.GP9, board.GP0, board.GP26), # (pin_a, pin_b, pin_button)
    (board.GP27, board.GP28, board.GP29),) # (pin_a, pin_b, pin_button)

#define encoder actions
encoder_handler.map = [
    # layer 0
    [
        (KC.MS_RIGHT, KC.MS_LEFT, KC.MB_LMB), # First encoder Layer 0: turn left, turn right, press 
        (KC.MS_UP, KC.MS_DOWN, KC.MB_RMB),    # Second encoder Layer 0
    ], 
    # layer 1
    [
        (KC.VOLU, KC.VOLD, KC.MUTE), # First encoder Layer 1
        (KC.RGB_VAI, KC.RGB_VAD, HACK),   # Second encoder Layer 1
    ], 
]

# Here you define the buttons corresponding to the pins
keyboard.keymap = [
    # Layer 0
    [KC.HT(SCREENSHOT,KC.TO(1)), # HoldTap example: tap for Screenshot, hold for layer toggle
     KC.MACRO(Press(KC.LCTL), Tap(KC.V), Release(KC.LCTL)), # Paste
     PARROT,
     KC.SPACE,]
    # Layer 1
    ,[KC.HT(KC.MPRV,KC.TO(0)), # HoldTap example: tap for media previous track, hold for layer toggle
      KC.HT(KC.MPLY, RICKROLL,), # Tap for media play/pause, hold for a macro
      KC.MNXT,
      KC.SPAM_E,
        ]
]

# Start kmk!
if __name__ == '__main__':
    keyboard.go()