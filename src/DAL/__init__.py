from logging import Logger

def get_databases():
    raise NotImplementedError()
    return [
        {
            'name': 'mongo',
            'factory': 'Some Factory Function that deconstructs logger and args and sends to DB class'
        }
    ]


default = 'fs'