#!/usr/bin/env python3
"""
Pull Notion data source pages in a date-aware, programmatic way.

This script uses the current Notion API model where databases can contain one
or more data sources. It can:

- resolve a data source from a database ID
- query rows by month or date range
- optionally fetch page content recursively
- emit stable JSON for downstream analysis

Examples:
  python3 scripts/notion_pull_database.py \
    --database-id 91af7780-5629-4cdf-bfa3-7b1180e25491 \
    --month 2024-03 \
    --include-content

  python3 scripts/notion_pull_database.py \
    --data-source-id 205d5996-6515-4744-ae53-266346d8b198 \
    --start-date 2024-01-01 \
    --end-date 2024-03-31 \
    --output journal-q1-2024.json

Environment:
  NOTION_TOKEN or NOTION_API_KEY must be set.
"""

from __future__ import annotations

import argparse
import calendar
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, Iterable, List, Optional


NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"


@dataclass
class QueryWindow:
    start_date: Optional[str]
    end_date: Optional[str]


class NotionClient:
    def __init__(self, token: str, version: str = NOTION_VERSION, timeout: int = 30):
        self.token = token
        self.version = version
        self.timeout = timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        retries: int = 4,
    ) -> Dict[str, Any]:
        url = f"{NOTION_API_BASE}{path}"
        if query:
            params = urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
            url = f"{url}?{params}"

        payload = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.version,
            "Accept": "application/json",
        }
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(url, data=payload, headers=headers, method=method)

        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                response_text = exc.read().decode("utf-8", errors="replace")
                retry_after = exc.headers.get("Retry-After")
                if exc.code in {429, 500, 502, 503, 504} and attempt < retries:
                    sleep_for = float(retry_after) if retry_after else 1.5 * (attempt + 1)
                    time.sleep(sleep_for)
                    continue
                raise SystemExit(
                    f"Notion API error {exc.code} for {method} {path}:\n{response_text}"
                ) from exc
            except urllib.error.URLError as exc:
                raise SystemExit(f"Network error calling Notion API: {exc}") from exc

        raise SystemExit(f"Failed to call Notion API after {retries + 1} attempts: {path}")

    def paginate(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        results_key: str = "results",
    ) -> Iterable[Dict[str, Any]]:
        next_cursor = None
        while True:
            current_body = dict(body or {})
            if next_cursor:
                current_body["start_cursor"] = next_cursor
            response = self.request(method, path, query=query, body=current_body or None)
            for item in response.get(results_key, []):
                yield item
            if not response.get("has_more"):
                return
            next_cursor = response.get("next_cursor")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--database-id", help="Notion database ID")
    source_group.add_argument("--data-source-id", help="Notion data source ID")
    parser.add_argument(
        "--data-source-name",
        help="Use when a database has multiple data sources and you want a specific one",
    )
    parser.add_argument(
        "--date-property",
        default="Date",
        help="Date property name to filter on. Default: %(default)s",
    )
    parser.add_argument("--month", help="Month to pull in YYYY-MM format")
    parser.add_argument("--start-date", help="Inclusive start date in YYYY-MM-DD")
    parser.add_argument("--end-date", help="Inclusive end date in YYYY-MM-DD")
    parser.add_argument("--page-size", type=int, default=100, help="Rows per Notion request")
    parser.add_argument(
        "--include-content",
        action="store_true",
        help="Fetch page blocks recursively and include plain text plus structured blocks",
    )
    parser.add_argument("--max-depth", type=int, default=8, help="Nested block depth limit")
    parser.add_argument("--output", help="Write JSON output to this file instead of stdout")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser.parse_args()


def ensure_iso_date(raw: str, label: str) -> str:
    try:
        return date.fromisoformat(raw).isoformat()
    except ValueError as exc:
        raise SystemExit(f"{label} must be in YYYY-MM-DD format, got: {raw}") from exc


def compute_window(month: Optional[str], start_date: Optional[str], end_date: Optional[str]) -> QueryWindow:
    if month and (start_date or end_date):
        raise SystemExit("Use either --month or --start-date/--end-date, not both")

    if month:
        try:
            year_str, month_str = month.split("-", 1)
            year = int(year_str)
            month_number = int(month_str)
            _, last_day = calendar.monthrange(year, month_number)
        except Exception as exc:
            raise SystemExit(f"--month must be in YYYY-MM format, got: {month}") from exc
        return QueryWindow(
            start_date=date(year, month_number, 1).isoformat(),
            end_date=date(year, month_number, last_day).isoformat(),
        )

    normalized_start = ensure_iso_date(start_date, "--start-date") if start_date else None
    normalized_end = ensure_iso_date(end_date, "--end-date") if end_date else None
    if normalized_start and normalized_end and normalized_start > normalized_end:
        raise SystemExit("--start-date must be on or before --end-date")
    return QueryWindow(start_date=normalized_start, end_date=normalized_end)


