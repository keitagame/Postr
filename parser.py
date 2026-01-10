import re
from markupsafe import Markup
def convert_reply_links(content, thread_id):
    # >>数字 のあとにスペースがある場合のみリンク化
    def repl(match):
        number = match.group(1)
        return f'<a href="/thread/{thread_id}#post-{number}">&gt;&gt;{number}</a>'
    return Markup(re.sub(r'>>(\d+)(?=\s|$)', repl, content))

