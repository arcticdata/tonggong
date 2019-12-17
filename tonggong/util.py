def padding_base64(base64_str: str) -> str:
    num = len(base64_str) % 4
    num = 4 - num if num else 0
    return base64_str + '=' * num
