class C(object):
    def __init__(self):
        self._a = 'a'
        self._b = 'b'

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, _x):
        self._b = _x

c = C()
print c.b

b = C()
b._b = 8
print b.b
