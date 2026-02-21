"""Test that all dataset URLs in catalogs return HTTP 200 status.

This test extracts URLs from all catalog entries and checks that the
remote resources are reachable via HEAD or GET requests. It does NOT
download data - only checks availability.

Note: These tests are often flaky because they depend on external URLs
which may change or become unavailable without notice.
"""

import re
import ssl
import urllib.request

import intake
import pytest

pytestmark = pytest.mark.skip(
    reason="External URLs frequently return 404; run manually to check availability"
)


@pytest.fixture(scope="module")
def cat():
    return intake.open_catalog("master.yaml")


def _resolve_url(item):
    """Extract a testable URL from a catalog item's urlpath."""
    try:
        urlpath = item.urlpath
    except Exception:
        return None

    if not isinstance(urlpath, str):
        return None

    # Strip simplecache:: prefix
    url = re.sub(r"^simplecache::", "", urlpath)
    # Strip zip:// prefix (e.g. "zip://*.nc::")
    url = re.sub(r"^zip://[^:]*::", "", url)

    # Skip FTP URLs
    if url.startswith("ftp://"):
        return None

    # Skip URLs that still contain unresolved template vars
    if "{{" in url:
        return None

    return url


def _get_all_items(cat):
    """Walk catalog and collect (name, item) pairs for non-catalog entries."""
    items = []
    for name in cat.walk(depth=5):
        try:
            entry = cat[name]
        except Exception:
            continue
        if isinstance(entry, intake.catalog.local.YAMLFileCatalog):
            continue
        if isinstance(entry, intake.source.derived.GenericTransform):
            continue
        items.append((name, entry))
    return items


def _check_url(url, timeout=20):
    """Check URL returns a success status code.

    Tries HEAD first, falls back to GET with Range header.
    Returns (status_code, ok) tuple.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {"User-Agent": "Mozilla/5.0 remote_climate_data URL check"}

    # Try HEAD first
    try:
        req = urllib.request.Request(url, method="HEAD", headers=headers)
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return resp.status, resp.status < 400
    except urllib.error.HTTPError as e:
        if e.code in (403, 405):
            pass  # Try GET fallback
        else:
            return e.code, False
    except Exception:
        pass

    # Fallback: GET with Range header (download only 1 byte)
    try:
        get_headers = {**headers, "Range": "bytes=0-0"}
        req = urllib.request.Request(url, headers=get_headers)
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return resp.status, resp.status < 400
    except urllib.error.HTTPError as e:
        return e.code, False
    except Exception as e:
        return str(e), False


# Build test parameters at module level
_cat = intake.open_catalog("master.yaml")
_all_items = _get_all_items(_cat)

# Collect items with resolvable URLs
_url_items = []
for name, item in _all_items:
    url = _resolve_url(item)
    if url is not None:
        _url_items.append((name, url))


@pytest.mark.parametrize("name,url", _url_items, ids=[t[0] for t in _url_items])
def test_url_returns_200(name, url):
    """Check that dataset URL is reachable (HTTP 200)."""
    status, ok = _check_url(url)
    assert ok, f"{name}: URL returned {status} — {url}"
