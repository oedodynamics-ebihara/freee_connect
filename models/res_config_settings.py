# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    freee_api_key = fields.Char(
        string='Freee API Key',
        config_parameter='freee_connect.api_key',
        help='OAuth2.0 Access Token or API Key for Freee'
    )
    freee_company_id = fields.Char(
        string='Freee Company ID',
        config_parameter='freee_connect.company_id',
        help='Company ID (事業所ID) to use for Freee API'
    )
