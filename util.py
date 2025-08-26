import time, math

def ts():
    return time.strftime("%H:%M:%S")

def log(msg: str):
    print(f"[{ts()}] {msg}")

def shaped(value: float, dz: float, exp: float) -> float:
    """Apply deadzone + exponential curve; keep sign."""
    if abs(value) < dz:
        return 0.0
    u = (abs(value) - dz) / (1 - dz)
    u = u ** exp
    return math.copysign(u, value)

def normalize_trigger(raw: float) -> float:
    """Map trigger value to [0..1] handling drivers reporting -1..1 or 0..1."""
    if raw < -0.001 or raw > 1.001:
        return (raw + 1.0) / 2.0  # -1..1 -> 0..1
    return max(0.0, min(1.0, raw))
