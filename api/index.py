from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, phonenumberutil
import re
import socket

app = Flask(__name__)

# --- Extended Helper Functions ---
def validate_aadhar(number):
    pattern = re.compile(r"^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$|^[2-9]{1}[0-9]{11}$")
    return bool(pattern.match(str(number)))

def validate_pan(pan):
    pattern = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")
    return bool(pattern.match(str(pan).upper()))

def get_ip_info(ip):
    try:
        # Basic DNS lookup
        host = socket.gethostbyaddr(ip)
        return {"ip": ip, "hostname": host[0], "status": "active"}
    except:
        return {"ip": ip, "status": "reachable" if ip else "invalid"}

# --- Main API Route ---
@app.route('/api', methods=['GET'])
def get_ultimate_intelligence():
    # All Parameters
    num = request.args.get('num')
    aadhar = request.args.get('aadhar')
    pan = request.args.get('pan')
    email = request.args.get('email')
    ip = request.args.get('ip')
    username = request.args.get('username')

    response = {
        "status": "success",
        "developer": "NarutoCodex",
        "results": {}
    }

    # 1. Phone Intelligence
    if num:
        try:
            parsed_num = phonenumbers.parse(num, "IN")
            response["results"]["phone"] = {
                "valid": phonenumbers.is_valid_number(parsed_num),
                "type": str(phonenumberutil.number_type(parsed_num)),
                "carrier": carrier.name_for_number(parsed_num, "en") or "Unknown",
                "location": geocoder.description_for_number(parsed_num, "en"),
                "timezone": list(timezone.time_zones_for_number(parsed_num))
            }
        except: response["results"]["phone"] = {"error": "Invalid format"}

    # 2. Identity Validators
    if aadhar: response["results"]["aadhar"] = {"valid_format": validate_aadhar(aadhar)}
    if pan: response["results"]["pan"] = {"valid_format": validate_pan(pan)}

    # 3. IP Intelligence
    if ip:
        response["results"]["ip_data"] = get_ip_info(ip)

    # 4. Social Username Intel
    if username:
        response["results"]["social_links"] = {
            "instagram": f"https://instagram.com/{username}",
            "github": f"https://github.com/{username}",
            "telegram": f"https://t.me/{username}"
        }

    # 5. Email & Domain Intel
    if email and "@" in email:
        domain = email.split('@')[-1]
        response["results"]["email_domain"] = {
            "address": email,
            "domain": domain,
            "web_link": f"https://{domain}"
        }

    return jsonify(response), 200

@app.route('/')
def home():
    return "Ultimate Naruto Intelligence API Live! Parameters: num, aadhar, pan, email, ip, username"

app = app

