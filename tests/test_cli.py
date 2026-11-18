"""CLI compatibility tests, independent of EEG hardware and optional packages."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import unittest
from unittest.mock import patch

from eeg_athenalyze import cli_commands
from eeg_athenalyze.cli import main
from eeg_athenalyze.cli_parser import build_parser


class CommandLineContractTests(unittest.TestCase):
    def test_all_command_routes(self) -> None:
        routes = (
            (["synthetic-record", "--output", "s.eegz"], "_record_synthetic"),
            (["experiment", "run", "eyes-open-closed", "--output", "out"], "_run_experiment"),
            (["analyze", "--session", "s.eegz"], "_analyze_session"),
            (["plot", "--session", "s.eegz"], "_plot_session"),
            (["bids", "export", "--session", "s.eegz", "--dataset", "bids"], "_bids_export"),
            (["bids", "validate", "--dataset", "bids"], "_bids_validate"),
            (["bids", "derivatives", "--session", "s.eegz", "--dataset", "bids"], "_bids_derivatives"),
            (["devices", "check", "--device", "muse-athena"], "_device_check"),
            (["devices", "openmuse", "find"], "_openmuse_external"),
            (["devices", "openmuse", "record", "--output", "raw"], "_openmuse_external"),
            (["devices", "assess", "--session", "s.eegz", "--report", "qc.json"], "_assess_physical"),
            (["record", "--device", "muse-athena", "--output", "s.eegz"], "_record_physical"),
        )
        parser = build_parser()
        for argv, target in routes:
            with self.subTest(argv=argv):
                self.assertIs(parser.parse_args(argv).handler, getattr(cli_commands, target))

    def test_defaults(self) -> None:
        parser = build_parser()
        synthetic = parser.parse_args(["synthetic-record", "--output", "s.eegz"])
        self.assertEqual(synthetic.output, Path("s.eegz"))
        self.assertEqual((synthetic.duration, synthetic.sample_rate, synthetic.seed), (10.0, 256.0, 0))
        self.assertEqual(synthetic.condition, "synthetic")
        experiment = parser.parse_args(["experiment", "run", "eyes-open-closed", "--output", "out"])
        self.assertEqual((experiment.participant, experiment.duration_scale), ("sub-001", 1.0))
        plot = parser.parse_args(["plot", "--session", "s.eegz"])
        self.assertEqual((plot.time_axis, plot.view, plot.max_points), ("samples", "trace", 8000))
        record = ["record", "--device", "muse-athena", "--output", "s.eegz"]
        self.assertEqual(parser.parse_args(record).preset, "p1041")
        self.assertTrue(parser.parse_args(record).low_latency)
        self.assertFalse(parser.parse_args(record + ["--no-low-latency"]).low_latency)

    def test_invalid_args_exit_two(self) -> None:
        invalid = ([], ["bids"], ["devices"], ["record", "--device", "muse-athena"],
                   ["plot", "--session", "s.eegz", "--time-axis", "invalid"],
                   ["devices", "check", "--device", "invalid"])
        for argv in invalid:
            with self.subTest(argv=argv), redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as error:
                    build_parser().parse_args(argv)
                self.assertEqual(error.exception.code, 2)

    def test_main_preserves_exit_status(self) -> None:
        with patch("eeg_athenalyze.cli_parser._record_synthetic", return_value=17) as handler:
            status = main(["synthetic-record", "--output", "s.eegz"])
        self.assertEqual(status, 17)
        self.assertEqual(handler.call_args.args[0].output, Path("s.eegz"))

    def test_help_does_not_execute_handler(self) -> None:
        output = StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as error:
            main(["--help"])
        self.assertEqual(error.exception.code, 0)
        self.assertIn("synthetic-record", output.getvalue())


if __name__ == "__main__":
    unittest.main()
