import re
from urllib.request import urlopen

url = "https://clinicaltrials.gov/"

page = urlopen(url)

print(page)

# To extract the HTML from the page, first use the HTTPResponse object’s .read() method, 
# which returns a sequence of bytes. 
# Then use .decode() to decode the bytes to a string using UTF-8:
html_bytes = page.read()
html = html_bytes.decode("utf-8")
# print(html)

title_index = html.find("<title>")
# print(title_index)

start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
print(title)


# .*? non-greedily matches all text 
pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title) # Remove HTML tags

print(title)