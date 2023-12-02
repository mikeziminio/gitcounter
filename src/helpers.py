
def format_number(num: float | int, decimal_places: int = 0, delimiter: str = " ") -> str:
    return f"{num:_.{decimal_places}f}".replace("_", delimiter)
