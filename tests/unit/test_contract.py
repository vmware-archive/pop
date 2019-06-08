from pop.contract import Contracted


def test_contracted_shortcut():
    def f(hub):
        pass

    c = Contracted(hub="a hub", contracts=[], func=f, ref=None, name=None)
    c.contract_functions['pre'] = [None]  # add some garbage so we raise if we try to evaluate contracts

    c()
