/*
 * @Author: xiakaijia xkjjusa1991@qq.com
 * @Date: 2025-02-04 01:33:43
 * @LastEditors: xiakaijia xkjjusa1991@qq.com
 * @LastEditTime: 2025-02-04 01:34:26
 * @FilePath: \RAG_Admin\src\api\user.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import request from '@/utils/request'

export interface User {
  user_id: string
  username: string
  email: string
  full_name: string
  create_at: string
  last_login: string | null
}

export interface UserCreate {
  username: string
  email: string
  full_name: string
  password: string
}

export interface UserUpdate {
  username?: string
  email?: string
  full_name?: string
  password?: string
}

export interface ListResponse<T> {
  items: T[]
  total: number
}

// 获取用户列表
export function getUserList() {
  return request<ListResponse<User>>({
    url: '/api/v1/users',
    method: 'get'
  })
}

// 创建用户
export function createUser(data: UserCreate) {
  return request<User>({
    url: '/api/v1/users',
    method: 'post',
    data
  })
}

// 更新用户
export function updateUser(id: string, data: UserUpdate) {
  return request<User>({
    url: `/api/v1/users/${id}`,
    method: 'put',
    data
  })
}

// 删除用户
export function deleteUser(id: string) {
  return request<void>({
    url: `/api/v1/users/${id}`,
    method: 'delete'
  })
}

// 获取单个用户
export function getUser(id: string) {
  return request<User>({
    url: `/api/v1/users/${id}`,
    method: 'get'
  })
}