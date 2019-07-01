#!/usr/bin/env python3

import json

from apps import topo
from apps.ids import get_events, net_history
from flask import Flask, request

from apps.sim import get_host_qos, get_attack_stats
from apps.vtn import get_vn, toggle_vn
from apps.topo import get_arp_table

from config import ALERTS, VNETS

app = Flask("Hasley")


@app.route("/")
def hello():
    return "Salam Donya!"


@app.route("/ids/events")
def events_legacy():

    ids_min_id = request.args.get('ids_min_id', 0)
    ips_min_id = request.args.get('ips_min_id', 0)
    interval = request.args.get('interval', None)

    fetch = lambda server, min: list(get_events(server, min, interval))
    
    return json.dumps({
        "ids": fetch("ids", ids_min_id),
        "ips": fetch("ips", ips_min_id),
    })


@app.route("/v1/ids/events")
def events():

    interval = request.args.get('interval', None)
    fetch = lambda server: list(get_events(server, interval=interval))

    return json.dumps({
        vn["name"]: fetch(vn["name"])
        for vn in VNETS
    })


@app.route("/ids/hist")
def events_hist():
    interval = request.args.get('interval', 3600)
    buckets = request.args.get('buckets', 10)
    net = request.args.get('net', None)
    return json.dumps(net_history(net, interval, buckets))


@app.route("/vnet/get")
def get_host_vn():
    host = request.args.get('host')
    if not host:
        return json.dumps({"status": "400"}), 400
    return json.dumps(get_vn(host))


@app.route("/vnet/toggle")
def toggle_host_vn():
    host = request.args.get('host')
    if not host:
        return json.dumps({"status": "400"}), 400
    return json.dumps(toggle_vn(host))


@app.route("/sim/qos")
def host_qos():
    return json.dumps(get_host_qos())


@app.route("/sim/attack")
def host_attack_stats():
    return json.dumps(get_attack_stats())


@app.route("/v1/topo/arp")
def arp_table():
    return json.dumps(topo.get_arp_table())


@app.route("/v1/topo/sims")
def get_simulations():
    return json.dumps(topo.get_sims())


@app.route("/v1/info/alerts")
def get_alerts_info():
    return json.dumps(ALERTS)


