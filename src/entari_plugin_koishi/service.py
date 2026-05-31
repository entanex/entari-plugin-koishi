import asyncio

from arclet.entari import add_service
from javascript import connection
from koishi import Context
from launart import Launart, Service
from launart.status import Phase


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
        self.ctx.requires(
            "@koishijs/plugin-http",
            "@koishijs/plugin-server",
            "@koishijs/plugin-server-satori",
            "koishi-plugin-adapter-onebot",
            config={
                "@koishijs/plugin-server": {"port": 5140},
                "@koishijs/plugin-server-satori": {"path": "/satori"},
                "koishi-plugin-adapter-onebot": {
                    "selfId": "3655509951",
                    "path": "/onebot/v11/ws",
                },
            },
        )

    async def launch(self, manager: Launart):
        async with self.stage("preparing"):
            koishi_task = asyncio.create_task(self.ctx._main())
        async with self.stage("blocking"):
            await manager.status.wait_for_sigexit()
        async with self.stage("cleanup"):
            if connection.is_alive():
                connection.stop()

            if koishi_task and not koishi_task.done():
                koishi_task.cancel()

            try:
                if koishi_task:
                    await koishi_task
            except asyncio.CancelledError:
                pass


koishi = KoishiService()
add_service(koishi)
