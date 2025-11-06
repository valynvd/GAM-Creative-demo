from flask import Flask, render_template, request, url_for, redirect
import os, base64
from urllib.parse import quote, unquote
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder = "templates", static_folder = "static")

# UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
UPLOAD_FOLDER = "static/uploads"

@app.route("/", methods=["GET", "POST"])
def dashboard():
    format = request.form.get("format", "skinad")
    site = request.form.get("site", "default")

    snippet_skinad = """
<script src="https://cdn.jsdelivr.net/gh/valynvd/yes@main/ad_Inventory.js"></script>
<script>
  adInventory.init("skinad", {
    clickUrl: "%%VIEW_URL_ESC%%",
    leftImage: "",
    rightImage: "",
  });
</script>"""

    snippet_newstag = """
<script src="https://cdn.jsdelivr.net/gh/valynvd/yes@main/ad_Inventory.js?creative=newstag"></script>
<script>
  adInventory.init('newstag', {
    textTag: '',
    landingPage: '%%VIEW_URL_ESC%%',
    position: '',
    site: ''
  });
</script>"""

    snippet = snippet_skinad if format == "skinad" else snippet_newstag
    text = request.form.get("text", "")
    position = request.form.get("position", 0)

    left_img = request.form.get("left_saved", "")
    right_img = request.form.get("right_saved", "")

    if "left_img" in request.files:
        f = request.files["left_img"]
        if f and f.filename:
            left_img = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

    if "right_img" in request.files:
        f = request.files["right_img"]
        if f and f.filename:
            right_img = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

    return render_template(
        "dashboard.html",
        format=format,
        snippet=snippet,
        text=text,
        position=position,
        left_img=quote(left_img) if left_img else "",
        right_img=quote(right_img) if right_img else "",
        site=site
    )


@app.route("/preview/skinad")
def preview_skinad():
    left = request.args.get("left", "")
    right = request.args.get("right", "")
    
    if left:
        left = unquote(left)
    if right:
        right = unquote(right)

    return render_template("preview_skinad.html", left=left, right=right)



@app.route("/preview/newstag")
def preview_newstag():
    text = request.args.get("text", "")
    site = request.args.get("site", "generic")
    position = request.args.get("position", 0)

    template_map = {
        "kapanlagi": "newstag/newstag_kapanlagi.html",
        "liputan6": "newstag/newstag_liputan6.html",
    }

    template = template_map.get(site, "newstag/preview_newstag.html")
    
    return render_template(template, text=text, site=site, position=position)

@app.route('/preview/newstag/live')
def preview_newstag_live():
    text = request.args.get("text", "")
    site = request.args.get("site", "kapanlagi")
    position = int(request.args.get("position", 0))

    site_map = {
        "kapanlagi": "https://www.kapanlagi.com",
    }

    url = site_map.get(site, "https://www.kapanlagi.com")

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        html = requests.get(url, headers=headers, timeout=5).text

    except:
        return "<p style='padding:20px'>⚠️ Failed to fetch site preview.</p>"
    
    soup = BeautifulSoup(html, "html.parser")

    trending = soup.find('div', class_='header25-trending')
    if trending is None:
        return "<p style='padding:20px'>⚠️ Trending section not found on site.</p>"

    tag_container = trending.find(id="tagContainer")
    if tag_container:
        new_tag = soup.new_tag("a", **{"class": "header25-trending__item active", "href": "#"})
        new_tag.string = text or "Tag"
        children = tag_container.find_all("a")
        if position >= len(children):
            tag_container.append(new_tag)
        else:
            children[position].insert_before(new_tag)

    snippet = f"""
<script src="https://cdn.jsdelivr.net/gh/valynvd/yes@main/ad_Inventory.js?creative=newstag"></script>
<script>
  adInventory.init('newstag', {{
    textTag: '{text}',
    landingPage: '%%VIEW_URL_ESC%%',
    position: '{position}',
    site: '{site}'
  }});
</script>
"""

    trending.append(BeautifulSoup(snippet, "html.parser"))

    return str(trending)
    

if __name__ == "__main__":
    app.run(debug=True)
