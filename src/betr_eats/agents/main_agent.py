import asyncio

from agents import Agent, Runner, OpenAIChatCompletionsModel, SQLiteSession

from betr_eats.helpers.model import Model
from betr_eats.agents.prompts import system_prompt
from betr_eats.agents.tools import (
    search_calorie_count,
    write_meal_log,
    get_meal_log_for_day,
    write_weight_log,
)


class MainAgent:
    def __init__(self, model: Model):
        self.session = SQLiteSession(session_id="betr-eats")
        self.agent = Agent(
            name="Betr Eats",
            instructions=system_prompt,
            tools=[search_calorie_count, write_meal_log, get_meal_log_for_day, write_weight_log],
            model=OpenAIChatCompletionsModel(
                model=model.model_id, openai_client=model.client
            ),
        )

    async def _run(self, user_input: str) -> str:
        result = await Runner.run(self.agent, user_input, session=self.session)
        return result.final_output

    def run(self, user_input: str) -> str:
        return asyncio.run(self._run(user_input))

    def clear_history(self) -> None:
        asyncio.run(self.session.clear_session())
