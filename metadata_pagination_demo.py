from typing import List, Dict, Optional


mock_runs = [
    {"id": 1, "flow": "IrisFlow", "tag": "prod", "status": "success"},
    {"id": 2, "flow": "IrisFlow", "tag": "dev", "status": "failed"},
    {"id": 3, "flow": "SalesFlow", "tag": "prod", "status": "success"},
    {"id": 4, "flow": "SalesFlow", "tag": "test", "status": "running"},
    {"id": 5, "flow": "WeatherFlow", "tag": "prod", "status": "success"},
    {"id": 6, "flow": "WeatherFlow", "tag": "dev", "status": "failed"},
    {"id": 7, "flow": "NLPFlow", "tag": "prod", "status": "success"},
    {"id": 8, "flow": "NLPFlow", "tag": "dev", "status": "success"},
]


def filter_runs(
    runs: List[Dict],
    tag: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Dict]:
    result = runs
    if tag is not None:
        result = [r for r in result if r["tag"] == tag]
    if status is not None:
        result = [r for r in result if r["status"] == status]
    return result


def paginate_runs(runs: List[Dict], limit: int = 3, offset: int = 0) -> Dict:
    total = len(runs)
    page = runs[offset: offset + limit]
    next_offset = offset + limit if offset + limit < total else None

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "next_offset": next_offset,
        "results": page,
    }


def query_runs(
    runs: List[Dict],
    tag: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 3,
    offset: int = 0,
) -> Dict:
    filtered = filter_runs(runs, tag=tag, status=status)
    return paginate_runs(filtered, limit=limit, offset=offset)


if __name__ == "__main__":
    print("=== All runs, paginated ===")
    print(query_runs(mock_runs, limit=3, offset=0))

    print("\n=== Filtered by tag=prod ===")
    print(query_runs(mock_runs, tag="prod", limit=2, offset=0))

    print("\n=== Filtered by status=failed ===")
    print(query_runs(mock_runs, status="failed", limit=5, offset=0))

    print("\n=== Filtered by tag=prod and status=success ===")
    print(query_runs(mock_runs, tag="prod", status="success", limit=2, offset=0))