const BASE_URL = 'http://localhost:5000'

const request = (options) => {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': uni.getStorageSync('token') ? `Bearer ${uni.getStorageSync('token')}` : '',
        ...options.header
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res)
        } else {
          reject(res)
        }
      },
      fail: (error) => {
        reject(error)
      }
    })
  })
}

export default request