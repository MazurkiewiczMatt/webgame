
def dict_to_display_string(d):
    result = ""
    for k, v in d.items():
        result += (f"{k}: {v}  \r")
    return result
