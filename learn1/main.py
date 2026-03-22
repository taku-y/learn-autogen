"""
AutoGen チュートリアル: 2エージェントの会話

このプログラムでは AutoGen の基本的な使い方を学びます。
- AssistantAgent: LLMを使って応答するエージェント
- RoundRobinGroupChat: 複数エージェントを順番に会話させる仕組み

LLM接続先は .env で設定します:
  LM_STUDIO_HOST=192.168.x.x
  LM_STUDIO_PORT=1234
"""

import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo

load_dotenv()


async def main() -> None:
    host = os.environ["LM_STUDIO_HOST"]
    port = os.environ.get("LM_STUDIO_PORT", "1234")
    base_url = f"http://{host}:{port}/v1"

    # LM Studio の OpenAI 互換クライアント
    # model名はLM Studioでロード中のモデル名に合わせてください
    model_client = OpenAIChatCompletionClient(
        model="local-model",
        base_url=base_url,
        api_key="lm-studio",  # LM Studioはキー不要だがライブラリ上は必須
        model_info=ModelInfo(
            vision=False,
            function_calling=False,
            json_output=False,
            family="unknown",
        ),
    )

    # アシスタントエージェント: アイデアを提案する役
    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="あなたは親切なアシスタントです。日本語で簡潔に答えてください。",
    )

    # ユーザープロキシエージェント: フィードバックを返す役
    critic = AssistantAgent(
        name="critic",
        model_client=model_client,
        system_message=(
            "あなたはレビュアーです。提案された内容に対して、"
            "改善点や良い点を日本語で1〜2文でコメントしてください。"
        ),
    )

    # 最大4回のメッセージでやり取りを終了する条件
    termination = MaxMessageTermination(max_messages=4)

    # ラウンドロビン形式でエージェントを会話させる
    team = RoundRobinGroupChat(
        participants=[assistant, critic],
        termination_condition=termination,
    )

    # タスクを与えてコンソールに出力
    await Console(
        team.run_stream(task="Pythonを学ぶ上で最も重要な概念を1つ挙げて説明してください。")
    )

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
