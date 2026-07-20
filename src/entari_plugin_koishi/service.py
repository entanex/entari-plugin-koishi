import asyncio
from pathlib import Path

from arclet.entari import add_service
from javascript import connection
from koishi import Context
from launart import Launart, Service
from launart.status import Phase

from .config import config
from .log import logger


class KoishiService(Service):
    id = "entari_plugin_koishi"

    @property
    def required(self):
        return set()

    @property
    def stages(self) -> set[Phase]:
        return {"preparing", "blocking", "cleanup"}

    def __init__(self):
        super().__init__()
        self.ctx = Context({})

        self.config_path = Path(config.path).expanduser().resolve() / "koishi.yml"
        self._available = self.config_path.is_file()
        if not self._available:
            logger.error(f"Koishi config file not found: {self.config_path}")
            return

        self.ctx.requires(
            "@koishijs/plugin-http",
            "@koishijs/plugin-server",
            "@koishijs/plugin-server-satori",
            "koishi-plugin-adapter-onebot",
            config=self.config_path,
        )

    async def launch(self, manager: Launart):
        koishi_task = None
        async with self.stage("preparing"):
            if self._available:
                koishi_task = asyncio.create_task(self.ctx._main())
        async with self.stage("blocking"):
            await manager.status.wait_for_sigexit()
        async with self.stage("cleanup"):
            if connection.is_alive():
                connection.stop()

            if koishi_task is not None and not koishi_task.done():
                koishi_task.cancel()

            try:
                if koishi_task is not None:
                    await koishi_task
            except asyncio.CancelledError:
                pass


koishi = KoishiService()
add_service(koishi)
