"""
Endpoints to query different types of logs
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Query, HTTPException, status

from api.schemas.agentlog_schemas import AgentLogSchema
from api.schemas.commandlog_schemas import CommandLogSchema
from api.schemas.soaplog_schemas import SoapLogSchema
from db_query_functions import query_agentlogs, query_commandlogs, query_soaplogs
from log_setups import commandlog_nodes

router = APIRouter()


def check_agentlog_input(
    msisdn: Optional[str],
    imsi: Optional[str],
) -> None:
    """Checks that input is valid, and raises HTTP exception if not"""
    if not (msisdn or imsi):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of msisdn or imsi must be provided",
        )

def check_date_input(start_date: date,end_date: date) -> None:
    """Checks that dates are correct"""
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be earlier than start date",
        )



@router.get("/get_agentlogs", response_model=list[AgentLogSchema])
async def get_logs(
    start_date: date = Query(description="Start date to filter logs"),
    end_date: date = Query(description="End date to filter logs"),
    msisdn: Optional[int] = Query(None, description="MSISDN to filter logs"),
    imsi: Optional[int] = Query(None, description="IMSI to filter logs"),
) -> list[AgentLogSchema]:
    """Returns logs info according to a query"""
    check_agentlog_input(msisdn, imsi)
    check_date_input(start_date, end_date)
    logs = await query_agentlogs(msisdn, imsi, start_date, end_date + timedelta(days=1))
    logs_dto = [AgentLogSchema.model_validate(row, from_attributes=True) for row in logs]

    return logs_dto


@router.get("/get_commandlogs", response_model=list[CommandLogSchema])
async def get_commandlogs(
    start_date: date = Query(description="Start date to filter logs"),
    end_date: date = Query(description="End date to filter logs"),
    username: Optional[str] = Query(None, description="Username of a person executing commands"),
    node_name: str = Query(None, description="Node name to filter logs", enum=commandlog_nodes),
) -> list[CommandLogSchema]:
    """Commandlogs by user and network element"""
    check_date_input(start_date, end_date)
    logs = await query_commandlogs(start_date, end_date + timedelta(days=1), username, node_name)
    logs_dto = [CommandLogSchema.model_validate(row, from_attributes=True) for row in logs]

    return logs_dto


@router.get("/get_soaplogs", response_model=list[SoapLogSchema])
async def get_soaplogs(
    msisdn: int,
    start_date: date = Query(description="Start date to filter logs"),
    end_date: date = Query(description="End date to filter logs"),
    node_type: str = Query(..., description="AGCF or SSS node type", enum=["AGCF", "SSS"]),
) -> list[SoapLogSchema]:
    """Soaplogs by msisdn and network element type"""
    check_date_input(start_date, end_date)

    logs = await query_soaplogs(start_date, end_date + timedelta(days=1), msisdn, node_type)
    logs_dto = [SoapLogSchema.model_validate(row, from_attributes=True) for row in logs]

    return logs_dto
