# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class LibraryBookRent(models.Model):
    _name = 'library.book.rent'

    book_id = fields.Many2one('library.book', 'Book', required=True)
    borrower_id = fields.Many2one('res.partner', 'Borrower', required=True)
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
    ], 'State', default='ongoing', required=True)
    rent_date = fields.Date(default=fields.Date.today)
    return_date = fields.Date()

    def book_return(self):
        self.ensure_one()
        self.book_id.sudo().make_available()
        self.sudo().write({
            'state': 'returned',
            'return_date': fields.Date.today(),
        })

    def book_lost(self):
        self.ensure_one()
        self.sudo().state = 'lost'
        book_with_different_context = self.book_id.with_context(avold_deactivate=True)
        book_with_different_context.sudo().make_lost()
