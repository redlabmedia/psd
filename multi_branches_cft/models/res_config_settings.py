# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    multi_branch = fields.Boolean(string='Multi Branch?')
    group_multi_branch = fields.Boolean('Multi Branch', implied_group='multi_branches_cft.group_multi_branch',
        help="Store products in specific Branch of your company.")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            multi_branch=self.env.user.company_id.multi_branch
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        company_id=self.env.user.company_id
        company_id.multi_branch = self.multi_branch


