<h1 align="center">

![urllib3](https://github.com/jawah/urllib3.future/raw/main/docs/_static/logo.png)

</h1>

<p align="center">
  <a href="https://pypi.org/project/urllib3-future"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/urllib3-future.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/urllib3-future"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/urllib3-future.svg?maxAge=86400" /></a>
  <br><small>urllib3.future is as BoringSSL is to OpenSSL but to urllib3 (except support is available!)</small>
</p>

⚡ urllib3.future is a powerful, *user-friendly* HTTP client for Python.<br>
⚡ urllib3.future goes beyond supported features while remaining compatible.<br>
⚡ urllib3.future brings many critical features that are missing from the Python standard libraries:

- Thread safety.
- Connection pooling.
- Client-side SSL/TLS verification.
- File uploads with multipart encoding.
- Helpers for retrying requests and dealing with HTTP redirects.
- Support for gzip, deflate, brotli, and zstd encoding.
- HTTP/1.1, HTTP/2 and HTTP/3 support.
- Proxy support for HTTP and SOCKS.
- Multiplexed connection.
- 93% test coverage.

urllib3.future is powerful and easy to use:

```python
>>> import urllib3
>>> resp = urllib3.request("GET", "https://httpbin.org/robots.txt")
>>> resp.status
200
>>> resp.data
b"User-agent: *\nDisallow: /deny\n"
>>> resp.version
20
```

## Installing

urllib3.future can be installed with [pip](https://pip.pypa.io):

```bash
$ python -m pip install urllib3.future
```

You either do 

```python
import urllib3
```

Or...

```python
import urllib3_future
```

Doing `import urllib3_future` is the safest option for you as there is a significant number of projects that
require `urllib3`.

## Notes

- **It's a fork**

⚠️ Installing urllib3.future shadows the actual urllib3 package (_depending on installation order_). 
The semver will always be like _MAJOR.MINOR.9PP_ like 2.0.941, the patch node  is always greater or equal to 900.

Support for bugs or improvements is served in this repository. We regularly sync this fork
with the main branch of urllib3/urllib3 against bugfixes and security patches if applicable.

- **OS Package Managers**

Fellow OS package maintainers, you cannot _just_ build and ship this package to your package registry.
As it override `urllib3` and due to its current criticality, you'll have to set:

`URLLIB3_NO_OVERRIDE=true python -m build`. Set `URLLIB3_NO_OVERRIDE` variable with "**true**" in it.

It will prevent the override.

## Compatibility with downstream

You should _always_ install the downstream project prior to this fork.

e.g. I want `requests` to be use this package.

```
python -m pip install requests
python -m pip install urllib3.future
```

We suggest using the package [**Niquests**](https://github.com/jawah/niquests) as a drop-in replacement for **Requests**. 
It leverages urllib3.future capabilities.

## Documentation

urllib3.future has usage and reference documentation at [urllib3future.readthedocs.io](https://urllib3future.readthedocs.io).

## Contributing

urllib3.future happily accepts contributions.

## Security Disclosures

To report a security vulnerability, please use the GitHub advisory disclosure form.

## Sponsorship

If your company benefits from this library, please consider sponsoring its
development.
