# learn4 - SelectorGroupChat による動的エージェント選択

LLM が毎ターン会話履歴を読んで次の発言者を動的に選ぶ `SelectorGroupChat` の例です。

## プログラムの内容

### エージェント構成

| エージェント | 役割 |
|-------------|------|
| `planner` | タスクを受け取り、実装ステップを計画する |
| `executor` | 計画に従って Python コードを実装する |
| `critic` | コードをレビューし、問題なければ `APPROVED` を出力する |

### 実行の流れ

```
タスク
  ↓
planner → 計画を立てる
  ↓
executor → コードを実装する
  ↓
critic → レビュー → 問題あれば指摘（executor に戻る）
                  → 問題なければ "APPROVED" → 終了
```

LLM が会話履歴を見て最適な次の発言者を選ぶため、必要に応じて同じエージェントが複数回発言したり、順番が入れ替わることがあります。

### 終了条件（OR）

| 条件 | 説明 |
|------|------|
| `TextMentionTermination("APPROVED")` | critic が承認したとき |
| `MaxMessageTermination(10)` | メッセージ数が上限に達したとき |

## learn1/2 との違い

| | learn1/2 | learn4 |
|--|----------|--------|
| チーム | `RoundRobinGroupChat` | `SelectorGroupChat` |
| 発言順 | 固定（ラウンドロビン） | LLM が動的に決定 |
| エージェント数 | 2 | 3（planner / executor / critic） |
| 終了条件 | `MaxMessageTermination` のみ | `TextMentionTermination` OR `MaxMessageTermination` |

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
learn4/
├── main.py          # メインプログラム
├── .env             # LM Studio接続先設定（git管理外）
├── pyproject.toml   # プロジェクト設定・依存パッケージ
└── README.md        # このファイル
```
