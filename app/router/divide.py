"""除算エンドポイント。"""

from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from fastapi import APIRouter, Query

router = APIRouter()

ROUNDING_UNIT = Decimal("0.1")


@router.get("/divide")
def divide(
    a: Annotated[int, Query(gt=0)],
    b: Annotated[int, Query(gt=0)],
) -> dict[str, int | float]:
    """正の整数 a を b で割った商を返す。

    割り切れる場合は int で返す。割り切れない場合は小数第2位を
    decimal の ROUND_HALF_UP で四捨五入し、小数第1位までの float で返す。
    b=0 や正の整数でない入力は FastAPI 標準の検証により 422 を返す。

    Parameters
    ----------
    a : int
        正の整数（被除数）。
    b : int
        正の整数（除数）。0 は 422 になる。

    Returns
    -------
    dict[str, int | float]
        商を result キーに入れた辞書。割り切れる場合は int、
        割り切れない場合は小数第1位に丸めた float。
    """
    if a % b == 0:
        return {"result": a // b}
    quotient = Decimal(a) / Decimal(b)
    return {"result": float(quotient.quantize(ROUNDING_UNIT, rounding=ROUND_HALF_UP))}
