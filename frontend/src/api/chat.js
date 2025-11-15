import request from '@/utils/request'

export function sendChatMessage(data) {
  return request({
    url: '/api/chat/message',
    method: 'POST',
    data
  })
}

export function getChatHistory(params) {
  return request({
    url: '/api/chat/history',
    method: 'GET',
    data: params
  })
}

export function getEmotionTimeline(params) {
  return request({
    url: '/api/chat/emotion-timeline',
    method: 'GET',
    data: params
  })
}