# -*- coding: utf-8 -*-
"""Constants for this package."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os

from . import __package__ as PACKAGE_ROOT
from . import tools


def get_var_int(name, default):
    """Pass."""
    try:
        return int(os.environ.get(name, default) or default)
    except Exception:
        return default


def get_var_bool(name, default):
    """Pass."""
    try:
        value = os.environ.get(name, default)
        return tools.coerce_bool(value)
    except Exception:
        return default


PAGE_SIZE = get_var_int("AX_PAGE_SIZE", 2000)
PAGE_SLEEP = get_var_int("AX_PAGE_SLEEP", 0)
PAGE_CACHE = get_var_bool("AX_PAGE_CACHE", False)
CONNECT_TIMEOUT = get_var_int("AX_CONNECT_TIMEOUT", 5)
RESPONSE_TIMEOUT = get_var_int("AX_RESPONSE_TIMEOUT", 900)

MAX_PAGE_SIZE = 2000
""":obj:`int`: Maximum page size that REST API allows."""

GUI_PAGE_SIZES = [25, 50, 100]
""":obj:`list` of :obj:`int`: Valid page sizes for GUI paging."""

LOG_REQUEST_ATTRS_BRIEF = [
    "request to {request.url!r}",
    "method={request.method!r}",
    "size={size}",
]
""":obj:`list` of :obj:`str`: Request attributes to log when verbose=False."""

LOG_REQUEST_ATTRS_VERBOSE = [
    "request to {request.url!r}",
    "method={request.method!r}",
    "headers={request.headers}",
    "size={size}",
]
""":obj:`list` of :obj:`str`: Request attributes to log when verbose=True."""

LOG_RESPONSE_ATTRS_BRIEF = [
    "response from {response.url!r}",
    "method={response.request.method!r}",
    "status={response.status_code!r}",
    "size={size}",
]
""":obj:`list` of :obj:`str`: Response attributes to log when verbose=False."""

LOG_RESPONSE_ATTRS_VERBOSE = [
    "response from {response.url!r}",
    "method={response.request.method!r}",
    "headers={response.headers}",
    "status={response.status_code!r}",
    "reason={response.reason!r}",
    "elapsed={response.elapsed}",
    "size={size}",
]
""":obj:`list` of :obj:`str`: Response attributes to log when verbose=True."""

LOG_FMT_CONSOLE = "%(levelname)-8s [%(name)s] %(message)s"
LOG_FMT_FILE = "%(asctime)s %(levelname)-8s [%(name)s:%(funcName)s()] %(message)s"

LOG_DATEFMT_CONSOLE = "%m/%d/%Y %I:%M:%S %p"
LOG_DATEFMT_FILE = "%m/%d/%Y %I:%M:%S %p"

LOG_LEVEL_CONSOLE = "debug"
LOG_LEVEL_FILE = "debug"
LOG_LEVEL_HTTP = "debug"
LOG_LEVEL_AUTH = "debug"
LOG_LEVEL_API = "debug"
LOG_LEVEL_PACKAGE = "debug"

LOG_LEVELS_STR = ["debug", "info", "warning", "error", "fatal"]
LOG_LEVELS_STR_CSV = ", ".join(LOG_LEVELS_STR)
LOG_LEVELS_INT = [getattr(logging, x.upper()) for x in LOG_LEVELS_STR]
LOG_LEVELS_INT_CSV = ", ".join([format(x) for x in LOG_LEVELS_INT])

LOG_FILE_PATH = os.getcwd()
LOG_FILE_PATH_MODE = 0o700
LOG_FILE_NAME = "{pkg}.log".format(pkg=PACKAGE_ROOT)
LOG_FILE_MAX_MB = 5
LOG_FILE_MAX_FILES = 5

LOG_NAME_STDERR = "handler_stderr"
LOG_NAME_STDOUT = "handler_stdout"
LOG_NAME_FILE = "handler_file"

CSV_FIELDS = {
    "device": ["id", "serial", "mac_address", "hostname", "name"],
    "user": ["id", "username", "mail", "name"],
    "sw": ["hostname", "installed_sw_name"],
}
SETTING_UNCHANGED = ["unchanged"]
DEFAULT_NODE = "master"
CSV_KEYS_META = {
    "file": "file_path",
    "is_users_csv": "is_users",
    "is_installed_sw": "is_installed_sw",
    "id": "user_id",
    "csv_http": "resource_path",
    "csv_share": "resource_path",
    "csv_share_username": "username",
    "csv_share_password": "password",
}
CSV_ADAPTER = "csv"
DEBUG_MATCHES = False

DEFAULT_PERM = "ReadOnly"

VALID_PERMS = ["Restricted", "ReadWrite", "ReadOnly"]
