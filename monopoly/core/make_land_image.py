from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from PIL import Image, ImageOps
from PIL import ImageFont, ImageDraw, ImageColor
from django.conf import settings
import secrets

def draw_text_45_into(text: str, into, at, land_text_color):
	# Measure the text area
	ttf_path = settings.MEDIA_ROOT + "/TaipeiSansTCBeta-Regular.ttf"
	font = ImageFont.truetype(ttf_path, 50)
	wi, hi = font.getsize (text)

	# Copy the relevant area from the source image
	img = into.crop((at[0], at[1], at[0] + hi, at[1] + wi))

	# Rotate it backwards
	img = img.rotate(270, expand = 1, fillcolor="rgb(205,230,208)")

	# Print into the rotated area
	d = ImageDraw.Draw(img)
	d.multiline_text((0, 0), text, font = font, fill = land_text_color)

	# Rotate it forward again
	img = img.rotate(45, expand = 1)

	# Insert it back into the source image
	# Note that we don't need a mask
	into.paste(img, at, img)

def save_image(img, pos, image_field):
	buffer = BytesIO()
	img = img.resize((256,256))
	"""rotate image to fit the board"""
	if (pos <= 19 and pos >= 11):
		img = img.transpose(Image.ROTATE_270)
	elif (pos <= 30 and pos >= 21):
		img = img.transpose(Image.ROTATE_180)
	elif (pos <= 39 and pos >= 31):
		img = img.transpose(Image.ROTATE_90)
	img.save(fp=buffer, format='PNG')
	pillow_image = ContentFile(buffer.getvalue())
	secrets_token = secrets.token_hex()
	image_field.save(str(pos) + "_" + secrets_token  + ".png", InMemoryUploadedFile(
		 pillow_image,       # file
		 None,               # field_name
		 str(pos) + "_" + secrets_token + ".png",           # file name
		 'image/png',       # content_type
		 pillow_image.tell,  # size
		 None)               # content_type_extra
	)

def replace_color_with_theother(img, origin, rgb_color, land_background_color):
	default_color = (205,230,208)
	change_color = land_background_color
	w, h = (img.width, img.height)
	for i in range(w):
		for j in range(h):
			data = (img.getpixel((i,j)))
			data_rgb = (data[0], data[1], data[2])
			bias = 90
			bias2 = 5
			if  default_color[0] - bias2 <= data_rgb[0] <= default_color[0] + bias2 and default_color[1] - bias2 <= data_rgb[1] <= default_color[1] + bias2 and default_color[2] - bias2 <= data_rgb[2] <= default_color[2] + bias2:
				img.putpixel((i, j), change_color)
			elif  origin[0] - bias <= data_rgb[0] <= origin[0] + bias and origin[1] - bias <= data_rgb[1] <= origin[1] + bias and origin[2] - bias <= data_rgb[2] <= origin[2] + bias:
				img.putpixel((i, j), rgb_color)
			

