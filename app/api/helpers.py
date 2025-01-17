from datetime import datetime, timezone
from typing import Optional


def ensure_utc(dt: Optional[datetime | str]) -> Optional[datetime]:
    """Ensure datetime is UTC timezone-aware"""
    if dt is None:
        return None

    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except ValueError:
            try:
                dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Unable to parse datetime string: {dt}")

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_bytes(bytes: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ["bytes", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"


def format_date_diff(reference_date: datetime, date: Optional[datetime]) -> str:
    """Calculate time difference between dates"""
    if not date:
        return "➖"

    ref_date = ensure_utc(reference_date)
    compare_date = ensure_utc(date)

    diff = compare_date - ref_date
    total_seconds = int(diff.total_seconds())

    if total_seconds == 0:
        return "now"

    abs_seconds = abs(total_seconds)

    if abs_seconds < 60:
        result = f"{abs_seconds} sec"
    elif abs_seconds < 3600:
        result = f"{abs_seconds // 60} min"
    elif abs_seconds < 86400:
        result = f"{abs_seconds // 3600} hour"
    else:
        result = f"{abs(diff.days)} day"

    return f"in {result}" if total_seconds > 0 else f"{result} ago"
