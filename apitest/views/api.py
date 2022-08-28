from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status as res_status

from apitest.views.renderers import JPEGRenderer
from apitest.views.serializers import BarcodeSerializer, SpreadsheetSerializer, QRCodeSerializer


@api_view(["POST"])
def spreadsheet_to_json(request) -> Response:
    spreadsheet = SpreadsheetSerializer(data=request.data)

    spreadsheet.is_valid(raise_exception=True)
    serialized_spreadsheet = spreadsheet.create(spreadsheet.validated_data)

    return Response(serialized_spreadsheet, res_status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([JPEGRenderer])
def generate_qr_code(request, **parameters) -> Response:
    qr_code = QRCodeSerializer(data=parameters)

    qr_code.is_valid(raise_exception=True)
    qr_code_image = qr_code.create(qr_code.validated_data)

    return Response(qr_code_image, res_status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([JPEGRenderer])
def generate_barcode(request, **parameters) -> Response:
    barcode = BarcodeSerializer(data=parameters)

    barcode.is_valid(raise_exception=True)
    barcode_image = barcode.create(barcode.validated_data)

    return Response(barcode_image, res_status.HTTP_200_OK)
