import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

import sys
sys.path.insert(0, 'D:/program/project/BKFlow')

# 手动加载环境变量
with open('.env', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip()

import django
django.setup()

from bkflow.template.models import TemplateInfo

template_id = 4
try:
    template = TemplateInfo.objects.get(id=template_id)
    print(f"\n流程模板 #{template_id} 信息：")
    print("="*60)
    print(f"模板名称: {template.name}")
    print(f"创建时间: {template.create_time}")
    print(f"更新时间: {template.edit_time}")
    print("="*60)
    print(f"\n回调配置 (notify_config):")
    print(template.notify_config)
    print("="*60)
    
    if template.notify_config:
        import json
        config = json.loads(template.notify_config) if isinstance(template.notify_config, str) else template.notify_config
        print("\n解析后的回调配置:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
    else:
        print("\n❌ 回调配置为空！")
        print("可能原因：配置没有正确保存到数据库")
        
except Exception as e:
    print(f"❌ 查询失败: {e}")
    import traceback
    traceback.print_exc()
