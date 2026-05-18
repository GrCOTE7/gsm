from .storage_base import Storage


class ClientStorageAdapter(Storage):
    """🟦 2) client_storage_adapter.py"""

    def __init__(self, page):
        self.page = page

    def get(self, key):
        return self.page.client_storage.get(key)

    def set(self, key, value):
        self.page.client_storage.set(key, value)
