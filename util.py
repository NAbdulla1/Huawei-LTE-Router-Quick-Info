def from_rgb(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def get_signal_bars(bars: int):
    sig = ""
    for i in range(0, 5):
        if i < bars:
            sig += "|"
        else:
            sig += "."
    return sig


def data_unit_calc(bytes: float, unit: str):
    units = ["", "K", "M", "G"]
    unitInd = 0
    while bytes >= 1024:
        bytes /= 1024
        unitInd += 1
    return ("%6.2f %s%s") % (bytes, units[unitInd], unit)
