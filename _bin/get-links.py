import json
import re

import requests
from bs4 import BeautifulSoup

links_container_id = "links-container"
linktree_url = "https://linktr.ee/defenseofdemocracy"
link_root = "_links"

response = requests.get(linktree_url)
soup = BeautifulSoup(response.content, "html.parser")

data_block = soup.find_all("script", type="application/json")
data_json = data_block[0].string
data = json.loads(data_json)

links = data["props"]["pageProps"]["links"]

for link in links:
    # print(json.dumps(link))
    url = link["url"]
    priority = link["position"] + 1
    img = None
    img_fn = None
    title = link["title"]

    if "thumbnail" in link:
        img = link["thumbnail"]
    elif "modifiers" in link and "thumbnailImage" in link["modifiers"]:
        img = link["modifiers"]["thumbnailImage"]

    if img:
        img_root = img.split("/")[-1]
        img_fn = "images/" + img_root
        img_response = requests.get(img)
        with open(img_fn, "wb") as f:
            f.write(img_response.content)

    stub = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower())
    stub = re.sub(r"^-+|-+$", "", stub)
    link_fn = f"{link_root}/{stub}.md"

    with open(link_fn, "w") as f:
        f.write(f"---\n")
        f.write(f"title: {title}\n")
        f.write(f"link: {url}\n")
        f.write("image: " + (f"/{img_fn}" if img_fn else "null") + "\n")
        f.write(f"priority: {priority}\n")
        f.write(f"---\n")
        f.write("\n")
