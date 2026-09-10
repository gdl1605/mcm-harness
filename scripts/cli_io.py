"""Use a stable UTF-8 wire format for CLI output, including redirected pipes."""

import sys


def configure_output() -> None:
    # Only CLI entrypoints call this; importing a tool does not alter host streams.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
