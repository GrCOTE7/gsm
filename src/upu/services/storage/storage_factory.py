from .client_storage_adapter import ClientStorageAdapter
from .file_storage_adapter import FileStorageAdapter


def create_storage(page=None):
    """🏭 4) storage_factory.py"""

    if page is not None:
        return ClientStorageAdapter(page)
    return FileStorageAdapter()
