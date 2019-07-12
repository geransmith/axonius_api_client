# -*- coding: utf-8 -*-
"""Axonius API Client package."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import warnings
import logging

import requests

from . import tools
from . import version

LOG = logging.getLogger(__name__)


class HttpClient(object):
    """Wrapper for sending requests usings :obj:`requests.Session`."""

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

    def __init__(self, url, **kwargs):
        """Constructor.

        Args:
            url (:obj:`str` or :obj:`axonius_api_client.tools.UrlParser`):
                Axonius API URL.
            **kwargs:
                connect_timeout (:obj:`int`, optional):
                    Seconds to wait for connection to url to open.

                    Defaults to: 5.
                response_timeout (:obj:`int`, optional):
                    Seconds to wait for response from url.

                    Defaults to: 60.
                verify (:obj:`bool` or :obj:`str`, optional):
                    Enable/Disable SSL cert validation.

                    Defaults to: False.
                verbose (:obj:`bool`, optional):
                    Log request and response verbose attributes.
                    * True = Log verbose attributes,
                    * False = Log brief attributes.
                    * None = Log no attributes.

                    Defaults to: None.
                save_last (:obj:`bool`, optional):
                    Save last request & response to :attr:`last_request` and
                    :attr:`last_response`.

                    Defaults to: False.
                save_history (:obj:`bool`, optional):
                    Add last response to :attr:`history`.

                    Defaults to: False.
                quiet_urllib (:obj:`bool`, optional):
                    Disable urllib3 InsecureRequestWarning and set logging level
                    for urllib3.connectionpool to WARNING.

                    Defaults to: True.

        Notes:
            If verify is False, no SSL cert verification is done.

            If verify is True, SSL cert verification is done using the default CA bundle
            for this OS.

            If verify is str, SSL cert verification is done using CA bundle at path.

            If :attr:`requests.Session.trust_env` is False or verify is False,
            no OS environment variables are used at all.

            If :attr:`requests.Session.trust_env` is True and verify is True, OS env
            variables $REQUESTS_CA_BUNDLE, and $CURL_CA_BUNDLE are used for path to
            CA bundle if set.

            Caveat: If previous request was made with :attr:`session` and
            :attr:`requests.Session.verify` is changed but
            :meth:`requests.Session.close` has not been called, the new verify will
            not be used.

        """
        self._log = LOG.getChild(self.__class__.__name__)
        """:obj:`logging.Logger`: Logger for this object."""

        if isinstance(url, tools.UrlParser):
            url = url.url
        else:
            parsed_url = tools.UrlParser(url=url, default_scheme="https")
            url = parsed_url.url

        self.url = url
        """:obj:`str`: URL of Axonius API."""

        self.last_request = None
        """:obj:`requests.PreparedRequest`: Last request sent."""

        self.last_response = None
        """:obj:`requests.Response`: Last response received."""

        self.save_last = kwargs.get("save_last", False)
        """:obj:`bool`: Save requests to last_request and responses to last_response."""

        self.history = []
        """:obj:`list` of :obj:`requests.Response`: History of responses."""

        self.save_history = kwargs.get("save_history", False)
        """:obj:`bool`: Append all responses to history."""

        self.connect_timeout = kwargs.get("connect_timeout", 5)
        """:obj:`int`: Seconds to wait for connection to url to open."""

        self.response_timeout = kwargs.get("response_timeout", 60)
        """:obj:`int`: Seconds to wait for response from url."""

        self.session = requests.Session()
        """:obj:`requests.Session`: Session object to use."""

        self.session.verify = kwargs.get("verify", False)

        verbose = kwargs.get("verbose", False)
        if verbose is False:
            self.LOG_REQUEST_ATTRS = self.LOG_REQUEST_ATTRS_BRIEF
            self.LOG_RESPONSE_ATTRS = self.LOG_RESPONSE_ATTRS_BRIEF
        elif verbose is True:
            self.LOG_REQUEST_ATTRS = self.LOG_REQUEST_ATTRS_VERBOSE
            self.LOG_RESPONSE_ATTRS = self.LOG_RESPONSE_ATTRS_VERBOSE
        elif verbose is None:
            self.LOG_REQUEST_ATTRS = []
            self.LOG_RESPONSE_ATTRS = []

        if kwargs.get("quiet_urllib", True):
            warnings.simplefilter(
                "ignore", requests.urllib3.exceptions.InsecureRequestWarning
            )
            urllog = logging.getLogger("urllib3.connectionpool")
            urllog.setLevel(logging.WARNING)

    def __call__(
        self,
        path="",
        route="",
        method="get",
        data=None,
        params=None,
        headers=None,
        json=None,
        files=None,
        **kwargs
    ):
        """Create, prepare, and then send a request using :attr:`session`.

        Args:
            path (:obj:`str`, optional):
                Path to append to :attr:`url` for this request.
            method (:obj:`str`, optional):
                Method to use.

                Defaults to: "get".
            data (:obj:`str`, optional):
                Data to send in request body.

                Defaults to: None.
            params (:obj:`dict`, optional):
                Parameters to encode in URL.

                Defaults to: None.
            headers (:obj:`dict`, optional):
                Headers to send in request.

                Defaults to: None.

        Returns:
            :obj:`requests.Response`

        """
        # FUTURE: doc kwargs and files
        url = tools.urljoin(self.url, path, route)

        headers = headers or {}
        headers.setdefault("User-Agent", self.user_agent)

        request = requests.Request(
            url=url,
            method=method,
            data=data,
            headers=headers,
            params=params,
            json=json,
            files=files or [],
        )
        prepped_request = self.session.prepare_request(request=request)

        if self.save_last:
            self.last_request = prepped_request

        if self.LOG_REQUEST_ATTRS:
            msg = ", ".join(self.LOG_REQUEST_ATTRS)
            msg = msg.format(
                request=prepped_request, size=len(prepped_request.body or "")
            )
            self._log.debug(msg)

        send_args = self.session.merge_environment_settings(
            url=prepped_request.url,
            proxies=kwargs.get("proxies", None),
            stream=kwargs.get("stream", None),
            verify=kwargs.get("verify", None),
            cert=kwargs.get("cert", None),
        )

        send_args["request"] = prepped_request
        send_args["timeout"] = (
            kwargs.get("connect_timeout", self.connect_timeout),
            kwargs.get("response_timeout", self.response_timeout),
        )

        response = self.session.send(**send_args)

        if self.save_last:
            self.last_response = response

        if self.save_history:
            self.history.append(response)

        if self.LOG_RESPONSE_ATTRS:
            msg = ", ".join(self.LOG_RESPONSE_ATTRS)
            msg = msg.format(response=response, size=len(response.text or ""))
            self._log.debug(msg)

        return response

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return "{c.__module__}.{c.__name__}(url={url!r})".format(
            c=self.__class__, url=self.url
        )

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @property
    def user_agent(self):
        """Build a user agent string for use in User-Agent header.

        Returns:
            :obj:`str`

        """
        msg = "{name}.{clsname}/{ver}"
        return msg.format(
            name=__name__, clsname=self.__class__.__name__, ver=version.__version__
        )
