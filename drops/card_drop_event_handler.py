from datetime import datetime
import pytz
from database.models.card_drop_event_model import CardDropEventModel
from database.models.user_card_model import UserCardModel
from database.models.user_model import UserModel
from database.session import get_session
from drops.card_drop_event import CardDropEvent
from schemas.pokemon_card_schema import PokemonCardSchema, PokemonTCGCardLoader


class CardDropEventHandler:
    async def create_drop_event_random(card_amount: int, discord_message):
        random_cards = [PokemonTCGCardLoader.random() for _ in range(card_amount)]
        event = CardDropEvent(random_cards, discord_message)

        async with get_session() as session:
            db_user = await session.get(UserModel, event.owner_discord_id)
            if db_user is None:
                raise UserNotExistError(f"User with id:{event.owner_discord_id} does not exist.")

            event_model = CardDropEventModel.from_card_drop_event(event)
            session.add(event_model)
            await session.commit()

        return event

    async def claim_card_index(drop_event: CardDropEvent, discord_user_id: int, card_index: int) -> PokemonCardSchema:
        can_claim, error_message = CardDropEventHandler.can_user_claim_card(drop_event, discord_user_id, card_index)

        if not can_claim:
            raise InvalidClaimError(error_message)

        drop_event.claimed_cards[card_index] = discord_user_id
        claimed_card = drop_event.all_cards[card_index]

        async with get_session() as session:
            ##get the db user
            db_user = await session.get(UserModel, discord_user_id)
            if db_user is None:
                raise UserNotExistError(f"User with id:{discord_user_id} does not exist.")

            user_card = UserCardModel.new_user_card_claim_event(discord_user_id, claimed_card, drop_event)
            session.add(user_card)
            await session.commit()

        return claimed_card
    
    def can_user_claim_card(drop_event: CardDropEvent, user_discord_id: int, card_index: int) -> tuple[bool, str]:
        if drop_event.claimed_cards[card_index] is not None:
            return False, "This card has already been claimed."

        # Check if user has already claimed a card
        if user_discord_id in drop_event.claimed_cards:
            return False, "You have already claimed a card from this drop."

        # Owner can always interact (provided they haven't claimed one already)
        if user_discord_id == drop_event.owner_discord_id:
            return True, None
        
        # Check if Non-Owner time brace has expired
        timezone = pytz.timezone('UTC')  # Use UTC for consistency
        current_time = datetime.now(timezone)
        time_difference = current_time - drop_event.created_at
        owner_only = time_difference.total_seconds() <= drop_event.OWNER_ONLY_DURATION_SECONDS
        if owner_only:
            return False, f"You must wait at least {drop_event.OWNER_ONLY_DURATION_SECONDS} seconds to claim someone else's drop. Time left: {time_difference.total_seconds()} seconds"
        else:
            return True, None

class InvalidClaimError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self):
        # You can customize the string representation of the error
        return f"Invalid Claim Error: {self.message}"

class UserNotExistError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self):
        # You can customize the string representation of the error
        return f"User Not Exist: {self.message}"
