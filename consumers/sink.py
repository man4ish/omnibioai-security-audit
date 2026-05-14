class Sink:
    """
    Future expansion:
    - PostgreSQL
    - OpenSearch
    - S3 archive
    """

    def write(self, event: dict):
        print("[SINK]", event)