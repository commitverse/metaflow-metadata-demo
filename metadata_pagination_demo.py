from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional


mock_runs: List[Dict[str, Any]] = [
    {
        "id": 1,
        "flow": "IrisFlow",
        "tag": "prod",
        "status": "success",
        "created_at": datetime(2026, 3, 20, 10, 30),
        "owner": "alice",
    },
    {
        "id": 2,
        "flow": "IrisFlow",
        "tag": "dev",
        "status": "failed",
        "created_at": datetime(2026, 3, 21, 9, 15),
        "owner": "alice",
    },
    {
        "id": 3,
        "flow": "SalesFlow",
        "tag": "prod",
        "status": "success",
        "created_at": datetime(2026, 3, 22, 14, 0),
        "owner": "bob",
    },
    {
        "id": 4,
        "flow": "SalesFlow",
        "tag": "test",
        "status": "running",
        "created_at": datetime(2026, 3, 23, 16, 45),
        "owner": "bob",
    },
    {
        "id": 5,
        "flow": "WeatherFlow",
        "tag": "prod",
        "status": "success",
        "created_at": datetime(2026, 3, 24, 11, 0),
        "owner": "carol",
    },
    {
        "id": 6,
        "flow": "WeatherFlow",
        "tag": "dev",
        "status": "failed",
        "created_at": datetime(2026, 3, 25, 8, 20),
        "owner": "carol",
    },
    {
        "id": 7,
        "flow": "NLPFlow",
        "tag": "prod",
        "status": "success",
        "created_at": datetime(2026, 3, 26, 13, 10),
        "owner": "dave",
    },
    {
        "id": 8,
        "flow": "NLPFlow",
        "tag": "dev",
        "status": "success",
        "created_at": datetime(2026, 3, 27, 17, 5),
        "owner": "dave",
    },
]


def validate_pagination(limit: int, offset: int) -> None:
    """Validate pagination arguments."""
    if limit <= 0:
        raise ValueError("limit must be greater than 0")
    if offset < 0:
        raise ValueError("offset must be 0 or greater")


def serialize_run(run: Dict[str, Any]) -> Dict[str, Any]:
    """Convert datetime fields to JSON-friendly strings."""
    serialized = dict(run)
    serialized["created_at"] = run["created_at"].isoformat()
    return serialized


def filter_runs(
    runs: List[Dict[str, Any]],
    tag: Optional[str] = None,
    status: Optional[str] = None,
    flow: Optional[str] = None,
    owner: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[Dict[str, Any]]:
    """Apply request-level filtering to runs."""
    result = runs

    if tag is not None:
        result = [r for r in result if r["tag"] == tag]

    if status is not None:
        result = [r for r in result if r["status"] == status]

    if flow is not None:
        result = [r for r in result if r["flow"] == flow]

    if owner is not None:
        result = [r for r in result if r["owner"] == owner]

    if start_date is not None:
        result = [r for r in result if r["created_at"] >= start_date]

    if end_date is not None:
        result = [r for r in result if r["created_at"] <= end_date]

    return result


def summarize_runs(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a lightweight summary similar to what a metadata service might expose."""
    status_counts: Dict[str, int] = {}
    tag_counts: Dict[str, int] = {}

    for run in runs:
        status_counts[run["status"]] = status_counts.get(run["status"], 0) + 1
        tag_counts[run["tag"]] = tag_counts.get(run["tag"], 0) + 1

    return {
        "count": len(runs),
        "status_counts": status_counts,
        "tag_counts": tag_counts,
    }


def paginate_runs(runs: List[Dict[str, Any]], limit: int = 3, offset: int = 0) -> Dict[str, Any]:
    """Return paginated runs in an API-like response format."""
    validate_pagination(limit, offset)

    total = len(runs)
    page = runs[offset : offset + limit]
    next_offset = offset + limit if offset + limit < total else None
    previous_offset = max(offset - limit, 0) if offset > 0 else None

    return {
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "next_offset": next_offset,
            "previous_offset": previous_offset,
            "returned": len(page),
        },
        "data": [serialize_run(run) for run in page],
    }


def query_runs(
    runs: List[Dict[str, Any]],
    tag: Optional[str] = None,
    status: Optional[str] = None,
    flow: Optional[str] = None,
    owner: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 3,
    offset: int = 0,
) -> Dict[str, Any]:
    """Filter first, then paginate, returning a metadata-style response."""
    filtered = filter_runs(
        runs,
        tag=tag,
        status=status,
        flow=flow,
        owner=owner,
        start_date=start_date,
        end_date=end_date,
    )

    response = paginate_runs(filtered, limit=limit, offset=offset)
    response["summary"] = summarize_runs(filtered)
    response["applied_filters"] = {
        "tag": tag,
        "status": status,
        "flow": flow,
        "owner": owner,
        "start_date": start_date.isoformat() if start_date else None,
        "end_date": end_date.isoformat() if end_date else None,
    }
    return response


def print_query(title: str, result: Dict[str, Any]) -> None:
    print(f"\n=== {title} ===")
    print(result)


if __name__ == "__main__":
    print_query(
        "All runs, paginated",
        query_runs(mock_runs, limit=3, offset=0),
    )

    print_query(
        "Filtered by tag=prod",
        query_runs(mock_runs, tag="prod", limit=2, offset=0),
    )

    print_query(
        "Filtered by status=failed",
        query_runs(mock_runs, status="failed", limit=5, offset=0),
    )

    print_query(
        "Filtered by flow=WeatherFlow",
        query_runs(mock_runs, flow="WeatherFlow", limit=5, offset=0),
    )

    print_query(
        "Filtered by owner=dave",
        query_runs(mock_runs, owner="dave", limit=5, offset=0),
    )

    print_query(
        "Filtered by date range 2026-03-22 to 2026-03-26",
        query_runs(
            mock_runs,
            start_date=datetime(2026, 3, 22),
            end_date=datetime(2026, 3, 26, 23, 59, 59),
            limit=10,
            offset=0,
        ),
    )

    print_query(
        "Filtered by tag=prod and status=success",
        query_runs(mock_runs, tag="prod", status="success", limit=2, offset=0),
    )