# -*- coding: utf-8 -*-
"""
AI婚恋匹配系统 - 项目主入口
快速启动脚本，无需进入core目录
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入主程序
from core.main import main

if __name__ == "__main__":
    main()
