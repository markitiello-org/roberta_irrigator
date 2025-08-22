from flask import Flask, jsonify, request, Blueprint
from backend.datatype.Zone import Zone
from backend.web_service.model.zone_web import ZoneWeb
from backend.datatype.IrrigationInfo import IrrigationInfo
from datetime import datetime
import rpyc
import json

app = Flask(__name__)

zones = Blueprint("zones", __name__, url_prefix="/zones")


@app.route("/zones")
def get_zones():
    c = rpyc.connect("localhost", 18871, config={"allow_public_attrs": True})
    zones = c.root.GetIrrigators()
    print(zones)
    zone_web_list = list()
    irrigation_info_list = list()
    for zone in zones:
        irrigation_info_list = list()
        if len(zone.irrigation_info) == 0:
            print("NO ZONE")
        for timing in zone.irrigation_info:
            print(type(timing.time_to_start))
            print(type(timing.day_of_the_week))
            irrigation_info_list.append(
                IrrigationInfo(
                    timing.time_to_start,
                    int(timing.for_how_many_seconds),
                    list(timing.day_of_the_week),
                )
            )
        zone_web_list.append(
            ZoneWeb(
                zone.name,
                zone.id,
                zone.IsOpen(),
                zone.IsOverride(),
                # zone.irrigation_info,
                irrigation_info_list,
            )
        )
    print("OK")
    print([s.serialize() for s in zone_web_list])
    return [s.serialize() for s in zone_web_list]


@app.route("/zones/<zone_id>/open", methods=["POST"])
def open_zone(zone_id):
    c = rpyc.connect("localhost", 18871, config={"allow_public_attrs": True})
    c.root.OpenZone(int(zone_id))
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/zones/<zone_id>")
def info_zone(zone_id):
    c = rpyc.connect("localhost", 18871, config={"allow_public_attrs": True})
    zone = c.root.GetZoneInfo(int(zone_id))
    zone_web= ZoneWeb(zone.name, zone.id, zone.IsOpen(), False, zone.irrigation_info, zone.GetLastIrrigationDate().strftime("%d-%m-%Y %H:%M:%S"))
    return json.dumps(zone_web.serialize(),indent=2), 200, {"ContentType": "application/json"}


@app.route("/zones/<zone_id>/close", methods=["POST"])
def close_zone(zone_id):
    c = rpyc.connect("localhost", 18871, config={"allow_public_attrs": True})
    c.root.CloseZone(int(zone_id))
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/logs")
def get_logs():
    c = rpyc.connect("localhost", 18871, config={"allow_public_attrs": True})
    logs_list = c.root.GetLogs()
    return [s.serialize() for s in logs_list]


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


app.register_blueprint(zones)

if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
# app.run()
