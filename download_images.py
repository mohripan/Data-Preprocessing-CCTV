import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

search_terms = [
    "city footage",
    "city background",
    "street",
    "conditions in the city",
    "housing areas"
]

# Create an output directory for images
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_image_resolution(image_content):
    with BytesIO(image_content) as f:
        img = Image.open(f)
        return img.size

total_images_downloaded = 0
while total_images_downloaded < 1000:
    for term in search_terms:
        search_url = f"https://duckduckgo.com/html/?q={requests.utils.quote(term)}"

        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        image_urls = []
        for link in soup.find_all("a", class_="tile--img__link"):
            image_urls.append(link["href"])

        for i, url in enumerate(image_urls):
            response = requests.get(url, headers=headers)

            # Check if the image resolution is at least 1080x1920
            image_resolution = get_image_resolution(response.content)
            if image_resolution[0] < 1080 or image_resolution[1] < 1920:
                continue

            file_name = f"{term.replace(' ', '_')}_{total_images_downloaded+1}.jpg"
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"Downloaded {file_name}")
            total_images_downloaded += 1

            if total_images_downloaded >= 1000:
                break

        if total_images_downloaded >= 1000:
            break

print("All images downloaded.")