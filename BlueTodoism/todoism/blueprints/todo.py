
from flask import Blueprint, render_template, url_for, request, jsonify
from flask_login import login_required, current_user

from todoism.models import Item
from todoism.extensions import db

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/items/new', methods=['GET', 'POST'])
@login_required
def new_item():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        jsonify(message='Invalid item body.'), 400
    item = Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('_item.html', item=item), message='+1')