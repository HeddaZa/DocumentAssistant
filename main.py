from llm.llm_factory import LLMFactory
from load_config import load_config


def main() -> str:
    """Loads configuration and creates LLM instance."""
    config = load_config("config.yaml")

    llm = LLMFactory.create_llm(config)

    prompt = "What is the capital of France?"
    response = llm.call(prompt)
    return response


if __name__ == "__main__":
    main()
