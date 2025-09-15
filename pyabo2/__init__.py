import config

ABO_WEBSITE = "https://agama.buddhason.org"

def dp(*args, **kwargs):
    if config.DEBUG:
        print(*args, **kwargs)
