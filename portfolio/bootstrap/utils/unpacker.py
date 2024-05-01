import zipfile


def unpack():
    with zipfile.ZipFile("bootstrap/files/static.zip") as zip_file:
        zip_file.extractall()
