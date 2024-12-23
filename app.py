from flask import Flask, jsonify, request, make_response
from model import Data

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/karyawan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def karyawan():
    try:
        # Panggil class model database
        dt = Data()
        values = ()

        # Jika Method GET
        if request.method == 'GET':
            no_ = request.args.get("no")
            if no_:
                query = "SELECT * FROM data_karyawan where no = %s "
                values = (no_,)
            else:
                query = "SELECT * FROM data_karyawan"
            data = dt.get_data(query, values)

        # Jika Method POST
        elif request.method == 'POST':
            datainput = request.json
            name = datainput['name']
            usia = datainput['usia']
            asal = datainput['asal']
            hobi = datainput['hobi']

            query = "INSERT INTO data_karyawan (name, usia, asal, hobi) values (%s,%s,%s,%s) "
            values = (name, usia, asal, hobi)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'berhasil menambah data'
            }]

        # Jika Method PUT
        elif request.method == 'PUT':
            query = "UPDATE data_karyawan SET no = %s"
            datainput = request.json
            no_ = datainput['no']
            values += (no_,)

            if 'name' in datainput:
                name = datainput['name']
                values += (name, )
                query += ", name = %s"
            if 'usia' in datainput:
                usia = datainput['usia']
                values += (usia, )
                query += ", usia = %s"
            if 'asal' in datainput:
                asal = datainput['asal']
                values += (asal, )
                query += ", asal = %s"
            if 'hobi' in datainput:
                hobi = datainput['hobi']
                values += (hobi, )
                query += ", hobi = %s"

            query += " where no = %s "
            values += (no_,)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'berhasil mengubah data'
            }]

        # Selain itu adalah DELETE, Bila ada method selain keempat ini maka dipastikan akan langsung Eror karena method tidak di assign.
        else:
            query = "DELETE FROM data_karyawan where no = %s "
            no_ = request.args.get("no")
            values = (no_,)
            dt.insert_data(query, values)
            data = [{
        'pesan': 'berhasil menghapus data'
    }]
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)
    return make_response(jsonify({'data': data}), 200)
if __name__ == '__main__':
    app.run()