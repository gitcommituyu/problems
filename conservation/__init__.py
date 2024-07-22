import check50

@check50.check()
def exists():
    """transcript.txt exists."""
    check50.exists("transcript.txt")
