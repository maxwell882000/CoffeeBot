from . import bp
from flask import render_template
from flask_login import login_required

from application.core import commentservice


@bp.route('/comments')
@login_required
def comments():
    user_comments = commentservice.get_all_comments()
    return render_template('admin/comments.html', comments=user_comments, title="Отзывы", area='comments')
