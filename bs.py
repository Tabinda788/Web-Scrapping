from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://clinicaltrials.gov/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# print(soup.get_text())


total_imgs = soup.find_all("img")
print(len(total_imgs))


# image1, image2 = soup.find_all("img")

# print(image1)

for img in total_imgs:
    src = img["src"]
    print(src)


print(soup.title)


print(soup.title.string)

print(soup.find_all("img", src="/ct2/html/images/pulldown.png"))

