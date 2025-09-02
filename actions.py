from pynput.mouse import Button, Controller as MouseCtl
from pynput.keyboard import Key, Controller as KeyCtl
import time

from .util import log


class MouseKeyboardActions:
    """Wrapper for pynput mouse/keyboard with fractional scroll accumulation.
       Movement/scroll are silent; only button/key events log."""

    def __init__(self):
        self.mouse = MouseCtl()
        self.kb = KeyCtl()
        self._h_acc = 0.0
        self._v_acc = 0.0

    # --- Mouse buttons ---
    def left_down(self):
        self.mouse.press(Button.left)
        log("Mouse LEFT DOWN")

    def left_up(self):
        self.mouse.release(Button.left)
        log("Mouse LEFT UP")

    def right_down(self):
        self.mouse.press(Button.right)
        log("Mouse RIGHT DOWN")

    def right_up(self):
        self.mouse.release(Button.right)
        log("Mouse RIGHT UP")

    def middle_down(self):
        self.mouse.press(Button.middle)
        log("Mouse MIDDLE DOWN")

    def middle_up(self):
        self.mouse.release(Button.middle)
        log("Mouse MIDDLE UP")

    # --- Movement (silent) ---
    def move(self, dx: int, dy: int, speed: float):
        if dx or dy:
            self.mouse.move(dx, dy)

    # --- Scrolling (silent, with fractional accumulation) ---
    def scroll(self, h: float, v: float):
        self._h_acc += h
        self._v_acc += v
        ticks_h = round(self._h_acc)
        ticks_v = round(self._v_acc)

        if ticks_h != 0 or ticks_v != 0:
            self.mouse.scroll(ticks_h, -ticks_v)  # flip v for OS direction
            self._h_acc -= ticks_h
            self._v_acc -= ticks_v

    # --- Keyboard keys ---
    def space_down(self):
        self.kb.press(Key.space)
        log("Key DOWN <space>")

    def space_up(self):
        self.kb.release(Key.space)
        log("Key UP <space>")

    def esc_down(self):
        self.kb.press(Key.esc)
        log("Key DOWN <esc>")

    def esc_up(self):
        self.kb.release(Key.esc)
        log("Key UP <esc>")

    def arrow_left(self, down: bool):
        (self.kb.press if down else self.kb.release)(Key.left)

    def arrow_right(self, down: bool):
        (self.kb.press if down else self.kb.release)(Key.right)

    def arrow_up(self, down: bool):
        (self.kb.press if down else self.kb.release)(Key.up)

    def arrow_down(self, down: bool):
        (self.kb.press if down else self.kb.release)(Key.down)

    def alt_tab_down(self):
        """Hold Alt and Tab down together."""
        try:
            self.kb.press(Key.alt)
            self.kb.press(Key.tab)
            log("Keys DOWN <Alt+Tab>")
        except Exception:
            pass

    def alt_tab_up(self):
        """Release Alt and Tab together."""
        try:
            self.kb.release(Key.tab)
            self.kb.release(Key.alt)
            log("Keys UP <Alt+Tab>")
        except Exception:
            pass

    def ctrl_tab_once(self):
        """Send a single Ctrl+Tab press (quick tap)."""
        try:
            self.kb.press(Key.ctrl)
            time.sleep(0.012)
            self.kb.press(Key.tab)
            time.sleep(0.012)
            self.kb.release(Key.tab)
            self.kb.release(Key.ctrl)
            log("Key COMBO Ctrl+Tab")
        except Exception:
            pass

    def alt_f4_once(self):
        """Send Alt+F4 (close window)."""
        try:
            self.kb.press(Key.alt)
            self.kb.press(Key.f4)
            self.kb.release(Key.f4)
            self.kb.release(Key.alt)
            log("Key COMBO Alt+F4")
        except Exception:
            pass

    def f5_once(self):
        """Send F5 (refresh)."""
        try:
            self.kb.press(Key.f5)
            self.kb.release(Key.f5)
            log("Key PRESS F5")
        except Exception:
            pass

    def increase_volume(self):
        """Increase system volume (by one step)."""
        try:
            self.kb.press(Key.media_volume_up)
            self.kb.release(Key.media_volume_up)
            log("Key PRESS Volume Up")
        except Exception:
            pass
    
    def decrease_volume(self):
        """Decrease system volume (by one step)."""
        try:
            self.kb.press(Key.media_volume_down)
            self.kb.release(Key.media_volume_down)
            log("Key PRESS Volume Down")
        except Exception:
            pass