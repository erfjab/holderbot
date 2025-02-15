from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from .items import access_generate, monitoring_nodes, monitoring_expired

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
        trigger=IntervalTrigger(seconds=30),
        id="monitoring_nodes",
        replace_existing=False,
        max_instances=1,
    )

    scheduler.add_job(
        monitoring_expired,
        trigger=CronTrigger(hour=6, minute=0),
        id="monitoring_expired",
        replace_existing=False,
        max_instances=1,
    )


async def stop() -> None:
    scheduler.shutdown(wait=True)
