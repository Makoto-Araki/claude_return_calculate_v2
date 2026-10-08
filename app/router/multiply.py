"""乗算エンドポイント。"""

from typing import Annotated

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/multiply")
def multiply(
    a: Annotated[int, Query(gt=0)],
    b: Annotated[int, Query(gt=0)],
) -> dict[str, int]:
    """正の整数 a と b の積を返す。

    正の整数でない入力は FastAPI 標準の検証により 422 を返す。

    Parameters
    ----------
    a : int
        正の整数。
    b : int
        正の整数。

    Returns
    -------
    dict[str, int]
        a * b を result キーに入れた辞書。
    """
    return {"result": a * b}
