import axios from 'axios';

export default {
  namespaced: true,
  state: {},
  mutations: {},
  actions: {
    // 获取用户偏好设置
    getUserPreference() {
      return axios.get('/api/user/preference/').then(response => response.data);
    },
    // 保存用户偏好设置
    saveUserPreference({}, data) {
      return axios.post('/api/user/preference/save/', data).then(response => response.data);
    },
  },
};
