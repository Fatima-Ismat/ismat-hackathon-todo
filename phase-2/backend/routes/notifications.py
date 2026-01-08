"""
Notification routes
Get and manage user notifications
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from datetime import datetime

from database import get_db
from models import Notification, NotificationResponse
from config import settings
from routes.tasks import get_current_user_id


router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("", response_model=List[NotificationResponse])
async def list_notifications(
    unread_only: bool = False,
    limit: int = 50,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    List notifications for current user

    - **unread_only**: Only return unread notifications
    - **limit**: Max results (default: 50)
    - **offset**: Pagination offset (default: 0)
    """
    statement = select(Notification).where(Notification.user_id == int(user_id))

    if unread_only:
        statement = statement.where(Notification.read == False)

    statement = statement.offset(offset).limit(limit).order_by(Notification.created_at.desc())

    result = await db.execute(statement)
    notifications = result.scalars().all()

    return [
        NotificationResponse(
            id=notif.id,
            user_id=notif.user_id,
            message=notif.message,
            notification_type=notif.notification_type,
            read=notif.read,
            created_at=notif.created_at,
            read_at=notif.read_at
        )
        for notif in notifications
    ]


@router.get("/unread-count")
async def get_unread_count(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get count of unread notifications

    Returns: {"unread_count": number}
    """
    from sqlmodel import func

    statement = select(func.count()).select_from(Notification).where(
        Notification.user_id == int(user_id),
        Notification.read == False
    )

    result = await db.execute(statement)
    count = result.scalar_one()

    return {"unread_count": count}


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a notification as read

    - **notification_id**: Notification ID
    """
    # Get notification
    statement = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == int(user_id)
    )
    result = await db.execute(statement)
    notification = result.scalar_one_or_none()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    # Mark as read
    notification.read = True
    notification.read_at = datetime.utcnow()

    await db.commit()
    await db.refresh(notification)

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        message=notification.message,
        notification_type=notification.notification_type,
        read=notification.read,
        created_at=notification.created_at,
        read_at=notification.read_at
    )


@router.put("/mark-all-read")
async def mark_all_read(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark all notifications as read

    Returns: {"marked_count": number}
    """
    # Get all unread notifications
    statement = select(Notification).where(
        Notification.user_id == int(user_id),
        Notification.read == False
    )
    result = await db.execute(statement)
    notifications = result.scalars().all()

    # Mark all as read
    count = 0
    for notification in notifications:
        notification.read = True
        notification.read_at = datetime.utcnow()
        count += 1

    await db.commit()

    return {"marked_count": count}


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a notification

    - **notification_id**: Notification ID
    """
    # Get notification
    statement = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == int(user_id)
    )
    result = await db.execute(statement)
    notification = result.scalar_one_or_none()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    # Delete
    await db.delete(notification)
    await db.commit()
