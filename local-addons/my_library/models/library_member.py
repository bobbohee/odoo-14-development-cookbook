# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryMember(models.Model):
    # 위임 상속
    # ex) res.users 에 partner_id
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Library Member'

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    # inherits 대신 delegate 사용 시, 동일하게 동작 -> delegate=True
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
