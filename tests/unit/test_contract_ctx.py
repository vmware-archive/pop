# -*- coding: utf-8 -*-

# Import pack
import pop.hub


def test_contract_context():
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods.contract_ctx',
            contracts_pypath='tests.contracts.ctx'
            )
    assert hub.mods.ctx.test() == 'contract executed'
    # Multiple calls have the same outcome
    assert hub.mods.ctx.test() == 'contract executed'


def test_contract_context_update():
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods.contract_ctx',
            contracts_pypath='tests.contracts.ctx'
            )
    assert hub.mods.ctx_update.test(True) == 'contract executed'
    # Multiple calls have the same outcome
    assert hub.mods.ctx_update.test(True) == 'contract executed'


def test_contract_ctx_argument_retrieval():
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods.contract_ctx',
            contracts_pypath='tests.contracts.ctx'
            )
    assert hub.mods.ctx_args.test('yes', yes=True) is True
    assert hub.mods.ctx_args.test('yes', yes=False) is False
    assert hub.mods.ctx_args.test('no', no=False) is False
    assert hub.mods.ctx_args.test('no', no=True) is True
