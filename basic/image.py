from pyquery import PyQuery
import urllib

images = PyQuery("http://mazlumagar.com")('img')

for k, i in enumerate(images):
    urllib.urlretrieve(i.get("src"), "images/{}.jpg".format(k))
