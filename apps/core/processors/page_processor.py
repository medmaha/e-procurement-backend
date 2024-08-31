from apps.accounts.models import Account


def get_url_query_from_string(query: str):
    data = {}
    try:
        queries = query.split("&")
        for query in queries:
            key, value = query.split("=")

            if key and value:
                data[key] = value
        return data
    except:
        return data


def verification_user(request):
    user_identifier = request.get_signed_cookie("v-identifier", default=None)

    if "/account/signup" in request.get_full_path():
        _profile = Account.objects.filter(unique_id=user_identifier).first()

        if _profile:
            homepage = "account_signup"
            return {"v_user": _profile, "homepage": homepage}

    return {"homepage": "index"}


def page_headings(request):
    context = {**verification_user(request)}

    return context
