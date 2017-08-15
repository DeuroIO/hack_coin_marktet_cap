import locale
def beatifiy_a_number(number):
    locale.setlocale(locale.LC_ALL, 'en_US')
    return locale.format('%d', number, grouping=True)