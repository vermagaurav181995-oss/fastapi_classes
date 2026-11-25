from typing import Annotated

from fastapi import Depends, Query


class Pagination:

    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
    ):
        self.skip = skip
        self.limit = limit

    def apply(self, items: list) -> list:
        return items[self.skip : self.skip + self.limit]


PaginationDep = Annotated[Pagination, Depends()]
