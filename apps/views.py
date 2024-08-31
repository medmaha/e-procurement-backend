from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
import os
from django.shortcuts import render

from APP_COMPANY import APP_COMPANY


def index(request):
    return HttpResponse(template_200)
    url = os.environ.get("CLIENT_HOST")
    if url:
        return HttpResponseRedirect(url + "/dashboard")
    return HttpResponseBadRequest(template_400)


template_200 = """
    <h1 style='text-align:center'>200 OK!</h1>
    <br/> 
    <p style='text-align:center;'>
        Web server <strong>up and running</strong> successfully
    </p>
"""
template_400 = """
    <h1 style='text-align:center'>404!</h1>
    <br/> 
    <p style='text-align:center'>
        This is not the page you're looking for.
    </p>
"""
