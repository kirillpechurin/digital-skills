from enum import Enum

from portfolio.enums.class_property import classproperty


class ErrorEnum(Enum):

    @classproperty
    def not_implemented(cls):
        return "Не реализовано"

    @classproperty
    def account_already_exists(cls):
        return "Аккаунт с таким email уже существует"

    @classproperty
    def account_not_found(cls):
        return "Аккаунт не найден"

    @classproperty
    def account_role_not_found(cls):
        return "Роль аккаунта не найдена"

    @classproperty
    def session_not_found(cls):
        return "Сессия не найдена"

    @classproperty
    def achievement_not_found(cls):
        return "Достижение не найдено"

    @classproperty
    def unique_point_achievement(cls):
        return "Достижение с занятым местом уже используется для другого обучающегося"

    @classproperty
    def unique_achievement_for_children(cls):
        return "Достижение по этой номинации уже добавлено для данного обучающегося"

    @classproperty
    def auth_code_not_found(cls):
        return "Неверный код подверждения"

    @classproperty
    def children_already_exists(cls):
        return "Ребенок с такими данными уже добавлен"

    @classproperty
    def children_not_found(cls):
        return "Ребенок не найден"

    @classproperty
    def children_organisation_already_exists(cls):
        return "Обучающийся уже добавлен к вам"

    @classproperty
    def children_organisation_not_found(cls):
        return "Обучающийся не найден"

    @classproperty
    def employee_not_found(cls):
        return "Сотрудник не найден"

    @classproperty
    def event_not_found(cls):
        return "Данное событие не существует"

    @classproperty
    def events_child_already_exists(cls):
        return "Ребенок уже добавлен на это событие"

    @classproperty
    def event_child_not_found(cls):
        return "Ребенок не добавлен к событию"

    @classproperty
    def organisation_already_exists(cls):
        return "Организация с такими данными уже зарегистрирована"

    @classproperty
    def organisation_not_found(cls):
        return "Организация не найдена"

    @classproperty
    def parents_already_exists(cls):
        return "Родитель с такими данными уже зарегистрирован"

    @classproperty
    def parents_not_found(cls):
        return "Родитель не найден"

    @classproperty
    def request_to_organisation_already_exists(cls):
        return "На это событие уже была подана заявка"

    @classproperty
    def request_to_organisation_not_found(cls):
        return "Запрос не найден"

    @classproperty
    def request_to_organisation_failed(cls):
        return "Принять запрос не удалось, попробуйте позже"

    @classproperty
    def password_is_not_equal(cls):
        return 'Пароли не одинаковы'

    @classproperty
    def select_child_for_request(cls):
        return 'Выберите ребенка, которого нужно зарегистрировать на это событие'
