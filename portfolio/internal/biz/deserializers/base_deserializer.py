class BaseDeserializer:
    @classmethod
    def deserialize(cls, obj_dict, format_des: str):
        deserializer = cls._get_deserializer(format_des)
        return deserializer(obj_dict)

    @classmethod
    def _get_deserializer(cls, format_des: str):
        raise NotImplemented
