import { request } from "@utils/http";

// API 前缀来自分系统包 module_xxx → /xxx
// 对齐 module_example/demo：业务接口固定为 /{prefix}/{module_name}
const API_PATH = "/omc/machine";

const OmcMachineAPI = {
  /** 获取列表 */
  getOmcMachineList(query: OmcMachinePageQuery) {
    return request<ApiResponse<PageResult<OmcMachineTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  /** 获取详情 */
  getOmcMachineDetail(id: number) {
    return request<ApiResponse<OmcMachineTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  /** 新增 */
  createOmcMachine(body: OmcMachineForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  /** 修改 */
  updateOmcMachine(id: number, body: OmcMachineForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  /** 删除（支持批量） */
  deleteOmcMachine(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  /** 批量启用/停用 */
  batchOmcMachine(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  /** 导出 Excel */
  exportOmcMachine(query: OmcMachinePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  /** 下载导入模板 */
  downloadTemplateOmcMachine() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  /** 导入 Excel */
  importOmcMachine(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export default OmcMachineAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

/** 列表查询参数 */
export interface OmcMachinePageQuery extends PageQuery {
  name?: string;
  status?: string;
  is_deleted?: number;
  deleted_time?: string;
  deleted_id?: number;
  private_ip?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

/** 列表展示项 */
export interface OmcMachineTable extends BaseType {
  name?: string;
  created_id?: number;
  updated_id?: number;
  is_deleted?: number;
  deleted_time?: string;
  deleted_id?: number;
  private_ip?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}

/** 新增/修改表单参数 */
export interface OmcMachineForm extends BaseFormType {
  name?: string;
  is_deleted?: number;
  deleted_time?: string;
  deleted_id?: number;
  private_ip?: string;
}
