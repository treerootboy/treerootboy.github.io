# 中国节假日订阅日历交接

## 目标与发布位置

订阅地址：<https://blog.ming01.dev/calendars/china-holidays.ics>。

站点仓库为 `treerootboy/treerootboy.github.io`，GitHub Pages 从 `master` 根目录发布，`CNAME` 为 `blog.ming01.dev`。本次直接增加静态文件，沿用现有公开博客的发布方式。

## 内容与依据

来源为[新华社转载的国务院办公厅通知](https://www.news.cn/politics/20261105/f90cd6ad4df94ab4833b141e52ccfc13/c.html)，发布于 2026 年 11 月 5 日。当前只收录 2027 年安排。

| 节日 | 放假日期（含首尾） | 补班日期 |
| --- | --- | --- |
| 元旦 | 1 月 1—3 日 | 无 |
| 春节 | 2 月 5—13 日 | 1 月 31 日、2 月 14 日 |
| 清明节 | 4 月 3—5 日 | 无 |
| 劳动节 | 5 月 1—5 日 | 5 月 8 日 |
| 端午节 | 6 月 9 日 | 无 |
| 中秋节 | 9 月 15 日 | 无 |
| 国庆节 | 10 月 1—7 日 | 9 月 26 日、10 月 9 日 |

合计 29 个放假日、5 个补班日，逐日生成 34 个全天事件。普通周末不另建事件。放假标题为“节日名（放假）”，补班标题统一为“补班”；不设提醒、不占用忙碌时间。全天日期不受设备时区转换影响，结束日期按 iCalendar 规则使用次日。

## 生成与维护

年度数据位于 `calendar-data/china-holidays/`，生成脚本位于 `scripts/generate_china_holidays.py`，成品位于 `calendars/china-holidays.ics`。

```sh
python3.11 -m venv /tmp/china-holidays-venv
/tmp/china-holidays-venv/bin/python3.11 -m pip install -r scripts/requirements-calendar.txt
/tmp/china-holidays-venv/bin/python3.11 scripts/generate_china_holidays.py
```

新增年份时，核对官方通知后新增对应 JSON，保留旧年份，重新生成并提交日历。更正既有年份时更新 `updated_at` 的 UTC 时间并递增 `sequence`。日期对应的 UID 必须保持不变。当前没有配置自动抓取或自动年度更新。

私有 Hugo 源码仓库 `treerootboy/blog` 的旧部署脚本会把生成文件复制到此站点仓库，未清空目标目录；本次未触发旧版全站重建。以后迁移或清空发布目录时，必须保留本日历、数据与脚本。

## 订阅与验收

在日历应用中选择“新增订阅日历”或“通过网址添加”，粘贴上方 HTTPS 地址；Apple 日历也可使用 `webcal://blog.ming01.dev/calendars/china-holidays.ics`。直接下载导入是一次性操作，不会同步后续修改。刷新频率由客户端决定。

本地验收：使用 `icalendar` 回读文件，核对全部日期、34 个唯一 UID、全天事件及次日结束、5 个补班日、无重复与冲突、UTF-8 折行和 CRLF。发布后必须再次下载正式 HTTPS 地址，核对 HTTP 状态、日历类型、事件及文件摘要；客户端实际订阅效果以用户设备为准。
