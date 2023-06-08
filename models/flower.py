from odoo import models, fields
class AModel(models.Model):
    _name = 'flower.flower'

    name = fields.Char("Common Name")
    scientific_name = fields.Char("Scientific Name")
    season_start = fields.Date("Season Start Date")
    season_end = fields.Date("Season End Date")
    watering_frequency = fields.Integer(help="Frequency is in number of days")
    watering_amount = fields.Float("watering Amount(ml)")
 