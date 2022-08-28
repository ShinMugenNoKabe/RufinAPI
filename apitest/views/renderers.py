from json import dumps

from rest_framework import renderers


class JPEGRenderer(renderers.BaseRenderer):
    media_type = "image/jpg"
    format = "jpg"
    charset = None
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, bytes):
            return data

        data_to_response = dumps(data)
        return bytes(data_to_response.encode("utf-8"))
