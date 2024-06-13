from dataclasses import dataclass


@dataclass
class UserID:
    id: int


@dataclass
class UserCreate:
    username: str


@dataclass
class UserGet(UserCreate):
    user_id: UserID


@dataclass
class SomeResult:
    user_id: int
