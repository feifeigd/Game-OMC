# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_params import PaginationQueryParam
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.core.base_schema import BatchSetAvailable

from .service import OmcMachineService
from .schema import OmcMachineCreateSchema, OmcMachineUpdateSchema, OmcMachineQueryParam

# 动态路由容器前缀由 module_xxx 决定（discover: module_xxx -> /xxx）
# 对齐 module_example/demo：业务路由前缀固定为 /{module_name}
OmcMachineRouter = APIRouter(prefix='/machine', tags=["omc-机器列表模块"])

@OmcMachineRouter.get(
    "/detail/{id}",
    summary="获取omc-机器列表详情",
    description="获取omc-机器列表详情"
)
async def get_omc_machine_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:query"]))
) -> JSONResponse:
    """
    获取omc-机器列表详情接口
    
    参数:
    - id: int - 数据ID
    - auth: AuthSchema - 认证信息
    
    返回:
    - JSONResponse - 包含omc-机器列表详情的JSON响应
    """
    result_dict = await OmcMachineService.detail_omc_machine_service(auth=auth, id=id)
    log.info(f"获取omc-机器列表详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取omc-机器列表详情成功")

@OmcMachineRouter.get(
    "/list",
    summary="查询omc-机器列表列表",
    description="查询omc-机器列表列表"
)
async def get_omc_machine_list_controller(
    page: PaginationQueryParam = Depends(),
    search: OmcMachineQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:query"]))
) -> JSONResponse:
    """
    查询omc-机器列表列表接口（数据库分页）
    
    参数:
    - page: PaginationQueryParam - 分页参数
    - search: OmcMachineQueryParam - 查询参数
    - auth: AuthSchema - 认证信息
    
    返回:
    - JSONResponse - 包含omc-机器列表列表的JSON响应
    """
    result_dict = await OmcMachineService.page_omc_machine_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询omc-机器列表列表成功")
    return SuccessResponse(data=result_dict, msg="查询omc-机器列表列表成功")

@OmcMachineRouter.post(
    "/create",
    summary="创建omc-机器列表",
    description="创建omc-机器列表"
)
async def create_omc_machine_controller(
    data: OmcMachineCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:create"]))
) -> JSONResponse:
    """
    创建omc-机器列表接口
    
    参数:
    - data: OmcMachineCreateSchema - 创建数据
    - auth: AuthSchema - 认证信息
    
    返回:
    - JSONResponse - 包含创建omc-机器列表结果的JSON响应
    """
    result_dict = await OmcMachineService.create_omc_machine_service(auth=auth, data=data)
    log.info("创建omc-机器列表成功")
    return SuccessResponse(data=result_dict, msg="创建omc-机器列表成功")

@OmcMachineRouter.put(
    "/update/{id}",
    summary="修改omc-机器列表",
    description="修改omc-机器列表"
)
async def update_omc_machine_controller(
    data: OmcMachineUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:update"]))
) -> JSONResponse:
    """
    修改omc-机器列表接口
    
    参数:
    - id: int - 数据ID
    - data: OmcMachineUpdateSchema - 更新数据
    - auth: AuthSchema - 认证信息
    
    返回:
    - JSONResponse - 包含修改omc-机器列表结果的JSON响应
    """
    result_dict = await OmcMachineService.update_omc_machine_service(auth=auth, id=id, data=data)
    log.info("修改omc-机器列表成功")
    return SuccessResponse(data=result_dict, msg="修改omc-机器列表成功")

@OmcMachineRouter.delete(
    "/delete",
    summary="删除omc-机器列表",
    description="删除omc-机器列表"
)
async def delete_omc_machine_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:delete"]))
) -> JSONResponse:
    """
    删除omc-机器列表接口
    
    参数:
    - ids: list[int] - 数据ID列表
    - auth: AuthSchema - 认证信息
    
    返回:
    - JSONResponse - 包含删除omc-机器列表结果的JSON响应
    """
    await OmcMachineService.delete_omc_machine_service(auth=auth, ids=ids)
    log.info(f"删除omc-机器列表成功: {ids}")
    return SuccessResponse(msg="删除omc-机器列表成功")

@OmcMachineRouter.patch(
    "/available/setting",
    summary="批量修改omc-机器列表状态",
    description="批量修改omc-机器列表状态"
)
async def batch_set_available_omc_machine_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:patch"]))
) -> JSONResponse:
    """
    批量修改omc-机器列表状态接口
    
    参数:
    - data: BatchSetAvailable - 批量修改状态数据
    - auth: AuthSchema - 认证信息
    
    返回:
    - JSONResponse - 包含批量修改omc-机器列表状态结果的JSON响应
    """
    await OmcMachineService.set_available_omc_machine_service(auth=auth, data=data)
    log.info(f"批量修改omc-机器列表状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改omc-机器列表状态成功")

@OmcMachineRouter.post(
    '/export',
    summary="导出omc-机器列表",
    description="导出omc-机器列表"
)
async def export_omc_machine_list_controller(
    search: OmcMachineQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:export"]))
) -> StreamingResponse:
    """
    导出omc-机器列表接口
    
    参数:
    - search: OmcMachineQueryParam - 查询参数
    - auth: AuthSchema - 认证信息
    
    返回:
    - StreamingResponse - 包含导出omc-机器列表数据的流式响应
    """
    result_dict_list = await OmcMachineService.list_omc_machine_service(search=search, auth=auth)
    export_result = await OmcMachineService.batch_export_omc_machine_service(obj_list=result_dict_list)
    log.info('导出omc-机器列表成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=omc_machine.xlsx'}
    )

@OmcMachineRouter.post(
    '/import',
    summary="导入omc-机器列表",
    description="导入omc-机器列表"
)
async def import_omc_machine_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_omc:machine:import"]))
) -> JSONResponse:
    """
    导入omc-机器列表接口
    
    参数:
    - file: UploadFile - 上传的Excel文件
    - auth: AuthSchema - 认证信息
    
    返回:
    - JSONResponse - 包含导入omc-机器列表结果的JSON响应
    """
    batch_import_result = await OmcMachineService.batch_import_omc_machine_service(file=file, auth=auth, update_support=True)
    log.info("导入omc-机器列表成功")
    return SuccessResponse(data=batch_import_result, msg="导入omc-机器列表成功")

@OmcMachineRouter.post(
    '/download/template',
    summary="获取omc-机器列表导入模板",
    description="获取omc-机器列表导入模板",
    dependencies=[Depends(AuthPermission(["module_omc:machine:download"]))]
)
async def export_omc_machine_template_controller() -> StreamingResponse:
    """
    获取omc-机器列表导入模板接口
    
    返回:
    - StreamingResponse - 包含omc-机器列表导入模板的流式响应
    """
    import_template_result = await OmcMachineService.import_template_download_omc_machine_service()
    log.info('获取omc-机器列表导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=omc_machine_template.xlsx'}
    )