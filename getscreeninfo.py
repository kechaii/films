from screeninfo import get_monitors

def get_size():
    width = 0
    height = 0

    for m in get_monitors():
        width = m.width
        height = m.height

    return width, height