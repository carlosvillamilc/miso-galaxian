def convert_double_digit(num: int) -> str:
    if num < 10:
        return f"0{num}"
    return str(num)
