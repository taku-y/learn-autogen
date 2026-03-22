# learn-autogen

Microsoft AutoGen を学ぶためのサンプル集です。
LLMには自宅サーバで動作する **LM Studio** を使用します（OpenAI互換API）。

## サンプル一覧

| ディレクトリ | テーマ | 概要 |
|-------------|--------|------|
| [learn1](./learn1/) | 基本的な2エージェント会話 | `AssistantAgent` + `RoundRobinGroupChat` の最小構成 |
| [learn2](./learn2/) | リアルタイムストリーミング出力 | `run_stream` イベントを直接処理してトークン単位で出力 |
| [learn3](./learn3/) | Function Calling | 天気予報・計算ツールをエージェントから呼び出す |

## learn1 - 基本的な2エージェント会話

`assistant`（提案役）と `critic`（レビュー役）が最大4回やり取りする最もシンプルな構成。
詳細は [learn1/README.md](./learn1/README.md) を参照。

```bash
cd learn1
uv run python main.py
```

## learn2 - リアルタイムストリーミング出力

learn1 と同じ2エージェント構成だが、`Console` を使わず `run_stream` のイベントを直接処理することで、LM Studio からのトークンをリアルタイムに表示する。
詳細は [learn2/README.md](./learn2/README.md) を参照。

```bash
cd learn2
uv run python main.py
```

## learn3 - Function Calling

`get_weather`（天気予報）と `calculate`（計算）の2つのツールを持つエージェントが、タスクに応じてツールを呼び出す。Function Calling 対応モデルが必要。
詳細は [learn3/README.md](./learn3/README.md) を参照。

```bash
cd learn3
uv run python main.py
```

## 共通セットアップ

各ディレクトリの `.env` にLM StudioサーバのIPアドレスとポートを設定してください。

```
LM_STUDIO_HOST=192.168.x.x
LM_STUDIO_PORT=1234
```

LM Studio の「Local Server」タブからサーバを起動し、モデルをロードしてから実行してください。
