from enum import Enum

from portfolio.enums.class_property import classproperty


class SuccessEnum(Enum):

    @classproperty
    def update(cls):
        return "Успешно обновлено!"

    @classproperty
    def register_request(cls):
        return "Успешно зарегистрировали заявку, ждите ответа от организации!"

    @classproperty
    def add(cls):
        return "Успешно добавлено!"

    @classproperty
    def delete(cls):
        return "Успешно удален!"

    @classproperty
    def reject(cls):
        return "Отклонено"