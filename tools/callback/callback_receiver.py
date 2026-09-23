"""
BKFlow 任务回调接收服务

用于接收 BKFlow 流程执行完成后的回调通知，
显示任务的执行结果、输出数据等信息。

启动方式：
    python callback_receiver.py

访问地址：
    http://localhost:5000

回调地址：
    http://localhost:5000/callback
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# 存储接收到的回调记录（内存中，重启后清空）
callback_records = []


@app.route('/')
def index():
    """首页 - 显示所有回调记录"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>BKFlow 回调接收器</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #3a84ff;
                padding-bottom: 10px;
            }
            .info {
                background: #e1f0ff;
                border-left: 4px solid #3a84ff;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 4px;
            }
            .stats {
                display: flex;
                gap: 20px;
                margin-bottom: 20px;
            }
            .stat-box {
                flex: 1;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            .stat-number {
                font-size: 36px;
                font-weight: bold;
                color: #3a84ff;
            }
            .stat-label {
                color: #666;
                margin-top: 5px;
            }
            .record {
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .record-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #f0f0f0;
            }
            .record-title {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            .status-success {
                background: #2dcb56;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 14px;
            }
            .status-failed {
                background: #ea3536;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 14px;
            }
            .record-meta {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-bottom: 15px;
            }
            .meta-item {
                display: flex;
                flex-direction: column;
            }
            .meta-label {
                color: #999;
                font-size: 12px;
                margin-bottom: 4px;
            }
            .meta-value {
                color: #333;
                font-weight: 500;
            }
            .record-data {
                background: #f8f8f8;
                padding: 15px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                overflow-x: auto;
            }
            pre {
                margin: 0;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            .no-records {
                text-align: center;
                padding: 60px 20px;
                color: #999;
                font-size: 16px;
            }
            .clear-btn {
                background: #ea3536;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }
            .clear-btn:hover {
                background: #c92929;
            }
            .error-info {
                background: #fff3f3;
                border-left: 4px solid #ea3536;
                padding: 15px;
                margin-top: 15px;
                border-radius: 4px;
            }
            .error-title {
                color: #ea3536;
                font-weight: bold;
                margin-bottom: 5px;
            }
        </style>
    </head>
    <body>
        <h1>🔔 BKFlow 回调接收器</h1>

        <div class="info">
            <strong>回调地址：</strong> <code>http://localhost:5000/callback</code><br>
            <strong>使用说明：</strong> 在 BKFlow 流程配置中填写此地址，流程执行完成后会自动回调
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">""" + str(len(callback_records)) + """</div>
                <div class="stat-label">总回调次数</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">""" + str(sum(1 for r in callback_records if r.get('status') == 'success')) + """</div>
                <div class="stat-label">成功</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">""" + str(sum(1 for r in callback_records if r.get('status') == 'failed')) + """</div>
                <div class="stat-label">失败</div>
            </div>
        </div>

        """

    if len(callback_records) > 0:
        html += f"""
        <div style="text-align: right; margin-bottom: 20px;">
            <button class="clear-btn" onclick="if(confirm('确定清空所有记录？')) location.href='/clear'">清空记录</button>
        </div>
        """

        for record in reversed(callback_records):  # 最新的在前
            status = record.get('status', 'unknown')
            status_class = 'status-success' if status == 'success' else 'status-failed'
            status_text = '成功' if status == 'success' else '失败'

            html += f"""
            <div class="record">
                <div class="record-header">
                    <div class="record-title">任务 #{record['data'].get('task_id', 'N/A')}: {record['data'].get('task_name', '未命名')}</div>
                    <span class="{status_class}">{status_text}</span>
                </div>

                <div class="record-meta">
                    <div class="meta-item">
                        <div class="meta-label">接收时间</div>
                        <div class="meta-value">{record['received_at']}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">执行人</div>
                        <div class="meta-value">{record['data'].get('executor', 'N/A')}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">开始时间</div>
                        <div class="meta-value">{datetime.fromtimestamp(record['data']['start_time']).strftime('%Y-%m-%d %H:%M:%S') if record['data'].get('start_time') else 'N/A'}</div>
                    </div>
                </div>
            """

            # 如果是失败的，显示错误信息
            if status == 'failed' and 'extra_data' in record['data']:
                extra = record['data']['extra_data']
                html += f"""
                <div class="error-info">
                    <div class="error-title">❌ 失败原因</div>
                    <div><strong>失败节点：</strong>{extra.get('failed_node_name', 'N/A')} ({extra.get('failed_node', 'N/A')})</div>
                    <div><strong>错误信息：</strong>{extra.get('failed_message', 'N/A')}</div>
                </div>
                """

            html += f"""
                <div class="record-data">
                    <strong>完整数据：</strong>
                    <pre>{json.dumps(record['data'], indent=2, ensure_ascii=False)}</pre>
                </div>
            </div>
            """
    else:
        html += """
        <div class="no-records">
            📭 暂无回调记录<br>
            <small>配置 BKFlow 流程回调后，执行结果会显示在这里</small>
        </div>
        """

    html += """
    </body>
    </html>
    """

    return html


@app.route('/callback', methods=['POST'])
def callback():
    """接收 BKFlow 回调"""
    try:
        data = request.get_json()

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
        return jsonify({
            "result": True,
            "message": "回调接收成功"
        }), 200

    except Exception as e:
        print(f"[ERROR] 处理回调失败: {str(e)}")
        return jsonify({
            "result": False,
            "message": f"处理失败: {str(e)}"
        }), 500


@app.route('/clear')
def clear():
    """清空所有记录"""
    global callback_records
    callback_records = []
    return """
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url=/">
    </head>
    <body>记录已清空，正在跳转...</body>
    </html>
    """


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "service": "BKFlow Callback Receiver",
        "records_count": len(callback_records)
    })


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 BKFlow 回调接收服务启动")
    print("="*80)
    print(f"  访问地址: http://localhost:5000")
    print(f"  回调地址: http://localhost:5000/callback")
    print("="*80 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
