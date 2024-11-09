def get_public_props(obj):
    return [name for name in dir(obj) if not name.startswith('_')]