"""Base class which all classes derive from.

Uses a metaclass which contains a private loger by using it's attribute __logger.
"""

from {{cookiecutter.project_slug}}.logger import LoggingBase


class Base(metaclass=LoggingBase):
    ...
