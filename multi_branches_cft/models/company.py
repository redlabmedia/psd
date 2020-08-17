from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    multi_branch = fields.Boolean(string='Multi Branch?')
    

class ResUsers(models.Model):
    _inherit = "res.users"

    def _branches_count(self):
        for user in self:
            user.branches_count = self.env['operating.branch'].sudo().search_count([]) or 0

    
    # def _compute_branches_count(self):
    #     branches_count = self._companies_count()
    #     for user in self:
    #         user.branches_count = branches_count

    

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')
    operating_branch_ids = fields.Many2many('operating.branch', 'company_id', string='Branches')
    branches_count = fields.Integer(string="Branches Count", compute= '_branches_count')

class ProductProduct(models.Model):
    _inherit = "product.product"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')

class SaleOrder(models.Model):
    _inherit = "sale.order"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class AccountInvoice(models.Model):
    _inherit = "account.move"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class StockPicking(models.Model):
    _inherit = "stock.picking"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class ResPartner(models.Model):
    _inherit = "res.partner"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    

class Project(models.Model):
    _inherit = "project.project"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch') 

class Task(models.Model):
    _inherit = "project.task"

    operating_branch_id = fields.Many2one('operating.branch', string='Branch')    