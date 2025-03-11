import threading
from drops.card_drop_event import CardDropEvent
from pokemon_tcg_card import PokemonTCGCardLoader


class CardDropManager:
    _instance = None
    _lock = threading.Lock()

    """
    Manages DropEvent instances.
    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(CardDropManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.drop_events = {}

    def create_drop_event_random(self, card_amount: int, discord_message):
        random_cards = [PokemonTCGCardLoader.random() for _ in range(card_amount)]

        event = CardDropEvent(random_cards, discord_message)
        self.drop_events[event.id] = event

        #TODO save event in DB

        return event
    
    def on_event_timed_out(self, event_id: str):
        self.drop_events.pop(event_id, None)