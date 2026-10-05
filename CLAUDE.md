# CLAUDE.md

このファイルは、このリポジトリで作業するClaude Code (claude.ai/code) に向けたガイダンスを提供する。

## プロジェクト概要

2つの正の整数を受け取り、四則演算を行うシンプルな計算APIサーバー。

## エンドポイント

- `add`: 加算
- `subtract`: 減算
- `multiply`: 乗算
- `divide`: 除算

## 仕様

- 引数は正の整数2つ（例: `a`, `b`）
- divide で b=0 は正の整数でないため 422 エラーを返す
- divide の結果が小数の場合は小数点第2位を四捨五入して小数点以下を1桁にする
- divide の四捨五入は decimal の ROUND_HALF_UP などを使う
- divide で割り切れる場合は整数で返す
- subtract で結果が負数の場合は問題なし
- 入力が正の整数でない場合は 422 エラーを返す

## 実装完了後の想定ディレクトリ構成

```text
pyproject.toml
app/
    main.py
    router/
        add.py
        subtract.py
        multiply.py
        divide.py
tests/
    unit/
        test_add.py
        test_subtract.py
        test_multiply.py
        test_divide.py
```

## 使用ツール

- 使用言語: Python 3.12
- 使用フレームワーク: FastAPI
- リント: Ruff
- 静的チェック: MyPy
- テスト: Pytest

## 使用コマンド

```bash
uv sync                                            # 依存関係のインストール
uv run uvicorn app.main:app --reload               # 開発サーバー起動
uv run pytest tests/unit/ -v                       # ユニットテスト実行
uv run pytest tests/unit/test_xxx.py::test_name -v # 単一テスト実行
uv run ruff check .                                # lint実行
uv run ruff format --check .                       # フォーマット差分チェック(適用しない)
uv run mypy app/                                   # 型チェック(appディレクトリのみ対象)
```

