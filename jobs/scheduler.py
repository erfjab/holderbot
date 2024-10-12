from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from jobs.token_updater import token_update
from jobs.node_monitoring import node_checker
from utils.log import logger

scheduler = AsyncIOScheduler()


async def start_scheduler() -> bool:
    logger.info("Trying to start the scheduler.")

    try:
        logger.info("Testing token update job...")
        test_token = await token_update()
        if not test_token:
            logger.error("Token update test failed. Scheduler will not start.")
            return False

        logger.info("Token update test succeeded.")

        scheduler.start()
        logger.info("Scheduler started successfully.")

        scheduler.add_job(
            token_update,
            trigger=IntervalTrigger(hours=8),
            id="token_update",
            replace_existing=True,
        )
        logger.info("Token update job added to scheduler with ID 'token_update'.")
        scheduler.add_job(
            node_checker,
            trigger=IntervalTrigger(seconds=20),
            id="node_monitor",
            replace_existing=True,
        )
        logger.info("Token update job added to scheduler with ID 'node_monitor'.")
        return True

    except Exception as e:
        logger.error(f"An error occurred while starting the scheduler: {e}")
        return False


async def stop_scheduler() -> None:
    logger.info("Trying to stop the scheduler.")
    try:
        scheduler.shutdown(wait=True)
        logger.info("Scheduler stopped successfully.")
    except Exception as e:
        logger.error(f"An error occurred while stopping the scheduler: {e}")
