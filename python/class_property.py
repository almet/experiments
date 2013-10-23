

def classproperty(meth):
    return property(meth)


class SuperMeta(type):

    def __getattribute__(self, attr):
        attr_ = type.__getattribute__(self, attr)
        if getattr(attr_, 'is_decorated', False):
            return attr_()
        return attr_


class TestClass(object):

    __metaclass__ = SuperMeta

    @classmethod
    @classproperty
    def test(cls):
        return "yeah"

    @classmethod
    def no(cls):
        return "no"


if __name__ == '__main__':
    print(TestClass.test)
    print(TestClass.no())
