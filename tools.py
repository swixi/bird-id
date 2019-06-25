# try to parse a float from a string
def try_parse_float(val):
    try:
        return float(val)
    except ValueError:
        return None