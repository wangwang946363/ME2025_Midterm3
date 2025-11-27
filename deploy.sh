#!/bin/bash

# 請將此 URL 換成您的 GitHub Repo
REPO_URL="YOUR_GITHUB_REPO_URL" 
DIR_NAME="ME2025_Midterm3"

if [ ! -d "$DIR_NAME" ]; then
    echo "=== 首次執行部署 ==="
    git clone "$REPO_URL"
    cd "$DIR_NAME"
    
    echo "建立虛擬環境..."
    python3 -m venv .venv
    source .venv/bin/activate
    
    pip install -r requirements.txt
    
    echo "啟動應用程式..."
    nohup python3 app.py > output.log 2>&1 &
    
else
    echo "=== 更新專案版本 ==="
    cd "$DIR_NAME"
    git pull
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -r requirements.txt
    
    echo "重啟應用程式..."
    PID=$(ps aux | grep 'python3 app.py' | grep -v grep | awk '{print $2}')
    if [ -n "$PID" ]; then
        kill -9 $PID
    fi
    
    nohup python3 app.py > output.log 2>&1 &
fi

echo "部署完成！"