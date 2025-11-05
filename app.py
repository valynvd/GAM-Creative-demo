from flask import Flask, render_template, request, url_for
import os

app = Flask(__name__)

# Folder static upload
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            save_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(save_path)
            left_img = f.filename

    if "right_img" in request.files:
        f = request.files["right_img"]
        if f and f.filename:
            save_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(save_path)
            right_img = f.filename

    return render_template(
        "dashboard.html",
        format=format,
        snippet=snippet,
        text=text,
        position=position,
        left_img=left_img,
        right_img=right_img,
        site=site
    )


@app.route("/preview/skinad")
def preview_skinad():
    left = request.args.get("left", "")
    right = request.args.get("right", "")
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


if __name__ == "__main__":
    app.run(debug=True)
