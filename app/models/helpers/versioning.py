import re

import bleach
from bleach.callbacks import nofollow, target_blank

"""
Class to modify strings
"""

# Removes \r
def remove_line_breaks(target_string: str) -> str:
    return target_string.replace('\r', '')


# Removes \n
def strip_line_breaks(target_string: str) -> str:
    return target_string.replace('\n', '').replace('\r', '')


# Removes whitespace and \r, then removes \n if it contains a-z or A-Z
def clean_up_string(target_string):
    if target_string:
        if not re.search('[a-zA-Z]', target_string):
            return strip_line_breaks(target_string).strip().replace(" ", "")
        return remove_line_breaks(target_string).strip()
    return target_string


# Makes html safe
def clean_html(html, allow_link=False):
    if html is None:
        return None
    tags = [
        'b',
        'strong',
        'span',
        'p',
        'em',
        'i',
        'u',
        'center',
        'sup',
        'sub',
        'ul',
        'ol',
        'li',
        'strike',
        'br',
    ]
    attrs = {'*': ['style']}
    if allow_link:
        tags.append('a')
        attrs['a'] = ['href']
    styles = ['text-align', 'font-weight', 'text-decoration']
    cleaned = bleach.clean(html, tags=tags, attributes=attrs, styles=styles, strip=True)
    return bleach.linkify(
        cleaned,
        callbacks=[nofollow, target_blank],
        parse_email=True,  # pytype: disable=wrong-arg-types
    )


# Removes html from text
def strip_tags(html):
    if html is None:
        return None
    return bleach.clean(html, tags=[], attributes={}, styles=[], strip=True)
