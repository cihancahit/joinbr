from users.models import UserProfileModel

import unicodedata
import re


def get_user(request):
    user = request.user
    if user.is_authenticated:
        user1 = UserProfileModel.objects.get(user=user)
    else:
        user1 = "anonymous"
    return user1


def strip_accents(s):
    """
    Sanitarize the given unicode string and remove all special/localized
    characters from it.

    Category "Mn" stands for Nonspacing_Mark
    """
    try:
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )
    except:
        return s


def remove_special(s):
    a = re.sub('[^A-Za-z0-9]+', '_', s)
    return a


def is_int(anyNumberOrString):
    try:
        int(anyNumberOrString)
        return True
    except ValueError:
        return False


def slugify(title):
    symbol_mapping = (
        (' ', '-'),
        ('.', '-'),
        (',', '-'),
        (')', '-'),
        ('(', '-'),
        ('!', '-'),
        ('?', '-'),
        ('&', '-'),
        ("'", '-'),
        ('"', '-'),
        ('ə', 'e'),
        ('ı', 'i'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
        ('ş', 's'),
        ('ç', 'c'),
    )
    title_url = title.strip().lower()

    for before, after in symbol_mapping:
        title_url = title_url.replace(before, after)

    return title_url
