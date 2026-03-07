# -*- coding: utf-8 -*-
from odoo import models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_connection_test(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('テスト実行'),
                'message': _('テスト中'),
                'type': 'info',
                'sticky': False,
            }
        }
