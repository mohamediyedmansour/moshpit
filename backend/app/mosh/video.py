import random


def mosh_video(data: bytes, intensity: int) -> bytes:
    data = bytearray(data)
    length = len(data)

    passes = intensity * random.randint(10, 25)

    for _ in range(passes):
        start = random.randint(0, length - 1)
        size = random.randint(500, 15000 * intensity)
        end = min(start + size, length)

        mode = random.choice(["overwrite", "xor", "loop"])

        if mode == "overwrite":
            for i in range(start, end):
                data[i] = random.randint(0, 255)

        elif mode == "xor":
            key = random.randint(1, 255)
            for i in range(start, end):
                data[i] ^= key

        elif mode == "loop":
            chunk = data[start:end]
            insert_at = random.randint(0, length - 1)
            data[insert_at:insert_at] = chunk * random.randint(1, 3)

    return bytes(data)
