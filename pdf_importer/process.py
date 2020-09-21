from .parser import Parser
from .config import config as default_config


class Process:

    def __init__(self, config=None):
        self.config = config or {}

    def run(self, pdfs, transform_emit_args=None):
        config = self.get_config()
        parser_kwargs = config['parser']
        transform_emit = config['transform_emit']
        for i, pdf in enumerate(pdfs):
            parser = Parser(pdf, **parser_kwargs)
            header_row, rows, rows_by_page = parser.parse()
            transform_emit(
                pdf,
                header_row,
                rows,
                rows_by_page,
                (
                    transform_emit_args[i]
                    if transform_emit_args is not None
                    else None
                ),
            )

    def get_config(self):
        try:
            from config import config as custom_config
        except (ModuleNotFoundError, ImportError):
            custom_config = {}
        config = {
            **default_config,
            **custom_config,
            **self.config,
        }
        return config
