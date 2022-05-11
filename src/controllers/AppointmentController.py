from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import common_bp
from src.models.RoasterModel import RoasterModel
from src.models.AppointmentModel import AppointmentModel
import datetime


@common_bp.route('/get_appointments', methods=['GET'])
@Authentication.decode_auth_token
def get_appointments():
    try:
        id = request.args.get('id', '')
        requester = request.args.get('requester', '')
        appointer = request.args.get('appointer', '')
        date = request.args.get('date', '')
        day = request.args.get('day', '')
        status = request.args.get('status', '')
        date = datetime.datetime.strptime(date, "%d-%m-%Y") if date else date
        appointment_data = AppointmentModel.get_appointment(id=id, requester=requester, appointer=appointer, date=date,
                                                     day=day, status=status)

        if appointment_data:
            data = []
            for app_data in appointment_data:
                each = {
                    'id': app_data.id,
                    'req_id': app_data.requester,
                    'req_name': app_data.requestor_name,
                    'appointer_id': app_data.appointer,
                    'appointer_name': app_data.appointer_name,
                    'date': app_data.date,
                    'day': app_data.day,
                    'start_time': app_data.start_time.strftime("%H:%M"),
                    'end_time': app_data.end_time.strftime("%H:%M"),
                    'status': app_data.status
                }
                data.append(each)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.medicine_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@common_bp.route('/delete_appointment', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_appointment():
    try:
        id = request.args.get('id')
        AppointmentModel.delete_by_id(id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@common_bp.route('/set_appointment', methods=['POST'])
@Authentication.decode_auth_token
def set_appointment():
    try:
        id = request.form.get("id", None)
        requester = request.form['requester']
        appointer = request.form['appointer']
        str_date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        avoid_clash = request.form.get('avoid_clash', '0')
        date = datetime.datetime.strptime(str_date, "%d-%m-%Y")
        day = date.strftime("%A")
        start_time = datetime.datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_time, "%H:%M").time()
        check_self_clash = verify_clash(id, requester, date, day, start_time, end_time, type='requestor')
        if check_self_clash and (avoid_clash == '0' or verify_clash(id, appointer, date, day, start_time, end_time, type='appointer')):
            if id:
                data_to_update = {
                    'requester': requester,
                    'appointer': appointer,
                    'date': date,
                    'day': day,
                    'start_time': start_time,
                    'end_time': end_time,
                    'status': 'pending'
                }
                AppointmentModel.update_by_id(id, data_to_update)
            else:
                appointment = AppointmentModel(requester, appointer, date, day, start_time, end_time)
                appointment.save()
                id = appointment.id
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='appointment_id',
                                            data=id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.appointment_not_found.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


def verify_clash(app_id, user_id, date, day, start_time, end_time, type='requestor'):
    verify = True
    roaster = RoasterModel.get_roaster(user_id)
    if roaster:
        available_days = roaster.days.lower().split(',')
        if day.lower() in available_days:
            roaster_start = roaster.start_time
            roaster_end = roaster.end_time
            if not (start_time <= roaster_end and start_time >= roaster_start) and \
                (end_time <= roaster_end and end_time >= roaster_start):
                verify = False
        else:
            verify = False
    if verify:
        requestor = user_id if type == 'requestor' else None
        appointer = user_id if type != 'requestor' else None
        scheduled_appointments = AppointmentModel.get_appointment(id=app_id, requester=requestor, appointer= appointer,
                                                                  date=date)
        if scheduled_appointments:
            for each in scheduled_appointments:
                app_start = each.start_time
                app_end = each.end_time
                if (start_time >= app_start and start_time < app_end) or \
                        (end_time > app_start and end_time <= app_end) or \
                        (app_start >= start_time and app_start < end_time) or \
                        (app_end > start_time and app_end <= end_time):
                    verify = False

    return verify