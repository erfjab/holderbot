from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .items import access_generate, monitoring_nodes

scheduler = AsyncIOScheduler()


async def start() -> bool:
    await access_generate()
    scheduler.start()
    scheduler.add_job(
        access_generate,
        trigger=IntervalTrigger(hours=8),
        id="access_generate",
        replace_existing=False,
        max_instances=1,
    )

    scheduler.add_job(
        monitoring_nodes,
        trigger=IntervalTrigger(minutes=1),
        id="monitoring_nodes",
        replace_existing=False,
        max_instances=1,
    )


async def stop() -> None:
    scheduler.shutdown(wait=True)
