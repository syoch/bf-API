def auto(src: str) -> str:
    _src = src
    oldsrc = ""
    while src != oldsrc:
        oldsrc = src.replace("<>", "")
        oldsrc = oldsrc.replace("><", "")
        src = oldsrc
    print("optimized: ", len(_src)-len(src), "b")
    return src
