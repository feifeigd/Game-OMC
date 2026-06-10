<template>
  <div class="fa-full-height">
    <FaSearchBarWithAudit
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="businessSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearch"
      @reset="onResetSearch"
    />

    <ElCard class="fa-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
      <FaTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <FaTableHeaderLeft
            :remove-ids="selectedIds"
            :perm-create="['module_omc:machine:create']"
            :perm-import="['module_omc:machine:import']"
            :perm-export="['module_omc:machine:export']"
            :perm-delete="['module_omc:machine:delete']"
            :perm-patch="['module_omc:machine:patch']"
            :delete-loading="batchDeleting"
            @add="openEditDialog('add')"
            @import="openImportModal"
            @export="openExportModal"
            @delete="handleBatchDelete"
            @more="runBatchStatus"
          />
        </template>
      </FaTableHeader>

      <FaTable
        ref="faTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="pagination"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <FaDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="920px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="4" border>
            <ElDescriptionsItem label="主键ID" :span="2">
              {{ detailFormData.id }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="UUID全局唯一标识" :span="2">
              {{ detailFormData.uuid }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="名称" :span="2">
              {{ detailFormData.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="状态" :span="2">
              <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
                {{ detailFormData.status === "0" ? "启用" : "停用" }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="备注/描述" :span="2">
              {{ detailFormData.description }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建时间" :span="2">
              {{ detailFormData.created_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新时间" :span="2">
              {{ detailFormData.updated_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建人" :span="2">
              {{ detailFormData.created_by?.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新人" :span="2">
              {{ detailFormData.updated_by?.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="是否已删除(0:未删除 1:已删除)" :span="2">
              {{ detailFormData.is_deleted }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="删除时间" :span="2">
              {{ detailFormData.deleted_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="删除人ID" :span="2">
              {{ detailFormData.deleted_id }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="内网ip" :span="2">
              {{ detailFormData.private_ip }}
            </ElDescriptionsItem>
          </ElDescriptions>
        </ElScrollbar>
      </template>
      <template v-else>
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ElForm
            ref="dataFormRef"
            :model="formData"
            :rules="rules"
            label-suffix=":"
            label-width="auto"
            label-position="right"
            inline
          >
            <ElFormItem label="名称" prop="name" :required="false">
              <ElInput v-model="formData.name" placeholder="请输入名称" />
            </ElFormItem>
            <ElFormItem label="状态" prop="status" :required="true">
              <ElRadioGroup v-model="formData.status">
                <ElRadio value="0">启用</ElRadio>
                <ElRadio value="1">停用</ElRadio>
              </ElRadioGroup>
            </ElFormItem>
            <ElFormItem label="描述" prop="description">
              <ElInput
                v-model="formData.description"
                :rows="4"
                :maxlength="100"
                show-word-limit
                type="textarea"
                placeholder="请输入描述"
              />
            </ElFormItem>
            <ElFormItem label="是否已删除(0:未删除 1:已删除)" prop="is_deleted" :required="true">
              <ElInputNumber
                v-model="formData.is_deleted"
                placeholder="请输入是否已删除(0:未删除 1:已删除)"
              />
            </ElFormItem>
            <ElFormItem label="删除时间" prop="deleted_time" :required="false">
              <ElDatePicker v-model="formData.deleted_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="请选择删除时间" style="width: 100%" />
            </ElFormItem>
            <ElFormItem label="删除人ID" prop="deleted_id" :required="false">
              <ElInputNumber
                v-model="formData.deleted_id"
                placeholder="请输入删除人ID"
              />
            </ElFormItem>
            <ElFormItem label="内网ip" prop="private_ip" :required="true">
              <ElInput v-model="formData.private_ip" placeholder="请输入内网ip" />
            </ElFormItem>
          </ElForm>
        </ElScrollbar>
      </template>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </FaDialog>

    <FaImportDialog
      v-model="importModalVisible"
      :content-config="importContentConfig"
      default-template-file-name="machine_import_template.xlsx"
      @upload="handleCrudImportUpload"
    />

    <FaExportDialog
      v-model="exportModalVisible"
      :content-config="exportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { h, computed, ref, reactive, onMounted } from "vue";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";
import { useTable } from "@/hooks/core/useTable";
import FaTableHeaderLeft from "@/components/tables/fa-table-header-left/index.vue";
import FaImportDialog from "@/components/modal/fa-import-dialog/index.vue";
import FaExportDialog from "@/components/modal/fa-export-dialog/index.vue";
import type { IContentConfig, IObject } from "@/components/modal/types";
import FaSearchBarWithAudit from "@/components/forms/fa-search-bar/FaSearchBarWithAudit.vue";
import type { AuditSearchFormParams } from "@/components/forms/fa-search-bar/auditSearchFormItems";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import type { ColumnOption } from "@/types/component";
import OmcMachineAPI, {
  type OmcMachineForm,
  type OmcMachinePageQuery,
  type OmcMachineTable,
} from "@/api/module_omc/machine";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";

defineOptions({
  name: "OmcMachine",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type OmcMachineSearchFormParams = {
  name?: string;
  status?: string;
  is_deleted?: string;
  deleted_time?: string;
  deleted_id?: string;
  private_ip?: string;
} & AuditSearchFormParams;

function normalizeOmcMachineQuery(params: Record<string, unknown>): OmcMachinePageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as OmcMachinePageQuery;
}

const searchForm = ref<OmcMachineSearchFormParams>({
  name: undefined,
  status: undefined,
  is_deleted: undefined,
  deleted_time: undefined,
  deleted_id: undefined,
  private_ip: undefined,
  created_id: undefined,
  updated_id: undefined,
  created_time: [],
  updated_time: [],
});

/** 搜索区域默认展开展示 */
const showSearchBar = ref(true);

const searchBarRef = ref<InstanceType<typeof FaSearchBarWithAudit> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

/** 业务搜索项（审计四字段由 FaSearchBarWithAudit 自动追加） */
const businessSearchItems = computed(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    placeholder: "请输入名称",
    clearable: true,
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      options: statusOptions.value,
      clearable: true,
    },
    span: 6,
  },
  {
    label: "是否已删除(0:未删除 1:已删除)",
    key: "is_deleted",
    type: "input",
    placeholder: "请输入是否已删除(0:未删除 1:已删除)",
    clearable: true,
    span: 6,
  },
  {
    label: "删除时间",
    key: "deleted_time",
    type: "date-picker",
    props: {
      type: "date",
      valueFormat: "YYYY-MM-DD",
      clearable: true,
      placeholder: "请选择删除时间",
    },
    span: 6,
  },
  {
    label: "删除人ID",
    key: "deleted_id",
    type: "input",
    placeholder: "请输入删除人ID",
    clearable: true,
    span: 6,
  },
  {
    label: "内网ip",
    key: "private_ip",
    type: "input",
    placeholder: "请输入内网ip",
    clearable: true,
    span: 6,
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<OmcMachineTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: OmcMachineTable[]) {
  selectedRows.value = rows;
}

const PK = "id" as const;

const {
  columns,
  columnChecks,
  data,
  loading,
  pagination,
  searchParams,
  getData,
  replaceSearchParams,
  resetSearchParams,
  handleSizeChange,
  handleCurrentChange,
  refreshData,
  refreshCreate,
  refreshUpdate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: OmcMachineAPI.getOmcMachineList,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<OmcMachineTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { prop: "name", label: "名称", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: OmcMachineTable) => {
          const ok = row.status === "0";
          const cfg = ok
            ? { type: "success" as const, text: "启用" }
            : { type: "info" as const, text: "停用" };
          return h(ElTag, { type: cfg.type }, () => cfg.text);
        },
      },
      { prop: "description", label: "备注/描述", minWidth: 120, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "created_by",
        label: "创建人ID",
        minWidth: 100,
        formatter: (row: OmcMachineTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_by",
        label: "更新人ID",
        minWidth: 100,
        formatter: (row: OmcMachineTable) => row.updated_by?.name ?? "—",
      },
      { prop: "is_deleted", label: "是否已删除(0:未删除 1:已删除)", minWidth: 120, showOverflowTooltip: true },
      { prop: "deleted_time", label: "删除时间", minWidth: 120, showOverflowTooltip: true },
      { prop: "deleted_id", label: "删除人ID", minWidth: 120, showOverflowTooltip: true },
      { prop: "private_ip", label: "内网ip", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: OmcMachineTable) => formatOperationCell(row),
      },
    ],
  },
});

/** 供 FaImportDialog / FaExportDialog 的列配置 */
const crudCols = computed(() =>
  columns.value.map((c: ColumnOption<OmcMachineTable>) => {
    const t = (c as { type?: string }).type;
    return {
      prop: c.prop,
      label: c.label,
      type: t === "selection" ? ("selection" as const) : ("default" as const),
      show: true,
    };
  })
);

const exportQueryParams = computed(() => {
  const sp = { ...(searchParams as object) } as Record<string, unknown>;
  delete sp.current;
  delete sp.size;
  delete sp.page_no;
  delete sp.page_size;
  return normalizeOmcMachineQuery(sp);
});

const importContentConfig = computed<IContentConfig>(() => ({
  permPrefix: "module_omc:machine",
  cols: crudCols.value,
  indexAction: async () => ({}),
  importTemplate: () => OmcMachineAPI.downloadTemplateOmcMachine(),
}));

const exportContentConfig = computed(() => ({
  permPrefix: "module_omc:machine",
  cols: crudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeOmcMachineQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await OmcMachineAPI.exportOmcMachine(merged as OmcMachinePageQuery);
    return res.data as Blob;
  },
}));

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const detailFormData = ref<OmcMachineTable>({});

const formData = ref<OmcMachineForm>({
  name: undefined,
  status: "0",
  description: undefined,
  is_deleted: undefined,
  deleted_time: undefined,
  deleted_id: undefined,
  private_ip: undefined,
});

const rules = reactive({
  name: [{ required: false, message: "请填写名称", trigger: "blur" }],
  status: [{ required: true, message: "请填写状态(0:正常 1:禁用)", trigger: "blur" }],
  description: [{ required: false, message: "请填写备注/描述", trigger: "blur" }],
  is_deleted: [{ required: true, message: "请填写是否已删除(0:未删除 1:已删除)", trigger: "blur" }],
  deleted_time: [{ required: false, message: "请填写删除时间", trigger: "blur" }],
  deleted_id: [{ required: false, message: "请填写删除人ID", trigger: "blur" }],
  private_ip: [{ required: true, message: "请填写内网ip", trigger: "blur" }],
});

const dataFormRef = ref();
const importModalVisible = ref(false);
const exportModalVisible = ref(false);

const initialFormData: OmcMachineForm = {
  name: undefined,
  status: "0",
  description: undefined,
  is_deleted: undefined,
  deleted_time: undefined,
  deleted_id: undefined,
  private_ip: undefined,
};

const handleSearch = async (params: OmcMachineSearchFormParams) => {
  await searchBarRef.value?.validate();
  replaceSearchParams({
    name: params.name,
    status: params.status,
    is_deleted: params.is_deleted,
    deleted_time: params.deleted_time,
    deleted_id: params.deleted_id,
    private_ip: params.private_ip,
    created_id: params.created_id ?? undefined,
    updated_id: params.updated_id ?? undefined,
    created_time:
      Array.isArray(params.created_time) && params.created_time.length === 2
        ? params.created_time
        : undefined,
    updated_time:
      Array.isArray(params.updated_time) && params.updated_time.length === 2
        ? params.updated_time
        : undefined,
  } as Record<string, unknown>);
  getData();
};

const onResetSearch = async () => {
  searchForm.value = {
    name: undefined,
    status: undefined,
    is_deleted: undefined,
    deleted_time: undefined,
    deleted_id: undefined,
    private_ip: undefined,
    created_id: undefined,
    updated_id: undefined,
    created_time: [],
    updated_time: [],
  };
  await resetSearchParams();
};

function buildRowActions(row: OmcMachineTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      icon: "ri:file-list-3-line",
      perm: "module_omc:machine:detail",
      run: () => void openDetailDialog(row),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_omc:machine:update",
      run: () => void openEditDialog("edit", row),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_omc:machine:delete",
      run: () => deleteRow(row),
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatOperationCell(row: OmcMachineTable) {
  return renderTableOperationCell(buildRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1",
  });
}

async function openDetailDialog(row: OmcMachineTable) {
  if (!row[PK]) return;
  const response = await OmcMachineAPI.getOmcMachineDetail(row[PK] as number);
  dialogVisible.type = "detail";
  dialogVisible.title = "详情";
  detailFormData.value = response.data.data ?? { ...row };
  dialogVisible.visible = true;
}

async function openEditDialog(type: "add" | "edit", row?: OmcMachineTable) {
  dialogVisible.type = type === "add" ? "create" : "update";
  if (type === "add") {
    dialogVisible.title = "新增omc-机器列表";
    Object.assign(formData.value, initialFormData);
    formData.value[PK] = undefined;
  } else if (row?.[PK]) {
    dialogVisible.title = "修改";
    const response = await OmcMachineAPI.getOmcMachineDetail(row[PK] as number);
    Object.assign(formData.value, response.data.data);
  }
  dialogVisible.visible = true;
}

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData.value, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return;
    const submitData = { ...formData.value };
    const id = formData.value[PK] as number | undefined;
    try {
      if (id) {
        await OmcMachineAPI.updateOmcMachine(id, { [PK]: id, ...submitData });
        await refreshUpdate();
      } else {
        await OmcMachineAPI.createOmcMachine(submitData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
    } catch (error: unknown) {
      console.error(error);
    }
  });
}

const deleteRow = async (row: OmcMachineTable) => {
  if (!row[PK]) return;
  try {
    await ElMessageBox.confirm(
      `确定删除该omc-机器列表吗？此操作不可恢复！`,
      "删除确认",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    await OmcMachineAPI.deleteOmcMachine([row[PK] as number]);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    ElMessage.info("已取消删除");
  }
};

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await ElMessageBox.confirm(
      `确定删除选中的 ${ids.length} 条数据吗？此操作不可恢复！`,
      "批量删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    batchDeleting.value = true;
    await OmcMachineAPI.deleteOmcMachine(ids);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    ElMessage.info("已取消删除");
  } finally {
    batchDeleting.value = false;
  }
}

async function runBatchStatus(status: string) {
  const ids = selectedIds.value;
  if (ids.length === 0) {
    ElMessage.warning("请先在列表中勾选数据");
    return;
  }
  try {
    await ElMessageBox.confirm(
      `确认对选中的 ${ids.length} 条数据${status === "0" ? "启用" : "停用"}？`,
      "批量设置",
      { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" }
    );
    await OmcMachineAPI.batchOmcMachine({ ids, status });
    ElMessage.success("操作成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshData();
  } catch {
    // 用户取消
  }
}

function openImportModal() {
  importModalVisible.value = true;
}

async function handleCrudImportUpload(uploadFormData: FormData) {
  try {
    const res = await OmcMachineAPI.importOmcMachine(uploadFormData);
    if (res.data.code !== ResultEnum.SUCCESS) {
      ElMessage.error(res.data.msg || "导入失败");
      return;
    }
    ElMessage.success(res.data.msg || "导入成功");
    importModalVisible.value = false;
    await refreshData();
  } catch (error) {
    console.error("[Import]", error);
    ElMessage.error("导入失败");
  }
}

function openExportModal() {
  exportModalVisible.value = true;
}

onMounted(async () => {
  getData();
});
</script>

<style lang="scss" scoped></style>
