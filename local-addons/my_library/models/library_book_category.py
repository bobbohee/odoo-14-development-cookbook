# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# ** 계층 구조는 덜 업데이트되는 정적 계층에 사용해야함 **
# 카테고리가 CRUD 될 때마다 모든 parent_path가 변경되어 작업량이 증가함


class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'

    _parent_store = True
    _parent_name = 'parent_id' # optional: if field is 'parent_id'

    name = fields.Char('Category')
    parent_id = fields.Many2one('library.book.category', string='Parent Category', ondelete='restrict', index=True)
    child_ids = fields.One2many('library.book.category', 'parent_id', string='Child Categories')
    parent_path = fields.Char(index=True)


    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')

    def create_categories(self):
        categ1 = {'name': 'Child category 1'}
        categ2 = {'name': 'Child category 2'}
        parent_category_val = {
            'name': 'Parent Category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        record = self.env['library.book.category'].create(parent_category_val)
