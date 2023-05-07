import numpy as np
from PIL import Image

img = np.array(Image.open("./Datas/img/2.png").resize((28, 28))) / 255
Image.open("./Datas/img/2.png").resize((28, 28)).show()