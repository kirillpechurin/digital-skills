from portfolio.internal.http.rest_api.accounts import account
from portfolio.internal.http.rest_api.main_api import main
from portfolio.internal.http.rest_api.private_office_parents import private_office_parents
from portfolio.internal.http.rest_api.private_office_organisation import private_office_organisation

rest_apis = [
    main,
    account,
    private_office_parents,
    private_office_organisation,
]
