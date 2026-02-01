from quart import Quart, request, render_template, jsonify
from pymongo import AsyncMongoClient
from hypercorn.asyncio import serve
from hypercorn.config import Config
from config import *
import ipaddress
import asyncio


db = AsyncMongoClient(DB_URL)[DB_NAME]

app = Quart(__name__)


@app.get("/")
async def index():
    return await render_template("index.html")


@app.get("/api")
async def api():
    ip = request.headers.get("X-Forwarded-For")
    ip_int = int(ipaddress.IPv4Address(ip))

    geo = await db["city"].find_one({"ip_range_start": {"$lte": ip_int}, "ip_range_end": {"$gte": ip_int}})
    if not geo:
        geo = {}
    country_code = geo.get("country_code")
    if country := await db["country_codes"].find_one({"id": country_code}):
        country = country["name"]
    city = geo.get("city")

    asn = await db["asn"].find_one({"ip_range_start": {"$lte": ip_int}, "ip_range_end": {"$gte": ip_int}})
    if not asn:
        asn = {}
    autonomous_system_number = asn.get("autonomous_system_number")
    autonomous_system_organization = asn.get("autonomous_system_organization")

    return jsonify({
        "ip": ip,
        "country_code": country_code,
        "country": country,
        "city": city,
        "autonomous_system_number": autonomous_system_number,
        "autonomous_system_organization": autonomous_system_organization
    })


hc_config = Config()
hc_config.bind = f"0.0.0.0:{PORT}"
asyncio.run(serve(app, hc_config))
