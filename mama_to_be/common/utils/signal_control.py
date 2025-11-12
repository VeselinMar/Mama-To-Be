from contextlib import contextmanager

DISABLE_SEED_SIGNALS = False

@contextmanager
def disable_seed_signals():
    """
    Temporarily disable signals during seeding.
    Usage:
        with disable_seed_signals():
            # do seeding (loaddata, fixtures, custom commands)
    """
    global DISABLE_SEED_SIGNALS
    DISABLE_SEED_SIGNALS = True
    try:
        yield
    finally:
        DISABLE_SEED_SIGNALS = False