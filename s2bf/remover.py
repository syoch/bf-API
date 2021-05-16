def auto(src: str) -> str:
    oldsrc = ""
    while src != oldsrc:
        oldsrc = src.replace("<>", "")
        oldsrc = oldsrc.replace("><", "")
        src = oldsrc
    return src
