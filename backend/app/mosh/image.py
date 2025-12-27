from PIL import Image
import numpy as np
import random
import io


def clamp(arr):
    return np.clip(arr, 0, 255).astype(np.uint8)


def mosh_pixels(
    image_bytes: bytes,
    intensity: int = 5,
) -> bytes:
    """
    intensity: 1–10
    """

    # ---- Load image safely ----
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(img).astype(np.int16)  # allow overflow safely

    h, w, _ = arr.shape
    passes = intensity * random.randint(3, 8)

    for _ in range(passes):
        mode = random.choice([
            "channel_shift",
            "block_swap",
            "line_smear",
            "color_burn",
            "pixel_loop",
        ])

        # -------------------------------
        # CHANNEL SHIFT (classic datamosh)
        # -------------------------------
        if mode == "channel_shift":
            ch = random.randint(0, 2)
            dx = random.randint(-30, 30) * intensity
            dy = random.randint(-30, 30) * intensity
            arr[..., ch] = np.roll(arr[..., ch], shift=(dy, dx), axis=(0, 1))

        # -------------------------------
        # BLOCK SWAP (spatial destruction)
        # -------------------------------
        elif mode == "block_swap":
            bw = random.randint(16, 64) * intensity
            bh = random.randint(16, 64) * intensity

            x1 = random.randint(0, w - bw)
            y1 = random.randint(0, h - bh)
            x2 = random.randint(0, w - bw)
            y2 = random.randint(0, h - bh)

            block1 = arr[y1:y1+bh, x1:x1+bw].copy()
            block2 = arr[y2:y2+bh, x2:x2+bw].copy()

            arr[y1:y1+bh, x1:x1+bw] = block2
            arr[y2:y2+bh, x2:x2+bw] = block1

        # -------------------------------
        # LINE SMEAR (feedback trails)
        # -------------------------------
        elif mode == "line_smear":
            y = random.randint(0, h - 1)
            smear_len = random.randint(50, w) // intensity
            direction = random.choice([-1, 1])

            for i in range(smear_len):
                x = (i * direction) % w
                arr[y, x] = arr[y, (x - 5) % w]

        # -------------------------------
        # COLOR BURN / OVERDRIVE
        # -------------------------------
        elif mode == "color_burn":
            gain = random.randint(20, 80) * intensity
            channel = random.randint(0, 2)
            arr[..., channel] += gain * random.choice([-1, 1])

        # -------------------------------
        # PIXEL LOOP FEEDBACK
        # -------------------------------
        elif mode == "pixel_loop":
            x = random.randint(0, w - 50)
            y = random.randint(0, h - 50)
            bw = random.randint(20, 80)
            bh = random.randint(20, 80)

            chunk = arr[y:y+bh, x:x+bw]
            for _ in range(random.randint(2, intensity + 2)):
                dx = random.randint(-40, 40)
                dy = random.randint(-40, 40)
                ny = max(0, min(h - bh, y + dy))
                nx = max(0, min(w - bw, x + dx))
                arr[ny:ny+bh, nx:nx+bw] = chunk

    # ---- Clamp + rebuild ----
    arr = clamp(arr)
    out = Image.fromarray(arr, "RGB")

    buf = io.BytesIO()
    out.save(buf, format="JPEG", quality=92, subsampling=0)

    return buf.getvalue()
