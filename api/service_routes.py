"""
Service endpoints to control app data
"""
from fastapi import APIRouter, Query

from api.schemas.agentlog_schemas import AgentLogSchema
from api.schemas.commandlog_schemas import CommandLogSchema
from api.schemas.soaplog_schemas import SoapLogSchema
from db_query_functions import query_last_logs
from log_setups import log_setups
from models.agentlog_model import AgentLogModel
from models.commandlog_model import CommandLogModel
from models.soaplog_model import SoapLogModel

router = APIRouter()


log_dict = {
    "agentlog": (AgentLogModel, AgentLogSchema),
    "commandlog": (CommandLogModel, CommandLogSchema),
    "soaplog": (SoapLogModel, SoapLogSchema),
}
node_names = [ne.node_name for ne in log_setups]


@router.get("/get_last_logs",
            response_model=list[AgentLogSchema | CommandLogSchema | SoapLogSchema])
async def get_last_logs(log_type: str = Query(..., description="log type", enum=["agentlog", "commandlog", "soaplog"]),
                        n_logs: int = 5,
                        node_name: str = Query(None, description="node names", enum=node_names)) -> list[AgentLogSchema | CommandLogSchema | SoapLogSchema]:
    """Returns N last records of a requested log type.
    Just to check that logs a being updatetd normally."""
    log_model, log_schema = log_dict[log_type]
    logs = await query_last_logs(log_model, n_logs, node_name)
    logs_dto = [log_schema.model_validate(row, from_attributes=True) for row in logs]
    return logs_dto
