from django import template

register = template.Library()


@register.filter
def status_badge(status):
    styles = {
        "ACEITE": "bg-green-100 text-green-700",
        "PENDENTE": "bg-yellow-100 text-yellow-700",
        "REJEITADO": "bg-red-100 text-red-700",
        "APROVADO": "bg-green-100 text-green-700",
    }

    return styles.get(status, "bg-gray-100 text-gray-700")