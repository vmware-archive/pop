import pop.hub
repeats = 10000


def test_direct():
    hub = pop.hub.Hub()
    hub.pop.sub.add('tests.mods')
    for i in range(repeats):
        hub.mods.test.ping()


def test_contract():
    hub = pop.hub.Hub()
    hub.pop.sub.add('tests.cmods')
    for i in range(repeats):
        hub.cmods.ctest.cping()


def test_via_underscore():
    hub = pop.hub.Hub()
    hub.pop.sub.add('tests.mods')
    for i in range(repeats):
        hub.mods.test.this()


def test_via_fqn():
    hub = pop.hub.Hub()
    hub.pop.sub.add('tests.mods')
    for i in range(repeats):
        hub.mods.test.fqn()