def rich_text_to_plain_text(items: List[Dict[str, Any]]) -> str:
    return "".join(item.get("plain_text", "") for item in items or [])


def extract_property_value(prop: Dict[str, Any]) -> Any:
    prop_type = prop.get("type")
    if prop_type == "title":
        return rich_text_to_plain_text(prop.get("title", []))
    if prop_type == "rich_text":
        return rich_text_to_plain_text(prop.get("rich_text", []))
    if prop_type == "number":
        return prop.get("number")
    if prop_type == "select":
        select = prop.get("select")
        return select.get("name") if select else None
    if prop_type == "multi_select":
        return [item.get("name") for item in prop.get("multi_select", [])]
    if prop_type == "status":
        status = prop.get("status")
        return status.get("name") if status else None
    if prop_type == "date":
        return prop.get("date")
    if prop_type == "checkbox":
        return prop.get("checkbox")
    if prop_type == "url":
        return prop.get("url")
    if prop_type == "email":
        return prop.get("email")
    if prop_type == "phone_number":
        return prop.get("phone_number")
    if prop_type == "people":
        return [person.get("name") or person.get("id") for person in prop.get("people", [])]
    if prop_type == "files":
        return [item.get("name") for item in prop.get("files", [])]
    if prop_type == "relation":
        return [item.get("id") for item in prop.get("relation", [])]
    if prop_type == "formula":
        formula = prop.get("formula", {})
        return formula.get(formula.get("type"))
    if prop_type == "rollup":
        rollup = prop.get("rollup", {})
        return rollup.get(rollup.get("type"))
    if prop_type == "created_time":
        return prop.get("created_time")
    if prop_type == "last_edited_time":
        return prop.get("last_edited_time")
    if prop_type == "created_by":
        created_by = prop.get("created_by")
        return created_by.get("name") if created_by else None
    if prop_type == "last_edited_by":
        last_edited_by = prop.get("last_edited_by")
        return last_edited_by.get("name") if last_edited_by else None
    if prop_type == "unique_id":
        unique_id = prop.get("unique_id")
        if not unique_id:
            return None
        prefix = unique_id.get("prefix") or ""
        number = unique_id.get("number")
        return f"{prefix}{number}" if prefix else number
    return prop.get(prop_type)


def block_text(block: Dict[str, Any]) -> str:
    block_type = block["type"]
    payload = block.get(block_type, {})

    for field in ("rich_text", "caption"):
        if isinstance(payload, dict) and field in payload:
            text = rich_text_to_plain_text(payload.get(field, []))
            if text:
                return text

    if block_type == "child_page":
        return payload.get("title", "")
    if block_type == "callout":
        icon = payload.get("icon")
        prefix = f"{icon.get('emoji', '')} " if icon and icon.get("type") == "emoji" else ""
        return f"{prefix}{rich_text_to_plain_text(payload.get('rich_text', []))}".strip()
    if block_type == "to_do":
        checked = "[x]" if payload.get("checked") else "[ ]"
        return f"{checked} {rich_text_to_plain_text(payload.get('rich_text', []))}".strip()
    if block_type in {"bulleted_list_item", "numbered_list_item", "paragraph", "quote", "toggle"}:
        return rich_text_to_plain_text(payload.get("rich_text", []))
    if block_type.startswith("heading_"):
        return rich_text_to_plain_text(payload.get("rich_text", []))
    return ""


def read_block_children(
    client: NotionClient,
    block_id: str,
    *,
    depth: int,
    max_depth: int,
) -> List[Dict[str, Any]]:
    if depth > max_depth:
        return []

    blocks = list(
        client.paginate(
            "GET",
            f"/blocks/{block_id}/children",
            query={"page_size": 100},
        )
    )

    serialized = []
    for block in blocks:
        item = {
            "id": block.get("id"),
            "type": block.get("type"),
            "text": block_text(block),
            "has_children": block.get("has_children", False),
        }
        if block.get("has_children"):
            item["children"] = read_block_children(
                client,
                block["id"],
                depth=depth + 1,
                max_depth=max_depth,
            )
        serialized.append(item)
    return serialized


