import requests
from urllib.parse import urlparse


def scan_website(url):

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    response = requests.get(url, timeout=10)

    headers = response.headers

    score = 100

    recommendations = []

    security_headers = {

        "Content-Security-Policy": "Missing",

        "X-Frame-Options": "Missing",

        "X-Content-Type-Options": "Missing",

        "Strict-Transport-Security": "Missing",

        "Referrer-Policy": "Missing",

        "Permissions-Policy": "Missing"

    }

    for header in security_headers:

        if header in headers:

            security_headers[header] = headers[header]

        else:

            score -= 10

            recommendations.append(
                f"Add {header} header."
            )

    https_enabled = url.startswith("https://")

    if not https_enabled:

        score -= 20

        recommendations.append(
            "Use HTTPS instead of HTTP."
        )

    server = headers.get("Server", "Unknown")

    if server != "Unknown":

        recommendations.append(
            "Consider hiding the Server header."
        )

    cookie_secure = "No"

    cookie_httponly = "No"

    cookie_samesite = "No"

    cookies = response.headers.get("Set-Cookie", "")

    if "Secure" in cookies:

        cookie_secure = "Yes"

    else:

        score -= 5

        recommendations.append(
            "Use Secure cookies."
        )

    if "HttpOnly" in cookies:

        cookie_httponly = "Yes"

    else:

        score -= 5

        recommendations.append(
            "Use HttpOnly cookies."
        )

    if "SameSite" in cookies:

        cookie_samesite = "Yes"

    else:

        score -= 5

        recommendations.append(
            "Use SameSite cookies."
        )

    try:

        options = requests.options(url)

        methods = options.headers.get("Allow", "Unknown")

    except:

        methods = "Unknown"

    if score < 0:

        score = 0

    if score >= 90:

        level = "Excellent"

        color = "green"

    elif score >= 70:

        level = "Good"

        color = "lime"

    elif score >= 50:

        level = "Average"

        color = "orange"

    else:

        level = "Poor"

        color = "red"

    if len(recommendations) == 0:

        recommendations.append(
            "No major security issues detected."
        )

    return {

        "url": url,

        "domain": urlparse(url).netloc,

        "status": response.status_code,

        "https": "Enabled" if https_enabled else "Disabled",

        "server": server,

        "headers": security_headers,

        "secure_cookie": cookie_secure,

        "httponly_cookie": cookie_httponly,

        "samesite_cookie": cookie_samesite,

        "methods": methods,

        "score": score,

        "level": level,

        "color": color,

        "recommendations": recommendations

    }