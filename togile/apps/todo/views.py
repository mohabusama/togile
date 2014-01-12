from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from togile.settings import FRONTEND_APP_LISTS, FRONTEND_APP_INDEX


def index_view(request):
    if request.user.is_authenticated():
        # redirect to lists
        response = HttpResponseRedirect(FRONTEND_APP_LISTS)
        response.set_cookie('togile', request.user.id)
        return response

    return redirect(FRONTEND_APP_INDEX)


def logout_view(request):
    response = HttpResponseRedirect(FRONTEND_APP_INDEX)
    if request.user.is_authenticated():
        response.delete_cookie('togile')
        logout(request)

    return response
