import uuid

from sqlmodel import select, col, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.task import Item
from app.api.v1.schemas.task import ItemCreate, ItemUpdate


class TaskRepository:
    """Repository for Task/Item model operations."""

    @staticmethod
    async def create(
        *, session: AsyncSession, item_in: ItemCreate, owner_id: uuid.UUID
    ) -> Item:
        """Create a new item."""
        db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item

    @staticmethod
    async def update(
        *, session: AsyncSession, db_item: Item, item_in: ItemUpdate
    ) -> Item:
        """Update an existing item."""
        item_data = item_in.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(item_data)
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item

    @staticmethod
    async def get_by_id(*, session: AsyncSession, item_id: uuid.UUID) -> Item | None:
        """Get an item by ID."""
        return await session.get(Item, item_id)

    @staticmethod
    async def get_all(
        *, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> tuple[list[Item], int]:
        """Get all items with pagination."""
        count = (await session.exec(select(func.count()).select_from(Item))).one()
        items = (
            await session.exec(
                select(Item)
                .order_by(col(Item.created_at).desc())
                .offset(skip)
                .limit(limit)
            )
        ).all()
        return items, count

    @staticmethod
    async def get_by_owner(
        *,
        session: AsyncSession,
        owner_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Item], int]:
        """Get all items for a specific owner."""
        count = (
            await session.exec(
                select(func.count()).select_from(Item).where(Item.owner_id == owner_id)
            )
        ).one()
        items = (
            await session.exec(
                select(Item)
                .where(Item.owner_id == owner_id)
                .order_by(col(Item.created_at).desc())
                .offset(skip)
                .limit(limit)
            )
        ).all()
        return items, count

    @staticmethod
    async def delete(*, session: AsyncSession, db_item: Item) -> None:
        """Delete an item."""
        await session.delete(db_item)
        await session.commit()
