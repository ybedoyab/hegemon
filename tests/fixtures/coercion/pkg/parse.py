"""parse_value should ignore non-integers instead of raising."""


def parse_value(raw):
    if raw is None:
        return None
    return int(raw)
