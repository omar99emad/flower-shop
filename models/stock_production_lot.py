from odoo import models, fields


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    is_flower = fields.Boolean(related='product_id.is_flower', readonly=True)
    water_ids = fields.One2many("flower.water", "serial_id")

    def action_water_flower(self):
        flowers = self.filtered(lambda rec: rec.is_flower)
    
        for record in flowers:
            if record.water_ids:
                last_watered_date = record.water_ids[0].watering_date
                frequency = record.product_id.flower_id.watering_frequency
                today = fields.Date.today()
                if (today - last_watered_date).days < frequency:
                
                    continue
            self.env["flower.water"].create({
                "flower_id": record.product_id.flower_id.id,
                "watering_date" :fields.Date.today(),
                "serial_id": record.id,
            })



    def action_open_watering_times(self):
        self.ensure_one()
        action = {
            'name': 'Watering Times',
            'type': 'ir.actions.act_window',
            'res_model': 'flower.water',
            'view_mode': 'tree,form',
           'domain': [('serial_id', '=', self.id)],
        }
        return action
