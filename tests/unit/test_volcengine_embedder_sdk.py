"""Focused tests for the optional Volcengine SDK import guard."""

import importlib
import sys

import pytest

from openviking.models.embedder import volcengine_embedders



def test_volcengine_embedder_module_imports_without_sdk():
    """The module must stay importable when volcenginesdkarkruntime is absent."""
    module_name = "openviking.models.embedder.volcengine_embedders"
    sdk_name = "volcenginesdkarkruntime"
    module = importlib.import_module(module_name)
    sdk_was_present = sdk_name in sys.modules
    original_sdk = sys.modules.get(sdk_name)

    try:
        sys.modules[sdk_name] = None
        reloaded = importlib.reload(module)
        assert reloaded.volcenginesdkarkruntime is None
    finally:
        if sdk_was_present:
            sys.modules[sdk_name] = original_sdk
        else:
            sys.modules.pop(sdk_name, None)
        importlib.reload(module)


def test_create_sync_ark_raises_clear_error_without_sdk(monkeypatch):
    monkeypatch.setattr(volcengine_embedders, "volcenginesdkarkruntime", None)

    with pytest.raises(RuntimeError, match="volcenginesdkarkruntime not installed"):
        volcengine_embedders._create_sync_ark({})


def test_create_async_ark_raises_clear_error_without_sdk(monkeypatch):
    import asyncio

    monkeypatch.setattr(volcengine_embedders, "volcenginesdkarkruntime", None)

    with pytest.raises(RuntimeError, match="volcenginesdkarkruntime not installed"):
        asyncio.run(volcengine_embedders._create_async_ark({}))
