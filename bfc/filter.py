def filter(src: str) -> str:
    dest = ""
    for ch in src:
        if ch in "+-<>.,":
            dest += ch
    return dest
