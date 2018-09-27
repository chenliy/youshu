import tesserocr
from PIL import Image

image = Image.open(r'C:\Users\ll\Desktop\123.jpg')
result = tesserocr.image_to_text(image)
print(result)

#灰度处理
image = image.convert('L')
image.show()
result = tesserocr.image_to_text(image)
print(result)

#二值化处理

threshold = 100
table = []

for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table,'1')
image.show()
result = tesserocr.image_to_text(image)
print(result)