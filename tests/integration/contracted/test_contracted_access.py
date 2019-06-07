from pop.hub import Hub


def hub():
    hub = Hub()
    hub.tools.sub.add(
        pypath='tests.integration.contracted.mods',
        subname='mods',
    )
    return hub


def test_two_hubs():
    h = hub()

    # we should be able to call a function with two hubs as parameters
    h.mods.contracted_access.two_hubs(h)


def test_contracted_different_mod_dereferenced():
    # create hub
    # call hub,
    # function on module calls another function with a different hub
    # Does that other function use the correct hub?
    # Does it call applicable contracts?
    # And does it work correctly with a MockHub?
    h1 = hub()
    h2 = hub()
    h1.mods.contracted_access.hub2_dereferenced_call(h2)

    assert h1.mods.contracted_access.hub1_called
    assert h2.mods.contracted_access.hub2_called

    assert h1.contract_called
    assert h2.contract_called

    # contract_hub = testing.ContractHub(hub)


def test_contracted_different_mod_direct():
    h1 = hub()
    h2 = hub()

    h1.mods.contracted_access.hub2_direct_call(h2)

    assert h1.mods.contracted_access.hub1_called
    assert h2.mods.contracted_access.hub2_called

    assert h1.contract_called
    assert h2.contract_called

    # TODO: how should '_' work on mock hubs? does it work correctly?


def test_contracted_different_mod_direct_kwargs():
    # create hub
    # call hub,
    # function on module calls another function with a different hub
    # Does that other function use the correct hub?
    # Does it call applicable contracts?
    # And does it work correctly with a MockHub?
    h1 = hub()
    h2 = hub()
    h1.mods.contracted_access.hub2_direct_call_kwargs(h2)

    assert h1.mods.contracted_access.hub1_called
    assert h2.mods.contracted_access.hub2_called

    assert h1.contract_called
    assert h2.contract_called

    # contract_hub = testing.ContractHub(hub)
