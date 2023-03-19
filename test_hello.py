from approvaltests.approvals import set_default_reporter, verify
from approvaltests.reporters import GenericDiffReporterFactory

set_default_reporter(GenericDiffReporterFactory().get("WinMerge"))


def test_simple():
    result = """
    Hello world!
    This is an approval test!
    """
    verify(result)
