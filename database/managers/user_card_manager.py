from sqlalchemy import func, select
from database.managers.user_manager import UserNotExistError
from database.models.user_card_model import UserCardModel
from database.models.user_model import UserModel
from database.session import get_session
from drops.card_drop_event import CardDropEvent
from schemas.pokemon_card_schema import PokemonCardSchema
from utils.card_utils import CardUtil

class UserCardManager:
    @staticmethod
    async def create_new_user_card(discord_user_id: int, pokemon_tcg_card_id: str, card_drop_event: CardDropEvent) -> UserCardModel:
        async with get_session() as session:

            db_user = await session.get(UserModel, discord_user_id)
            if db_user is None:
                raise UserNotExistError(f"User with id:{discord_user_id} does not exist.")

            user_card = UserCardModel()
            user_card.pokemon_tcg_card_id = pokemon_tcg_card_id
            user_card.owner_id = discord_user_id
            user_card.drop_event_id = card_drop_event.id

            user_card.pattern_number = CardUtil.get_random_pattern_number()
            user_card.float_value = CardUtil.get_random_float_value()

            result = await session.execute(
                select(func.max(UserCardModel.print_number)).filter_by(
                    pokemon_tcg_card_id=pokemon_tcg_card_id
                )
            )

            max_print_number: int = result.scalar() or 0
            new_print_number = max_print_number + 1

            user_card.print_number = new_print_number

            session.add(user_card)
            await session.commit()

            return user_card

