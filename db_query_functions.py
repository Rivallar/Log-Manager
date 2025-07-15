"""
Tools to query a data from a database
"""
from datetime import date
from typing import Optional

from sqlalchemy import select, or_, and_

from database import async_session_factory
from models.agentlog_model import AgentLogModel


async def query_agentlogs(
    msisdn: Optional[int],
    imsi: Optional[int],
    start_date: date,
    end_date: date
) -> list[AgentLogModel]:
    """Request to db to get agentlogs according to query conditions"""
    async with async_session_factory() as session:
        filters = []
        if imsi is not None:
            filters.append(AgentLogModel.true_imsi == imsi)
        if msisdn is not None:
            filters.append(AgentLogModel.true_msisdn == msisdn)
        query = select(AgentLogModel).filter(or_(*filters)).filter(
            and_(
                AgentLogModel.log_time >= start_date,
                AgentLogModel.log_time <= end_date,
            )
        ).order_by(AgentLogModel.log_time)
        result = await session.execute(query)
        logs = result.scalars().all()
    return logs
