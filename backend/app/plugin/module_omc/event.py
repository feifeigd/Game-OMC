# -*- coding: utf-8 -*-

from sqlalchemy import func, select
from fastapi import FastAPI

from app.core.database import async_db_session
from app.core.logger import log
from app.plugin.module_omc.machine.model import OmcMachineModel

"""
app/plugin/module_XX/event.py 中的顶级异步函数，自动注册为开关机回调函数
其中 status=true表示开机事件，status=false表示关机事件
模块启动时会自动调用 seed_omc_machine(app, True)，模块关闭时会自动调用 seed_omc_machine(app, False)，因此无需手动调用
"""
async def seed_omc_machine(app: FastAPI, status: bool) -> None:
    """模块启动事件：仅在启动阶段且表为空时写入默认数据。"""
    if not status:
        return

    async with async_db_session() as session:
        async with session.begin():
            count_result = await session.execute(select(func.count()).select_from(OmcMachineModel))
            existing_count = count_result.scalar() or 0
            if existing_count > 0:
                return

            session.add_all(
                [
                    OmcMachineModel(name="默认机器-001", description="模块初始化数据"),
                    OmcMachineModel(name="默认机器-002", description="模块初始化数据"),
                ]
            )
            log.info("✅ module_omc 初始化: 已写入 omc_machine 默认数据")
