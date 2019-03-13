"""
figur.zenodo
~~~~~~~~~~~~

This module implements the API to Zenodo.
"""

import requests
import wget


def download(doi, filepath):
    url = f"https://doi.org/{doi}"
    r = requests.get(url)
    record = r.url.split("/")[-1].strip()
    url = f"https://zenodo.org/api/records/{record}"
    r = requests.get(url)
    if r.ok:
        print("Downloading model from Zenodo...")
        print(f"Target directory: {filepath}")
        response = r.json()
        files = response["files"]
        total = sum(file["size"] for file in files)
        for file in files:
            link = file["links"]["self"]
            size = file["size"] / 2 ** 20
            print(f"Total size: {size:.1f} MB")
            fname = file["key"]
            checksum = file["checksum"]
            filename = wget.download(link, filepath)
            return filename
    else:
        raise Excpetion("Unable to download model from Zenodo.")
