import os
from dotenv import load_dotenv
from betr_eats.helpers.model import Model
from betr_eats.agents.main_agent import MainAgent

load_dotenv()

model = Model(os.getenv("HF_MODEL"))
agent = MainAgent(model)
query = "I ate a mcdonalds cheeseburger and large fries. How many calories did I consume? Log the meal."
# query = "What did I eat on May 21st 2026?"
#query = "I weighed 280.5 lbs on May 25th 2026. Log it."
result = agent.run(query)
print(result)