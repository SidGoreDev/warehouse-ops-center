REASONING_SUFFIX = """Answer the question using the following format:

<think>
Briefly explain your reasoning (max 3 sentences).
</think>

Write your final answer immediately after the </think> tag.
"""


def with_reasoning_suffix(prompt: str) -> str:
    prompt = prompt.rstrip() + "\n\n" + REASONING_SUFFIX
    return prompt
