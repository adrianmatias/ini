"""The one error base: a refusal the operator reads, as opposed to a programmer error."""


class IniError(Exception):
    """A refusal: the project is not in a shape ini can judge, and the message says why."""
