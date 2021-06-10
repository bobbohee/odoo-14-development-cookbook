# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    # 클래스 상속 (확장)
    _inherit = 'res.partner'
    _order = 'name'

    published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
    authored_book_ids = fields.Many2many(
        'library.book', string='Authored Books',
         # optional: relation='library_book_res_partner_rel'
    )
    count_books = fields.Integer('Number of Authored Books', compute='_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for record in self:
            record.count_books = len(record.authored_book_ids)