import request from './request'

export const login = (data) => {
  return request({
    url: '/login',
    method: 'POST',
    data
  })
}

export const register = (data) => {
  return request({
    url: '/register',
    method: 'POST',
    data
  })
}

export const getCurrentUser = () => {
  return request({
    url: '/me',
    method: 'GET'
  })
}