import random


def mosh_image(data: bytes, intensity: int) -> bytes:
    data = bytearray(data)
    length = len(data)

    header_safe = min(2048, length // 10)
    passes = intensity * random.randint(5, 15)

    for _ in range(passes):
        start = random.randint(header_safe, length - 1)
        size = random.randint(50, 5000 * intensity)
        end = min(start + size, length)

        mode = random.choice(["xor", "swap", "overwrite", "loop"])

        if mode == "xor":
            key = random.randint(1, 255)
            for i in range(start, end):
                data[i] ^= key

        elif mode == "swap":
            for i in range(start, end, 3):
                if i + 2 < length:
                    data[i], data[i + 2] = data[i + 2], data[i]

        elif mode == "overwrite":
            for i in range(start, end):
                data[i] = random.randint(0, 255)

        elif mode == "loop":
            chunk = data[start:end]
            insert_at = random.randint(header_safe, length - 1)
            data[insert_at:insert_at] = chunk * random.randint(1, intensity)

    return bytes(data)
