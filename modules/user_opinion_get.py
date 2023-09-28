def add_pluses_part(message, parts):
    return parts.append(message.text)


def add_minuses_part(message, parts):
    return parts.append(message.text)


def add_rate_part(message, parts):
    try:
        return parts.append(message.text)
    except ValueError:
        return 'bad input'
