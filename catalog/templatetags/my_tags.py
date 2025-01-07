from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.inclusion_tag("catalog/product_detail.html")
def render_product_card(product):
    return {"product": product}