from contents.models import Menu


def addMenus(context: dict) -> dict:
    context['menus'] = Menu.objects.order_by('sort_num').all()
    return context
