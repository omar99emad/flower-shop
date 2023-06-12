from odoo import models, fields, api
from datetime import date, datetime, time
from collections import defaultdict


class Product(models.Model):
    _inherit = "product.product"

    is_flower = fields.Boolean(string="Is Flower Product?")
    flower_id = fields.Many2one("flower.flower")
    sequence_id = fields.Many2one("ir.sequence", "Flower Sequence")
    needs_watering = fields.Boolean(string="Needs Watering")
    gardeners = fields.Many2many('res.users', string='Assigned Gardeners', relation='product_product_gardener_rel', column1='product_id', column2='user_id',
                                 domain=lambda self: [('groups_id', 'in', self.env.ref('flower_shop.group_gardeners').id)])
    





    def action_needs_watering(self):
        flowers = self.search([("is_flower", "=", True)])
        serials = self.env["stock.production.lot"].search([("product_id", "in", flowers.ids)])
        product_vals = defaultdict(bool)
        
        today = date.today()
        
        for serial in serials:
            if serial.water_ids:
                last_watered_date = serial.water_ids[0].watering_date
                frequency = serial.product_id.flower_id.watering_frequency
                needs_watering = (today - last_watered_date).days >= frequency
                product_vals[serial.product_id.id] |= needs_watering
            else:
                product_vals[serial.product_id.id] = True
        
        for flower in flowers:
            flower.needs_watering = product_vals[flower.id]
