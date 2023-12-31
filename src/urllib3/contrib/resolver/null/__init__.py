from __future__ import annotations

import socket
import typing

from ..protocols import BaseResolver, ProtocolResolver
from ..utils import is_ipv4, is_ipv6


class NullResolver(BaseResolver):
    protocol = ProtocolResolver.NULL
    implementation = "dummy"

    def __init__(self, *patterns: str, **kwargs: typing.Any):
        if "server" in kwargs:
            kwargs.pop("server")
        if "port" in kwargs:
            kwargs.pop("port")
        super().__init__(None, None, *patterns, **kwargs)

    def recycle(self) -> BaseResolver:
        return self

    def close(self) -> None:
        pass  # no-op

    def is_available(self) -> bool:
        return True

    def getaddrinfo(
        self,
        host: bytes | str | None,
        port: str | int | None,
        family: socket.AddressFamily,
        type: socket.SocketKind,
        proto: int = 0,
        flags: int = 0,
        *,
        quic_upgrade_via_dns_rr: bool = False,
    ) -> list[
        tuple[
            socket.AddressFamily,
            socket.SocketKind,
            int,
            str,
            tuple[str, int] | tuple[str, int, int, int],
        ]
    ]:
        if host is None:
            host = "localhost"

        if port is None:
            port = 0
        if isinstance(port, str):
            port = int(port)
        if port < 0:
            raise socket.gaierror("Servname not supported for ai_socktype")

        if isinstance(host, bytes):
            host = host.decode("ascii")

        if is_ipv4(host):
            return [
                (
                    socket.AF_INET,
                    type,
                    6,
                    "",
                    (
                        host,
                        port,
                    ),
                )
            ]
        elif is_ipv6(host):
            return [
                (
                    socket.AF_INET6,
                    type,
                    17,
                    "",
                    (
                        host,
                        port,
                        0,
                        0,
                    ),
                )
            ]

        raise socket.gaierror(f"Tried to resolve '{host}' using the NullResolver")


__all__ = ("NullResolver",)