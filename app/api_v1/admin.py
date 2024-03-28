from flask import render_template, url_for

from . import api

@api.route('/admin')
def admin ():
    return render_template('admin.html')

