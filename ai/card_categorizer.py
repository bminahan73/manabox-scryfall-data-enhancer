from typing import List, Dict
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class CardCategory(BaseModel):
    category: str = Field(
        description="label/category of these cards"
    )
    cards: List[str] = Field(
        description="list of card names"
    )

class CardCategories(BaseModel):
    categories: List[CardCategory] = Field(
        description="organized list of cards into different categories"
    )

class MagicCardSelector:
    def __init__(self, model_name: str = "glm-4.5-flash", temperature: float = 0.1):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            model_kwargs={"response_format": {"type": "json_object"}},
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
            max_completion_tokens=2000
        )

        self.parser = JsonOutputParser(pydantic_object=CardCategories)

        self.prompt_template = PromptTemplate(
            input_variables=["cards", "deck_concept"],
            template="""You are a Magic: The Gathering commander deck building expert.
            You will be given a deck concept and a list of Magic: The Gathering cards that have been filtered from a broader collection,
            but the card list is not as focused as it should be towards the deck concept.
            The cards you will see will also not be the full list of filtered cards, but rather a handful of what remains.
            To aid in completing a deck list, your job is to organize these cards into categories that would be relevant to the deck concept.
            The categories for this deck are:
            {categories}
            A card can be in more than one category. If it fulfills more than one job, it should be placed in all relevant categories.
            If a card does not fit into a category which is relevant to the deck concept, put it in a special category called "CUT" to signify I should cut the card from the deck.
            {format_instructions}
            Deck Concept: {deck_concept}
            Cards:
            {cards}"""
        )
        
        self.chain = self.prompt_template | self.llm | self.parser

    def categorize_cards(self, cards: List[Dict], deck_concept: str, categories: list[str]) -> CardCategories:
        formatted_cards = "\n".join(
            f"- {card.get('name', 'Unknown')}: {card.get('mana_cost', '')} - {card.get('type_line', '')}\n" +
            f"  Text: {card.get('oracle_text', '')}\n" +
            f"  {card.get('power', '')}/{card.get('toughness', '') if 'power' in card else ''}\n"
            for card in cards
        )
        formatted_categories = "\n".join(f"- {category}" for category in categories)
        response = self.chain.invoke({
            "cards": formatted_cards,
            "deck_concept": deck_concept,
            "categories": formatted_categories,
            "format_instructions": self.parser.get_format_instructions()
        })
        return response

if __name__ == "__main__":
    sample_cards = [
        {
            "name": "Lightning Bolt",
            "mana_cost": "{R}",
            "type_line": "Instant",
            "oracle_text": "Lightning Bolt deals 3 damage to any target."
        },
        {
            "name": "Sol Ring",
            "mana_cost": "{1}",
            "type_line": "Artifact",
            "oracle_text": "{T}: Add {C}{C}."
        },
        {
            "name": "Dark Ritual",
            "mana_cost": "{B}",
            "type_line": "Instant",
            "oracle_text": "Add {B}{B}{B} to your mana pool."
        },
        {
            "name": "Island",
            "mana_cost": "",
            "type_line": "Basic Land",
            "oracle_text": "{T}: Add {U}."
        },
        {
            "name": "Tarmogoyf",
            "mana_cost": "{1}{G}",
            "type_line": "Creature — Lhurgoyf",
            "oracle_text": "Tarmogoyf's power is equal to the number of card types among cards in all graveyards and its toughness is equal to that number plus 1.",
            "power": "0",
            "toughness": "1"
        },
        {
            "name": "Ancestral Recall",
            "mana_cost": "{U}",
            "type_line": "Instant",
            "oracle_text": "Target player draws three cards."
        },
        {
            "name": "Black Lotus",
            "mana_cost": "",
            "type_line": "Artifact",
            "oracle_text": "{T}, Sacrifice Black Lotus: Add three mana of any one color."
        },
        {
            "name": "Serra Angel",
            "mana_cost": "{3}{W}{W}",
            "type_line": "Creature — Angel",
            "oracle_text": "Flying, Vigilance",
            "power": "4",
            "toughness": "4"
        },
        {
            "name": "Counterspell",
            "mana_cost": "{U}{U}",
            "type_line": "Instant",
            "oracle_text": "Counter target spell."
        },
        {
            "name": "Swords to Plowshares",
            "mana_cost": "{W}",
            "type_line": "Instant",
            "oracle_text": "Exile target creature. Its controller gains life equal to its power."
        }
    ]
    selector = MagicCardSelector()
    deck_concept = "I'm building a red burn deck focused on direct damage to the opponent"
    categories = selector.categorize_cards(sample_cards, deck_concept, ["Direct Damage", "Removal", "Ramp"])
    print(categories)