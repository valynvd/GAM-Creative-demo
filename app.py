from flask import Flask, render_template, request, send_file
import os, base64
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from markupsafe import Markup

app = Flask(__name__, template_folder="templates", static_folder="static")

def fetch_trending_html(site: str):
    """
    Fetch page and return sanitized inner HTML of the trending list.
    Returns None on failure.
    """
    try:
        if site.lower() == "kapanlagi":
            url = "https://www.kapanlagi.com/"
        else:
            return None

        resp = requests.get(url, timeout=6, headers={
            "User-Agent": "Mozilla/5.0 (compatible; preview-bot/1.0)"
        })
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        container = soup.select_one("#spotlightbelt2025 .header25-trending__list")
        if not container:
            container = soup.select_one(".header25-trending__list")
        if not container:
            container = soup.find(class_="header25-trending")
        if not container:
            return None
        
        for s in container.select("script"):
            s.decompose()

        for el in container.find_all(True):
            for k in list(el.attrs.keys()):
                if k.startswith("on"):
                    del el.attrs[k]

            safe = {}
            for k,v in el.attrs.items():
                if k in ("href","src","class","id","title","alt","rel","aria-label"):
                    safe[k] = v
            el.attrs = safe

        inner_html = str(container)
        return inner_html
    except Exception as e:
        return None

@app.route("/", methods=["GET", "POST"])
def dashboard():
    format = request.form.get("format", "skinad")
    site = request.form.get("site", "kapanlagi")

    snippet_skinad_copy = """
<script src="https://cdn.jsdelivr.net/gh/valynvd/yes@main/ad_Inventory.js"></script>
<script>
  adInventory.init("skinad", {
    clickUrl: "%%VIEW_URL_ESC%%",
    leftImage: "",
    rightImage: ""
  });
</script>""".strip()

    snippet_newstag_copy = """
<script src="https://cdn.jsdelivr.net/gh/valynvd/yes@main/ad_Inventory.js"></script>
<script>
  adInventory.init('newstag', {
    textTag: '',
    landingPage: '%%VIEW_URL_ESC%%',
    position: '',
    site: ''
  });
</script>""".strip()

    snippet_copy = snippet_skinad_copy if format == "skinad" else snippet_newstag_copy

    text = request.form.get("text", "")
    position = request.form.get("position", 0)
    left_img = request.form.get("left_saved", "")
    right_img = request.form.get("right_saved", "")

    if format == "skinad":
        file_left = request.files.get("left_img")
        if file_left and left_img:
            try:
                left_data = left_img.split(",")[1]
                with open("/tmp/left.png", "wb") as f:
                    f.write(base64.b64decode(left_data))
            except:
                pass

        file_right = request.files.get("right_img")
        if file_right and right_img:
            try:
                right_data = right_img.split(",")[1]
                with open("/tmp/right.png", "wb") as f:
                    f.write(base64.b64decode(right_data))
            except:
                pass

    return render_template(
        "dashboard.html",
        format=format,
        snippet_copy=snippet_copy,
        snippet_preview=snippet_copy,
        text=text,
        position=position,
        left_img=quote(left_img) if left_img else "",
        right_img=quote(right_img) if right_img else "",
        site=site
    )

@app.route("/preview/skinad")
def preview_skinad():
    return render_template("preview_skinad.html", left="/temp/left.png", right="/temp/right.png")


@app.route("/preview/newstag")
def preview_newstag():
    text = request.args.get("text", "")
    site = request.args.get("site", "generic")
    position = request.args.get("position", 0)
    copy_snippet = request.args.get("snippet", "")

    snippet_preview = f"""
<script src="https://cdn.jsdelivr.net/gh/valynvd/yes@main/ad_Inventory.js"></script>
<script>
  window.kly = window.kly || {{}};
  window.kly.site = "{site}";
  (window.adInventory || parent.adInventory)?.init('newstag', {{
    textTag: '{text}',
    landingPage: '%%VIEW_URL_ESC%%',
    position: '{position}',
    site: '{site}'
  }});
</script>
""".strip()

    template_map = {
        "kapanlagi": "newstag/newstag_kapanlagi.html",
        "liputan6": "newstag/newstag_liputan6.html",
    }

    template = template_map.get(site, "newstag/newstag_kapanlagi.html")
    return render_template(template, text=text, position=position, snippet=snippet_preview)

@app.route("/preview/newstag_remote")
def preview_newstag_remote():
    site = request.args.get("site", "kapanlagi").lower()
    position = int(request.args.get("position", 0) or 0)
    text = request.args.get("text", "")
    remote_html = fetch_trending_html(site)
    if not remote_html:
        remote_html = ""
    return render_template(
        "newstag_kapanlagi.html",
        text=text,
        position=position,
        site=site,
        remote_trending_html=Markup(remote_html)
    )

@app.route("/temp/<filename>")
def serve_temp(filename):
    filepath = f"/tmp/{filename}"
    if os.path.exists(filepath):
        return send_file(filepath)
    return "", 404


if __name__ == "__main__":
    app.run(debug=True)
