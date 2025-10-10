from pydantic_ai import Agent, RunContext
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from todoaiagent.adapters.trello.models import TrelloCard
from todoaiagent.agents.config import TodoAgentSettings
from todoaiagent.agents.models.dependencies import TodoAgentDependencies
from todoaiagent.agents.models.responses import AgentResponseModel
from todoaiagent.agents.prompts.system import system_prompt
from todoaiagent.domain.models import Todo


class TodoAgent():
    def __init__(self, settings: TodoAgentSettings):
        self.settings = settings
        self.agent = self._init_agent()

    def _init_mistral_model_provider(self):
        return MistralModel(self.settings.llm_mistral_model, provider=MistralProvider(api_key=self.settings.mistral_api_key))

    def _init_agent(self) -> Agent:
        agent = Agent(
            model = self._init_mistral_model_provider(),
            output_type=AgentResponseModel,
            system_prompt=system_prompt
            )

        @agent.tool
        def create_todos(ctx: RunContext[TodoAgentDependencies], todo_list: list[Todo]) -> list[TrelloCard]:
            """Creates todos in the project management system"""
            if ctx.deps is None:
                raise ValueError("Dependencies (ctx.deps) are not set.")
            
            todo_service = ctx.deps.todo_service
            return todo_service.createTodo(todo_list, ctx.deps.idList)
        
        return agent
    
    def run(self, query: str, deps) -> str:
        try:
            result = self.agent.run_sync(user_prompt=query, deps=deps)
            return result.output.todos
        except Exception as e:
            return f"An error occurred: {str(e)}"