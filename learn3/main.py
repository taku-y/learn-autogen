"""
AutoGen チュートリアル: Function Calling

エージェントがツール（Python関数）を呼び出してタスクを解決する例。
- get_weather: 指定した都市の天気予報を返す（モック）
- calculate: 四則演算を行う

LLM接続先は .env で設定します:
  LM_STUDIO_HOST=192.168.x.x
  LM_STUDIO_PORT=1234

注意: Function Calling はモデルが対応している必要があります。
LM Studio でロードするモデルは function calling 対応のものを選んでください。
"""

import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo

load_dotenv()


# --- ツール定義 ---
# 関数の型アノテーションと docstring が AutoGen によってスキーマに変換される

def get_weather(city: str) -> str:
    """指定した都市の現在の天気予報を返す。

    Args:
        city: 天気を調べたい都市名（例: 東京、大阪、札幌）
    """
    # 実際のAPIの代わりにモックデータを返す
    weather_data = {
        "東京": "晴れ、気温22℃、湿度50%",
        "大阪": "曇り、気温20℃、湿度60%",
        "札幌": "雪、気温-2℃、湿度70%",
        "福岡": "雨、気温18℃、湿度80%",
        "名古屋": "晴れ、気温21℃、湿度55%",
    }
    return weather_data.get(city, f"{city}の天気データは見つかりませんでした。")


def calculate(expression: str) -> str:
    """数式を計算して結果を返す。四則演算（+, -, *, /）と括弧が使える。

    Args:
        expression: 計算したい数式（例: "3 + 5 * 2", "(10 + 5) / 3"）
    """
    try:
        # eval は通常危険だが、ここでは学習目的のためシンプルに実装
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "エラー: 使用できない文字が含まれています。"
        result = eval(expression)  # noqa: S307
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "エラー: ゼロ除算はできません。"
    except Exception as e:
        return f"エラー: {e}"


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
            function_calling=True,   # Function Calling を有効化
            json_output=False,
            family="unknown",
        ),
    )

    # ツールを持つエージェント
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[get_weather, calculate],  # 関数をそのまま渡す
        system_message=(
            "あなたは便利なアシスタントです。"
            "天気を調べたり計算が必要な場合はツールを使ってください。"
            "日本語で答えてください。"
        ),
    )

    # 複数のツールを使うタスクを与える
    await Console(
        agent.run_stream(
            task=(
                "東京と大阪の天気を教えてください。"
                "また、東京の気温と大阪の気温の平均を計算してください。"
            )
        )
    )

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
