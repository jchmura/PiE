class Meta(type):
    def __new__(mcs, name, bases, attrs):
        debug_attrs = {}
        for key, val in attrs.items():
            if not key.startswith('__'):
                debug_attrs[key] = Meta._debug(val, name)
            else:
                debug_attrs[key] = val

        return type.__new__(mcs, name, bases, debug_attrs)

    @staticmethod
    def _debug(f, name):
        def wrapper(*args, **kwargs):
            print('{}: {}'.format(name, f.__name__))
            return f(*args, **kwargs)
        return wrapper


class A(metaclass=Meta):
    def __init__(self, x):
        self.x = x

    def add(self, y):
        self.x += y

    def sub(self, y):
        self.x -= y


class B(A):
    def mul(self, y):
        self.x *= y

    def div(self, y):
        self.x /= y


class C(B):
    def mod(self, y):
        self.x %= y

    def sub(self, y):
        super().sub(y)

if __name__ == '__main__':
    x = A(2)
    x.add(3)
    x.sub(10)

    y = B(8)
    y.add(4)
    y.div(6)

    z = C(20)
    z.mod(3)
    z.sub(9)
