from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """
    Divides the value by the arg.
    Usage: {{ value|div:arg }}
    """
    try:
        return float(value) / float(arg) if arg != 0 else 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    """
    Multiplies the value by the arg.
    Usage: {{ value|mul:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Alias for mul"""
    return mul(value, arg)

@register.filter
def chr_(value):
    """
    Converts an ASCII code to its corresponding character.
    Usage: {{ value|chr_ }} - e.g., 65 becomes 'A'
    """
    try:
        return chr(int(value))
    except (ValueError, TypeError):
        return ''

@register.filter
def dictkey(d, key):
    """
    Gets a value from a dictionary by key.
    Usage: {{ my_dict|dictkey:my_key }}
    """
    try:
        return d.get(key) if d else None
    except (AttributeError, TypeError):
        return None

@register.filter
def replace_blank(value, arg):
    """
    Replaces occurrences of 'arg' in 'value' with an input blank.
    Usage: {{ dialogue|replace_blank:missing_word }}
    """
    if not arg:
        return value
    
    # We use a placeholder to avoid escaping issues when combined with |safe
    replacement = f'<input type="text" class="blank-input" placeholder="..." data-answer="{arg}">'
    return value.replace(arg, replacement)

@register.filter
def split(value, key):
    """
    Splits the string by the given key.
    Usage: {{ "a,b,c"|split:"," }}
    """
    return value.split(key)
