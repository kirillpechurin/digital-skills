from portfolio.internal.http.views.accounts import account
from portfolio.internal.http.views.main_api import main
from portfolio.internal.http.views.private_office_parents import private_office_parents
from portfolio.internal.http.views.private_office_organisation import private_office_organisation

apis = [
    main,
    account,
    private_office_parents,
    private_office_organisation,
]
