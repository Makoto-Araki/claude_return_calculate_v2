"""multiply エンドポイントのユニットテスト。"""

from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """FastAPI アプリを対象とする TestClient を返す。"""
    from app.main import app

    return TestClient(app)


def test_multiply_returns_product_with_200(client: TestClient) -> None:
    """2 * 3 でステータス 200 と {"result": 6} が返る。"""
    response = client.get("/multiply", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 6}


def test_multiply_result_is_int(client: TestClient) -> None:
    """乗算結果は int で返る。"""
    response = client.get("/multiply", params={"a": 2, "b": 3})
    assert isinstance(response.json()["result"], int)


def test_multiply_by_one_returns_same_number(client: TestClient) -> None:
    """1 を掛けると元の値が int で返る。"""
    response = client.get("/multiply", params={"a": 7, "b": 1})
    assert response.status_code == 200
    assert response.json() == {"result": 7}
    assert isinstance(response.json()["result"], int)


def test_multiply_large_numbers(client: TestClient) -> None:
    """大きな正の整数でも正しく乗算される。"""
    response = client.get("/multiply", params={"a": 3000000, "b": 2000000})
    assert response.status_code == 200
    assert response.json() == {"result": 6000000000000}


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
def test_multiply_invalid_input_returns_422(
    client: TestClient, params: dict[str, Any]
) -> None:
    """正の整数でない入力と引数の欠落は 422 と detail を返す。"""
    response = client.get("/multiply", params=params)
    assert response.status_code == 422
    assert "detail" in response.json()
