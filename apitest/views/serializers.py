import io
from csv import DictReader
from io import BytesIO, StringIO
from json import loads, dumps
from zipfile import ZipFile

import requests
from barcode import EAN13, Code39, Code128, EAN8
from barcode.codex import PZN7, Gs1_128
from barcode.ean import JapanArticleNumber, EuropeanArticleNumber14
from barcode.isxn import InternationalStandardBookNumber13, InternationalStandardBookNumber10, \
    InternationalStandardSerialNumber
from barcode.upc import UniversalProductCodeA
from barcode.writer import ImageWriter
from django.utils.translation import gettext_lazy as translate
from pandas import read_excel
from qrcode import QRCode, constants
from rest_framework import serializers

from apitest.utils import clean_string, download_extract_zip, clean_zip_file

DICT_BARCODE_CLASS_BY_FORMAT = {
    "CODE39": Code39,
    "CODE128": Code128,
    "PZN7": PZN7,
    "EAN13": EAN13,
    "EAN8": EAN8,
    "JAN": JapanArticleNumber,
    "ISBN13": InternationalStandardBookNumber13,
    "ISBN10": InternationalStandardBookNumber10,
    "ISSN": InternationalStandardSerialNumber,
    "UPCA": UniversalProductCodeA,
    "EAN14": EuropeanArticleNumber14,
    "GS1128": Gs1_128
}

JSON_TO_APEX_API = "https://json2apex.herokuapp.com/makeApex"

DICT_JSON_KEY_BY_APEX_FILE = {
    "SpreadsheetWrapper.apxc": "apex_class",
    "SpreadsheetWrapper_Test.apxc": "apex_test"
}

class SpreadsheetSerializer(serializers.Serializer):
    spreadsheet = serializers.FileField()
    as_list = serializers.BooleanField()
    to_apex = serializers.BooleanField()

    def validate(self, data):
        return data

    def create(self, validated_data):
        spreadsheet = validated_data.get("spreadsheet")
        as_list = validated_data.get("as_list")
        to_apex = validated_data.get("to_apex")

        spreadsheet_file = read_excel(spreadsheet.read())
        csv_string = StringIO(spreadsheet_file.to_csv(sep=";", index=False, header=True))

        reader = DictReader(csv_string, delimiter=";")

        # Clean Keys
        reader.fieldnames = [clean_string(key) for key in reader.fieldnames]

        if as_list:
            return_json = {}

            # Initialize values as list
            for key in reader.fieldnames:
                return_json[f"{key}_as_list"] = []

            for row in reader:
                for key in reader.fieldnames:
                    return_json[f"{key}_as_list"].append(row[key])
        else:
            return_json = list(reader)

        if to_apex:
            response = requests.post(JSON_TO_APEX_API, data={
                "json": dumps(return_json),
                "className": "SpreadsheetWrapper"
            })

            return_json = {}

            extracted_zip = download_extract_zip(response.content)

            for f_name, f_content in extracted_zip:
                return_json[DICT_JSON_KEY_BY_APEX_FILE.get(f_name)] = f_content.read().decode("utf-8")

        return return_json


class QRCodeSerializer(serializers.Serializer):
    code_data = serializers.CharField()

    def validate(self, data):
        # barcode_format = data.get("barcode_format")
        # class_format = DICT_BARCODE_CLASS_BY_FORMAT.get(barcode_format.upper())
        #
        # # Not found
        # if not class_format:
        #     raise serializers.ValidationError({"barcode_format": translate("The format is not valid.")})
        #
        # data["barcode_format"] = class_format

        return data

    def create(self, validated_data):
        code_data = validated_data.get("code_data")

        try:
            qr_big = QRCode(
                error_correction=constants.ERROR_CORRECT_H
            )

            qr_big.add_data(code_data)
            qr_big.make()

            buffered = BytesIO()
            generated_image = qr_big.make_image().convert("RGB")
            generated_image.save(buffered, format="JPEG")
        except Exception as ex:
            raise serializers.ValidationError({"code_data": [str(ex)]})

        return buffered.getvalue()


class BarcodeSerializer(serializers.Serializer):
    number_code = serializers.CharField()
    barcode_format = serializers.CharField()

    def validate(self, data):
        barcode_format = data.get("barcode_format")
        class_format = DICT_BARCODE_CLASS_BY_FORMAT.get(barcode_format.upper(), None)

        # Not found
        if not class_format:
            raise serializers.ValidationError({"barcode_format": translate("The format is not valid.")})

        data["barcode_format"] = class_format

        return data

    def create(self, validated_data):
        number_code = validated_data.get("number_code")
        barcode_format = validated_data.get("barcode_format")

        try:
            buffered = BytesIO()
            generated_image = barcode_format(number_code, writer=ImageWriter()).render()
            generated_image.save(buffered, format="JPEG")
        except Exception as ex:
            raise serializers.ValidationError({"number_code": [str(ex)]})

        return buffered.getvalue()
