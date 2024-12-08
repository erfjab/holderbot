import asyncio
from app.holderbot import main


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()
