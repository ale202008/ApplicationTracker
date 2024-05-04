from django import template

register = template.Library()

@register.filter
def remove_https(url):
    url_without_https = url.replace('https://', '')
    url_without_https = url_without_https.replace("www.", "")
    if url_without_https.endswith('/'):
        url_without_https = url_without_https[:-1]  # Remove the final slash
    return url_without_https