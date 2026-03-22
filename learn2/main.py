"""
AutoGen チュートリアル: リアルタイムストリーミング出力

learn1 との違い:
- Console への委譲をやめ、run_stream のイベントを直接処理する
- ModelClientStreamingChunkEvent を拾うことでトークン単位のリアルタイム出力を実現

LLM接続先は .env で設定します:
  LM_STUDIO_HOST=192.168.x.x
  LM_STUDIO_PORT=1234
"""

import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo

load_dotenv()


async def main() -> None:
    host = os.environ["LM_STUDIO_HOST"]
    port = os.environ.get("LM_STUDIO_PORT", "1234")
    base_url = f"http://{host}:{port}/v1"

    model_client = OpenAIChatCompletionClient(
        model="local-model",
        base_url=base_url,
        api_key="lm-studio",
        model_info=ModelInfo(
            vision=False,
            function_calling=False,
            json_output=False,
            family="unknown",
        ),
    )

    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="あなたは親切なアシスタントです。日本語で簡潔に答えてください。",
    )

    critic = AssistantAgent(
        name="critic",
        model_client=model_client,
        system_message=(
            "あなたはレビュアーです。提案された内容に対して、"
            "改善点や良い点を日本語で1〜2文でコメントしてください。"
        ),
    )

    termination = MaxMessageTermination(max_messages=4)

    team = RoundRobinGroupChat(
        participants=[assistant, critic],
        termination_condition=termination,
    )

    # run_stream のイベントを直接処理してリアルタイム出力
    current_source = None
    async for event in team.run_stream(
        task="Pythonを学ぶ上で最も重要な概念を1つ挙げて説明してください。"
    ):
        if isinstance(event, ModelClientStreamingChunkEvent):
            # トークンが届くたびに即時出力（ストリーミングあり）
            if event.source != current_source:
                current_source = event.source
                print(f"\n[{current_source}]: ", end="", flush=True)
            print(event.content, end="", flush=True)
        elif isinstance(event, TextMessage):
            if current_source == event.source:
                # ストリーミングチャンクの後にくる完了通知 → 改行のみ
                print()
                current_source = None
            else:
                # ストリーミングなし → テキスト全体を一括表示
                print(f"\n[{event.source}]: {event.content}")

    print("\n--- 会話終了 ---")
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
