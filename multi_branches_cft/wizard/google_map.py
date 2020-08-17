from odoo import api, fields, models

class Config(models.TransientModel):
    _name = 'gmap.config'
    _description = 'Google Map Configuration'

    @api.model
    def get_key_api(self):
        return self.env['ir.config_parameter'].sudo().get_param('google_maps_api_key')