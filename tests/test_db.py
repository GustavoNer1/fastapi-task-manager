from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.models.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):

    with mock_db_time(model=User) as (time, updated_time):
        new_user = User(
            username='testexin',
            email='testexin@test.com',
            password='secret',
            phone='11970299255',
        )
        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'testexin')
        )

    assert asdict(user) == {
        'id': 1,
        'username': 'testexin',
        'email': 'testexin@test.com',
        'password': 'secret',
        'phone': '11970299255',
        'created_at': time,
        'updated_at': updated_time,
    }
