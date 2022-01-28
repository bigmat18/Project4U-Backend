# --------------- DECORATE ALLA CLASS METHODS ----------------
def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate
# --------------- DECORATE ALLA CLASS'S METHODS ----------------
