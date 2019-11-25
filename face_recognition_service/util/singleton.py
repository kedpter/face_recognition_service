class Singleton(type):
    _instances = {}

    # c = MyClass()  =>    Singleton.__call__ => MyClass.__new__ => MyClass.__init__
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]
