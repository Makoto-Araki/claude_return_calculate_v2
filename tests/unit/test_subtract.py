"""subtract エンドポイントのユニットテスト。"""

from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """FastAPI アプリを対象とする TestClient を返す。"""
    from app.main import app

    return TestClient(app)


def test_subtract_returns_difference_with_200(client: TestClient) -> None:
    """3 - 1 でステータス 200 と {"result": 2} が返る。"""
    response = client.get("/subtract", params={"a": 3, "b": 1})
    assert response.status_code == 200
    assert response.json() == {"result": 2}


def test_subtract_result_is_int(client: TestClient) -> None:
    """減算結果は int で返る。"""
    response = client.get("/subtract", params={"a": 3, "b": 1})
    assert isinstance(response.json()["result"], int)


def test_subtract_negative_result_is_allowed(client: TestClient) -> None:
    """結果が負数になる 1 - 3 は 200 と {"result": -2} が返る。"""
    response = client.get("/subtract", params={"a": 1, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": -2}


def test_subtract_same_numbers_returns_zero(client: TestClient) -> None:
    """同じ値同士の減算は 0 が int で返る。"""
    response = client.get("/subtract", params={"a": 5, "b": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 0}
    assert isinstance(response.json()["result"], int)


def test_subtract_large_numbers(client: TestClient) -> None:
    """大きな正の整数でも正しく減算される。"""
    response = client.get("/subtract", params={"a": 3000000, "b": 1000000})
    assert response.status_code == 200
    assert response.json() == {"result": 2000000}


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"a": 0, "b": 1}, id="a_zero"),
        pytest.param({"a": 1, "b": 0}, id="b_zero"),
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
def test_subtract_invalid_input_returns_422(
    client: TestClient, params: dict[str, Any]
) -> None:
    """正の整数でない入力と引数の欠落は 422 と detail を返す。"""
    response = client.get("/subtract", params=params)
    assert response.status_code == 422
    assert "detail" in response.json()
