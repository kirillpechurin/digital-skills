from internal.biz.dao.account_role import AccountRoleDao
from models.account_role import AccountRole

account_roles = [
    AccountRole(
        id=1,
        name="Организация"
    ),
    AccountRole(
        id=2,
        name="Родитель"
    )
]


def seed():
    AccountRoleDao().bulk_create(account_roles)
