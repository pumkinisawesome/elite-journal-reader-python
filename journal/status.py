class Status:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Status, cls).__new__(cls, *args, **kwargs)
            print("Creating Status")
        else:
            print("Reusing Status")

        return cls._instance

    def __init__(self):
        pass

    def set_attribute(self, attribute, value):
        setattr(
            self,
            attribute,
            value if value is not None else getattr(self, attribute, None),
        )

    def get_attribute(self, attribute):
        return getattr(self, attribute, None)
