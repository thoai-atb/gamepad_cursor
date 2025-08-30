# 🎮 Gamepad → Cursor

Control your PC cursor with a standard gamepad controller.

## 🛠 Requirements
```bash
pip install pygame-ce pynput
```

## ▶️ Running
After cloning to gamepad_cursor folder, run:
```bash
python3 -m gamepad_cursor.app
```

## 🚀 Features
- **Mouse movement**: Left stick (fast by default, slows when holding RT, or even slower with RS toggle)
- **Scrolling**: Right stick (vertical only)
- **Mouse buttons**:
  - **A** → Left click (hold/release)
  - **B** → Right click (hold/release)
  - **X** → Middle click (hold/release)
- **Keyboard shortcuts**:
  - **LB** → Decrease volume
  - **RB** → Increase volume
  - **Y** → Ctrl+Tab (switch tab once)
  - **LT** → Hold Alt+Tab (task switcher stays open while held)
  - **Back** → Esc (hold/release)
- **Precision toggle**:
  - **RS** → Toggle precision mode (persistent slower pointer)
  - **RT** → Slow mouse while held (stacks with RS toggle)
- **D-Pad** → Arrow