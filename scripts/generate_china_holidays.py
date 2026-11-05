"""从已核实的年度安排生成中国放假及补班订阅日历。"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

from icalendar import Calendar, Event, vDuration


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "calendars/china-holidays.ics"
SUBSCRIPTION = "https://blog.ming01.dev/calendars/china-holidays.ics"


def build_calendar() -> Calendar:
    """汇总全部年度数据，按日期生成具有稳定标识的全天事件。"""
    calendar = Calendar()
    calendar.add("prodid", "-//Ming//China Holidays//ZH-CN")
    calendar.add("version", "2.0")
    calendar.add("calscale", "GREGORIAN")
    calendar.add("method", "PUBLISH")
    calendar.add("x-wr-calname", "中国节假日与调休")
    calendar.add("x-wr-caldesc", "中国大陆官方放假及补班安排；当前收录2027年。")
    calendar.add("x-wr-timezone", "Asia/Shanghai")
    calendar.add("x-published-ttl", "P1D")
    calendar.add("refresh-interval", vDuration(timedelta(days=1)))
    calendar.add("url", SUBSCRIPTION)
    events = []
    seen = set()
    files = sorted((ROOT / "calendar-data/china-holidays").glob("*.json"))
    if not files:
        raise ValueError("没有找到年度数据")
    years = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        year = data["year"]
        years.append(str(year))
        updated = datetime.fromisoformat(data["updated_at"])
        if updated.utcoffset() != timedelta(0):
            raise ValueError("更新时间必须使用 UTC")
        for holiday in data["holidays"]:
            start, end = (date.fromisoformat(holiday[key]) for key in ("start", "end"))
            if start > end:
                raise ValueError("放假开始日期不能晚于结束日期")
            dates = [(start + timedelta(days=i), "放假") for i in range((end - start).days + 1)]
            dates += [(date.fromisoformat(value), "补班") for value in holiday["workdays"]]
            for day, kind in dates:
                if day.year != year or day in seen:
                    raise ValueError(f"日期跨年、重复或放假补班冲突：{day}")
                seen.add(day)
                event = Event()
                event.add("uid", f"china-holidays-{day:%Y%m%d}@blog.ming01.dev")
                event.add("dtstamp", updated)
                event.add("last-modified", updated)
                event.add("sequence", data["sequence"])
                event.add("dtstart", day)
                event.add("dtend", day + timedelta(days=1))
                event.add("summary", "补班" if kind == "补班" else f"{holiday['name']}（放假）")
                event.add("description", f"中国大陆{kind}安排。\n来源：{data['source_title']}\n{data['source']}")
                event.add("url", data["source"])
                event.add("categories", ["中国节假日", kind])
                event.add("status", "CONFIRMED")
                event.add("transp", "TRANSPARENT")
                events.append((day, event))
    calendar["x-wr-caldesc"] = f"中国大陆官方放假及补班安排；当前收录{'、'.join(years)}年。"
    for _, event in sorted(events, key=lambda item: item[0]):
        calendar.add_component(event)
    return calendar


if __name__ == "__main__":
    result = build_calendar()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(result.to_ical())
    print(f"已生成 {OUTPUT}，共 {len(result.subcomponents)} 个事件")
