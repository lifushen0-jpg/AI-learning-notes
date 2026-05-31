import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, send_from_directory, redirect, url_for

# 初始化 Flask 应用
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
DB_PATH = 'games.db'

# ======================
# 数据库初始化
# ======================
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                game_type TEXT DEFAULT 'go',  -- go / chess / custom
                created_at TEXT NOT NULL,
                moves_json TEXT,              -- 自定义 JSON 棋谱
                sgf_filename TEXT             -- SGF 文件名（可选）
            )
        ''')
        conn.commit()
        conn.close()

# ======================
# 首页：上传 + 列表
# ======================
@app.route('/')
def index():
    # 获取最新10条棋谱
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games ORDER BY created_at DESC LIMIT 10")
    recent_games = cursor.fetchall()
    conn.close()

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>棋谱共享平台</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 0 20px; }
            .upload-form { background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
            input, textarea, select, button { width: 100%; padding: 8px; margin: 5px 0; box-sizing: border-box; }
            button { background: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background: #45a049; }
            .game-item { border-bottom: 1px solid #eee; padding: 10px 0; }
            .game-title { font-weight: bold; color: #2c3e50; }
            .game-meta { color: #7f8c8d; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>♟️ 棋谱共享平台</h1>
        
        <div class="upload-form">
            <h2>上传新棋谱</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="text" name="title" placeholder="棋谱标题（必填）" required>
                <input type="text" name="author" placeholder="你的名字（必填）" required>
                <select name="game_type">
                    <option value="go">围棋 (Go)</option>
                    <option value="chess">国际象棋 (Chess)</option>
                    <option value="custom">自定义格式</option>
                </select>
                <textarea name="moves_json" rows="4" placeholder='[{"x":3,"y":4},{"x":15,"y":16}] （仅自定义格式）'></textarea>
                <p>或上传 SGF 文件（围棋）：<input type="file" name="sgf_file" accept=".sgf"></p>
                <button type="submit">上传棋谱</button>
            </form>
        </div>

        <h2>最新棋谱</h2>
        {% for game in recent_games %}
        <div class="game-item">
            <div class="game-title">{{ game['title'] }}</div>
            <div class="game-meta">
                作者: {{ game['author'] }} | 
                类型: {{ game['game_type'] }} | 
                日期: {{ game['created_at'][:10] }}
            </div>
            <a href="/game/{{ game['id'] }}">查看详情</a>
        </div>
        {% endfor %}

        <hr>
        <a href="/all">查看全部棋谱</a>
    </body>
    </html>
    '''
    return render_template_string(html, recent_games=recent_games)

# ======================
# 上传接口
# ======================
@app.route('/upload', methods=['POST'])
def upload_game():
    try:
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        game_type = request.form.get('game_type', 'go')
        moves_json = request.form.get('moves_json', '').strip()
        sgf_file = request.files.get('sgf_file')

        if not title or not author:
            return "标题和作者不能为空！", 400

        # 验证 JSON（如果提供了）
        if moves_json:
            json.loads(moves_json)  # 可能抛出异常

        # 保存 SGF 文件（如果上传了）
        sgf_filename = None
        if sgf_file and sgf_file.filename.endswith('.sgf'):
            sgf_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{sgf_file.filename}"
            sgf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], sgf_filename))

        # 存入数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (title, author, game_type, created_at, moves_json, sgf_filename)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, author, game_type, datetime.now().isoformat(), moves_json, sgf_filename))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    except ValueError as e:
        return f"JSON 格式错误: {e}", 400
    except Exception as e:
        return f"上传失败: {e}", 500

# ======================
# 查看单个棋谱
# ======================
@app.route('/game/<int:game_id>')
def view_game(game_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
    game = cursor.fetchone()
    conn.close()

    if not game:
        return "棋谱不存在", 404

    html = f'''
    <h1>{game['title']}</h1>
    <p><b>作者:</b> {game['author']} | <b>类型:</b> {game['game_type']} | <b>时间:</b> {game['created_at'][:19]}</p>
    '''
    
    if game['sgf_filename']:
        html += f'<p><a href="/sgf/{game["sgf_filename"]}" target="_blank">下载 SGF 文件</a></p>'
    elif game['moves_json']:
        moves = json.loads(game['moves_json'])
        html += f"<p>共 {len(moves)} 步</p><pre>{json.dumps(moves, indent=2, ensure_ascii=False)}</pre>"
    else:
        html += "<p>无棋谱数据</p>"

    html += '<br><a href="/">返回首页</a>'
    return html

# ======================
# 下载 SGF 文件
# ======================
@app.route('/sgf/<filename>')
def download_sgf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ======================
# API：获取所有棋谱（JSON）
# ======================
@app.route('/api/games')
def api_games():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, game_type, created_at FROM games ORDER BY created_at DESC")
    games = cursor.fetchall()
    conn.close()
    
    result = [
        {
            'id': g['id'],
            'title': g['title'],
            'author': g['author'],
            'game_type': g['game_type'],
            'created_at': g['created_at']
        }
        for g in games
    ]
    return jsonify(result)

# ======================
# 启动应用
# ======================
if __name__ == '__main__':
    init_db()
    print("✅ 棋谱服务器启动成功！")
    print("🌐 访问地址: http://localhost:5000")
    print("👥 局域网访问: 将 localhost 替换为本机 IP（如 192.168.x.x）")
    app.run(host='0.0.0.0', port=5000, debug=True)