from __future__ import annotations

import logging

from openai import AsyncOpenAI

from src.models.assistant import Assistant, AssistantCreate

logger = logging.getLogger(__name__)
client = AsyncOpenAI()


async def create_assistant(cfg: AssistantCreate) -> Assistant:
    response = await client.beta.assistants.create(**cfg.input_to_api_create())
    return Assistant.from_api_output(response)


async def list_assistants(limit: int = "20", order: str = "desc",
        after: str = '') -> list[Assistant]:
    if after == '':
        response = await client.beta.assistants.list(limit=limit, order=order)
    else:
        response = await client.beta.assistants.list(limit=limit, order=order,
                after=after)
    assistants = []
    for d in response.data:
        assistants.append(Assistant.from_api_output(d))
    return assistants


async def get_assistant(id: str) -> Assistant:
    """Get an assistant. If the assistant is not found, raise openai.NotFoundError."""
    response = await client.beta.assistants.retrieve(assistant_id=id)
    return Assistant.from_api_output(response)


async def update_assistant(cfg: Assistant) -> Assistant:
    response = await client.beta.assistants.update(**cfg.input_to_api_update())
    return Assistant.from_api_output(response)


async def delete_assistant(id: str) -> None:
    """Delete an assistant. If the assistant is not found, raise openai.NotFoundError."""
    response = await client.beta.assistants.delete(assistant_id=id)
    if response.deleted:
        logger.info(f"Deleted assistant {response.id}")
        return
    else:
        logger.info(f"Failed to delete assistant {response.id}")
        return
