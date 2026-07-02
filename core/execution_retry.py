"""
BTC Trend Trader Professional v4
Milestone M3

Execution Retry Engine

Responsibilities
----------------
- Retry failed execution requests
- Retry transient failures
- Configurable retry count
- Configurable retry delay

This module performs NO:
- MT5 logic
- Trade management
- Risk calculations
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class RetryResult:
    """
    Result of retry execution.
    """

    success: bool
    result: Any = None
    retries: int = 0
    error: Optional[str] = None


class RetryEngine:
    """
    Generic retry engine.

    Intended for execution operations.
    """

    DEFAULT_RETRYABLE = (
        TimeoutError,
        ConnectionError,
    )

    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 0.5,
        retry_exceptions=None,
    ):

        self.max_retries = max(1, int(max_retries))

        self.retry_delay = max(0.0, retry_delay)

        if retry_exceptions is None:
            retry_exceptions = self.DEFAULT_RETRYABLE

        self.retry_exceptions = tuple(retry_exceptions)

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    def configure(
        self,
        *,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
    ):

        if max_retries is not None:
            self.max_retries = max(1, int(max_retries))

        if retry_delay is not None:
            self.retry_delay = max(0.0, retry_delay)

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
        func: Callable,
        *args,
        **kwargs,
    ) -> RetryResult:
        """
        Execute callable with retry.
        """

        retries = 0

        while True:

            try:

                result = func(*args, **kwargs)

                return RetryResult(
                    success=True,
                    result=result,
                    retries=retries,
                )

            except self.retry_exceptions as exc:

                retries += 1

                if retries > self.max_retries:

                    return RetryResult(
                        success=False,
                        retries=retries,
                        error=str(exc),
                    )

                time.sleep(self.retry_delay)

            except Exception as exc:

                return RetryResult(
                    success=False,
                    retries=retries,
                    error=str(exc),
                )

    # --------------------------------------------------
    # Compatibility
    # --------------------------------------------------

    def run(
        self,
        func: Callable,
        *args,
        **kwargs,
    ):
        """
        Backward-compatible helper.

        Returns callable result or raises RuntimeError.
        """

        result = self.execute(
            func,
            *args,
            **kwargs,
        )

        if result.success:
            return result.result

        raise RuntimeError(result.error)

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    @staticmethod
    def is_retryable(
        exception: Exception,
    ) -> bool:
        """
        Hook for future MT5-specific retry checks.
        """

        return isinstance(
            exception,
            (
                TimeoutError,
                ConnectionError,
            ),
        )