def _auto(src: str) -> str:
    oldsrc = ""
    while src != oldsrc:
        oldsrc = src.replace("<>", "").replace("><", "")
        src = oldsrc
    return src


def auto(src: str) -> str:
    oldsrc = ""
    while src != oldsrc:
        oldsrc = src
        src = _auto(src)
    return src
