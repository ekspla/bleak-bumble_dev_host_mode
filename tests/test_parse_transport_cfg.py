"""Test to parse transport configuration"""

import pytest

import bleak_bumble
from bleak_bumble import (
    BumbleTransportCfg,
    TransportScheme,
    _env_transport_cfg,
    _scheme_delimiter,
    get_default_transport_cfg,
)


def test_parse_transport_cfg():
    assert _env_transport_cfg is None

    transport = str(get_default_transport_cfg())
    scheme_val, *args = transport.split(_scheme_delimiter, 1)

    reproduced_transport = str(
        BumbleTransportCfg(
            TransportScheme.from_string(scheme_val), args[0] if args else None
        )
    )
    assert reproduced_transport == transport

    bleak_bumble._env_transport_cfg = reproduced_transport
    assert str(get_default_transport_cfg()) == transport

    with pytest.raises(ValueError):
        _ = TransportScheme.from_string("bluetooth")
