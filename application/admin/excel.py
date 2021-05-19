from application.admin import bp
from application.core import excelservice
from flask import request, redirect, flash, url_for
from flask_login import login_required
from config import Config
import os
from application.utils import files


@bp.route('/parse', methods=['POST'])
@login_required
def parse_excel():
    excel_file = request.files['file']
    if excel_file and excel_file.filename:
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, excel_file.filename)
        files.save_file(excel_file, file_path, recreate=True)
        excelservice.parse_excel_file(file_path)
        flash('Файл {0} успешно сохранён в каталог!'.format(excel_file.filename), category='success')
    return redirect(url_for('admin.catalog'))
