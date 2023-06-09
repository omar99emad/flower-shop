from odoo import models, fields

class Product(models.Model):
    _inherit = "product.product"

    is_flower = fields.Boolean(string="Is Flower Product?")
    flower_id = fields.Many2one("flower.flower")
