import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import sys
sys.setdefaultencoding( "utf-8" )
text = ''
lines = open('tweepy_result_washed_already.csv', 'r').readlines()
for line in lines:
    text += line.split(',')[0]
with open('full_text.txt', 'w+') as output:
    output.write(text)

from PIL import Image
import numpy as np
my_mask = np.array(Image.open('/Users/hectorli/PycharmProjects/twitter/logo_clean.jpg'))
world_cloud = WordCloud(background_color='white',
                        max_words=2000, scale=3
                        ).generate(text)
world_cloud.to_file("result_square1.png")
image_colors = ImageColorGenerator(my_mask)

plt.imshow(world_cloud, interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(world_cloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(my_mask, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()
world_cloud.to_file("result_square2.png")