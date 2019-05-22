from django import template
import random
register = template.Library()


@register.filter
def randomColor(x):
    colorList = ["warning","default","warning","success","success","warning"]
    rindex = random.randint(int(x),len(colorList)-1)
    selectedColor = colorList[rindex]
    return selectedColor
