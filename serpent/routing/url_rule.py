from typing import Callable
from typing import Iterable


SCHEMES = ["http", "https"]   


class Authority:
    def __init__(self, host_name: str, port_number: int, userinfo=None):
        if userinfo:
            self._user_info = userinfo + "@"
        else:
            self._user_info = ""

        self._host = host_name
        self._port = port_number

        self.authority = self.parse()

    def parse(self):
        return "{0._user_info}{0._host}:{0._port}".format(self)

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host_name: str):
        self._host = host_name

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port_number: str):
        if int(port_number):
            self._port = port_number
        else:
            raise TypeError("Port must be a number")

    @property
    def user_info(self) -> str:
        if self._user_info == "":
            return
        else:
            return self._user_info

    @user_info.setter
    def user_info(self, userinfo: str):
        self._user_info = userinfo
   

class Rule:
    def __init__(self, 
    sch: str, 
    auth: Authority, 
    path: str, 
    end_point: Callable, 
    methods: Iterable) -> None:
        self._scheme = sch
        self._authority = auth.authority
        self._methods = methods
        self._endpoint = end_point
        self._path = path
        self.parse()

    def parse(self):
        self.rule = "{0._scheme}://{0._authority}{0._path}".format(self)

    @property
    def scheme(self) -> str:
        return self._scheme

    @scheme.setter
    def scheme(self, sch):
        if sch in SCHEMES:
            self._scheme = sch
            self.parse()
        else:
            raise TypeError("Scheme {} is not supported".format(sch))

    @property
    def authority(self) -> Authority:
        return self._authority

    @authority.setter
    def authority(self, auth: Authority):
        has_host = hasattr(auth, "host")
        has_port = hasattr(auth, "port")
        has_user_info = hasattr(auth, "user_info")

        if not has_host:
            raise TypeError("Must have host attribute")

        elif not has_port:
            raise TypeError("Must have port attribute")

        elif has_user_info:
            user_info = getattr(auth, "user_info")
            if len(user_info) >= 1:
                if user_info.find("@") == -1:
                    raise TypeError("User Info must contain @")
        else:
            self._authority = auth
            self.parse()

    @property
    def endpoint(self) -> Callable:
        return self._endpoint

    @endpoint.setter
    def endpoint(self, end_point):
        self._endpoint = end_point

    @property
    def method(self) -> Iterable:
        return self._methods
    
    @method.setter
    def method(self, methods):
        self._methods = methods
