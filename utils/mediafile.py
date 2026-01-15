from fastapi import UploadFile
from random import randint

async def save_media(file: UploadFile, folder: str ="root"):
    numero = randint(1,500)
    return f"filefake.com/image/{numero}"

