from typing import List, Dict, Callable, Any

import pdfminer.layout as layout


# TODO: How to specify Intersection[LTText, LTComponent]?
Element = layout.LTText
Type = Callable[[str], Any]
