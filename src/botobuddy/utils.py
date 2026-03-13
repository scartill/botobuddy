def dslice(d, *keys):
    """Slice a dictionary into a new dictionary using specified keys and optional transformations.

    Args:
        d (dict): The source dictionary to slice.
        *keys: Variable number of key definitions. Each can be:
            - A string: the key to extract.
            - A dict with:
                - 'k': the key to slice from source.
                - 'c': (optional) a callable to cast or convert the value.
                - 'd': (optional) a default value if key is missing.
                - 'n': (optional) the name of the key in the result dictionary.

    Returns:
        dict: A new dictionary containing the sliced and optionally transformed values.
    """
    result = {}

    for k_def in keys:
        if isinstance(k_def, dict):
            key = k_def['k']
            cast = k_def.get('c', None)
            default = k_def.get('d', None)
            name = k_def.get('n', key)
        else:
            key = k_def
            cast = None
            default = None
            name = key

        if key in d:
            value = d[key]

            if cast:
                value = cast(value)
        else:
            value = default

        if value is not None:
            result[name] = value

    return result
