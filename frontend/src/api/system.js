import request from './request'

export const getSystemHealth = () => {
  return request({
    url: '/system/health',
    method: 'GET'
  })
}

export const getAvailableModels = () => {
  return request({
    url: '/system/models',
    method: 'GET'
  })
}

export const switchModel = (modelName) => {
  return request({
    url: '/system/switch-model',
    method: 'POST',
    data: { model_name: modelName }
  })
}