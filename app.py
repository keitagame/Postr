from flask import Flask, render_template, request, redirect, url_for
# import 追加
from datetime import datetime, timedelta

import uuid
import os
import parser
app = Flask(__name__)

threads = []  # スレッドを保存するリスト
THREAD_TTL = timedelta(hours=24)  # ← 例：24時間で削除
weekdays = ["月", "火", "水", "木", "金", "土", "日"]
app.jinja_env.filters['reply_links'] = parser.convert_reply_links
@app.route('/')
def home():
    # ホームはスレッド一覧へリダイレクト
    return redirect(url_for('thread_list'))

@app.route('/threads')
def thread_list():
    now = datetime.now()
    global threads
    threads = [t for t in threads if now - t['created_at'] < THREAD_TTL]
    return render_template('threads.html', threads=threads)

@app.route('/add', methods=['GET', 'POST'])
def create_thread():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form.get('category', '未分類')
        if title:
            thread_id = str(uuid.uuid4())[:8]
            threads.append({
                'id': thread_id,
                'title': title,
                'category': category,
                'created_at': datetime.now(),
                'posts': []
            })
        return redirect(url_for('thread_list'))
    return render_template('add.html')

@app.route('/thread/<thread_id>', methods=['GET', 'POST'])
def thread_detail(thread_id):
    thread = next((t for t in threads if t['id'] == thread_id), None)
    if not thread:
        return "スレッドが見つかりません", 404

    if request.method == 'POST':
        name = request.form.get('name', '名無し')
        content = request.form['content']
        if content:
            now = datetime.now()
            weekday = weekdays[now.weekday()]
            post_data = {
                'number': len(thread['posts']) + 1,
                'id': str(uuid.uuid4())[:8],
                'name': name,
                'content': content,
                'time': now.strftime(f"%Y/%m/%d({weekday})")
            }
            thread['posts'].append(post_data)
        return redirect(url_for('thread_detail', thread_id=thread_id))

    return render_template('thread.html', thread=thread)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
