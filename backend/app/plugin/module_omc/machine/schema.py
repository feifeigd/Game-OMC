# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
from app.core.validator import DateTimeStr
from datetime import datetime
from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, UserBySchema

class OmcMachineCreateSchema(BaseModel):
    """
    omc-机器列表新增模型
    """
    name: str = Field(default=..., description='名称')
    status: str = Field(default="0", description='状态(0:正常 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')
    private_ip: str = Field(default=..., description='内网ip')


class OmcMachineUpdateSchema(OmcMachineCreateSchema):
    """
    omc-机器列表更新模型
    """
    ...


class OmcMachineOutSchema(OmcMachineCreateSchema, BaseSchema, UserBySchema):
    """
    omc-机器列表响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class OmcMachineQueryParam:
    """omc-机器列表查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="名称"),
        status: str | None = Query(None, description="状态(0:正常 1:禁用)"),
        private_ip: str | None = Query(None, description="内网ip"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        is_deleted: int | None = Query(None, description="是否已删除(0:未删除 1:已删除)"),
        deleted_time: datetime | None = Query(None, description="删除时间"),
        deleted_id: int | None = Query(None, description="删除人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.name = (QueueEnum.like.value, name)
        # 模糊查询字段
        self.status = (QueueEnum.like.value, status)
        # 精确查询字段
        if created_id is not None:
            self.created_id = (QueueEnum.eq.value, created_id)
        # 精确查询字段
        if updated_id is not None:
            self.updated_id = (QueueEnum.eq.value, updated_id)
        # 精确查询字段
        if is_deleted is not None:
            self.is_deleted = (QueueEnum.eq.value, is_deleted)
        # 精确查询字段
        if deleted_time is not None:
            self.deleted_time = (QueueEnum.eq.value, deleted_time)
        # 精确查询字段
        if deleted_id is not None:
            self.deleted_id = (QueueEnum.eq.value, deleted_id)
        # 模糊查询字段
        self.private_ip = (QueueEnum.like.value, private_ip)
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))
