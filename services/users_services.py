from typing import Optional, Dict

from models.user import User


async def get_user_by_id(user_id: int) -> Optional[User]:
    return await User.get(user_id)


async def create_user(user_data: Dict) -> User:
    user = await User.create(
        id=int(user_data['id']),
        username=user_data['display_name'],
        avatar=user_data['profile_image_url']
    )
    return user


async def update_user(user: User, user_data: Dict):
    if (
            user.username != user_data['display_name']
            or user.avatar != user_data['profile_image_url']
    ):
        await user.update(
            username=user_data['display_name'],
            avatar=user_data['profile_image_url']
        ).apply()


async def set_favorite_streamer(user: User, streamer_name: str) ->  None:
    await user.update(
        follow_to=streamer_name
    ).apply()
