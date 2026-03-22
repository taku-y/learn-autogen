"""
AutoGen チュートリアル: SelectorGroupChat による動的エージェント選択

LLM が毎ターン会話履歴を読み、次に発言するエージェントを動的に選ぶ。

エージェント構成:
- planner : タスクの計画を立てる
- executor: 計画に従って実装する
- critic  : 成果物をレビューし、問題なければ "APPROVED" を出力する

終了条件:
- TextMentionTermination: "APPROVED" が出たら終了
- MaxMessageTermination : 最大10メッセージで強制終了
- 上記の OR で設定

出力: learn2 と同様に run_stream イベントを直接処理してリアルタイム表示

LLM接続先は .env で設定します:
  LM_STUDIO_HOST=192.168.x.x
  LM_STUDIO_PORT=1234
"""

import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage
from autogen_agentchat.teams import SelectorGroupChat
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

    planner = AssistantAgent(
        name="planner",
        model_client=model_client,
        system_message=(
            "あなたはソフトウェア開発の計画担当者です。"
            "タスクを受け取ったら、実装ステップを箇条書きで簡潔に計画してください。"
            "日本語で答えてください。"
        ),
    )

    executor = AssistantAgent(
        name="executor",
        model_client=model_client,
        system_message=(
            "あなたはソフトウェアエンジニアです。"
            "planner の計画に従い、Pythonコードを実装してください。"
            "コードはコードブロック（```python）で記述してください。"
            "日本語で説明を添えてください。"
        ),
    )

    critic = AssistantAgent(
        name="critic",
        model_client=model_client,
        system_message=(
            "あなたはコードレビュアーです。"
            "executor が実装したコードをレビューし、改善点があれば指摘してください。"
            "問題がなく承認できる場合は、必ず最後に 'APPROVED' と出力してください。"
            "日本語で答えてください。"
        ),
    )

    # 終了条件: "APPROVED" が出るか、最大10メッセージで終了
    termination = TextMentionTermination("APPROVED") | MaxMessageTermination(max_messages=10)

    # SelectorGroupChat: model_client が毎ターン次の発言者を選ぶ
    team = SelectorGroupChat(
        participants=[planner, executor, critic],
        model_client=model_client,
        termination_condition=termination,
        selector_prompt=(
            "You are a facilitator. The following roles are available:\n"
            "{roles}\n\n"
            "{history}\n\n"
            "Select the next role to speak from {participants}. "
            "Return only the role name, nothing else."
        ),
    )

    # run_stream イベントを直接処理してリアルタイム出力
    current_source = None
    async for event in team.run_stream(
        task="Pythonで簡単なFizzBuzzを実装する計画を立て、実装し、レビューしてください。"
    ):
        if isinstance(event, ModelClientStreamingChunkEvent):
            if event.source != current_source:
                current_source = event.source
                print(f"\n[{current_source}]: ", end="", flush=True)
            print(event.content, end="", flush=True)
        elif isinstance(event, TextMessage):
            if current_source == event.source:
                print()
                current_source = None
            else:
                print(f"\n[{event.source}]: {event.content}")

    print("\n--- 会話終了 ---")
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
