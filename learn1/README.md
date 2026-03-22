# learn1 - AutoGen チュートリアル

Microsoft AutoGen の基本的な使い方を学ぶためのサンプルプログラムです。

## プログラムの内容

2つのエージェントが順番に会話する、最もシンプルな AutoGen の構成です。

| エージェント | 役割 |
|-------------|------|
| `assistant` | タスクに対して回答・提案を行う |
| `critic` | `assistant` の回答にコメント・フィードバックを返す |

会話は `RoundRobinGroupChat` によってラウンドロビン形式で進み、最大4メッセージで終了します。

```
タスク → assistant → critic → assistant → critic → 終了
```

LLMには自宅サーバで動作する **LM Studio** を使用します（OpenAI互換API）。

## セットアップ

### 1. 依存パッケージのインストール

```bash
uv sync
```

### 2. `.env` の設定

`.env` ファイルにLM StudioサーバのIPアドレスとポートを記載します。

```
LM_STUDIO_HOST=192.168.x.x
LM_STUDIO_PORT=1234
```

### 3. LM Studio の起動

LM Studio の「Local Server」タブからサーバを起動し、使用するモデルをロードしてください。

## 実行

```bash
uv run python main.py
```

## ファイル構成

```
learn1/
├── main.py          # メインプログラム
├── .env             # LM Studio接続先設定（git管理外）
├── pyproject.toml   # プロジェクト設定・依存パッケージ
└── README.md        # このファイル
```
