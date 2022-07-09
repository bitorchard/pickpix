import os
import pwd
import grp
import PIL
from PIL import Image
from PIL import ImageDraw

def test():
    ice_cream = Image.open("secret_lake_mod.png")
    ice_cream = ice_cream.convert('RGBA')

    MAX_ROW = 224
    MAX_COL = 224

    grid_size = ice_cream.size[0] / MAX_COL

    #used_pixels = [p.pixel_index for p in Pixel.objects.all()]

    #overlay = Image.new('L', (ice_cream.size[0], ice_cream.size[1]), 255)
    #draw = ImageDraw.Draw(overlay)

    last_pixel = 0
    lcg_c_val = 6666
    a_big_prime = 50177
    max_pixels = 50176 # 224^2
    for p in range(max_pixels):
        last_pixel = (last_pixel + lcg_c_val) % a_big_prime
        if last_pixel >= max_pixels:
            last_pixel = (last_pixel + lcg_c_val) % a_big_prime
        x_coord = int((last_pixel % MAX_COL) * grid_size)
        y_coord = int(int(last_pixel / MAX_COL) * grid_size)
        #file_path = 'broken_img/%d.jpg' % p
        file_path = '../static/pickpix/broken_img/%d.jpg' % (p+1)
        copy_region = ice_cream.crop((x_coord, y_coord, x_coord+grid_size, y_coord+grid_size))
        piece_im = PIL.Image.new(mode="RGB", size=(int(grid_size), int(grid_size)))
        piece_im.paste(copy_region)
        resize = piece_im.resize((64, 64))
        resize.save(file_path)
        uid = pwd.getpwnam('www-data')[2]
        gid = grp.getgrnam('www-data')[2]
        os.chown(file_path, uid, gid)

test()
