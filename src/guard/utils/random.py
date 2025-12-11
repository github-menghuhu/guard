import string
from random import choice


def generate_random_string(length: int = 6) -> str:
    """
    生成指定长度的随机字符串

    Args:
        length (int): 字符串长度

    Returns:
        str: 随机字符串，包含字母和数字
    """
    characters = string.ascii_letters + string.digits
    return ''.join(choice(characters) for _ in range(length))
