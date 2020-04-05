#!/usr/bin/env python -i
# -*- coding: utf-8 -*-
"""Utilities for this package."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

import axonius_api_client as axonapi

if __name__ == "__main__":
    axonapi.cli.cli_constants.load_dotenv()

    AX_URL = os.environ["AX_URL"]
    AX_KEY = os.environ["AX_KEY"]
    AX_SECRET = os.environ["AX_SECRET"]
    AX_CLIENT_CERT_BOTH = os.environ.get("AX_CLIENT_CERT_BOTH", None) or None
    AX_CLIENT_CERT_CERT = os.environ.get("AX_CLIENT_CERT_CERT", None) or None
    AX_CLIENT_CERT_KEY = os.environ.get("AX_CLIENT_CERT_KEY", None) or None

    def jdump(obj, **kwargs):
        """JSON dump utility."""
        print(axonapi.tools.json_reload(obj, **kwargs))

    ctx = axonapi.Connect(
        url=AX_URL,
        key=AX_KEY,
        secret=AX_SECRET,
        certwarn=False,
        cert_client_both=AX_CLIENT_CERT_BOTH,
        cert_client_cert=AX_CLIENT_CERT_CERT,
        cert_client_key=AX_CLIENT_CERT_KEY,
        log_level_console="debug",
        log_level_api="debug",
        log_level_http="info",
        log_request_attrs=["url", "size"],
        log_console=True,
    )

    ctx.start()

    devices = ctx.devices
    users = ctx.users
    adapters = ctx.adapters
    enforcements = ctx.enforcements
    system = ctx.system

    # import jsonstreams
    # import sys

    # import pathlib

    callbacks = [
        # "first_page",
        # "field_excludes",
        # "field_nulls",
        # "field_flatten",
        "field_titles",
        # "field_joiner",
        # "export_json",
        "export_csv",
    ]

    z = devices.get(
        callbacks=callbacks,
        fields=["network_interfaces", "hostname_preferred"],
        fields_default=False,
        # export_file="blah.json",
        export_file="blah.csv",
        export_overwrite=True,
        explode_field="network_interfaces",
        # max_rows=2,
        # field_excludes=["internal_axon_id"],
        log_once=True,
        # joiner="!!",
        # joiner_trim_len=60,
        # null_value="AAAAA",
    )
    # stdout_orig = sys.__stdout__
    # fd_stdout = os.fdopen(os.dup(stdout_orig.fileno()), stdout_orig.mode)
    # fd_file = open("test.json", "w")
    # callbacks = {
    #     "asset": [axonapi.api.assets.cb_firstpage, axonapi.api.assets.cb_jsonstream]
    # }
    # with jsonstreams.Stream(
    #     jsonstreams.Type.array, fd=fd_file, indent=2, pretty=True
    # ) as stream:
    #     devices.get(
    #         callbacks=callbacks,
    #         stream=stream,
    #         echo_method=axonapi.cli.context.Context.echo_ok,
    #     )

# WIP CODE FOR _download_file
# csv = adapters.get_single("csv")
# adapter_name = csv["name_raw"]
# node_id = csv["node_id"]
# cnx = csv["cnx"][0]
# cnx_uuid = cnx["uuid"]

# ret = adapters._download_file(adapter_name, node_id, cnx_uuid, "file_path")