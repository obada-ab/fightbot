from io import BytesIO
from PIL import Image, ImageDraw
import requests

dl = 175

def get_image_from_url(url):

    try:
        response = requests.head(url, allow_redirects=True)
        size = response.headers.get('content-length', -1)
    except:
        return "invalid image url :("
    if int(size) > 10 * (1 << 20):
        return "image too large :("

    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
    except:
        return "invalid image url :("

    img = img.resize((dl, dl))
    
    return img

def generate_image(arg1, arg2=None):

    if not arg2 is None:
        images = arg1
        healths = [x.get_health() for x in arg2]
    else:
        images = [arg1]
        healths = [100]

    if len(images) > 4:
        return None

    dx = 10
    dy = 10
    dh = 5
    x = 400
    y = dy * 4 + dl if len(images) <= 2 else dy * 5 + dl * 2

    image = Image.new("RGBA", (x, y))
    draw = ImageDraw.Draw(image)

    draw.rectangle([(0, 0), image.size], (25,129,153))
    draw.rectangle((dx, dy, x - dx, y - dy), (31,110,132))

    for i, img in enumerate(images):
        posx = dx * 2 + (dl + dx) * (i % 2)
        if i % 2 == 0 and i == len(images) - 1:
            posx = x // 2 - dl // 2
        
        posy = dy * 2 + (dl + dy) * (i // 2)

        image.paste(img, (posx, posy), img)
        draw.rectangle([(posx, posy + dl - dh), (posx + dl - 1, posy + dl)], (255,0,0,200))
        if healths[i] > 0:
            draw.rectangle([(posx, posy + dl - dh),
            (posx + dl * healths[i] // 100 - 1, posy + dl)],
            (0,255,0,200))

    return image

def generate_bytes(img):
    arr = BytesIO()
    img.save(arr, format='PNG')
    arr.seek(0)
    return arr
