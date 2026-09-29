"""
BKFlow 任务回调接收服务（轻量版）

使用 Python 内置的 http.server，无需安装额外依赖。

启动方式：
    python callback_receiver_simple.py

访问地址：
    http://localhost:5000

回调地址：
    http://localhost:5000/callback
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
from urllib.parse import urlparse
import html

# 存储接收到的回调记录
callback_records = []


class CallbackHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/':
            self.serve_index()
        elif parsed_path.path == '/clear':
            self.clear_records()
        elif parsed_path.path == '/health':
            self.serve_health()
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        """处理 POST 请求（回调）"""
        if self.path == '/callback':
            self.handle_callback()
        else:
            self.send_error(404, "Endpoint not found")

    def serve_index(self):
        """首页 - 显示所有回调记录"""
        success_count = sum(1 for r in callback_records if r.get('status') == 'success')
        failed_count = sum(1 for r in callback_records if r.get('status') == 'failed')

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>BKFlow 回调接收器</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ color: #333; border-bottom: 3px solid #3a84ff; padding-bottom: 10px; }}
        .info {{ background: #e1f0ff; border-left: 4px solid #3a84ff; padding: 15px; margin-bottom: 20px; border-radius: 4px; }}
        .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .stat-box {{ flex: 1; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .stat-number {{ font-size: 36px; font-weight: bold; color: #3a84ff; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .record {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .record-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #f0f0f0; }}
        .record-title {{ font-size: 18px; font-weight: bold; color: #333; }}
        .status-success {{ background: #2dcb56; color: white; padding: 4px 12px; border-radius: 12px; font-size: 14px; }}
        .status-failed {{ background: #ea3536; color: white; padding: 4px 12px; border-radius: 12px; font-size: 14px; }}
        .record-meta {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px; }}
        .meta-item {{ display: flex; flex-direction: column; }}
        .meta-label {{ color: #999; font-size: 12px; margin-bottom: 4px; }}
        .meta-value {{ color: #333; font-weight: 500; }}
        .record-data {{ background: #f8f8f8; padding: 15px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 13px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }}
        .no-records {{ text-align: center; padding: 60px 20px; color: #999; font-size: 16px; }}
        .clear-btn {{ background: #ea3536; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-block; }}
        .error-info {{ background: #fff3f3; border-left: 4px solid #ea3536; padding: 15px; margin-top: 15px; border-radius: 4px; }}
        .error-title {{ color: #ea3536; font-weight: bold; margin-bottom: 5px; }}
    </style>
</head>
<body>
    <h1>🔔 BKFlow 回调接收器</h1>

    <div class="info">
        <strong>回调地址：</strong> <code>http://localhost:5000/callback</code><br>
        <strong>使用说明：</strong> 在 BKFlow 流程配置中填写此地址，流程执行完成后会自动回调<br>
        <strong>自动刷新：</strong> 页面每 10 秒自动刷新一次
    </div>

    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">{len(callback_records)}</div>
            <div class="stat-label">总回调次数</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{success_count}</div>
            <div class="stat-label">成功</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{failed_count}</div>
            <div class="stat-label">失败</div>
        </div>
    </div>
"""

        if len(callback_records) > 0:
            html_content += f"""
    <div style="text-align: right; margin-bottom: 20px;">
        <a href="/clear" class="clear-btn" onclick="return confirm('确定清空所有记录？')">清空记录</a>
    </div>
"""
            for record in reversed(callback_records):  # 最新的在前
                status = record.get('status', 'unknown')
                status_class = 'status-success' if status == 'success' else 'status-failed'
                status_text = '成功' if status == 'success' else '失败'

                data = record['data']
                task_id = data.get('task_id', 'N/A')
                task_name = html.escape(data.get('task_name', '未命名'))
                executor = html.escape(data.get('executor', 'N/A'))

                start_time = 'N/A'
                if data.get('start_time'):
                    start_time = datetime.fromtimestamp(data['start_time']).strftime('%Y-%m-%d %H:%M:%S')

                html_content += f"""
    <div class="record">
        <div class="record-header">
            <div class="record-title">任务 #{task_id}: {task_name}</div>
            <span class="{status_class}">{status_text}</span>
        </div>

        <div class="record-meta">
            <div class="meta-item">
                <div class="meta-label">接收时间</div>
                <div class="meta-value">{record['received_at']}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">执行人</div>
                <div class="meta-value">{executor}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">开始时间</div>
                <div class="meta-value">{start_time}</div>
            </div>
        </div>
"""

                # 如果是失败的，显示错误信息
                if status == 'failed' and 'extra_data' in data:
                    extra = data['extra_data']
                    failed_node_name = html.escape(extra.get('failed_node_name', 'N/A'))
                    failed_node = html.escape(extra.get('failed_node', 'N/A'))
                    failed_message = html.escape(extra.get('failed_message', 'N/A'))

                    html_content += f"""
        <div class="error-info">
            <div class="error-title">❌ 失败原因</div>
            <div><strong>失败节点：</strong>{failed_node_name} ({failed_node})</div>
            <div><strong>错误信息：</strong>{failed_message}</div>
        </div>
"""

                data_json = json.dumps(data, indent=2, ensure_ascii=False)
                html_content += f"""
        <div class="record-data"><strong>完整数据：</strong>
{html.escape(data_json)}</div>
    </div>
"""
        else:
            html_content += """
    <div class="no-records">
        📭 暂无回调记录<br>
        <small>配置 BKFlow 流程回调后，执行结果会显示在这里</small>
    </div>
"""

        html_content += """
</body>
</html>
"""

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def handle_callback(self):
        """处理 BKFlow 回调"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8')) if post_data else {}

            # 判断请求类型
            if not data or len(data) == 0:
                # 空数据 - 验证请求，不记录
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 收到验证请求（空数据），已忽略")
                response = {
                    "result": True,
                    "message": "验证成功"
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            # 判断是成功还是失败
            status = 'success' if 'outputs' in data else 'failed'

            # 保存记录
            record = {
                'received_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': status,
                'data': data
            }
            callback_records.append(record)

            # 打印到控制台
            print("\n" + "="*80)
            print(f"[{record['received_at']}] 收到回调 - 状态: {status.upper()}")
            print("="*80)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print("="*80 + "\n")

            # 返回成功响应
            response = {
                "result": True,
                "message": "回调接收成功"
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"[ERROR] 处理回调失败: {str(e)}")

            error_response = {
                "result": False,
                "message": f"处理失败: {str(e)}"
            }

            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def clear_records(self):
        """清空所有记录"""
        global callback_records
        callback_records = []

        redirect_html = """
<html>
<head>
    <meta http-equiv="refresh" content="0;url=/">
</head>
<body>记录已清空，正在跳转...</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(redirect_html.encode('utf-8'))

    def serve_health(self):
        """健康检查"""
        health_data = {
            "status": "ok",
            "service": "BKFlow Callback Receiver",
            "records_count": len(callback_records)
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(health_data).encode('utf-8'))


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000

    print("\n" + "="*80)
    print("🚀 BKFlow 回调接收服务启动（轻量版）")
    print("="*80)
    print(f"  访问地址: http://localhost:{port}")
    print(f"  回调地址: http://localhost:{port}/callback")
    print(f"  健康检查: http://localhost:{port}/health")
    print("="*80)
    print("  提示: 页面每 10 秒自动刷新")
    print("  提示: 按 Ctrl+C 停止服务")
    print("="*80 + "\n")

    server = HTTPServer((host, port), CallbackHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务已停止")
        server.shutdown()
