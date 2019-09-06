from PIL import Image
import glob, os
im_w = int(input("Ingrese el ancho de la nueva imagen\nR: "))
im_h = int(input("Ingrese la altura de la nueva imagen\nR: "))
size = (im_w, im_h)
for filename in glob.glob("*.jpg"):
    file, ext = os.path.splitext(filename)
    im=Image.open(filename)
    im_resize = im.resize(size, Image.ANTIALIAS)
    im_resize.save('R-'+file +'.jpg')