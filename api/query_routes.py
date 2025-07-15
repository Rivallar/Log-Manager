"""
Endpoints to query different types of logs
"""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Query, HTTPException, status

from api.schemas.agentlog_schemas import AgentLogSchema
from db_query_functions import query_agentlogs

router = APIRouter()


def check_input(
    start_date: date,
    end_date: date,
    msisdn: Optional[str],
    imsi: Optional[str],
) -> None:
    """Checks that input is valid, and raises HTTP exception if not"""
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be earlier than start date",
        )

    if not (msisdn or imsi):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of msisdn or imsi must be provided",
        )


@router.get("/get_agentlogs", response_model=list[AgentLogSchema])
async def get_logs(
    start_date: date = Query(description="Start date to filter logs"),
    end_date: date = Query(description="End date to filter logs"),
    msisdn: Optional[int] = Query(None, description="MSISDN to filter logs"),
    imsi: Optional[int] = Query(None, description="IMSI to filter logs"),
) -> list[AgentLogSchema]:
    """Returns logs info according to a query"""
    check_input(start_date, end_date, msisdn, imsi)
    logs = await query_agentlogs(msisdn, imsi, start_date, end_date)
    logs_dto = [AgentLogSchema.model_validate(row, from_attributes=True) for row in logs]

    return logs_dto
