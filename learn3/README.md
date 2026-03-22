# learn3 - Function Calling

エージェントがツール（Python関数）を呼び出してタスクを解決する例です。

## プログラムの内容

`AssistantAgent` にツールを登録し、エージェントが必要に応じてツールを呼び出します。

### 登録ツール

| ツール | 説明 |
|--------|------|
| `get_weather(city)` | 指定した都市の天気予報を返す（モック） |
| `calculate(expression)` | 四則演算を行う |

### 実行の流れ

```
タスク → エージェントが判断 → ツール呼び出し（Function Call）→ 結果を受け取り → 回答
```

エージェントは1つのタスクに対して複数のツールを順番に呼び出すことができます。

## learn1/2 との違い

| | learn1/2 | learn3 |
|--|----------|--------|
| エージェント数 | 2（assistant + critic） | 1 |
| ツール | なし | `get_weather`, `calculate` |
| `ModelInfo.function_calling` | `False` | `True` |

## 注意: モデルの要件

Function Calling はモデルが対応している必要があります。
LM Studio でロードするモデルは **function calling 対応** のものを選んでください。

対応モデルの例:
- Llama 3.1 / 3.2 / 3.3
- Qwen 2.5
- Mistral / Mixtral（一部）

## セットアップ

### 1. 依存パッケージのインストール

```bash
uv sync
```

### 2. `.env` の設定

```
LM_STUDIO_HOST=192.168.x.x
LM_STUDIO_PORT=1234
```

### 3. LM Studio の起動

Function Calling 対応モデルをロードしてサーバを起動してください。

## 実行

```bash
uv run python main.py
```

## ファイル構成

```
learn3/
├── main.py          # メインプログラム（ツール定義 + エージェント）
├── .env             # LM Studio接続先設定（git管理外）
├── pyproject.toml   # プロジェクト設定・依存パッケージ
└── README.md        # このファイル
```
