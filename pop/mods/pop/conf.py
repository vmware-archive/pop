'''
Convenience wrappers to make using the conf system as easy and seamless as possible
'''


def integrate(
        hub,
        imports,
        override=None,
        cli=None,
        roots=None,
        home_root=None,
        loader='json',
        logs=True):
    '''
    Load the conf sub and run the integrate sequence.
    '''
    hub.pop.sub.add('pop.mods.conf')
    hub.conf.integrate.load(
        imports,
        override,
        cli=cli,
        roots=roots,
        home_root=home_root,
        loader=loader,
        logs=logs)
