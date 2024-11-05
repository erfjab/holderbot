"""
This module serves as the initialization for the jobs package, 
including the scheduling of background tasks such as token updates 
and node monitoring.
"""

from .scheduler import start_scheduler, stop_scheduler
