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
  - **Y** → Middle click (hold/release)
- **Keyboard shortcuts**:
  - **X** → Space (hold/release)
  - **LB** → Decrease volume
  - **RB** → Increase volume
  - **LS Button** → Ctrl+Tab (hold/release)
  - **RS Button** → Alt+Tab (hold/release)
  - **LT** → (unused)
  - **Back** → Esc (hold/release)
- **Precision toggle**:
  - **RT** → Slow mouse while held (stacks with RS toggle)
  - **RS Button** → Alt+Tab (hold/release)
- **D-Pad** → Arrow keys (hold/release)
- **Start** → Toggle controls (with rumble feedback if supported)