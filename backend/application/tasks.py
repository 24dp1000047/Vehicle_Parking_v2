from app import celery, mail, app
from application.models import User, Reservation, ParkingLot
from datetime import datetime, timedelta
import pytz
from flask_mail import Message
from sqlalchemy import func
import logging

@celery.task
def send_daily_reminders():
    india = pytz.timezone('Asia/Kolkata')
    today = datetime.now(india).date()
    users = User.query.filter(User.role != 'admin').all()
    reminded = 0
    with app.app_context():
        for user in users:
            reservation_today = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.start_time >= datetime.combine(today, datetime.min.time()),
                Reservation.start_time <= datetime.combine(today, datetime.max.time()),
                Reservation.status == 'active'
            ).first()
            if not reservation_today:
                try:
                    msg = Message(
                        subject="Parking Reminder",
                        sender="sharma001prateek@gmail.com",  # must match MAIL_USERNAME
                        recipients=[user.email],
                        body="You have not booked a parking spot today. Please book if needed!"
                    )
                    mail.send(msg)
                    print(f"Sent reminder email to {user.email}")
                    reminded += 1
                except Exception as e:
                    logging.error(f"Failed to send email to {user.email}: {e}")
    return f"Daily reminders sent to {reminded} users"

@celery.task
def send_monthly_reports():
    india = pytz.timezone('Asia/Kolkata')
    today = datetime.now(india)
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

    users = User.query.filter(User.role != 'admin').all()
    with app.app_context():
        for user in users:
            # Reservations for this month
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.start_time >= first_day,
                Reservation.start_time <= last_day
            ).all()
            total_booked = len(reservations)
            total_amount = sum(r.parking_cost_per_unit for r in reservations)
            # Most used lot
            lot_counts = {}
            for r in reservations:
                spot = r.spot
                if spot:
                    lot_id = spot.lot_id
                    lot_counts[lot_id] = lot_counts.get(lot_id, 0) + 1
            most_used_lot = None
            if lot_counts:
                most_lot_id = max(lot_counts, key=lot_counts.get)
                lot = ParkingLot.query.get(most_lot_id)
                most_used_lot = lot.prime_location_name if lot else "N/A"

            # HTML Report
            html = f"""
            <h2>Monthly Parking Activity Report</h2>
            <p>Hello {user.fullname},</p>
            <ul>
                <li><b>Parking spots booked this month:</b> {total_booked}</li>
                <li><b>Most used parking lot:</b> {most_used_lot or "N/A"}</li>
                <li><b>Total amount spent:</b> ₹{total_amount:.2f}</li>
            </ul>
            <h3>Details:</h3>
            <table border="1" cellpadding="4">
                <tr>
                    <th>Date</th>
                    <th>Lot</th>
                    <th>Spot</th>
                    <th>Amount</th>
                </tr>
                {''.join([
                    f"<tr><td>{r.start_time.strftime('%d-%m-%Y')}</td><td>{ParkingLot.query.get(r.spot.lot_id).prime_location_name if r.spot else ''}</td><td>{r.spot.spot_number if r.spot else ''}</td><td>₹{r.parking_cost_per_unit:.2f}</td></tr>"
                    for r in reservations
                ])}
            </table>
            <p>Thank you for using our parking service!</p>
            """

            msg = Message(
                subject="Your Monthly Parking Activity Report",
                sender="noreply@yourapp.com",
                recipients=[user.email],
                html=html
            )
            mail.send(msg)
            print(f"Sent monthly report to {user.email}")

    return "Monthly reports sent"

# Celery Beat schedule (add this to your celery config, e.g. in app.py or a separate celeryconfig.py)
# Example: Run every day at 6:00 PM IST
celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'application.tasks.send_daily_reminders',
        'schedule': 60 * 60 * 24,  # every 24 hours
        'options': {'expires': 60 * 60},
    },
}


