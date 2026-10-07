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
- divide の四捨五入は decimal の ROUND_HALF_UP を使う
- divide で割り切れる場合は整数で返す
- subtract で結果が負数の場合は問題なし
- 入力が正の整数でない場合は 422 エラーを返す
- 計算結果は整数は int、小数は float で返す
- APIサーバーへのプロトコルは HTTP を使用する

## 引数の渡し方

| 演算名    | 引数の渡し方             |
| -------- | ----------------------- |
| add      | `GET /add?a=1&b=2`      |
| subtract | `GET /subtract?a=1&b=2` |
| multiply | `GET /multiply?a=1&b=2` |
| divide   | `GET /divide?a=1&b=2`   |

## HTTPメソッドの正常時・異常時のレスポンス形式

```text
{
    "result": 3 # 正常時は結果のみ返す
}

{
    "detail": [] # detail は FastAPI 標準の検証エラー配列
}
```

## 開発環境

- APIサーバーは Dev Container 内で起動（起動コマンドはコンテナ内で実行）
- Dockerfile は Dev Container のイメージ定義

## 開発フロー

- TDD で進める（テストエージェント → 実装エージェント → レビューエージェント）
- 各エージェントの定義は `.claude/agents/` に置く
- レビューで承認が出るまでを最大3周とし、3周で承認されない場合、または同じ指摘が2周続いた場合は、作業を止めて報告する
- 報告には、エンドポイント名、各周の指摘の要約、未解決の指摘、考えられる原因を含める
- コミット、プッシュ、PR 作成は、ユーザーが明示的に指示するまで行わない（各エージェントも同様で、変更は作業ツリーに残して報告するだけにする）
- ユーザーの指示は、その作業1回分の許可であり、以降の常時の許可ではない
- ユーザーが「PR をマージし、GitHub 上の開発ブランチを削除した」と連絡したら、`main` に切り替えて `origin/main` の最新を取り込み（`git fetch --prune` で削除済みブランチの追跡情報も整理する）、ローカルの開発ブランチを `git branch -d` で削除して次の依頼に備える
- `git branch -d` で削除できない場合は `-D` を使わず、理由を報告して指示を待つ（`-D` はユーザーが指示した場合のみ使う）

## 実装完了後の想定ディレクトリ構成

```text
.claude/
    agents/
        test-agent.md
        implement-agent.md
        review-agent.md
.devcontainer/
    devcontainer.json
    Dockerfile
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

## コーディング規約

- 命名は PEP 8 に従う（変数・関数・メソッドは `snake_case`、定数は `UPPER_SNAKE_CASE`、クラスは `CapWords`）
- PEP 8 の準拠は Ruff の `N` ルールで検証する（設定は `pyproject.toml`）
- 引数名は仕様どおり `a`, `b` に統一する
- 関数名はエンドポイント名と一致させる（例: `divide`）
- テスト関数名は `test_` で始め、観点が分かる名前にする（例: `test_divide_by_zero_returns_422`）
- 全ての関数に型ヒントを付ける（MyPy の strict で検証する）

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

マージ後の後片付けで使う git コマンド（実行はユーザーの連絡を受けた後のみ。手順は「開発フロー」を参照）:

```bash
git switch main                # main に切り替え
git pull origin main           # 最新の main を取り込み
git fetch --prune              # 削除済みブランチの追跡情報を整理
git branch -d <開発ブランチ名>   # ローカルの開発ブランチを削除（-D は指示があるまで使わない）
```
