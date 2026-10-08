"""add エンドポイントのユニットテスト。"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """FastAPI アプリを対象とする TestClient を返す。"""
    from app.main import app

    return TestClient(app)


def test_add_returns_sum_with_200(client: TestClient) -> None:
    """1 + 2 でステータス 200 と {"result": 3} が返る。"""
    response = client.get("/add", params={"a": 1, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 3}


def test_add_result_is_int(client: TestClient) -> None:
    """加算結果は int で返る。"""
    response = client.get("/add", params={"a": 1, "b": 2})
    assert isinstance(response.json()["result"], int)


def test_add_large_numbers(client: TestClient) -> None:
    """大きな正の整数でも正しく加算される。"""
    response = client.get("/add", params={"a": 1000000, "b": 2000000})
    assert response.status_code == 200
    assert response.json() == {"result": 3000000}


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
def test_add_invalid_input_returns_422(client: TestClient, params: dict) -> None:
    """正の整数でない入力と引数の欠落は 422 と detail を返す。"""
    response = client.get("/add", params=params)
    assert response.status_code == 422
    assert "detail" in response.json()
