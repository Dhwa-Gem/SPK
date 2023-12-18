from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import Kamera as KameraModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'harga': 4, 'resolusi_sensor': 3, 'rentang_iso': 4, 'kecepatan_rana': 6, 'jumlah_fStop': 3}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(KameraModel.id_kamera, KameraModel.harga, KameraModel.resolusi_sensor, KameraModel.rentang_iso, KameraModel.kecepatan_rana, KameraModel.jumlah_fStop)
        result = session.execute(query).fetchall()
        print(result)
        return [{'id_kamera': kamera.id_kamera, 'harga': kamera.harga, 'resolusi_sensor': kamera.resolusi_sensor, 'rentang_iso': kamera.rentang_iso, 'kecepatan_rana': kamera.kecepatan_rana, 'jumlah_fStop': kamera.jumlah_fStop} for kamera in result]

    @property
    def normalized_data(self):
        harga_values = []
        resolusi_sensor_values = []
        rentang_iso_values = []
        kecepatan_rana_values = []
        jumlah_fStop_values = []

        for data in self.data:
            harga_values.append(data['harga'])
            resolusi_sensor_values.append(data['resolusi_sensor'])
            rentang_iso_values.append(data['rentang_iso'])
            kecepatan_rana_values.append(data['kecepatan_rana'])
            jumlah_fStop_values.append(data['jumlah_fStop'])

        return [
            {'id_kamera': data['id_kamera'],
             'harga': min(harga_values) / data['harga'],
             'resolusi_sensor': data['resolusi_sensor'] / max(resolusi_sensor_values),
             'rentang_iso': data['rentang_iso'] / max(rentang_iso_values),
             'kecepatan_rana': data['kecepatan_rana'] / max(kecepatan_rana_values),
             'jumlah_fStop': data['jumlah_fStop'] / max(jumlah_fStop_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
                row['harga'] ** self.raw_weight['harga'] *
                row['resolusi_sensor'] ** self.raw_weight['resolusi_sensor'] *
                row['rentang_iso'] ** self.raw_weight['rentang_iso'] *
                row['kecepatan_rana'] ** self.raw_weight['kecepatan_rana'] *
                row['jumlah_fStop'] ** self.raw_weight['jumlah_fStop']
            )

            produk.append({
                'id_kamera': row['id_kamera'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'id_kamera': product['id_kamera'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id_kamera']:
                  round(row['harga'] * weight['harga'] +
                        row['resolusi_sensor'] * weight['resolusi_sensor'] +
                        row['rentang_iso'] * weight['rentang_iso'] +
                        row['kecepatan_rana'] * weight['kecepatan_rana'] +
                        row['jumlah_fStop'] * weight['jumlah_fStop'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class Kamera(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(KameraModel)
        data = [{'id_kamera': kamera.id_kamera, 'harga': kamera.harga, 'resolusi_sensor': kamera.resolusi_sensor, 'rentang_iso': kamera.rentang_iso, 'kecepatan_rana': kamera.kecepatan_rana, 'jumlah_fStop': kamera.jumlah_fStop} for kamera in session.scalars(query)]
        return self.get_paginated_result('kamera/', data, request.args), HTTPStatus.OK.value


api.add_resource(Kamera, '/kamera')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)