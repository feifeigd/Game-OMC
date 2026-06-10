# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import SmallInteger, String, Integer, DateTime, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class OmcMachineModel(ModelMixin, UserMixin):
    """
    omc-机器列表表
    """
    __tablename__: str = 'omc_machine'
    __table_args__: dict[str, str] = {'comment': 'omc-机器列表'}
    __loader_options__: list[str] = ["created_by", "updated_by", "deleted_by"]

    name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='名称')

