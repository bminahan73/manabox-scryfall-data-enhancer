from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class Category(BaseModel):
    label: str = Field(
        description="label/category"
    )
    count: int = Field(
        description="approximate number of cards in this category"
    )

class CategoryList(BaseModel):
    categories: list[Category] = Field(
        description="A list of categories with their counts"
    )

class MagicCardSelector:
    def __init__(self, model_name: str = "glm-4.5-flash", temperature: float = 0.1):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            model_kwargs={"response_format": {"type": "json_object"}},
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
        )

        self.parser = JsonOutputParser(pydantic_object=CategoryList)

        self.prompt_template = PromptTemplate(
            input_variables=["cards", "deck_concept"],
            template="""You are a Magic: The Gathering commander deck building expert.
            You will be given a deck concept. Given that deck concept, and your knowledge of the commander format and best practices within, come up with 10-12 categories of cars that should be in the deck, as well as how many of each category the 100 card commander deck should have.
            The categories should be as specific as possible, and the number of cards in each category should be a reasonable estimate based on the deck concept.
            You sould also take the "flavor" of the deck concept into account when categorizing the cards. For example, if the deck has a funny or quirky theme, your categories should be equally as quirky and fun.
            Similarly, if the deck concept is more serious or strategic, your categories should be optimal and focused on the most effective strategies to win the game.
            Do not forget about land! The total for all categories should add up to 100 cards, including the commander(s).
            {format_instructions}
            Deck Concept: {deck_concept}"""
        )
        
        self.chain = self.prompt_template | self.llm | self.parser

    def determine_categories(self, deck_concept: str) -> CategoryList:
        response = self.chain.invoke({
            "deck_concept": deck_concept,
            "format_instructions": self.parser.get_format_instructions()
        })
        return response

if __name__ == "__main__":
    selector = MagicCardSelector()
    deck_concept = "I'm building a red burn deck focused on direct damage to the opponent"
    categories = selector.determine_categories(deck_concept)
    print(categories)