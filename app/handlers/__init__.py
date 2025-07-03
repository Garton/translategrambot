from .pair_select import router as pair_select_router
from .start import router as start_router
from .translate import router as translate_router

__all__ = [
    "start_router",
    "pair_select_router",
    "translate_router",
]

all_routers = [
    start_router,
    pair_select_router,
    translate_router,
]
