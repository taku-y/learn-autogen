# learn2 - リアルタイムストリーミング出力

learn1 をベースに、エージェントの応答をトークン単位でリアルタイム表示するサンプルです。

## learn1 との違い

learn1 では `Console` に `run_stream` を委譲していたため、LM Studio が応答をまとめて返す場合に一括出力となっていました。

learn2 では `run_stream` のイベントを直接 `async for` で処理し、`ModelClientStreamingChunkEvent` を受け取るたびに即時出力します。

| | learn1 | learn2 |
|--|--------|--------|
| 出力方式 | `Console(team.run_stream(...))` | `async for event in team.run_stream(...)` |
| 出力タイミング | メッセージ完了後 | トークン受信ごと（リアルタイム） |

## プログラムの内容

2つのエージェントがラウンドロビン形式で会話し、各エージェントの応答がトークン単位で出力されます。

| エージェント | 役割 |
|-------------|------|
| `assistant` | タスクに対して回答・提案を行う |
| `critic` | `assistant` の回答にコメント・フィードバックを返す |

```
タスク → [assistant]: トークン1トークン2... → [critic]: トークン1トークン2... → 終了
```

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

LM Studio の「Local Server」タブからサーバを起動し、使用するモデルをロードしてください。

## 実行

```bash
uv run python main.py
```

## ファイル構成

```
learn2/
├── main.py          # メインプログラム
├── .env             # LM Studio接続先設定（git管理外）
├── pyproject.toml   # プロジェクト設定・依存パッケージ
└── README.md        # このファイル
```
