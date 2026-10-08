"""divide エンドポイントのユニットテスト。"""

from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """FastAPI アプリを対象とする TestClient を返す。"""
    from app.main import app

    return TestClient(app)


def test_divide_exact_returns_int_with_200(client: TestClient) -> None:
    """割り切れる 6 / 3 はステータス 200 と {"result": 2} が返る。"""
    response = client.get("/divide", params={"a": 6, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 2}


def test_divide_exact_result_is_int(client: TestClient) -> None:
    """割り切れる場合の結果は int で返る。"""
    response = client.get("/divide", params={"a": 6, "b": 3})
    assert isinstance(response.json()["result"], int)


def test_divide_same_numbers_returns_one_as_int(client: TestClient) -> None:
    """同じ値同士の除算は 1 が int で返る。"""
    response = client.get("/divide", params={"a": 5, "b": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 1}
    assert isinstance(response.json()["result"], int)


def test_divide_non_exact_rounds_to_one_decimal(client: TestClient) -> None:
    """割り切れない 1 / 3 は小数第1位までの {"result": 0.3} が返る。"""
    response = client.get("/divide", params={"a": 1, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 0.3}


def test_divide_non_exact_result_is_float(client: TestClient) -> None:
    """割り切れない場合の結果は float で返る。"""
    response = client.get("/divide", params={"a": 1, "b": 3})
    assert isinstance(response.json()["result"], float)


def test_divide_rounds_up_second_decimal(client: TestClient) -> None:
    """2 / 3 は小数第2位が切り上がり {"result": 0.7} が返る。"""
    response = client.get("/divide", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 0.7}


def test_divide_rounding_is_half_up_not_bankers(client: TestClient) -> None:
    """1 / 4 = 0.25 は ROUND_HALF_UP で 0.3 になる（偶数丸めの 0.2 ではない）。"""
    response = client.get("/divide", params={"a": 1, "b": 4})
    assert response.status_code == 200
    assert response.json() == {"result": 0.3}


def test_divide_one_decimal_exact_value_is_float(client: TestClient) -> None:
    """5 / 2 = 2.5 は割り切れないため float の 2.5 が返る。"""
    response = client.get("/divide", params={"a": 5, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 2.5}
    assert isinstance(response.json()["result"], float)


def test_divide_smaller_than_divisor_rounds_up(client: TestClient) -> None:
    """1 / 6 = 0.1666... は小数第2位を四捨五入して 0.2 が返る。"""
    response = client.get("/divide", params={"a": 1, "b": 6})
    assert response.status_code == 200
    assert response.json() == {"result": 0.2}


def test_divide_large_numbers(client: TestClient) -> None:
    """大きな正の整数でも正しく除算される。"""
    response = client.get("/divide", params={"a": 3000000, "b": 1000000})
    assert response.status_code == 200
    assert response.json() == {"result": 3}


def test_divide_by_zero_returns_422(client: TestClient) -> None:
    """b=0 は 422 と detail を返す。"""
    response = client.get("/divide", params={"a": 1, "b": 0})
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"a": 0, "b": 1}, id="a_zero"),
        pytest.param({"a": -1, "b": 1}, id="a_negative"),
        pytest.param({"a": 1, "b": -1}, id="b_negative"),
        pytest.param({"a": 1.5, "b": 1}, id="a_decimal"),
        pytest.param({"a": 1, "b": 1.5}, id="b_decimal"),
        pytest.param({"a": "abc", "b": 1}, id="a_string"),
        pytest.param({"a": 1, "b": "abc"}, id="b_string"),
        pytest.param({"a": 1}, id="b_missing"),
        pytest.param({"b": 1}, id="a_missing"),
        pytest.param({}, id="both_missing"),
    ],
)
def test_divide_invalid_input_returns_422(
    client: TestClient, params: dict[str, Any]
) -> None:
    """正の整数でない入力と引数の欠落は 422 と detail を返す。"""
    response = client.get("/divide", params=params)
    assert response.status_code == 422
    assert "detail" in response.json()
