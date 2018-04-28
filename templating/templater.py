from templating.nodes import *

from templating.Syntax import render_info

def render(request, filename, context=None):
    if context is None:
        context = {}
    request.write(render_info(filename, context))
