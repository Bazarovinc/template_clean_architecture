from common.dto.base import BaseEventSchema


class BaseBookEventSchema(BaseEventSchema):
    id: int
    name: str
    release_year: int


class BookCreatedEventSchema(BaseBookEventSchema):
    pass


class BookUpdatedEventSchema(BaseBookEventSchema):
    pass


class BookDeletedEventSchema(BaseBookEventSchema):
    pass


class SomeInternalEventSchema(BaseEventSchema):
    id: int
