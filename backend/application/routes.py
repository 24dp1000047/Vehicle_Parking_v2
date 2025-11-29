from flask import current_app as app, jsonify, request, abort, Response
from .models import User, ParkingLot, ParkingSpot, Reservation
from .database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime
import pytz
from sqlalchemy import or_
from flask_caching import Cache
from app import cache
# from application.tasks import export_csv  # <-- Remove or comment this line

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user = User.query.filter_by(email=get_jwt_identity()).first()
            if not user or user.role != required_role:
                return jsonify(msg="Forbidden"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def format_datetime(dt):
    if not dt:
        return None
    return dt.strftime('%d/%m/%Y, %I:%M:%S %p')

def to_india_time(dt):
    if not dt:
        return None
    india = pytz.timezone('Asia/Kolkata')
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(india).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not user.password == password:
        return jsonify({"msg": "Invalid credentials"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, role=user.role), 200

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    fullname = data.get('fullname')
    address = data.get('address')
    pin_code = data.get('pin_code')
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 409
    new_user = User(email=email, password=password, fullname=fullname, address=address, pin_code=pin_code, role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Registration successful"}), 201


@app.route('/api/admin/lots', methods=['GET'])
@role_required('admin')
@cache.cached(timeout=60, query_string=True)  # <-- ENABLED
def get_parking_lots():
    location = request.args.get('location')
    user_id = request.args.get('user_id')
    spot_status = request.args.get('spot_status')  # NEW

    if location:
        lots = ParkingLot.query.filter(
            or_(
                ParkingLot.address.ilike(f'%{location}%'),
                ParkingLot.prime_location_name.ilike(f'%{location}%'),
                ParkingLot.pin_code.ilike(f'%{location}%')
            )
        ).all()
    elif user_id:
        # Find all lot_ids where this user has an active reservation ordered by spot status
        reservations = Reservation.query.filter_by(user_id=user_id, status='active').all()
        lot_ids = set()
        for r in reservations:
            spot = ParkingSpot.query.get(r.spot_id)
            if spot:
                lot_ids.add(spot.lot_id)
        lots = ParkingLot.query.filter(ParkingLot.id.in_(lot_ids)).all()
    else:
        lots = ParkingLot.query.all()

    result = []
    for lot in lots:
        spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        if spot_status in ['A', 'O']:
            spots = [s for s in spots if s.status == spot_status]
        occupied = sum(1 for s in spots if s.status == 'O')
        result.append({
            "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "price": lot.price,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "maximum_number_of_spots": lot.maximum_number_of_spots,
            "description": lot.description,
            "occupied_spots": occupied,
            "spots": [{"id": s.id, "spot_number": s.spot_number, "status": s.status} for s in spots]
        })
    return jsonify(result)

@app.route('/api/admin/lots', methods=['POST'])
@role_required('admin')
def add_parking_lot():
    data = request.json
    lot = ParkingLot(
        prime_location_name=data['prime_location_name'],
        price=data['price'],
        address=data['address'],
        pin_code=data['pin_code'],
        maximum_number_of_spots=data['maximum_number_of_spots'],
        description=data.get('description', '')
    )
    db.session.add(lot)
    db.session.commit()
    for i in range(int(lot.maximum_number_of_spots)):
        spot = ParkingSpot(lot_id=lot.id, spot_number=i+1, status='A')
        db.session.add(spot)
    db.session.commit()
    
    # Invalidate cache
    cache.delete_memoized(get_parking_lots)
    cache.delete_memoized(user_get_parking_lots)
    
    return jsonify({"msg": "Parking lot created"}), 201

@app.route('/api/admin/lots/<int:lot_id>', methods=['PUT'])
@role_required('admin')
def edit_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.json
    old_max = lot.maximum_number_of_spots
    lot.prime_location_name = data['prime_location_name']
    lot.price = data['price']
    lot.address = data['address']
    lot.pin_code = data['pin_code']
    lot.maximum_number_of_spots = data['maximum_number_of_spots']
    db.session.commit()
    new_max = int(lot.maximum_number_of_spots)
    if new_max > old_max:
        for i in range(old_max+1, new_max+1):
            spot = ParkingSpot(lot_id=lot.id, spot_number=i, status='A')
            db.session.add(spot)
        db.session.commit()
    elif new_max < old_max:
        extra_spots = ParkingSpot.query.filter(ParkingSpot.lot_id==lot.id, ParkingSpot.spot_number.in_(range(new_max+1, old_max+1))).all()
        if all(s.status == 'A' for s in extra_spots):
            for s in extra_spots:
                db.session.delete(s)
            db.session.commit()
        else:
            return jsonify({"msg": "Cannot reduce spots. Some are occupied."}), 400
    
    # Invalidate cache
    cache.delete_memoized(get_parking_lots)
    cache.delete_memoized(user_get_parking_lots)
    
    return jsonify({"msg": "Paking lot update successful"}), 200

@app.route('/api/admin/lots/<int:lot_id>', methods=['DELETE'])
@role_required('admin')
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
    if any(s.status == 'O' for s in spots):
        return jsonify({"msg": "Cannot delete lot with occupied spots"}), 400
    ParkingSpot.query.filter_by(lot_id=lot.id).delete()
    db.session.delete(lot)
    db.session.commit()
    
    # Invalidate cache
    cache.delete_memoized(get_parking_lots)
    cache.delete_memoized(user_get_parking_lots)
    
    return jsonify({"msg": "Parking lot deleted"}), 200

@app.route('/api/admin/spots/<int:spot_id>', methods=['GET'])
@role_required('admin')
def get_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)

    reservation = Reservation.query.filter_by(spot_id=spot.id, status='active').order_by(Reservation.start_time.desc()).first()
    reservation_data = None
    if reservation:
        user = User.query.get(reservation.user_id)
        reservation_data = {
            "id": reservation.id,
            "user_id": user.id if user else None,
            "user_email": user.email if user else "",
            "vehicle_number": reservation.vehicle_number,
            "start_time": format_datetime(reservation.start_time),
            "parking_cost_per_unit": reservation.parking_cost_per_unit,
            "status": reservation.status
        }
    return jsonify({
        "spot": {
            "id": spot.id,
            "lot_id": spot.lot_id,
            "spot_number": spot.spot_number,
            "status": spot.status
        },
        "reservation": reservation_data
    })

@app.route('/api/admin/spots/<int:spot_id>', methods=['DELETE'])
@role_required('admin')
def delete_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status == 'O':
        return jsonify({"msg": "Can't delete occupied spot"}), 400
    db.session.delete(spot)
    db.session.commit()
    return jsonify({"msg": "Spot deleted"}), 200



@app.route('/api/admin/users', methods=['GET'])
@role_required('admin')
def get_users():
    query = request.args.get('query')
    q = User.query.filter(User.role != 'admin')
    if query:
        q = q.filter(
            or_(
                User.fullname.ilike(f'%{query}%'),
                User.email.ilike(f'%{query}%')
            )
        )
    users = q.all()
    return jsonify([
        {
            "id": u.id,
            "email": u.email,
            "fullname": u.fullname,
            "address": u.address,
            "pin_code": u.pin_code
        } for u in users
    ])

@app.route('/api/admin/user/<int:user_id>/active-reservations')
@role_required('admin')
def admin_user_active_reservations(user_id):
    reservations = Reservation.query.filter_by(user_id=user_id, status='active').all()
    result = []
    for r in reservations:
        spot = ParkingSpot.query.get(r.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        result.append({
            "id": r.id,
            "vehicle_number": r.vehicle_number,
            "start_time": format_datetime(r.start_time),
            "parking_cost_per_unit": r.parking_cost_per_unit,
            "status": r.status,
            "spot_number": spot.spot_number if spot else '',
            "lot_name": lot.prime_location_name if lot else ''
        })
    return jsonify(result)

# --- Admin: Summary ---

@app.route('/api/admin/summary', methods=['GET'])
@role_required('admin')
def admin_summary():
    reservations = Reservation.query.order_by(Reservation.start_time.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "user_id": r.user_id,
            "spot_id": r.spot_id,
            "spot_id": r.spot_id,
            "start_time": format_datetime(r.start_time),
            "end_time": format_datetime(r.end_time),
            "parking_cost_per_unit": r.parking_cost_per_unit,
            "status": r.status
        } for r in reservations
    ])


@app.route('/api/user/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    history = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.start_time.desc()).limit(10).all()
    result = []
    for r in history:
        spot = ParkingSpot.query.get(r.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        
        # Debug logging
        location_value = ""
        if lot:
            location_value = lot.prime_location_name or "No Name Set"
        else:
            location_value = "Lot Not Found"
        
        print(f"DEBUG - Reservation {r.id}: spot={r.spot_id}, lot_id={spot.lot_id if spot else 'N/A'}, location='{location_value}'")
        
        result.append({
            "id": r.id,
            "spot_id": r.spot_id,
            "start_time": format_datetime(r.start_time),
            "start_time_iso": r.start_time.replace(tzinfo=pytz.timezone('Asia/Kolkata')).isoformat() if r.start_time else None,
            "end_time": format_datetime(r.end_time),
            "vehicle_number": r.vehicle_number,
            "status": r.status,
            "location": location_value,
            "address": lot.address if lot else "",
            "parking_cost_per_unit": r.parking_cost_per_unit
        })
    return jsonify(result)

@app.route('/api/user/book/<int:lot_id>', methods=['POST'])
@jwt_required()
def book_spot(lot_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    data = request.json
    vehicle_number = data.get('vehicle_number')
    if not vehicle_number:
        return jsonify({'msg': 'Vehicle number required'}), 400

    # Find an available spot
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({'msg': 'No available spots'}), 400

    # Mark spot as occupied
    spot.status = 'O'
    india = pytz.timezone('Asia/Kolkata')
    now = datetime.now(india)

    # Get parking cost from lot, or set a default value
    lot = ParkingLot.query.get(lot_id)
    parking_cost = lot.price if lot and lot.price else 0.0

    reservation = Reservation(
        user_id=user.id,
        spot_id=spot.id,
        vehicle_number=vehicle_number,
        start_time=now,
        parking_cost_per_unit=parking_cost,  # <-- FIXED: set required field
        status='active'
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'msg': 'Spot booked', 'reservation_id': reservation.id})

@app.route('/api/user/release/<int:reservation_id>', methods=['POST'])
@jwt_required()
def release_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    spot = ParkingSpot.query.get_or_404(reservation.spot_id)
    spot.status = 'A'
    reservation.status = 'completed'
    reservation.end_time = datetime.now()
    
    # Calculate Cost
    duration = reservation.end_time - reservation.start_time
    hours = duration.total_seconds() / 3600
    # Minimum 1 hour charge
    # Exact cost calculation
    hours = duration.total_seconds() / 3600
    # Round to 2 decimal places for currency
    total_cost = round(hours * reservation.parking_cost_per_unit, 2)
    
    # We don't have a total_cost column in Reservation model yet? 
    # The model has parking_cost_per_unit. 
    # We might need to add a total_cost field or just calculate it on the fly.
    # For now, let's just return it.
    
    db.session.commit()
    return jsonify({"msg": "Spot released", "total_cost": total_cost}), 200

@app.route('/api/analytics', methods=['GET'])
@role_required('admin')
def get_analytics():
    total_reservations = Reservation.query.count()
    active_reservations = Reservation.query.filter_by(status='active').count()
    completed_reservations = Reservation.query.filter_by(status='completed').count()
    
    # Revenue (Mock calculation if we don't store total cost)
    # Assuming completed reservations average 2 hours for estimation if not stored
    # Ideally we should store total_cost in DB.
    # For this milestone, let's just count.
    
    return jsonify({
        "total_reservations": total_reservations,
        "active_reservations": active_reservations,
        "completed_reservations": completed_reservations
    })

@app.route('/api/export/csv', methods=['POST'])
@jwt_required()
def trigger_export_csv():
    user_email = get_jwt_identity()
    export_csv.delay(user_email)
    return jsonify({"msg": "CSV export started. You will be notified."}), 202


@app.route('/api/user/summary', methods=['GET'])
@jwt_required()
def user_summary():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    used_spots = Reservation.query.filter_by(user_id=user.id, status='completed').count()
    active_spots = Reservation.query.filter_by(user_id=user.id, status='active').count()
    return jsonify({"used_spots": used_spots, "active_spots": active_spots})

@app.route('/api/user/lots', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, query_string=True)  # <-- ENABLED
def user_get_parking_lots():
    # Updated to include price field - FORCE RELOAD 2025-11-29 14:40
    location = request.args.get('location', '').strip()
    query = ParkingLot.query
    if location:
        query = query.filter(
            (ParkingLot.prime_location_name.ilike(f'%{location}%')) |
            (ParkingLot.address.ilike(f'%{location}%')) |
            (ParkingLot.pin_code.ilike(f'%{location}%'))
        )
    lots = query.all()
    result = []
    for lot in lots:
        # Count occupied spots for this lot
        occupied_spots = (
            db.session.query(ParkingSpot)
            .join(Reservation, Reservation.spot_id == ParkingSpot.id)
            .filter(
                ParkingSpot.lot_id == lot.id,
                Reservation.status == 'active'
            )
            .count()
        )
        result.append({
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'address': lot.address,
            'maximum_number_of_spots': lot.maximum_number_of_spots,
            'occupied_spots': occupied_spots,
            'description': lot.description,
            'pin_code': lot.pin_code,
            'price': lot.price,
        })
    return jsonify(result)

@app.route('/api/user/export/csv', methods=['GET'])
@jwt_required()
def user_export_csv():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    reservations = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.start_time.desc()).all()
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Reservation ID', 'Spot ID', 'Lot Name', 'Start Time', 'End Time', 'Cost', 'Status', 'Remarks'])
    for r in reservations:
        spot = ParkingSpot.query.get(r.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        cw.writerow([
            r.id,
            r.spot_id,
            lot.prime_location_name if lot else '',
            r.start_time,
            r.end_time,
            r.parking_cost_per_unit,
            r.status,
            getattr(r, 'remarks', '')
        ])
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=parking_report.csv"}
    )

