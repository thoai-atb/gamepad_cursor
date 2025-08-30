import os, time, pygame
from typing import Optional, List, Tuple
from .config import Config
from .util import log, shaped, normalize_trigger

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

class GamepadController:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.js: Optional[pygame.joystick.Joystick] = None
        self.prev_buttons: List[int] = []
        self.prev_hats: List[Tuple[int,int]] = []
        # Right stick neutral calibration (for scroll)
        self.calibrated = False
        self.neutral_rx = 0.0
        self.neutral_ry = 0.0
        self.samples = []
        self.enabled = True
        self.precision_toggle = False  # RS toggle

    def init(self):
        pygame.init()
        try:
            pygame.display.init()
            pygame.display.set_mode((1,1), flags=pygame.HIDDEN)
        except Exception:
            pygame.display.set_mode((1,1))
        pygame.joystick.init()
        self._connect_first()

    def _connect_first(self):
        if pygame.joystick.get_count() == 0:
            self.js = None
            return
        self.js = pygame.joystick.Joystick(0)
        self.js.init()
        log(f"Connected: {self.js.get_name()} (axes={self.js.get_numaxes()}, buttons={self.js.get_numbuttons()}, hats={self.js.get_numhats()})")
        self.prev_buttons = [0] * self.js.get_numbuttons()
        self.prev_hats = [(0,0)] * self.js.get_numhats()
        self.calibrated = False
        self.samples.clear()

    def pump(self):
        pygame.event.pump()

    def hotplug_check(self):
        # Simple periodic rescan could be called by outer loop; here no-op.
        if self.js is None and pygame.joystick.get_count() > 0:
            self._connect_first()

    def read_axes(self):
        cfg = self.cfg
        try:
            lx = self.js.get_axis(cfg.AX_LX)
            ly = self.js.get_axis(cfg.AX_LY)
        except Exception:
            lx, ly = 0.0, 0.0
        try:
            rx = self.js.get_axis(cfg.AX_RX)
            ry = self.js.get_axis(cfg.AX_RY)
        except Exception:
            rx, ry = 0.0, 0.0
        try:
            lt_raw = self.js.get_axis(cfg.AX_LT)
        except Exception:
            lt_raw = 0.0
        try:
            rt_raw = self.js.get_axis(cfg.AX_RT)
        except Exception as e:
            print(e)
            rt_raw = 0.0

        # --- Mouse movement ---
        mx = shaped(lx, cfg.DEADZONE_MOVE, cfg.ACCEL_EXP)
        my = shaped(ly, cfg.DEADZONE_MOVE, cfg.ACCEL_EXP)

        # --- Scroll mapping ---
        # the controller: rx = vertical scroll, ry = useless
        def apply_deadzone(val, dz=0.15):
            return 0.0 if abs(val) < dz else val

        hscroll = apply_deadzone(ry, cfg.DEADZONE_SCROLL)
        vscroll = apply_deadzone(rx, cfg.DEADZONE_SCROLL)

        if cfg.INVERT_Y:
            my = -my
            vscroll = -vscroll

        # Normalize triggers
        lt = normalize_trigger(lt_raw)
        rt = normalize_trigger(rt_raw)

        # log(f"Scroll raw: rx={rx:.3f}, ry={ry:.3f}, mapped -> vscroll={vscroll:.3f}")

        return mx, my, hscroll, vscroll, lt, rt


    def read_buttons(self):
        nbtn = self.js.get_numbuttons()
        if not self.prev_buttons or len(self.prev_buttons) != nbtn:
            self.prev_buttons = [0] * nbtn

        prev = self.prev_buttons[:]   # copy old state
        curr = [self.js.get_button(i) for i in range(nbtn)]

        def down(i): return i < len(curr) and prev[i] == 0 and curr[i] == 1
        def up(i):   return i < len(curr) and prev[i] == 1 and curr[i] == 0

        self.prev_buttons = curr      # update AFTER checks
        return down, up, curr

    def read_hats(self):
        nh = self.js.get_numhats()
        if not self.prev_hats or len(self.prev_hats)!=nh:
            self.prev_hats = [(0,0)]*nh
        curr = [self.js.get_hat(i) for i in range(nh)]
        changed = []
        for i,(px,py) in enumerate(self.prev_hats):
            cx, cy = curr[i]
            changed.append(((px,py),(cx,cy)))
        self.prev_hats = curr
        return changed
