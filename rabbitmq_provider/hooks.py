from __future__ import annotations

from typing import Any, Tuple

import requests
from requests.auth import HTTPBasicAuth

from airflow.hooks.base import BaseHook


class RabbitmqHook(BaseHook):
    """
    Sample Hook that interacts with an HTTP endpoint the Python requests library.

    :param method: the API method to be called
    :type method: str
    :param sample_conn_id: connection that has the base API url i.e https://www.google.com/
        and optional authentication credentials. Default headers can also be specified in
        the Extra field in json format.
    :type sample_conn_id: str
    :param auth_type: The auth type for the service
    :type auth_type: AuthBase of python requests lib
    """

    conn_name_attr = "rabbitmq_conn_id"
    default_conn_name = "Rabbitmq"
    conn_type = "sample"
    hook_name = "Sample"

    def __init__(
        self,
        method: str = "POST",
        sample_conn_id: str = default_conn_name,
        auth_type: Any = HTTPBasicAuth,
    ) -> None:
        super().__init__()
        self.sample_conn_id = sample_conn_id
        self.method = method.upper()
        self.base_url: str = ""
        self.auth_type: Any = auth_type

    def get_conn(self, headers: dict[str, Any] | None = None) -> requests.Session:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        session = requests.Session()

        if self.sample_conn_id:
            conn = self.get_connection(self.sample_conn_id)

            if conn.host and "://" in conn.host:
                self.base_url = conn.host
            else:
                # schema defaults to HTTP
                schema = conn.schema if conn.schema else "http"
                host = conn.host if conn.host else ""
                self.base_url = schema + "://" + host

            if conn.port:
                self.base_url = self.base_url + ":" + str(conn.port)
            if conn.login:
                session.auth = self.auth_type(conn.login, conn.password)
            if conn.extra:
                try:
                    session.headers.update(conn.extra_dejson)
                except TypeError:
                    self.log.warning("Connection to %s has invalid extra field.", conn.host)
        if headers:
            session.headers.update(headers)

        return session

    @staticmethod
    def get_connection_form_widgets() -> dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget, BS3PasswordFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import StringField

        return {
            "host": StringField(lazy_gettext("Host"), widget=BS3TextFieldWidget()),
            "port": StringField(lazy_gettext("Port"), widget=BS3TextFieldWidget()),
            "login": StringField(lazy_gettext("Login"), widget=BS3TextFieldWidget()),
            "password": StringField(lazy_gettext("Password"), widget=BS3PasswordFieldWidget()),
        }
