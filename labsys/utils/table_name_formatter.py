def format_tablename(classname):
    formatted = ''
    for index, char in enumerate(classname):
        if char.isupper():
            char = char.lower()
            if index is not 0:
                char = '_' + char
        formatted += char
    return formatted
