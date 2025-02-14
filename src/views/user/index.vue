<template>
  <div class="user-container">
    <div class="filter-container">
      <el-button type="primary" @click="handleCreate">
        添加用户
      </el-button>
    </div>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading..."
      border
      fit
      highlight-current-row
    >
      <el-table-column label="用户ID" align="center" width="220">
        <template #default="{ row }">
          <span>{{ row.user_id }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="用户名" align="center" width="150">
        <template #default="{ row }">
          <span>{{ row.username }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="邮箱" align="center" width="200">
        <template #default="{ row }">
          <span>{{ row.email }}</span>
        </template>
      </el-table-column>

      <el-table-column label="姓名" align="center" width="150">
        <template #default="{ row }">
          <span>{{ row.full_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="创建时间" align="center" width="180">
        <template #default="{ row }">
          <span>{{ formatDateTime(row.create_at) }}</span>
        </template>
      </el-table-column>

      <el-table-column label="最后登录" align="center" width="180">
        <template #default="{ row }">
          <span>{{ row.last_login ? formatDateTime(row.last_login) : '从未登录' }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="230" fixed="right">
        <template #default="{ row }">
          <el-button
            type="primary"
            link
            @click="handleUpdate(row)"
          >
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
          <el-button
            type="danger"
            link
            @click="handleDelete(row)"
          >
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="listQuery.page"
      v-model:page-size="listQuery.limit"
      :page-sizes="[10, 20, 30, 50]"
      :total="total"
      layout="total, sizes, prev, pager, next"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      class="pagination-container"
    />

    <!-- 用户表单对话框 -->
    <el-dialog
      :title="dialogStatus === 'create' ? '创建用户' : '编辑用户'"
      v-model="dialogFormVisible"
      width="500px"
    >
      <el-form
        ref="dataFormRef"
        :rules="rules"
        :model="temp"
        label-position="right"
        label-width="80px"
        style="width: 400px; margin: 0 auto;"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="temp.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="temp.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="temp.full_name" placeholder="请输入姓名" />
        </el-form-item>
        
        <el-form-item 
          label="密码" 
          prop="password"
          :required="dialogStatus === 'create'"
        >
          <el-input
            v-model="temp.password"
            type="password"
            show-password
            :placeholder="dialogStatus === 'create' ? '请输入密码' : '不修改请留空'"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button
            type="primary"
            @click="dialogStatus === 'create' ? createData() : updateData()"
          >
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'
import { getUserList, createUser, updateUser, deleteUser } from '@/api/user'

interface User {
  user_id: string
  username: string
  email: string
  full_name: string
  create_at: string
  last_login: string | null
}

interface UserForm {
  user_id?: string
  username: string
  email: string
  full_name: string
  password?: string
}

const dataFormRef = ref<FormInstance>()
const listLoading = ref(true)
const dialogFormVisible = ref(false)
const dialogStatus = ref<'create' | 'update'>('create')
const list = ref<User[]>([])
const total = ref(0)

const listQuery = reactive({
  page: 1,
  limit: 10
})

const temp = reactive<UserForm>({
  username: '',
  email: '',
  full_name: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '长度至少为3个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  password: [
    { 
      required: dialogStatus.value === 'create',
      message: '请输入密码',
      trigger: 'blur'
    },
    { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
  ]
}

const getList = async () => {
  try {
    listLoading.value = true
    const { data } = await getUserList()
    list.value = data.items
    total.value = data.total
  } catch (error: any) {
    console.error('Error:', error)
    ElMessage.error(error.response?.data?.detail || '获取用户列表失败')
  } finally {
    listLoading.value = false
  }
}

const handleFilter = () => {
  listQuery.page = 1
  getList()
}

const resetTemp = () => {
  temp.user_id = undefined
  temp.username = ''
  temp.email = ''
  temp.full_name = ''
  temp.password = ''
}

const handleCreate = () => {
  resetTemp()
  dialogStatus.value = 'create'
  dialogFormVisible.value = true
  nextTick(() => {
    dataFormRef.value?.clearValidate()
  })
}

const createData = async () => {
  if (!dataFormRef.value) return
  
  try {
    await dataFormRef.value.validate()
    await createUser(temp)
    dialogFormVisible.value = false
    ElMessage.success('创建成功')
    handleFilter()
  } catch (error: any) {
    console.error('Error:', error)
    ElMessage.error(error.response?.data?.detail || '创建失败')
  }
}

const handleUpdate = (row: User) => {
  temp.user_id = row.user_id
  temp.username = row.username
  temp.email = row.email
  temp.full_name = row.full_name
  temp.password = ''
  dialogStatus.value = 'update'
  dialogFormVisible.value = true
  nextTick(() => {
    dataFormRef.value?.clearValidate()
  })
}

const updateData = async () => {
  if (!dataFormRef.value) return
  
  try {
    await dataFormRef.value.validate()
    const updateData = { ...temp }
    if (!updateData.password) {
      delete updateData.password
    }
    await updateUser(temp.user_id!, updateData)
    dialogFormVisible.value = false
    ElMessage.success('更新成功')
    handleFilter()
  } catch (error: any) {
    console.error('Error:', error)
    ElMessage.error(error.response?.data?.detail || '更新失败')
  }
}

const handleDelete = (row: User) => {
  ElMessageBox.confirm('确认要删除该用户吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteUser(row.user_id)
        ElMessage.success('删除成功')
        handleFilter()
      } catch (error: any) {
        console.error('Error:', error)
        ElMessage.error(error.response?.data?.detail || '删除失败')
      }
    })
    .catch(() => {
      // 用户点击取消
    })
}

const handleSizeChange = (val: number) => {
  listQuery.limit = val
  getList()
}

const handleCurrentChange = (val: number) => {
  listQuery.page = val
  getList()
}

const formatDateTime = (date: string) => {
  if (!date) return '-'
  return new Date(date).toLocaleString()
}

onMounted(() => {
  getList()
})
</script>

<style scoped>
.user-container {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  text-align: right;
  padding-top: 20px;
}

:deep(.el-table) {
  border-radius: 4px;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
}

.el-pagination {
  margin-top: 15px;
  justify-content: center;
}
</style>
