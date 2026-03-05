import config


def dp(*args, **kwargs):
    if config.DEBUG:
        print(*args, **kwargs)
