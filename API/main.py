import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/add', methods=['POST'])
def add_car():
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		_json = request.json
		_destination = _json['destination']
		_schedule = _json['schedule']
		_position = _json['position']

		# validate the received values
		if _destination and _schedule and _position and request.method == 'POST':
			# save edits
			sql = "INSERT INTO tbl_car(car_destination, car_schedule, car_position) VALUES(%s, %s, %s)"
			data = (_destination, _schedule, _position,)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Car added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/cars')
def cars():
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	try:
		cursor.execute("SELECT car_id id, car_destination destination, car_schedule schedule, car_position position FROM tbl_car")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/car/<int:id>')
def car(id):
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	try:
		cursor.execute("SELECT car_id id, car_destination destination, car_schedule schedule, car_position position FROM tbl_carr WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update', methods=['PUT'])
def update_car():
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		_json = request.json
		_id = _json['id']
		_destination = _json['destination']
		_schedule = _json['schedule']
		_position = _json['position']		

		# validate the received values
		if _destination and _schedule and _position and _id and request.method == 'PUT':
			# save edits
			sql = "UPDATE tbl_car SET car_destination=%s, car_schedule=%s, car_position=%s WHERE car_id=%s"
			data = (_destination, _schedule, _position, _id,)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Car updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_car(id):
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		cursor.execute("DELETE FROM tbl_car WHERE car_id=%s", (id,))
		conn.commit()
		resp = jsonify('Car deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run()
