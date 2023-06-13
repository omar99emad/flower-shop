from odoo import models, fields
from odoo.exceptions import UserError
from datetime import datetime

import requests



class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    weather_ids = fields.One2many('stock.warehouse.weather', 'warehouse_id', string='Weather Records')


    def _get_api_key_and_location(self, show_error=True):
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")
    
        if api_key == "unset" or not api_key:
            raise UserError("API key not set. Please configure the weather API key in system parameters.")


        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            print(self.partner_id)
            print(self.partner_id.partner_latitude)
            print(self.partner_id.partner_longitude)
            raise UserError("Warehouse location not defined. Please set the latitude and longitude coordinates for the warehouse's partner.")
        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude



    def fetch_current_weather(self, show_error=True):
        self.ensure_one()
        api_key, lat, lng = self._get_api_key_and_location(show_error)
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lng, api_key)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            entries = response.json()
            self.env["stock.warehouse.weather"].create({
                "warehouse_id": self.id,
                "description": entries["weather"][0]["description"],
                "pressure": entries["main"]["pressure"],
                "temperature": entries["main"]["temp"],
                "humidity": entries["main"]["humidity"] / 100,
                "wind_speed": entries["wind"]["speed"],
                "rain_volume": entries["rain"]["1h"] if "rain" in entries else 0,
                "capture_time": fields.Datetime.now(),
            })
        except requests.exceptions.Timeout:
            # Handle timeout error
            raise UserError("Request timed out. Please check your internet connection or try again later.")

        except requests.exceptions.RequestException as e:
            # Handle other request exceptions
            raise UserError("An error occurred during the request: {}".format(str(e)))

        except KeyError:
            # Handle key error if required data is missing in the response
            raise UserError("Incomplete forecast data. Response format may have changed.")

        except Exception as e:
            # Handle any other unexpected exceptions
            raise UserError("An unexpected error occurred: {}".format(str(e)))



    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.fetch_current_weather(show_error=False)


    def get_forecast_all_warehouses(self, show_error=True):
        Flower = self.env['flower.flower']
        FlowerWater = self.env['flower.water']
        StockQuant = self.env['stock.quant']
        current_user_company_id = self.env.user.company_id.id

        for warehouse in self.search([('company_id', '=', current_user_company_id)]):
            print(self.search([]))
            api_key, lat, lng = warehouse._get_api_key_and_location(show_error)
            url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat, lng, api_key)
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                forecast_data = response.json()

                # Get forecast data between 9 AM to 6 PM for the current day
                current_day_forecast = []
                for entry in forecast_data['list']:
                    dt = entry['dt']
                    dt_time = datetime.fromtimestamp(dt)
                    if dt_time.hour >= 9 and dt_time.hour <= 18:
                        current_day_forecast.append(entry)
                
                # Check rain volume and water flowers if necessary
                watering_needed = False
                for entry in current_day_forecast[:4]:
                    rain_volume = entry.get('rain', {}).get('3h', 0)
                    print(rain_volume)
                    if rain_volume > 0.2:
                        watering_needed = True
                        break
                if watering_needed:
                    flower_stocks = StockQuant.search([
                        ('location_id', '=', warehouse.lot_stock_id.id),
                        ('lot_id', '!=', False),
                        ('product_id.is_flower', '!=', False)])
                    print(flower_stocks)
                    for stock in flower_stocks:
                        flower = Flower.browse(stock.product_id.flower_id.id)
                        print(flower)
                        watering_date = fields.Date.today()
                        FlowerWater.create({
                            'flower_id': flower.id,
                            'watering_date': watering_date,
                            'notes': 'Auto watering due to forecasted rain',
                            'serial_id': stock.lot_id.id
                            })

            except requests.exceptions.Timeout:
                # Handle timeout error
                raise UserError("Request timed out. Please check your internet connection or try again later.")

            except requests.exceptions.RequestException as e:
                # Handle other request exceptions
                raise UserError("An error occurred during the request: {}".format(str(e)))

            except KeyError:
                # Handle key error if required data is missing in the response
                raise UserError("Incomplete forecast data. Response format may have changed.")

            except Exception as e:
                # Handle any other unexpected exceptions
                raise UserError("An unexpected error occurred: {}".format(str(e)))


