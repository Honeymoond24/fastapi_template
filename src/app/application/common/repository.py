from typing import Protocol


class UserRepository(Protocol):
    """User repository interface"""

    async def create(self, user: User) -> UserDTO:
        """Create"""

    async def get(self, user_id: UserId) -> UserDTO | None:
        """Get by id"""

    async def update(self, user_id: UserId, updated_user: UserDTO) -> UserDTO | None:
        """Update"""

    async def delete(self, user_id: UserId) -> None:
        """Delete"""