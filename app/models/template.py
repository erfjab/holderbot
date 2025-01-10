from enum import Enum


class TemplateModify(str, Enum):
    ACTIVATED = "✅ Activated"
    DISABLED = "❌ Disabled"
    REMOVE = "🗑 Remove"
    DATA_LIMIT = "📊 Data Limit"
    DATE_LIMIT = "⏱️ Date Limit"
    REMARK = "🏷 Remark"
