"""CLI command implementations, separate from argument parsing."""

from __future__ import annotations

import argparse
import sys

from eeg_athenalyze.archive import save_recording
from eeg_athenalyze.analysis.spectral import compare_resting_alpha
from eeg_athenalyze.experiments.eyes_open_closed import (
    EyesOpenClosedConfig,
    run_eyes_open_closed,
)
from eeg_athenalyze.recording import SyntheticConfig, generate_synthetic_recording
from eeg_athenalyze.reporting.html_report import write_resting_report


def _record_synthetic(arguments: argparse.Namespace) -> int:
    try:
        config = SyntheticConfig(
            sample_rate_hz=arguments.sample_rate,
            seed=arguments.seed,
        )
        recording = generate_synthetic_recording(
            arguments.duration,
            config=config,
            condition=arguments.condition,
        )
        path = save_recording(recording, arguments.output)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(
        f"Saved simulated recording {recording.recording_id}: "
        f"{len(recording.samples_uv)} samples, {len(recording.channel_names)} channels "
        f"at {recording.sample_rate_hz:g} Hz -> {path}"
    )
    return 0


def _run_experiment(arguments: argparse.Namespace) -> int:
    try:
        defaults = EyesOpenClosedConfig()
        config = EyesOpenClosedConfig(
            stabilization_seconds=defaults.stabilization_seconds
            * arguments.duration_scale,
            eyes_open_seconds=defaults.eyes_open_seconds * arguments.duration_scale,
            break_seconds=defaults.break_seconds * arguments.duration_scale,
            eyes_closed_seconds=defaults.eyes_closed_seconds
            * arguments.duration_scale,
            participant_id=arguments.participant,
            session_id=arguments.session,
            synthetic=SyntheticConfig(
                sample_rate_hz=arguments.sample_rate,
                seed=arguments.seed,
            ),
        )
        result = run_eyes_open_closed(arguments.output, config=config)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Saved raw simulated EEG: {result.archive_path}")
    print(f"Saved EO/EC report: {result.report_path}")
    return 0


def _analyze_session(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.archive import load_recording

    try:
        recording = load_recording(arguments.session)
        comparison = compare_resting_alpha(recording)
        report_path = write_resting_report(
            recording,
            comparison,
            arguments.output or arguments.session.with_suffix(".html"),
        )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Saved resting-state report: {report_path}")
    return 0



def _plot_session(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.visualization import inspect_signal, plot_signal

    try:
        if arguments.view == "trace" and arguments.start == 0 and arguments.duration is None and arguments.channel is None and arguments.scale_uv is None and arguments.time_axis == "source":
            result = plot_signal(arguments.session, output=arguments.output,
                                 time_axis="source", max_points=arguments.max_points)
        else:
            if arguments.time_axis == "source":
                raise ValueError("Source timestamps are supported only for the unfiltered trace view")
            result = inspect_signal(arguments.session, output=arguments.output,
                                    view=arguments.view, channel=arguments.channel,
                                    start=arguments.start, duration=arguments.duration,
                                    scale_uv=arguments.scale_uv, max_points=arguments.max_points)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"EEG plot failed: {error}", file=sys.stderr)
        return 1
    print(f"Saved EEG plot: {result}" if result else "EEG plot window closed")
    return 0


def _bids_export(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.bids import export_bids

    try:
        dataset = export_bids(arguments.session, arguments.dataset)
    except (OSError, ValueError, ImportError, RuntimeError) as error:
        print(f"BIDS export failed: {error}", file=sys.stderr)
        return 1
    print(f"Exported EEG-BIDS candidate: {dataset}")
    print("Run BIDS validation before claiming compliance.")
    return 0


def _bids_validate(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.bids import validate_bids

    try:
        status = validate_bids(arguments.dataset)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"BIDS validation failed: {error}", file=sys.stderr)
        return 1
    print(f"BIDS validator exit status: {status}")
    return status


def _bids_derivatives(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.derivatives import export_alpha_derivatives

    try:
        path = export_alpha_derivatives(arguments.session, arguments.dataset)
    except (OSError, ValueError) as error:
        print(f"BIDS derivatives failed: {error}", file=sys.stderr)
        return 1
    print(f"Saved custom alpha-power derivative: {path}")
    return 0


def _device_check(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.muse_athena import device_info

    try:
        import json
        print(json.dumps(device_info(), indent=2))
        print("BrainFlow layout only; physical connection not verified.")
        return 0
    except (RuntimeError, ValueError) as error:
        print(f"Device diagnostics failed: {error}", file=sys.stderr)
        return 1


def _record_physical(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.muse_athena import AthenaSettings, record_athena, make_preset_command

    try:
        output = record_athena(arguments.output, AthenaSettings(
            duration_seconds=arguments.duration,
            serial_number=arguments.serial_number,
            mac_address=arguments.mac_address,
            discovery_timeout_seconds=arguments.discovery_timeout,
            preset_command=make_preset_command(arguments.preset, arguments.low_latency),
        ))
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Physical Muse S Athena acquisition failed: {error}", file=sys.stderr)
        return 1
    print(f"Saved physical EEG source archive: {output}")
    print("Hardware reference, BLE continuity and source timing remain unverified.")
    return 0


def _openmuse_external(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.openmuse_external import find_openmuse, capture_openmuse
    try:
        if arguments.action == "find":
            return find_openmuse(executable=arguments.openmuse_executable)
        if arguments.output is None:
            raise ValueError("--output is required for openmuse record")
        output = capture_openmuse(
            arguments.address, arguments.output, duration=arguments.duration,
            executable=arguments.openmuse_executable,
        )
    except (OSError, RuntimeError, ValueError) as error:
        print(f"OpenMuse operation failed: {error}", file=sys.stderr)
        return 1
    print(f"Saved external OpenMuse raw capture (not validated EEGZ): {output}")
    return 0


def _assess_physical(arguments: argparse.Namespace) -> int:
    from eeg_athenalyze.hardware_validation import assess_archive

    try:
        result = assess_archive(arguments.session, arguments.report)
    except (OSError, ValueError) as error:
        print(f"Hardware assessment failed: {error}", file=sys.stderr)
        return 1
    print(f"Saved hardware assessment: {arguments.report}")
    print(f"Assessment status: {result['status']} (not hardware certification)")
    return 0
