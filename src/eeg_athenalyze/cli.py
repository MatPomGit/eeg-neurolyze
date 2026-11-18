"""Stable command-line entry point for EEG Neurolyze."""

from __future__ import annotations

from eeg_athenalyze.cli_parser import build_parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and return the selected command's exit status."""
    arguments = build_parser().parse_args(argv)
    return arguments.handler(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
