from dataclasses import dataclass

@dataclass
class Config:
    # Sensitivity / shaping
    DEADZONE_MOVE: float = 0.12        # left-stick (pointer) deadzone
    DEADZONE_SCROLL: float = 0.15      # right-stick (scroll) deadzone (lower so it's responsive)
    BASE_SPEED: float = 12.0         # ↓ as requested
    ACCEL_EXP: float = 1.6             # response curve
    PRECISION_FACTOR_TOGGLE: float = 0.33  # RS toggle multiplier
    RT_SLOW_MULT: float = 0.2           # new behavior: RT held => ~1/3 speed
    SCROLL_SPEED: int = 0.2              # vertical scroll units per tick (at full tilt)
    HSCROLL_SPEED: int = 1             # horizontal scroll units per tick
    POLL_DELAY_MS: int = 8             # ~125 Hz
    INVERT_Y: bool = False             # normal Y (up = up)
    NEUTRAL_SAMPLES: int = 30          # right-stick neutral calibration samples
    LOG_MOVE_EVERY_MS: int = 120
    LOG_SCROLL_EVERY_MS: int = 120

    # Axes (adjust here if the controller differs)
    AX_LX: int = 0
    AX_LY: int = 1
    AX_LT: int = 4   # was 2; the tester shows LT is axis 4
    AX_RX: int = 3
    AX_RY: int = 2
    AX_RT: int = 5   # Right Trigger axis

    # Buttons (adjust here if the controller differs)
    BTN_A: int = 0
    BTN_B: int = 1
    BTN_X: int = 2
    BTN_Y: int = 3
    BTN_LB: int = 4
    BTN_RB: int = 5
    BTN_BACK: int = 6
    BTN_START: int = 7
    BTN_LS: int = 8
    BTN_RS: int = 9

    # Trigger threshold to consider "held"
    TRIGGER_HELD_THRESH: float = 0.30
