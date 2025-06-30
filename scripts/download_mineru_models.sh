#!/bin/bash
# 下载MinerU pipeline模型，使用modelscope源

set -e

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 执行模型下载
mineru-models-download --source modelscope --type pipeline

echo "MinerU pipeline模型下载完成（modelscope源）" 