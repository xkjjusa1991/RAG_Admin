<template>
  <div class="user-list">
    <div class="operation-bar">
      <el-button type="primary" @click="handleAdd">添加用户</el-button>
    </div>

    <el-table 
      :data="users" 
      style="width: 100%"
      v-loading="loading"
      border
    >
      <el-table-column prop="user_id" label="ID" width="220" show-overflow-tooltip />
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="email" label="邮箱" width="200" show-overflow-tooltip />
      <el-table-column prop="full_name" label="姓名" width="150" />
      <el-table-column label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.create_at) }}
        </template>
      </el-table-column>
      <el-table-column label="最后登录" width="180">
        <template #default="{ row }">
          {{ row.last_login ? formatDate(row.last_login) : '从未登录' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="150">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">
            <el-icon><Edit /></el-icon>编辑
          </el-button>
          <el-button type="danger" link @click="handleDelete(row)">
            <el-icon><Delete /></el-icon>删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="formType === 'add' ? '添加用户' : '编辑用户'"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="form.full_name" />
        </el-form-item>
        <el-form-item 
          label="密码" 
          prop="password"
          :required="formType === 'add'"
        >
          <el-input
            v-model="form.password"
            type="password"
            placeholder="新建用户必填，修改用户选填"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'
import { getUserList, createUser, updateUser } from '@/api/user'
import type { User, UserCreate, UserUpdate } from '@/types/user'

const loading = ref(false)
const users = ref<User[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const formType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

const form = ref<UserCreate & UserUpdate>({
  username: '',
  email: '',
  full_name: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: formType.value === 'add', message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
  ]
}

const getUsers = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const response = await getUserList({ skip, limit: pageSize.value })
    users.value = response.data
    total.value = response.total
  } catch (error) {
    console.error('Error fetching users:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  getUsers()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  getUsers()
}

const handleAdd = () => {
  formType.value = 'add'
  form.value = {
    username: '',
    email: '',
    full_name: '',
    password: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row: User) => {
  formType.value = 'edit'
  form.value = {
    ...row,
    password: ''
  }
  dialogVisible.value = true
}

const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该用户吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    // TODO: 实现删除用户的功能
    ElMessage.success('删除成功')
    getUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting user:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (formType.value === 'add') {
      await createUser(form.value as UserCreate)
      ElMessage.success('添加成功')
    } else {
      const { user_id } = form.value as User
      const updateData = { ...form.value }
      if (!updateData.password) {
        delete updateData.password
      }
      await updateUser(user_id, updateData as UserUpdate)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    getUsers()
  } catch (error: any) {
    console.error('Error submitting form:', error)
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const formatDate = (date: string) => {
  if (!date) return '-'
  return new Date(date).toLocaleString()
}

onMounted(() => {
  getUsers()
})
</script>

<style scoped>
.user-list {
  padding: 20px;
}

.operation-bar {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-table) {
  border-radius: 4px;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
