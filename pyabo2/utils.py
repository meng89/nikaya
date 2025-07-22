def get_last_folder(data: dict):
    last_folder = None
    for _, v in data.items():
        if isinstance(v, dict):
            last_folder = v

    if last_folder is None:
        return data
    else:
        return get_last_folder(last_folder)
