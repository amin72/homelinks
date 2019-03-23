from django import template


register = template.Library()

@register.filter(name='to_persian')
def date_persian(english_input):
    """
    Convert english numbers to persian or arabic.
    If any other character found in the gived input they won't be changed.
    """
    english_nums = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    persian_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    date = ''
    for c in english_input:
        if c in english_nums:
            date += persian_nums[int(c)]
        else:
            date += c # eg. /:
    return date
