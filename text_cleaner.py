import re  #стандартный модуль для регулярных выражений


def normalize_whitespace(text):
    text = re.sub(r"\s+", " ", text)  #re.sub найти и заменить на что то другое
    return text.strip()  # strip убирает пробелы в начале и конце строки


def remove_special_characters(text, keep_punctuation=True):
    # Разрешённые знаки препинания
    allowed_punctuation = ".,?!-" if keep_punctuation else ""

    result = ""

    for char in text:
        # Оставляем буквы, цифры, пробелы и разрешённую пунктуацию
        if char.isalnum() or char.isspace() or char in allowed_punctuation:
            result += char

    return result

def normalize_case(text, lower=True):  #lower встроенный метод строк Python большой маленький текст
    if lower:
        return text.lower()

    return text

def clean_text(text, **kwargs):  # повторный вызов после удаления спецсимволов **kwargs позволяет передавать дополнительные настройки именованными аргументами
    keep_punctuation = kwargs.get("keep_punctuation", True)
    lower = kwargs.get("lower", True)
    
    text = normalize_whitespace(text)
    text = remove_special_characters(text, keep_punctuation)
    text = re.sub(r"\s+([.,?!])", r"\1", text)
    text = normalize_whitespace(text)
    text = normalize_case(text, lower)

    return text