class Storage:
    """🧱 1) storage_base.py"""
    def get(self, key: str):
        raise NotImplementedError

    def set(self, key: str, value):
        raise NotImplementedError
