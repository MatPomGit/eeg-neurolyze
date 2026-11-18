"""Argument parser for the stable eeg-athenalyze CLI."""

from __future__ import annotations

import argparse
from pathlib import Path

from eeg_athenalyze.cli_commands import (
    _record_synthetic,
    _run_experiment,
    _analyze_session,
    _plot_session,
    _bids_export,
    _bids_validate,
    _bids_derivatives,
    _device_check,
    _record_physical,
    _openmuse_external,
    _assess_physical,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eeg-athenalyze")
    subcommands = parser.add_subparsers(dest="command", required=True)
    synthetic = subcommands.add_parser(
        "synthetic-record", help="generate and archive simulated EEG"
    )
    synthetic.add_argument("--output", type=Path, required=True)
    synthetic.add_argument("--duration", type=float, default=10.0)
    synthetic.add_argument("--sample-rate", type=float, default=256.0)
    synthetic.add_argument("--seed", type=int, default=0)
    synthetic.add_argument("--condition", default="synthetic")
    synthetic.set_defaults(handler=_record_synthetic)

    experiment = subcommands.add_parser("experiment", help="run an experiment")
    experiment_commands = experiment.add_subparsers(
        dest="experiment_command", required=True
    )
    run = experiment_commands.add_parser("run")
    run.add_argument("name", choices=("eyes-open-closed",))
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--participant", default="sub-001")
    run.add_argument("--session")
    run.add_argument("--sample-rate", type=float, default=256.0)
    run.add_argument("--seed", type=int, default=0)
    run.add_argument(
        "--duration-scale",
        type=float,
        default=1.0,
        help="scale all protocol blocks (use 1 for the specified 30/120/30/120 s)",
    )
    run.set_defaults(handler=_run_experiment)

    analyze = subcommands.add_parser(
        "analyze", help="analyze an archived EO/EC recording without reacquiring data"
    )
    analyze.add_argument("--session", type=Path, required=True)
    analyze.add_argument("--output", type=Path)
    analyze.set_defaults(handler=_analyze_session)

    plot = subcommands.add_parser("plot", help="display EEGZ or recovery journal channels")
    plot.add_argument("--session", type=Path, required=True)
    plot.add_argument("--output", type=Path, help="save .png, .svg or .pdf instead of showing a window")
    plot.add_argument("--time-axis", choices=("samples", "source"), default="samples")
    plot.add_argument("--max-points", type=int, default=8000)
    plot.add_argument("--view", choices=("trace", "psd", "spectrogram", "all"), default="trace")
    plot.add_argument("--channel", help="Select one channel, e.g. AF7")
    plot.add_argument("--start", type=float, default=0.0, help="Start time in nominal seconds")
    plot.add_argument("--duration", type=float, help="Selected duration in nominal seconds")
    plot.add_argument("--scale-uv", type=float, help="Symmetric amplitude limit in microvolts")
    plot.set_defaults(handler=_plot_session)

    bids = subcommands.add_parser("bids", help="EEG-BIDS export and validation")
    bids_commands = bids.add_subparsers(dest="bids_command", required=True)
    bids_export = bids_commands.add_parser("export")
    bids_export.add_argument("--session", type=Path, required=True)
    bids_export.add_argument("--dataset", type=Path, required=True)
    bids_export.set_defaults(handler=_bids_export)
    bids_validate = bids_commands.add_parser("validate")
    bids_validate.add_argument("--dataset", type=Path, required=True)
    bids_validate.set_defaults(handler=_bids_validate)

    derivatives = bids_commands.add_parser("derivatives", help="write custom EO/EC derivatives")
    derivatives.add_argument("--session", type=Path, required=True)
    derivatives.add_argument("--dataset", type=Path, required=True)
    derivatives.set_defaults(handler=_bids_derivatives)

    devices = subcommands.add_parser("devices", help="inspect real EEG device capabilities")
    device_commands = devices.add_subparsers(dest="device_command", required=True)
    check = device_commands.add_parser("check")
    check.add_argument("--device", choices=("muse-athena",), required=True)
    check.set_defaults(handler=_device_check)
    physical = subcommands.add_parser("record", help="acquire actual device EEG")
    physical.add_argument("--device", choices=("muse-athena",), required=True)
    physical.add_argument("--output", type=Path, required=True)
    physical.add_argument("--duration", type=float, default=30.0)
    physical.add_argument("--serial-number", default="")
    physical.add_argument("--mac-address", default="")
    physical.add_argument("--discovery-timeout", type=int, default=15)
    physical.add_argument("--preset", choices=("p21", "p1035", "p1041"), default="p1041")
    physical.add_argument("--low-latency", action=argparse.BooleanOptionalAction, default=True)
    physical.set_defaults(handler=_record_physical)

    external = device_commands.add_parser(
        "openmuse", help="run separate OpenMuse raw capture, without decoding to EEGZ"
    )
    external.add_argument("action", choices=("find", "record"))
    external.add_argument("--openmuse-executable", default="OpenMuse")
    external.add_argument("--address", default="")
    external.add_argument("--duration", type=float, default=60.0)
    external.add_argument("--output", type=Path)
    external.set_defaults(handler=_openmuse_external)

    assess = device_commands.add_parser("assess", help="assess a real Muse archive")
    assess.add_argument("--session", type=Path, required=True)
    assess.add_argument("--report", type=Path, required=True)
    assess.set_defaults(handler=_assess_physical)

    return parser

