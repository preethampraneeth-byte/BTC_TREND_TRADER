"""
Configuration Manager

Provides centralized access to application configuration.
Initially, this is a thin wrapper around config.py.
"""

from __future__ import annotations

import config


class ConfigurationManager:
    """
    Centralized access to application configuration.
    """

    def get(self, name):
        """
        Return the value of a configuration setting.

        Raises:
            AttributeError:
                If the configuration value does not exist.
        """
        return getattr(config, name)