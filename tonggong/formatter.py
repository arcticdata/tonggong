_special_characters = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏·° \t\n\r\v\f"""
_translator = str.maketrans('', '', _special_characters)


def remove_special_character(_str: str) -> str:
    """ 过滤掉字符串中的特殊字符 """
    return _str.translate(_translator)
