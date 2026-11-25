"""Unrelated rendering helper."""


def render_table(rows):
    return "\n".join(str(row) for row in rows)
