import string


def is_correct_link(link: str) -> bool:
    for char in link:
        if char not in string.ascii_uppercase + string.ascii_lowercase + string.digits:
            return False
    return True


def is_correct_source(link: str) -> bool:
    return link.startswith("https://")
