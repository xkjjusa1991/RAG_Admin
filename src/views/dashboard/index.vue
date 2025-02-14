<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户总数</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ userCount }}</h2>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>今日新增</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ todayNewUsers }}</h2>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>在线用户</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ onlineUsers }}</h2>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>系统消息</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ messageCount }}</h2>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>最近登录</span>
            </div>
          </template>
          <el-table :data="recentLogins" style="width: 100%">
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="login_time" label="登录时间" />
            <el-table-column prop="ip" label="IP地址" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>系统状态</span>
            </div>
          </template>
          <div class="system-info">
            <p><strong>CPU使用率：</strong> {{ systemInfo.cpu }}%</p>
            <p><strong>内存使用率：</strong> {{ systemInfo.memory }}%</p>
            <p><strong>磁盘使用率：</strong> {{ systemInfo.disk }}%</p>
            <p><strong>运行时间：</strong> {{ systemInfo.uptime }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 模拟数据
const userCount = ref(1000)
const todayNewUsers = ref(25)
const onlineUsers = ref(150)
const messageCount = ref(8)

const recentLogins = ref([
  {
    username: 'admin',
    login_time: '2024-02-10 10:30:25',
    ip: '192.168.1.100'
  },
  {
    username: 'user1',
    login_time: '2024-02-10 10:25:18',
    ip: '192.168.1.101'
  },
  {
    username: 'user2',
    login_time: '2024-02-10 10:20:05',
    ip: '192.168.1.102'
  }
])

const systemInfo = ref({
  cpu: 35,
  memory: 45,
  disk: 60,
  uptime: '10天 5小时 30分钟'
})

onMounted(() => {
  // TODO: 从后端获取实际数据
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-body {
  text-align: center;
  padding: 20px 0;
}

.card-body h2 {
  margin: 0;
  font-size: 28px;
  color: #303133;
}

.system-info {
  padding: 10px;
}

.system-info p {
  margin: 10px 0;
  font-size: 14px;
}

.system-info strong {
  color: #606266;
}
</style>
