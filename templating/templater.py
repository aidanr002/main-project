from templating.nodes import * #Imports the various functions from other templating files

from templating.Syntax import render_info

def render(request, filename, context=None): #Sets up the render function. Uses request and filename.
    if context is None:
        context = {}
    request.write(render_info(filename, context))#Calls the write function given a set of parameters.

#Purpose of function is to streamline the rest of the render functions - one function call instead of 4/5 lines of code.
