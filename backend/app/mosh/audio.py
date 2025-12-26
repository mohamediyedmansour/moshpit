import random

def mosh_audio(data: bytes, intensity: int) -> bytes:
    data = bytearray(data)
    length = len(data)

    passes = intensity * random.randint(3, 7)

    for _ in range(passes):
        mode = random.choice(["loop", "crush", "silence", "noise"])

        start = random.randint(0, length - 1)
        size = random.randint(100, 8000 * intensity)
        end = min(start + size, length)

        if mode == "loop":
            chunk = data[start:end]
            insert_at = random.randint(0, length - 1)
            data[insert_at:insert_at] = chunk * random.randint(2, 6)

        elif mode == "crush":
            for i in range(start, end):
                data[i] &= random.choice([0xF0, 0xE0, 0xC0])

        elif mode == "silence":
            for i in range(start, end):
                data[i] = 0

        elif mode == "noise":
            for i in range(start, end):
                data[i] = random.randint(0, 255)

    return bytes(data)