def flatten_block_text(blocks: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for block in blocks:
        text = (block.get("text") or "").strip()
        if text:
            lines.append(text)
        children = block.get("children") or []
        if children:
            nested = flatten_block_text(children)
            if nested:
                lines.append(nested)
    return "\n".join(lines)


def resolve_data_source_id(
    client: NotionClient,
    database_id: str,
    *,
    data_source_name: Optional[str],
) -> str:
    database = client.request("GET", f"/databases/{database_id}")
    data_sources = database.get("data_sources") or []
    if not data_sources:
        raise SystemExit(f"Database {database_id} did not return any data_sources")
    if len(data_sources) == 1:
        return data_sources[0]["id"]
    if data_source_name:
        normalized = data_source_name.strip().lower()
        for data_source in data_sources:
            if data_source.get("name", "").strip().lower() == normalized:
                return data_source["id"]
        available = ", ".join(ds.get("name", ds["id"]) for ds in data_sources)
        raise SystemExit(f"Data source named {data_source_name!r} not found. Available: {available}")
    available = ", ".join(ds.get("name", ds["id"]) for ds in data_sources)
    raise SystemExit(f"Database has multiple data sources. Pass --data-source-name. Available: {available}")


def build_filter(date_property: str, window: QueryWindow) -> Optional[Dict[str, Any]]:
    clauses = []
    if window.start_date:
        clauses.append({"property": date_property, "date": {"on_or_after": window.start_date}})
    if window.end_date:
        clauses.append({"property": date_property, "date": {"on_or_before": window.end_date}})
    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"and": clauses}


def query_pages(
    client: NotionClient,
    *,
    data_source_id: str,
    date_property: str,
    window: QueryWindow,
    page_size: int,
) -> List[Dict[str, Any]]:
    body: Dict[str, Any] = {
        "page_size": page_size,
        "sorts": [{"property": date_property, "direction": "ascending"}],
    }
    data_filter = build_filter(date_property, window)
    if data_filter:
        body["filter"] = data_filter
    return list(client.paginate("POST", f"/data_sources/{data_source_id}/query", body=body))


def serialize_page(
    client: NotionClient,
    page: Dict[str, Any],
    *,
    include_content: bool,
    max_depth: int,
) -> Dict[str, Any]:
    properties = {
        name: extract_property_value(prop)
        for name, prop in page.get("properties", {}).items()
    }
    serialized = {
        "id": page.get("id"),
        "url": page.get("url"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time"),
        "archived": page.get("archived"),
        "in_trash": page.get("in_trash"),
        "properties": properties,
    }
    if include_content:
        blocks = read_block_children(client, page["id"], depth=1, max_depth=max_depth)
        serialized["content_blocks"] = blocks
        serialized["content_text"] = flatten_block_text(blocks)
    return serialized


def main() -> None:
    args = parse_args()
    token = os.getenv("NOTION_TOKEN") or os.getenv("NOTION_API_KEY")
    if not token:
        raise SystemExit("Set NOTION_TOKEN or NOTION_API_KEY before running this script")

    window = compute_window(args.month, args.start_date, args.end_date)
    client = NotionClient(token=token)

    data_source_id = args.data_source_id
    if args.database_id:
        data_source_id = resolve_data_source_id(
            client,
            args.database_id,
            data_source_name=args.data_source_name,
        )

    data_source = client.request("GET", f"/data_sources/{data_source_id}")
    pages = query_pages(
        client,
        data_source_id=data_source_id,
        date_property=args.date_property,
        window=window,
        page_size=args.page_size,
    )

    output = {
        "meta": {
            "database_id": args.database_id,
            "data_source_id": data_source_id,
            "data_source_name": data_source.get("name"),
            "date_property": args.date_property,
            "window": {
                "start_date": window.start_date,
                "end_date": window.end_date,
            },
            "page_count": len(pages),
            "include_content": args.include_content,
            "notion_version": client.version,
        },
        "pages": [
            serialize_page(
                client,
                page,
                include_content=args.include_content,
                max_depth=args.max_depth,
            )
            for page in pages
        ],
    }

    json_output = json.dumps(
        output,
        indent=2 if (args.pretty or not args.output) else None,
        ensure_ascii=False,
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(json_output)
            handle.write("\n")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
