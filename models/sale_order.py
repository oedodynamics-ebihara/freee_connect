# -*- coding: utf-8 -*-
from odoo import models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_inspection(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('確認'),
                'message': _('点検中'),
                'type': 'warning',
                'sticky': False,
            }
        }
