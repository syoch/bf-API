table = {
    "pop": ["pop eax"],
    "push": ["push eax"],
    "peek": ["mov eax, DWORD PTR [esp]"],
    "ins": ["add sp, 1"],
    "des": ["sub sp, 1"],
    "inc": ["add eax,1"],
    "dec": ["sub eax,1"],
    "add": ["add eax, {}"]
}
