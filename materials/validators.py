import re
from django.core.exceptions import ValidationError


def validate_url(url):
    youtube_url = re.compile(r'https?://(?:www\.)?youtube\.com/watch\?v=.*')
    if not youtube_url.match(url):
        raise ValidationError("Разрешены ссылки только с youtube.com!")
