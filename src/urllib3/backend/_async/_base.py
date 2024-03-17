from __future__ import annotations

import typing

from ..._collections import HTTPHeaderDict
from ...contrib.ssa import AsyncSocket, SSLAsyncSocket
from .._base import BaseBackend, ResponsePromise


class AsyncLowLevelResponse:
    """Implemented for backward compatibility purposes. It is there to impose http.client like
    basic response object. So that we don't have to change urllib3 tested behaviors."""

    __internal_read_st: typing.Callable[
        [int | None, int | None], typing.Awaitable[tuple[bytes, bool]]
    ] | None

    def __init__(
        self,
        method: str,
        status: int,
        version: int,
        reason: str,
        headers: HTTPHeaderDict,
        body: typing.Callable[
            [int | None, int | None], typing.Awaitable[tuple[bytes, bool]]
        ]
        | None,
        *,
        authority: str | None = None,
        port: int | None = None,
        stream_id: int | None = None,
    ) -> None:
        self.status = status
        self.version = version
        self.reason = reason
        self.msg = headers
        self._method = method

        self.__internal_read_st = body
        self.closed = True if self.__internal_read_st is None else False
        self._eot = True if self.__internal_read_st is None else False

        # is kept to determine if we can upgrade conn
        self.authority = authority
        self.port = port

        self._stream_id = stream_id

        self.__buffer_excess: bytes = b""
        self.__promise: ResponsePromise | None = None

    @property
    def from_promise(self) -> ResponsePromise | None:
        return self.__promise

    @from_promise.setter
    def from_promise(self, value: ResponsePromise) -> None:
        if value.stream_id != self._stream_id:
            raise ValueError(
                "Trying to assign a ResponsePromise to an unrelated LowLevelResponse"
            )
        self.__promise = value

    @property
    def method(self) -> str:
        """Original HTTP verb used in the request."""
        return self._method

    def isclosed(self) -> bool:
        """Here we do not create a fp sock like http.client Response."""
        return self.closed

    async def read(self, __size: int | None = None) -> bytes:
        if self.closed is True or self.__internal_read_st is None:
            # overly protective, just in case.
            raise ValueError(
                "I/O operation on closed file."
            )  # Defensive: Should not be reachable in normal condition

        if __size == 0:
            return b""  # Defensive: This is unreachable, this case is already covered higher in the stack.

        if self._eot is False:
            data, self._eot = await self.__internal_read_st(__size, self._stream_id)

            # that's awkward, but rather no choice. the state machine
            # consume and render event regardless of your amt !
            if self.__buffer_excess:
                data = (  # Defensive: Difficult to put in place a scenario that verify this
                    self.__buffer_excess + data
                )
                self.__buffer_excess = b""  # Defensive:
        else:
            if __size is None:
                data = self.__buffer_excess
            else:
                data = self.__buffer_excess[:__size]
                self.__buffer_excess = self.__buffer_excess[__size:]

        if __size is not None and (0 < __size < len(data)):
            self.__buffer_excess = data[__size:]
            data = data[:__size]

        if self._eot and len(self.__buffer_excess) == 0:
            self.closed = True

        return data

    def close(self) -> None:
        self.__internal_read_st = None
        self.closed = True


class AsyncBaseBackend(BaseBackend):
    sock: AsyncSocket | SSLAsyncSocket | None  # type: ignore[assignment]

    async def _upgrade(self) -> None:  # type: ignore[override]
        """Upgrade conn from svn ver to max supported."""
        raise NotImplementedError

    async def _tunnel(self) -> None:  # type: ignore[override]
        """Emit proper CONNECT request to the http (server) intermediary."""
        raise NotImplementedError

    async def _new_conn(self) -> AsyncSocket | None:  # type: ignore[override]
        """Run protocol initialization from there. Return None to ensure that the child
        class correctly create the socket / connection."""
        raise NotImplementedError

    async def _post_conn(self) -> None:  # type: ignore[override]
        """Should be called after _new_conn proceed as expected.
        Expect protocol handshake to be done here."""
        raise NotImplementedError

    async def endheaders(  # type: ignore[override]
        self,
        message_body: bytes | None = None,
        *,
        encode_chunked: bool = False,
        expect_body_afterward: bool = False,
    ) -> ResponsePromise | None:
        """This method conclude the request context construction."""
        raise NotImplementedError

    async def getresponse(  # type: ignore[override]
        self, *, promise: ResponsePromise | None = None
    ) -> AsyncLowLevelResponse:
        """Fetch the HTTP response. You SHOULD not retrieve the body in that method, it SHOULD be done
        in the LowLevelResponse, so it enable stream capabilities and remain efficient.
        """
        raise NotImplementedError

    async def close(self) -> None:  # type: ignore[override]
        """End the connection, do some reinit, closing of fd, etc..."""
        raise NotImplementedError

    async def send(  # type: ignore[override]
        self,
        data: (bytes | typing.IO[typing.Any] | typing.Iterable[bytes] | str),
        *,
        eot: bool = False,
    ) -> ResponsePromise | None:
        """The send() method SHOULD be invoked after calling endheaders() if and only if the request
        context specify explicitly that a body is going to be sent."""
        raise NotImplementedError