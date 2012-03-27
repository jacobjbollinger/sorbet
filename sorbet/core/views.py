from django.template.response import TemplateResponse


def home(request):
    template = u'core/home.html'
    context = None
    return TemplateResponse(request, template, context)


def register(request):
    template = u'core/register.html'
    context = None
    return TemplateResponse(request, template, context)


def login(request):
    template = u'core/login.html'
    context = None
    return TemplateResponse(request, template, context)


def logout(request):
    template = u'core/logout.html'
    context = None
    return TemplateResponse(request, template, context)


def panel(request):
    template = u'core/panel.html'
    context = None
    return TemplateResponse(request, template, context)
