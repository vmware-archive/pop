#!/usr/bin/python3

import pop.hub


def pop_seed():
    CONFIG = {
            'seed_name': {
                'positional': True,
                'help': 'The name of the project that is being created',
                },
            }

    hub = pop.hub.Hub()
    hub.tools.sub.add('conf', pypath='pop.mods.conf')
    hub.opts = hub.conf.reader.read(CONFIG)
    hub.tools.seed.new()
