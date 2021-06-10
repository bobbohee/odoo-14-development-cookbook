# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

from datetime import timedelta

# 파이썬 예외 졸류

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive']
    _description = 'Library Book'
    _order = 'date_release desc, name'
    # _rec_name = 'short_name'
    # _log_access = False

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)', 'No of pages must be positive.')
    ]

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title', translate=True, index=True)
    notes = fields.Text('Internal Notes')
    state = fields.Selection([
        ('draft', 'Not Available'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
    ], 'State', default='draft')
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Date('Last Updated')
    pages = fields.Integer('Number of Pages',
                           groups='base.group_user', states={'lost': [('readonly', True)]},
                           help='Total book page count', company_dependent=False)
    render_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4),  # optional: precision decimals
    )
    cost_price = fields.Float('Book Cost', digits='Book Price')
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
        # optional: currency_field='currency_id'
    )
    publisher_id = fields.Many2one('res.partner', string='Publisher',
                                   # optional:
                                   ondelete='set null', context={}, domain=[])
    publisher_city = fields.Char('Publisher City', related='publisher_id.city', readonly=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    category_id = fields.Many2one('library.book.category', string='Category')
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age_days', inverse='_inverse_age_days', search='_search_age_days',
        store=False,  # optional
        compute_sudo=True,  # optional
    )
    ref_doc_id = fields.Reference(selection='_referencable_models', string='Reference Document')
    manage_remarks = fields.Text('Manager Remarks')
    isbn = fields.Char('ISBN')
    old_edition = fields.Many2one('library.book', string='Old Edition')

    # active = fields.Boolean('Active', default=True)

    # ex) 눈치껏 못 배웁니다, 일센스 (작가1, 작가2, 작가3)
    def name_get(self):
        result = []
        for book in self:
            authors = book.author_ids.mapped('name')
            name = "%s (%s)" % (book.short_name, ', '.join(authors))
            result.append((book.id, name))
        return result

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the post')

    @api.depends('date_release')
    def _compute_age_days(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age_days(self):
        today = fields.Date.today()
        for book in self:
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    def _search_age_days(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ('draft', 'available'),
            ('available', 'borrowed'),
            ('available', 'lost'),
            ('borrowed', 'available'),
            ('borrowed', 'lost'),
            ('lost', 'available'),
        ]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (book.state, new_state)  # O
                # msg = _('Moving from %s to %s is not allowed' % (book.state, new_state))  # X
                raise UserError(msg)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    def log_all_library_members(self):
        # This is an empty recordset of model library.member
        library_member_model = self.env['library.member']

        all_members = library_member_model.search([])
        print('ALL MEMBERS:', all_members)
        return True

    def change_release_date(self):
        self.ensure_one() # 하나의 레코드만 있는지 확인
        self.date_release = fields.Date.today()
        # or
        # self.update({
        #   'date_release': fields.Date.today(),
        # })

    def find_book(self):
        # ilike 연산자는 = 연산자와 동일
        domain = [
            '|',
            '&', ('name', 'ilike', '또 생각하는 개구리 - 개정판'), ('category_id.name', 'ilike', '그림책'),
            '&', ('name', 'ilike', '비전공자를 위한 이해할 수 있는 IT 지식 - IT시대의 필수 교양서'),
            ('category_id.name', 'ilike', '컴퓨터공학/전산학 개론'),
        ]
        books = self.search(domain)
        print('FIND BOOKS:', books)

    @api.model
    def books_with_multiple_authors(self, all_books):
        def predicate(book):
            if len(book.author_ids) > 1:
                return True
            return False

        return all_books.filter(predicate)
        # or
        # all_books.filter(lambda b: len(b.author_ids) > 1)
        # all_books.filter('author_ids')

    @api.model
    def get_author_names(self, books):
        return books.mapped('author_ids.name')

    @api.model
    def sort_books_by_date(self, books):
        return books.sorted(key='release_date', reverse=True)

    @api.model
    def create(self, values):
        if not self.user_has_groups('my_library.acl_book_librarian'):
            if 'manage_remarks' in values:
                raise UserError('You are not allowed to modify manage_remarks')
        return super(LibraryBook, self).create(values)

    # @api.model
    # def write(self, values):
    #     if not self.user_has_groups('my_library.acl_book_librarian'):
    #         if 'manage_remarks' in values:
    #             raise UserError('You are not allowed to modify manage_remarks')
    #     return super(LibraryBook, self).write(values)

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|',
                     ('name', operator, name),
                     ('isbn', operator, name),
                     ('author_ids.name', operator, name)]
        return super(LibraryBook, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [('cost_price', '!=', False)],      # domain
            ['category_id', 'cost_price:avg'],  # fields to access
            ['category_id']                     # group by
        )
        return grouped_result