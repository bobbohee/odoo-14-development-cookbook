# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LibraryBookCopy(models.Model):
    # 프로토타입 상속 : library.book 모델의 사본
    _inherit = 'library.book'
    _name = 'library.book.copy'
    _description = 'Library Book\'s Copy'
