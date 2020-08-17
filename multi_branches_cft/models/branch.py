import base64
import os
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError


class OperatingBranch(models.Model):
    _name = 'operating.branch'
    _description = 'Operating Branch'

    def _get_logo(self):
        return base64.b64encode(
            open(os.path.join(tools.config['root_path'], 'addons', 'base', 'static', 'img', 'res_company_logo.png'),
                 'rb').read())

    @api.model
    def _get_user_currency(self):
        return self.env.company.currency_id

    name = fields.Char(string="Name")
    parent_id = fields.Many2one('operating.branch', string='Parent branch', index=True)
    child_ids = fields.One2many('operating.branch', 'parent_id', string='Child Companies')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    logo = fields.Binary(related='partner_id.image_1920', default=_get_logo, string="branch Logo", readonly=False)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self._get_user_currency())
    account_no = fields.Char(string='Account No.')
    street = fields.Char(compute='_compute_address', inverse='_inverse_street')
    street2 = fields.Char(compute='_compute_address', inverse='_inverse_street2')
    zip = fields.Char(compute='_compute_address', inverse='_inverse_zip')
    city = fields.Char(compute='_compute_address', inverse='_inverse_city')
    state_id = fields.Many2one('res.country.state', compute='_compute_address', inverse='_inverse_state', string="Fed. State")
    country_id = fields.Many2one('res.country', compute='_compute_address', inverse='_inverse_country', string="Country")
    email = fields.Char(related='partner_id.email', store=True, readonly=False)
    phone = fields.Char(related='partner_id.phone', store=True, readonly=False)
    website = fields.Char(related='partner_id.website', readonly=False)
    vat = fields.Char(related='partner_id.vat', string="Tax ID", readonly=False)
    location = fields.Char()
    branch_head_user_id = fields.Many2one('res.users', string='Branch Head')
    company_id = fields.Many2one('res.company',string='Company')
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The branch name must be unique !')
    ]

    def _get_branch_address_fields(self, partner):
        return {
            'street'     : partner.street,
            'street2'    : partner.street2,
            'city'       : partner.city,
            'zip'        : partner.zip,
            'state_id'   : partner.state_id,
            'country_id' : partner.country_id,
        }

    def _compute_address(self):
        for branch in self.filtered(lambda branch: branch.partner_id):
            address_data = branch.partner_id.sudo().address_get(adr_pref=['contact'])
            if address_data['contact']:
                partner = branch.partner_id.browse(address_data['contact']).sudo()
                branch.update(branch._get_branch_address_fields(partner))

    def _inverse_street(self):
        for branch in self:
            branch.partner_id.street = branch.street

    def _inverse_street2(self):
        for branch in self:
            branch.partner_id.street2 = branch.street2

    def _inverse_zip(self):
        for branch in self:
            branch.partner_id.zip = branch.zip

    def _inverse_city(self):
        for branch in self:
            branch.partner_id.city = branch.city

    def _inverse_state(self):
        for branch in self:
            branch.partner_id.state_id = branch.state_id

    def _inverse_country(self):
        for branch in self:
            branch.partner_id.country_id = branch.country_id

    @api.depends('partner_id', 'partner_id.image_1920')
    def _compute_logo_web(self):
        for branch in self:
            branch.logo_web = tools.image_resize_image(branch.partner_id.image_1920, (180, None))

    @api.onchange('state_id')
    def _onchange_state(self):
        self.country_id = self.state_id.country_id

    
    def on_change_country(self, country_id):
        self.ensure_one()
        currency_id = self._get_user_currency()
        if country_id:
            currency_id = self.env['res.country'].browse(country_id).currency_id
        return {'value': {'currency_id': currency_id.id}}

    @api.onchange('country_id')
    def _onchange_country_id_wrapper(self):
        res = {'domain': {'state_id': []}}
        if self.country_id:
            res['domain']['state_id'] = [('country_id', '=', self.country_id.id)]
        values = self.on_change_country(self.country_id.id)['value']
        for fname, value in values.items():
            setattr(self, fname, value)
        return res

    @api.model
    @tools.ormcache('self.env.uid', 'branch')
    def _get_branch_children(self, branch=None):
        if not branch:
            return []
        return self.search([('parent_id', 'child_of', [branch])]).ids

    
    def _get_partner_hierarchy(self):
        self.ensure_one()
        parent = self.parent_id
        if parent:
            return parent._get_partner_hierarchy()
        else:
            return self._get_partner_descendance([])

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('partner_id'):
            return super(OperatingBranch, self).create(vals)
        partner = self.env['res.partner'].create({
            'name': vals['name'],
            'image_1920': vals.get('logo'),
            'email': vals.get('email'),
            'phone': vals.get('phone'),
            'website': vals.get('website'),
            'vat': vals.get('vat'),
        })
        vals['partner_id'] = partner.id
        branch = super(OperatingBranch, self).create(vals)
        partner.write({'operating_branch_id': branch.id})

        # Make sure that the selected currency is enabled
        if vals.get('currency_id'):
            currency = self.env['res.currency'].browse(vals['currency_id'])
            if not currency.active:
                currency.write({'active': True})
        return branch

    
    def write(self, values):
        # Make sure that the selected currency is enabled
        if values.get('currency_id'):
            currency = self.env['res.currency'].browse(values['currency_id'])
            if not currency.active:
                currency.write({'active': True})

        return super(OperatingBranch, self).write(values)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive Branches.'))

    @api.model
    def _get_main_branch(self):
        try:
            main_branch = self.sudo().env.ref('multi_branches_cft.main_branch')
        except ValueError:
            main_branch = self.env['res.branch'].sudo().search([], limit=1, order="id")

        return main_branch
