from django.http import HttpResponse
from django.shortcuts import redirect


def staff_view(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        profile = request.user.get_profile()

        if profile[0].lower() != "staff":
            return redirect(request.META["HTTP_REFERER"])
        return func(*args, **kwargs)

    return wrapper


def create_requisition(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        permissions = request.permissions

        if permissions["procurement"].get("create_requisition"):
            return func(*args, **kwargs)

        url = request.META.get("HTTP_REFERER", "/")
        return redirect(url)

    return wrapper


def create_requisition_approval(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        permissions = request.permissions

        if permissions["procurement"].get("approve_requisition"):
            perm_name = request.POST.get("perm_name")
            if permissions["procurement"].get(perm_name):
                return func(*args, **kwargs)

            return HttpResponse("Unable to approve request")

        url = request.META.get("HTTP_REFERER", "/")
        return redirect(url)

    return wrapper
