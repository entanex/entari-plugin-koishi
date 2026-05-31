from arclet.entari import metadata

from .config import Config
from .service import koishi as koishi

metadata(
    name="Koishi",
    author=[{"name": "Komorebi", "email": "mute231010@gmail.com"}],
    description="A plugin for Entari that integrates with Koishi.",
    classifier=["工具"],
    config=Config,
)
