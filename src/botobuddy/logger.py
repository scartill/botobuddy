import logging as lg
from rich.logging import RichHandler


logger = lg.getLogger('botobuddy')


def setup_logging(verbose: bool = False):
    """Configure logging for the application.

    Args:
        verbose: If True, set logging level to DEBUG. Otherwise, set to INFO.
    """
    handler = RichHandler(rich_tracebacks=False, show_path=False)
    logger.addHandler(handler)
    logger.setLevel(lg.INFO if not verbose else lg.DEBUG)
