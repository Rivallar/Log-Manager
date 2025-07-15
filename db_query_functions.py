"""
Tools to query a data from a database
"""
from datetime import date
from typing import Optional

from sqlalchemy import select, or_

from database import async_session_factory
from models.agentlog_model import AgentLogModel


async def query_agentlogs(
    msisdn: Optional[str],
    imsi: Optional[str],
    start_date: date,
    end_date: date
) -> list[AgentLogModel]:
    """Request to db to get agentlogs according to query conditions"""
    async with async_session_factory() as session:
        filters = []
        if imsi is not None:
            filters.append(AgentLogModel.imsi.ilike(imsi))
        if msisdn is not None:
            filters.append(AgentLogModel.msisdn.ilike(msisdn))
            filters.append(AgentLogModel.imsi.ilike(msisdn))
        query = select(AgentLogModel).filter(or_(*filters))


        result = await session.execute(query)
        logs = result.scalars().all()
    return logs