import os
import time
from utils import extract_regex, cleaning_images_folder, store_images, create_pdf_from_images
from playwright_scraping import playwright_scraping_url_image
import datetime as dt

from settings import ROOT_DIR


def fliphtml5_to_pdf(url_source):
    cleaning_images_folder(os.path.join(ROOT_DIR, 'images'))
    edition = extract_regex(url_source)
    url_images = playwright_scraping_url_image(edition)
    store_images(url_images)
    time.sleep(1)
    create_pdf_from_images(
        os.path.join(ROOT_DIR, 'images'),
        os.path.join(ROOT_DIR, 'pdfs', f'{edition.replace("/","-")}-{dt.datetime.now():%y-%m-%d}.pdf'))
    cleaning_images_folder(os.path.join(ROOT_DIR, 'images'))


if __name__ == '__main__':
    urls_example = [
        'https://online.fliphtml5.com/vhwco/clwv/',
         'https://online.fliphtml5.com/vhwco/xmww/'
]
    for url in urls_example:
        fliphtml5_to_pdf(url)