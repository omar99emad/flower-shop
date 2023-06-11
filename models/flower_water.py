from odoo import models, fields

class FlowerWater(models.Model):
    _name = "flower.water"
    _description = "Flower Watering"
    _order = "watering_date"
    
    flower_id = fields.Many2one('flower.flower', string='Flower')
    watering_date = fields.Date(string='Watering Date')
    notes = fields.Text(string='Notes')
    serial_id = fields.Many2one("stock.production.lot")

    
