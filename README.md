# 🎮 Gamepad → Cursor

Control your PC cursor with a standard gamepad controller.

## 🛠 Requirements
```bash
pip install pygame pynput
```

## ▶️ Running
After cloning to gamepad_cursor folder, run:
```bash
python3 -m gamepad_cursor.app
```

## 🚀 Features
- **Mouse movement**: Left stick (fast by default, slows when holding RT)
- **Scrolling**: Right stick
- **Mouse buttons**:
  - **A** → Left click (hold/release)
  - **B** → Right click (hold/release)
  - **RB** → Middle click (hold/release)
- **Keyboard shortcuts**:
  - **X** → Decrease volume
  - **Y** → Increase volume
  - **LB** → Ctrl+Tab (switch tab once)
  - **LT** → Hold Alt+Tab (task switcher stays open while held)
  - **Start** → Enable/disable all controls
- **Precision toggle**:
  - **RT** → Toggle precision mode (slower pointer).
- **D-Pad** → Arrow keys (←/→/↑/↓ with press/release).