import time
import threading
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
            "\n=== Gamepad Control Mapping ===\n"
            "  Left Stick      → Mouse Movement\n"
            "  Right Stick     → Scrolling\n"
            "  A               → Left Mouse Click\n"
            "  B               → Right Mouse Click\n"
            "  Y               → Middle Mouse Click\n"
            "  X               → Space Key\n"
            "  LB              → Decrease Volume\n"
            "  RB              → Increase Volume\n"
            "  LS Button       → Ctrl+Tab\n"
            "  RS Button       → Alt+Tab\n"
            "  LT (Hold)       → Alternate Actions:\n"
            "      A           → Enter\n"
            "      B           → Alt+F4\n"
            "      X           → Tab\n"
            "      Y           → F5\n"
            "      LB          → Ctrl + - (Zoom Out)\n"
            "      RB          → Ctrl + = (Zoom In)\n"
            "      Start       → Toggle Controls On/Off\n"
            "  RT (Hold)       → Slow Mouse/Scroll\n"
            "  D-pad           → Arrow Keys\n"
            "  Back            → Esc Key\n"
            "================================\n"
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

                # --- LT as alternate modifier ---
                lt_hold = lt >= cfg.TRIGGER_HELD_THRESH

                # Toggle enable/disable control with Start + LT held
                if lt_hold and down(cfg.BTN_START):
                    self.ctrl.enabled = not self.ctrl.enabled
                    log(f"Controls {'ENABLED' if self.ctrl.enabled else 'DISABLED'}")
                    if self.ctrl.enabled:
                        self.ctrl.rumble_feedback(ms=200)
                        threading.Timer(0.3, lambda: self.ctrl.rumble_feedback(ms=200)).start()
                    else:
                        self.ctrl.rumble_feedback(ms=200)

                # If control enabled, process inputs
                if self.ctrl.enabled:
                    if lt_hold:
                        self.handle_lt_hold(down, up, cfg)
                    else:
                        self.handle_lt_normal(down, up, cfg)

                    # Check D-Pad (Arrow keys)
                    self.check_dpad()

                    # --- Pointer movement (Left stick) ---
                    self.check_pointer_movement(mx, my, rt, cfg)

                    # --- Scroll (Right stick, fractional accumulation in actions) ---
                    self.check_rolling(sx, sy, rt, cfg)

                    # --- Alt+Tab (Right Stick Button) ---
                    if down(cfg.BTN_RS):
                        self.act.alt_tab_down()
                    if up(cfg.BTN_RS):
                        self.act.alt_tab_up()

                    # --- Ctrl+Tab (Left Stick Button) ---
                    if down(cfg.BTN_LS):
                        self.act.ctrl_tab_down()
                    if up(cfg.BTN_LS):
                        self.act.ctrl_tab_up()

                time.sleep(self.cfg.POLL_DELAY_MS / 1000.0)

        except KeyboardInterrupt:
            pass
        finally:
            import pygame
            pygame.joystick.quit()
            pygame.quit()
            log("Bye.")

    def handle_lt_normal(self, down, up, cfg):
        # Normal mappings
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

        # Space (X)
        if down(cfg.BTN_X):
            self.act.space_down()
        if up(cfg.BTN_X):
            self.act.space_up()

        # Middle mouse (Y)
        if down(cfg.BTN_Y):
            self.act.middle_down()
        if up(cfg.BTN_Y):
            self.act.middle_up()

        # Decrease volume (LB)
        if down(cfg.BTN_LB):
            self.act.decrease_volume()

        # Increase volume (RB)
        if down(cfg.BTN_RB):
            self.act.increase_volume()

        # Esc (Back)
        if down(cfg.BTN_BACK):
            self.act.esc_down()
        if up(cfg.BTN_BACK):
            self.act.esc_up()

    def handle_lt_hold(self, down, up, cfg):
        # LT held: alternate actions
        # A -> Enter
        if down(cfg.BTN_A):
            self.act.enter()
        # B -> Ctrl+F4
        if down(cfg.BTN_B):
            self.act.alt_f4()
        # X -> Tab
        if down(cfg.BTN_X):
            self.act.tab()
        # Y -> F5
        if down(cfg.BTN_Y):
            self.act.f5()
        # LB -> Ctrl + =
        if down(cfg.BTN_LB):
            self.act.zoom_out()
        # RB -> Ctrl + -
        if down(cfg.BTN_RB):
            self.act.zoom_in()

    def check_dpad(self):
        # --- D-pad → Arrow keys (edge detection on hats) ---
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

    def check_pointer_movement(self, mx, my, rt, cfg):
        speed = cfg.BASE_SPEED  # default fast
        # RT held = slow mouse
        if rt >= cfg.TRIGGER_HELD_THRESH:
            speed *= cfg.RT_SLOW_MULT

        dx = int(mx * speed)
        dy = int(my * speed)
        self.act.move(dx, dy, speed)

    def check_rolling(self, sx, sy, rt, cfg):
        scroll_speed = cfg.SCROLL_SPEED
        hscroll_speed = cfg.HSCROLL_SPEED
        # RT held = slow scroll
        if rt >= cfg.TRIGGER_HELD_THRESH:
            scroll_speed *= cfg.PRECISION_FACTOR_TOGGLE
            hscroll_speed *= cfg.PRECISION_FACTOR_TOGGLE
        self.act.scroll(sx * hscroll_speed, sy * scroll_speed)