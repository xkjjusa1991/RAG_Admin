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
