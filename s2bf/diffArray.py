def asciiArray(src: str):
    return [ord(ch) for ch in src]


def diffArray(src: str):
    ascArr = asciiArray(src)
    diff = []
    val = 0
    for ch in ascArr:
        diff.append(ch-val)
        val = ch
    return diff
