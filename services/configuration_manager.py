"""
Configuration Manager

Provides centralized access to application configuration.
"""

from __future__ import annotations

import config


class ConfigurationManager:
    """
    Centralized access to application configuration.
    """

    def get(self, name):
        """
        Return a configuration value.

        Raises:
            AttributeError:
                If the configuration setting does not exist.
        """

        if not hasattr(config, name):
            raise AttributeError(
                f"Unknown configuration setting: '{name}'"
            )

        return getattr(config, name)

    def has(self, name):
        """
        Return True if a configuration value exists.
        """

        return hasattr(config, name)