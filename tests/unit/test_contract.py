from pop.contract import Contracted


def test_contracted_shortcut():
    def f(hub):
        pass

    c = Contracted(hub=None, contracts=[], func=f)
    c.contract_functions['pre'] = [None]  # add some garbage so we raise if we try to evaluate contracts

    c()
