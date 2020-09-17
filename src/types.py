from typing import List, Dict, Callable, Any

import pdfminer.layout as layout


Element = layout.LTText
# Rows = Dict[float, List[Element]]
Type = Callable[[str], Any]
