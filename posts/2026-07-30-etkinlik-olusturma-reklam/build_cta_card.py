from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BG = (23, 23, 23)
PRIMARY = (90, 120, 255)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

logo = Image.open("brand/logo.png").convert("RGBA")
logo_size = 220
logo = logo.resize((logo_size, logo_size))
logo_x = (W - logo_size) // 2
logo_y = 480
img.paste(logo, (logo_x, logo_y), logo)

headline_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 76)
sub_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
button_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 44)

def draw_centered_text(draw, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)

draw_centered_text(draw, 800, "Etkinlik oluşturmak", headline_font, WHITE)
draw_centered_text(draw, 890, "bu kadar kolay.", headline_font, WHITE)
draw_centered_text(draw, 1010, "Aklındakini paylaş, katılsınlar.", sub_font, GRAY)

btn_w, btn_h = 480, 110
btn_x = (W - btn_w) // 2
btn_y = 1180
draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=28, fill=PRIMARY)
bbox = draw.textbbox((0, 0), "Hemen İndir", font=button_font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw.text((btn_x + (btn_w - tw) / 2, btn_y + (btn_h - th) / 2 - bbox[1]), "Hemen İndir", font=button_font, fill=WHITE)

img.save("posts/2026-07-30-etkinlik-olusturma-reklam/cta_card.png")
print("saved")
