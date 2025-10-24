pages = {}


def page(name):
    def decorator(cls):
        pages[name] = cls
        return cls

    return decorator
