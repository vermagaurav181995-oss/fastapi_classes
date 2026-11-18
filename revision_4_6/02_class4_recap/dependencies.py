from typing import Annotated

from fastapi import Depends, Header, HTTPException, Query, status

from config import settings

REPORTS = {2024: {"year": 2024, "sales": 1200}, 2025: {"year": 2025, "sales": 1850}}


def pagination(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


PageParams = Annotated[dict[str, int], Depends(pagination)]


class Pagination:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=20)] = 5,
    ):
        self.skip = skip
        self.limit = limit

    def apply(self, items: list) -> list:
        return items[self.skip : self.skip + self.limit]


PaginationDep = Annotated[Pagination, Depends()]


def get_report_store():
    print("[reports] open")
    try:
        yield REPORTS
    finally:
        print("[reports] close")


ReportStore = Annotated[dict[int, dict], Depends(get_report_store)]


def verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key")
