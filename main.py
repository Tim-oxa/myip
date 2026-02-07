from litestar import Litestar, get, Request
from litestar.response import Template
from litestar.template import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from pymongo import AsyncMongoClient
from config import *
import ipaddress


db = AsyncMongoClient(DB_URL)[DB_NAME]



@get("/")
async def index() -> Template:
    return Template("index.html")


@get("/api")
async def api(request: Request) -> dict:
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

    return {
        "ip": ip,
        "country_code": country_code,
        "country": country,
        "city": city,
        "autonomous_system_number": autonomous_system_number,
        "autonomous_system_organization": autonomous_system_organization
    }


app = Litestar(
    [index, api],
    template_config=TemplateConfig(directory="templates", engine=JinjaTemplateEngine),
)