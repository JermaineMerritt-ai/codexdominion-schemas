"""Storage Archiver Module"""

def archive_data(data, location):
    """Archive data to storage"""
    return {"archived": True, "location": location}

def retrieve_archive(location):
    """Retrieve archived data"""
    return {"status": "retrieved", "location": location}
