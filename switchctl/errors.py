from __future__ import annotations


class SwitchctlError(RuntimeError):
    pass


class ConfigError(SwitchctlError):
    pass


class BackendError(SwitchctlError):
    pass


class NotConfiguredError(SwitchctlError):
    pass


class SelectionError(SwitchctlError):
    pass
