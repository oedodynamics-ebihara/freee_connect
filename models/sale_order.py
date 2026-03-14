# -*- coding: utf-8 -*-
import requests
from odoo import models, _, exceptions
from datetime import datetime
import json

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_connection_test(self):
        self.ensure_one()
        
        # Get configuration parameters
        api_key = self.env['ir.config_parameter'].sudo().get_param('freee_connect.api_key')
        company_id = self.env['ir.config_parameter'].sudo().get_param('freee_connect.company_id')

        if not api_key or not company_id:
            raise exceptions.UserError(_("Freee API Key or Company ID is not configured. Please check Sales settings."))

        # 連携先 Freee Invoice API (Quotation/見積書は見積書用のエンドポイントを使用します)
        # 請求書の場合: /iv/invoices
        # 見積書の場合: /iv/quotations
        url = "https://api.freee.co.jp/iv/quotations"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        today_str = datetime.now().strftime("%Y-%m-%d")

        partner_id = 110536486  # ハードコードされたテスト用取引先ID
        
        # 見積書のペイロード作成 (freee見積書API /iv/quotations)
        payload = {
            "company_id": int(company_id),
            "partner_id": partner_id,
            "partner_title": "御中",
            "issue_date": today_str,
            "tax_entry_method": "out",
            "tax_fraction": "omit",
            "withholding_tax_entry_method": "in",
            "subject": self.name + " (テスト連携)",
            "lines": [
                {
                    "type": "item",
                    "quantity": 1,
                    "unit": "式",
                    "unit_price": str(int(self.amount_total)) if self.amount_total else "50000",
                    "description": "システムのテスト・連携構築",
                    "tax_rate": 10
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            created_data = response.json()
            quotation_info = created_data.get('quotation', created_data)
            quotation_id = quotation_info.get('id')
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('見積書作成成功'),
                    'message': _(f'Freeeで見積書 (ID: {quotation_id}) を作成しました。'),
                    'type': 'success',
                    'sticky': False,
                }
            }

        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            try:
                error_response = response.json()
                if isinstance(error_response, dict):
                    error_msg += f"\n\n詳細: {json.dumps(error_response, ensure_ascii=False, indent=2)}"
            except Exception:
                pass

            raise exceptions.UserError(_('API Request Error:\n%s') % error_msg)
        except Exception as e:
            raise exceptions.UserError(_('Unexpected Error:\n%s') % str(e))
