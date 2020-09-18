from .parser import Parser
from .config import config as default_config


class Process:

    def run(self, pdfs):
        config = self.get_config()
        parser_kwargs = config['parser']
        transform_emit = config['transform_emit']
        for pdf in pdfs:
            parser = Parser(pdf, **parser_kwargs)
            header_row, rows = parser.parse()
            transform_emit(pdf, header_row, rows)

    def get_config(self):
        try:
            from config import config as custom_config
        except ModuleNotFoundError:
            custom_config = {}
        config = {
            **default_config,
            **custom_config,
        }
        return config
