from base.META import APP_COMPANY


JAZZMIN_SETTINGS = {
    "site_title": APP_COMPANY["name"],
    "site_header": APP_COMPANY["name"],
    "site_brand": APP_COMPANY["name"],
    "site_index": "Procurement",
    "site_logo": APP_COMPANY["logo"],
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "%s - Procurement System" % (APP_COMPANY["name"]),
    "copyright": APP_COMPANY["by"],
    "search_model": [
        "organization.staff",
    ],
    "user_avatar": None,
    "topmenu_links": [
        # {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Home", "url": "admin:index"},
        {"app": "organization"},
        {"app": "procurement"},
        {"app": "vendors", "permissions": ["vendors.add_vendors"]},
    ],
    "usermenu_links": [
        {
            "name": "Help",
            "url": "/admin/help/",
            "new_window": True,
            "icon": "fas fa-help-circle",
        },
        {"model": "auth.user"},
    ],
    "ORDERED_MODEL": {
        # Example: Hide a specific model from an app
        "procurement": [
            "requisition",  # Add the model you want to hide
        ],
    },
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [
        "procurement.unitrequisitionapproval",
        "procurement.departmentrequisitionapproval",
        "procurement.financerequisitionapproval",
        "procurement.procurementrequisitionapproval",
        "procurement.rfqapproval",
        "organization.planitem",
        "vendors.certificates",
    ],
    "order_with_respect_to": ["auth", "accounts", "procurement", "organization"],
    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "auth": [
    #         {
    #             "name": "Accounts",
    #             "url": "accounts/account/",
    #         }
    #     ]
    # },
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "procurement/plan": "fas fa-business-time",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "single",  # Options are --> single, horizontal_tabs, vertical_tabs, callapsible, corousel
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    # "language_chooser": True,
}
