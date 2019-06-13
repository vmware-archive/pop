import pop.hub


def test_basic():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    for i in range(10000):
        hub.mods.test.ping()


def test_contract():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.cmods')
    for i in range(10000):
        hub.cmods.ctest.cping()


def test_underscore():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    for i in range(10000):
        hub.mods.test.this()
