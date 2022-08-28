import io
from zipfile import ZipFile


def clean_string(string: str) -> str:
    cleaned_string = "".join(char for char in string if char.isalnum())

    return cleaned_string


def download_extract_zip(content):
    with ZipFile(io.BytesIO(content)) as apex_zip_file:
        for zip_info in apex_zip_file.infolist():
            with apex_zip_file.open(zip_info) as apex_file:
                yield zip_info.filename, apex_file


def clean_zip_file(zipFileContainer):
    content = zipFileContainer.read()
    pos = content.rfind(
        '\x50\x4b\x05\x06')  # reverse find: this string of bytes is the end of the zip's central directory.
    if pos > 0:
        zipFileContainer.seek(pos + 20)  # +20: see secion V.I in 'ZIP format' link above.
        zipFileContainer.truncate()
        zipFileContainer.write(
            '\x00\x00')  # Zip file comment length: 0 byte length; tell zip applications to stop reading.
        zipFileContainer.seek(0)

    return zipFileContainer
