'''
Routines to verify the working environment etc.
'''
# Import python libs
import os


def env(hub):
    '''
    Verify that the directories specified in the system exist
    '''
    for key in hub.opts:
        if key.endswith('_dir'):
            try:
                os.makedirs(hub.opts[key])
            except OSError:
                pass

