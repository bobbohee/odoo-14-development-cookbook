# -*- coding: utf-8 -*-

from odoo import models, fields


class LibraryBookRentWizard(models.TransientModel):
    _name = 'library.book.rent.wizard'

    borrower_id = fields.Many2one('res.partner', string='Borrower')
    book_ids = fields.Many2many('library.book', string='Books')

    def add_book_rents(self):
        rent_model = self.env['library.book.rent']
        for wiz in self:
            for book in wiz.book_ids:
                rent_model.create({
                    'borrower_id': wiz.borrower_id.id,
                    'book_id': book.id
                })