from rest_framework.response import Response

def render_html_response(context, template_name):
    """
    Render HTML response using the provided serializer and template name.
    """
    return Response(context, template_name=template_name)