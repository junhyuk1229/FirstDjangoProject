from datetime import datetime

from django.core.exceptions import ValidationError


def check_semester_valid(value):
    now = datetime.now()
    if value // 10 < 1000 or now.year < value // 10:
        raise ValidationError(
            ('%(value)s does not contain a valid year'),
            params={'value': value},
        )
    if value % 10 not in [1, 2]:
        raise ValidationError(
            ('%(value)s does not contain a valid semester'),
            params={'value': value},
        )
