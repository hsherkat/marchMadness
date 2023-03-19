import pytest
from approvaltests.approvals import verify_file
from approvaltests.approvals import set_default_reporter
from approvaltests.reporters import GenericDiffReporterFactory
from genResults import main

set_default_reporter(GenericDiffReporterFactory().get("WinMerge"))


@pytest.fixture(scope="session")
def run_script():
    main()


def test_results(run_script):
    verify_file("userResultsPy.dat")


def test_scores(run_script):
    verify_file("userScores.dat")
