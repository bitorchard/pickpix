import os
import pwd
import grp
from PIL import Image
from PIL import ImageDraw
from pathlib import Path

def draw_mask(used_pixels, size=2050, rows=224, cols=224):
    mask_file = Path('images/mask.jpg')
    if mask_file.is_file():
        overlay = Image.open(mask_file)
    else:
        overlay = draw_grid()

    grid_size = size / rows
    draw = ImageDraw.Draw(overlay)

    for p in used_pixels:
        x_coord = int((p % cols) * grid_size)
        y_coord = int(int(p / cols) * grid_size)
        draw.rectangle((x_coord, y_coord, int(x_coord+grid_size), int(y_coord+grid_size)), fill=0)

    overlay.save(mask_file)

    uid = pwd.getpwnam('www-data')[2]
    gid = grp.getgrnam('www-data')[2]
    os.chown(mask_file, uid, gid)
    return overlay

def draw_grid(size=2050, rows=224, cols=224):
    grid_file = 'images/grid.jpg'
    step_count = rows
    grid = Image.new(mode='L', size=(size, size), color=255)

    draw = ImageDraw.Draw(grid)
    y_start = 0
    y_end = grid.height
    step_size = grid.width / step_count

    for x in range(cols):
        line = ((int(x*step_size), y_start), (int(x*step_size), y_end))
        draw.line(line, fill="#ddd")

    x_start = 0
    x_end = grid.width

    for y in range(rows):
        line = ((x_start, int(y*step_size)), (x_end, int(y*step_size)))
        draw.line(line, fill="#ddd", width=1)

    del draw

    grid.save(grid_file)

    uid = pwd.getpwnam('www-data')[2]
    gid = grp.getgrnam('www-data')[2]
    os.chown(grid_file, uid, gid)
    return grid

def render_secret_image2():
    secret_file_src = 'images/secret_lake_mod.png'
    secret_file_render = '../static/pickpix/secret.jpg'

    secret = Image.open(secret_file_src)
    secret = secret.convert('RGBA')

    overlay = draw_mask(used_pixels=[0, 4, 8, 20, 40, 200, 5000, 6666, 7777])

    secret.paste(overlay, mask=overlay)
    secret = secret.convert('RGB')
    secret.save(secret_file_render)

    uid = pwd.getpwnam('www-data')[2]
    gid = grp.getgrnam('www-data')[2]
    os.chown(secret_file_render, uid, gid)

draw_grid()
render_secret_image2()
