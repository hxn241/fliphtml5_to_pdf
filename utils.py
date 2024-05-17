import re
import requests
import shutil
from PIL import Image
import os

from settings import ROOT_DIR


def store_images(final_list):
    for page, url in enumerate(final_list):
        # Image URL and filename
        image_url = url
        filename = f"pic_{str(page).zfill(4)}.jpg"

        # Retrieving image without interruptions
        r = requests.get(image_url, stream=True)

        # Check image
        if r.status_code == 200:

            # Preventing the downloaded image’s size from being zero.
            r.raw.decode_content = True

            # Open a local file
            with open(os.path.join(ROOT_DIR, 'images', f'{filename}'), 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image successfully Downloaded: ', filename)
        else:
            print('Image Couldn\'t be retrieved')


def create_pdf_from_images(images_directory, pdf_path):
    try:
        images = [
            Image.open(os.path.join(images_directory, f))
            for f in sorted(os.listdir(images_directory))
            if f.endswith('.jpg')
        ]

        images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
        print(f"PDF guardado con éxito: {pdf_path}")

    except Exception as e:
        print(f"Imposible guardar PDF. {e}")


def cleaning_images_folder(folder_path):
    archivos = os.listdir(folder_path)
    for file in archivos:
        full_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(full_path):
                os.remove(full_path)
                # print(f'Archivo {ruta_completa} eliminado exitosamente.')
        except Exception as e:
            print(f'Error al eliminar {full_path}: {e}')


def extract_regex(url_source):
    edition = None
    patron = r'\/([a-zA-Z0-9]+\/[a-zA-Z0-9]+)\/'
    try:
        edition = re.search(patron, url_source).group(1)
    except Exception as e:
        print(e)
    finally:
        return edition