def make_construction_land_image(pos, description, value, color, image_field, land_background_color, land_text_color):
	img = Image.new('RGB', (500, 500))
	w, h = (img.width, img.height) 
	# create rectangle image
	draw = ImageDraw.Draw(img)
	draw.rectangle([(0, 0), (w, h)], fill = land_background_color, outline="black", width=4)  
	draw.rectangle([(0, 0), (w, h//5)], fill = color, outline="black", width=4)
	ttf_path = settings.MEDIA_ROOT + "/TaipeiSansTCBeta-Regular.ttf"
	font = ImageFont.truetype(ttf_path, 50)
	# draw.line(((0, h//2), (w, h//2)), "gray")
	# draw.line(((w//2, 0), (w//2, h)), "gray")
	draw.multiline_text((w//2, h//2), description, anchor="ms", fill = land_text_color, font=font, align="center")
	draw.multiline_text((w//2, 4*h//5), "$" + str(value), anchor="ms", fill = land_text_color, font=font, align="center")
	save_image(img, pos, image_field)

def make_chance_land_image(pos, description, value, color, image_field, land_background_color, land_text_color):
	rgb_color = ImageColor.getrgb(color)
	img = Image.open(settings.MEDIA_ROOT + "/chance.png")
	orange_color = (250, 128, 27)
	img = img.convert("RGB")
	replace_color_with_theother(img, orange_color, rgb_color, land_background_color)
	draw = ImageDraw.Draw(img)
	ttf_path = settings.MEDIA_ROOT + "/TaipeiSansTCBeta-Regular.ttf"
	font = ImageFont.truetype(ttf_path, 50)
	draw.multiline_text((250, 125), description, anchor="ms", fill= land_text_color, font=font, align="center")
	save_image(img, pos, image_field)

def make_start_land_image(pos, description, color, image_field, land_background_color, land_text_color):
	rgb_color = ImageColor.getrgb(color)
	img = Image.open(settings.MEDIA_ROOT + "/start.png")
	img = img.convert("RGBA")
	draw_text_45_into(description, img, (40,40), land_text_color)
	red_color = (229,29,36)
	replace_color_with_theother(img, red_color, rgb_color, land_background_color)
	save_image(img, pos, image_field)

def make_jail_land_image(pos, color, image_field, land_background_color):
	rgb_color = ImageColor.getrgb(color)
	img = Image.open(settings.MEDIA_ROOT + "/jail.png")
	img = img.convert("RGB")
	orange_color = (241,146,0)
	replace_color_with_theother(img, orange_color, rgb_color, land_background_color)
	save_image(img, pos, image_field)

def make_park_land_image(pos, color, image_field, land_background_color):
	rgb_color = ImageColor.getrgb(color)
	img = Image.open(settings.MEDIA_ROOT + "/park.png")
	img = img.convert("RGB")
	red_color = (253,27,51)
	replace_color_with_theother(img, red_color, rgb_color, land_background_color)
	save_image(img, pos, image_field)

def make_infra_land_image(pos, description, value, color, image_field, land_background_color, land_text_color):
	rgb_color = ImageColor.getrgb(color)
	img = Image.open(settings.MEDIA_ROOT + "/infra.png")
	img = img.convert("RGB")
	black_color = (0, 0, 0)
	replace_color_with_theother(img, black_color, rgb_color, land_background_color)
	draw = ImageDraw.Draw(img)
	ttf_path = settings.MEDIA_ROOT + "/TaipeiSansTCBeta-Regular.ttf"
	font = ImageFont.truetype(ttf_path, 50)
	w, h = (img.width, img.height)
	draw.multiline_text((w//2, 125), description, anchor="ms", fill=land_text_color, font=font, align="center")
	draw.multiline_text((w//2, 7*h//8), "$" + str(value), anchor="ms", fill=land_text_color, font=font, align="center")
	save_image(img, pos, image_field)

def make_one_land_image(land, land_background_color, land_text_color):
	land_type = land.land_type.land_type
	pos = land.pos
	description = land.description
	value = land.value
	color = land.color
	image_field = land.image
	if str(image_field)[4:11] != "default":
		image_field.delete()

	land_background_color = ImageColor.getrgb(land_background_color)
	land_text_color = ImageColor.getrgb(land_text_color)
	if land_type == "可建造土地":
		make_construction_land_image(pos, description, value, color, image_field, land_background_color, land_text_color)
	elif land_type == "機會":
		make_chance_land_image(pos, description, value, color, image_field, land_background_color, land_text_color)
	elif land_type == "起點":
		make_start_land_image(pos, description, color, image_field, land_background_color, land_text_color)
	elif land_type == "監獄":
		make_jail_land_image(pos, color, image_field, land_background_color)
	elif land_type == "基礎設施(不可蓋房子)":
		make_infra_land_image(pos, description, value, color, image_field, land_background_color, land_text_color)
	elif land_type == "公園":
		make_park_land_image(pos, color, image_field, land_background_color)