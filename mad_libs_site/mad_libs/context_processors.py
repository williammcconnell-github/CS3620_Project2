from .models import MadLib


def mad_lib_list_processor(request):
    mad_lib_list = list(MadLib.objects.all())
    return {'mad_lib_list': mad_lib_list}
