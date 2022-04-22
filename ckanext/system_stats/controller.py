# encoding: utf-8

from flask import render_template

class BaseController():

    def index():

        return render_template('stats_page.html')