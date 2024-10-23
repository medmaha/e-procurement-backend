import os

APP_COMPANY = {
    "name": "Any Company",
    "description": "Any description",
    "logo": "img/logo/brand.png",
    "industry": "Any Industry",
    "website": "https://www.anycompany.com",
    "address": "Any Address",
    "established_date": "2007-05-07",
    "client_site": os.environ.get("CLIENT_HOST"),
    "provider": {
        "name": "Any Provider",
        "logo": "img/logo/brand.png",
        "website": "https://anyprovider.com",
    },
}


# APP_COMPANY = {
#     "name": "IntraSoft Ltd",
#     "alias": "IntraSoft",
#     "logo": "img/brand/logo.png",
#     "industry": "Technology",
#     "website": "https://intrasoft.com",
#     "address": "Brusubi | Kombo North | WCR | The Gambia",
#     "established_date": "2007-05-07",
#     "description": "IntraSoft Ltd is an ICT company registered in The Gambia in 2007. We offer fully integrated services providing a whole spectrum of ICT solutions for business development, public sector support, and Non-Government Organizations in their quest for effective decision making for their various organizational goals.",
# }

APP_CONSTANTS = {
    "GROUPS": {
        "Annual Procurement Approver": {
            "name": "Annual Plan Approver",
        },
        "Annual Procurement Approver GPPA": {
            "name": "Annual Plan Approver GPPA",
        },
    }
}
