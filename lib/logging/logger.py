import click

class Logger:
    _instance = None

    def __new__(cls, verbose=False):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        cls._instance._verbose = verbose  # Ensure verbose is always updated
        return cls._instance


    def verbose(self, message):
        if self._verbose:
            click.echo(message)
            
    def log(self, message):
        click.echo(message)