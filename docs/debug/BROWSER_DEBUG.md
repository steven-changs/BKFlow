# 浏览器调试步骤

## 请在浏览器开发者工具的 Console 标签中执行以下代码：

```javascript
// 1. 检查 window.APP_CODE
console.log('APP_CODE:', window.APP_CODE);

// 2. 检查 axios 配置
console.log('xsrfCookieName:', axios.defaults.xsrfCookieName);
console.log('xsrfHeaderName:', axios.defaults.xsrfHeaderName);

// 3. 检查所有 cookies
console.log('All cookies:', document.cookie);

// 4. 检查特定的 CSRF cookie
const csrfCookie = document.cookie.split(';').find(c => c.trim().startsWith('bkflow_csrftoken='));
console.log('CSRF Cookie:', csrfCookie);

// 5. 手动读取 cookie 值
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
console.log('CSRF Token:', getCookie('bkflow_csrftoken'));
```

## 请将这些输出结果发给我

特别关注：
- `APP_CODE` 是否为 `bkflow`
- `All cookies` 中是否包含 `bkflow_csrftoken`
- `CSRF Token` 是否有值
