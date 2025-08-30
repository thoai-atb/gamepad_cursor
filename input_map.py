import time
from .config import Config
from .util import log
from .actions import MouseKeyboardActions
from .controller import GamepadController


class GamepadApp:
    """High-level glue: reads controller, applies mapping to actions (with D-pad → arrow keys)."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.ctrl = GamepadController(cfg)
        self.act = MouseKeyboardActions()
        self._lt_holding = False

    def run(self):
        self.ctrl.init()
        log(
            "Mapping:\n"
            "  LS = Mouse\n"
            "  RS = Scroll\n"
            "  A  = Left Click\n"
            "  B  = Right Click\n"
            "  X  = Middle Click\n"
            "  LB = Decrease Volume\n"
            "  RB = Increase Volume\n"
            "  Y  = Ctrl+Tab\n"
            "  LT = Alt+Tab\n"
            "  Start = Toggle Controls\n"
            "  RT = Slow Mouse\n"
            "  D-pad = Arrow Keys\n"
            "  Back = Esc"
        )
        try:
            while True:
                self.ctrl.pump()
                self.ctrl.hotplug_check()
                if self.ctrl.js is None:
                    time.sleep(self.cfg.POLL_DELAY_MS / 1000.0)
                    continue

                # --- Axes
                mx, my, sx, sy, lt, rt = self.ctrl.read_axes()

                # --- Buttons with edge detection
                down, up, curr = self.ctrl.read_buttons()
                cfg = self.cfg

                # Start toggles enable
                if down(cfg.BTN_START):
                    self.ctrl.enabled = not self.ctrl.enabled
                    log(f"Controls {'ENABLED' if self.ctrl.enabled else 'DISABLED'}")
                    # --- Add rumble feedback ---
                    js = self.ctrl.js
                    if js and hasattr(js, "rumble"):
                        try:
                            js.rumble(0.7, 0.7, 200)  # strong/weak, duration ms
                        except Exception as e:
                            log(f"Rumble failed: {e}")

                if self.ctrl.enabled:
                    # RS toggles persistent precision (stacks with RT slow when held)
                    if down(cfg.BTN_RS):
                        self.ctrl.precision_toggle = not self.ctrl.precision_toggle
                        log(f"Precision mode: {'ON' if self.ctrl.precision_toggle else 'OFF'} (toggle)")

                    # --- Mouse buttons ---
                    # Left (A)
                    if down(cfg.BTN_A):
                        self.act.left_down()
                    if up(cfg.BTN_A):
                        self.act.left_up()

                    # Right (B)
                    if down(cfg.BTN_B):
                        self.act.right_down()
                    if up(cfg.BTN_B):
                        self.act.right_up()

                    # --- Middle mouse --
                    if down(cfg.BTN_X):
                        self.act.middle_down()
                    if up(cfg.BTN_X):
                        self.act.middle_up()

                    # --- Decrease volume ---
                    if down(cfg.BTN_LB):
                        self.act.decrease_volume()

                    # --- Increase volume ---
                    if down(cfg.BTN_RB):
                        self.act.increase_volume()

                    # Ctrl+Tab (one time press)
                    if down(cfg.BTN_Y):
                        self.act.ctrl_tab_once()

                    # Esc (Back)
                    if down(cfg.BTN_BACK):
                        self.act.esc_down()
                    if up(cfg.BTN_BACK):
                        self.act.esc_up()

                    # --- D-p      ad → Arrow keys (edge detection on hats) ---
                    for (px, py), (cx, cy) in self.ctrl.read_hats():
                        # Horizontal arrows
                        if cx == -1 and px != -1:  # newly pressed LEFT
                            self.act.arrow_left(True)
                        if cx != -1 and px == -1:  # released LEFT
                            self.act.arrow_left(False)
                        if cx == 1 and px != 1:    # newly pressed RIGHT
                            self.act.arrow_right(True)
                        if cx != 1 and px == 1:    # released RIGHT
                            self.act.arrow_right(False)

                        # Vertical arrows (note: many pads use +1 = up, -1 = down)
                        if cy == 1 and py != 1:    # newly pressed UP
                            self.act.arrow_up(True)
                        if cy != 1 and py == 1:    # released UP
                            self.act.arrow_up(False)
                        if cy == -1 and py != -1:  # newly pressed DOWN
                            self.act.arrow_down(True)
                        if cy != -1 and py == -1:  # released DOWN
                            self.act.arrow_down(False)

                    # --- Pointer movement (Left stick) ---
                    speed = cfg.BASE_SPEED  # default fast
                    # RT held = slow mouse
                    if rt >= cfg.TRIGGER_HELD_THRESH:
                        speed *= cfg.RT_SLOW_MULT
                    # Optional: persistent precision toggle (RS) also slows
                    if self.ctrl.precision_toggle:
                        speed *= cfg.PRECISION_FACTOR_TOGGLE

                    dx = int(mx * speed)
                    dy = int(my * speed)
                    self.act.move(dx, dy, speed)

                    # --- Scroll (Right stick, always active; fractional accumulation in actions) ---
                    # RT held = slow scroll
                    scroll_speed = cfg.SCROLL_SPEED
                    hscroll_speed = cfg.HSCROLL_SPEED
                    if rt >= cfg.TRIGGER_HELD_THRESH:
                        scroll_speed *= cfg.PRECISION_FACTOR_TOGGLE  # or define a new factor if you want
                        hscroll_speed *= cfg.PRECISION_FACTOR_TOGGLE

                    self.act.scroll(sx * hscroll_speed, sy * scroll_speed)

                    # LT = hold Alt+Tab while trigger is down
                    lt_now = (lt >= self.cfg.TRIGGER_HELD_THRESH)

                    if lt_now and not self._lt_holding:
                        self._lt_holding = True
                        self.act.alt_tab_down()

                    elif not lt_now and self._lt_holding:
                        self._lt_holding = False
                        self.act.alt_tab_up()

                time.sleep(self.cfg.POLL_DELAY_MS / 1000.0)

        except KeyboardInterrupt:
            pass
        finally:
            import pygame
            pygame.joystick.quit()
            pygame.quit()
            log("Bye.")
