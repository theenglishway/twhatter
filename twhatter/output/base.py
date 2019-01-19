class OutputBase:
    """Base class for scraper's data output"""
    def output_tweets(self, user, limit) -> None:
        raise NotImplementedError()

    def output_user(self, user) -> None:
        raise NotImplementedError()

    def output_medias(self, user) -> None:
        raise NotImplementedError()
