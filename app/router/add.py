from typing import Annotated

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/add")
def add(
    a: Annotated[int, Query(gt=0)],
    b: Annotated[int, Query(gt=0)],
) -> dict[str, int]:
    return {"result": a + b}
