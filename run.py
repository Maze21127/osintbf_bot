from flask import redirect, jsonify, request
from app import create_app, db
from app.ip_info import get_info_by_ip
from models import Link, LinkData
from logger import logger
from settings import BASE_URL
from waitress import serve

app = create_app()


@app.route('/')
def index():
    return "<h1> Working...</h1>"


@app.route('/api/links')
def show_links():
    links = db.session.query(Link).all()
    return [i.json() for i in links]


@app.route('/api/check_link', methods=['GET'])
def check_link():
    responce_link = request.args.get('link')
    link = db.session.query(Link).filter(Link.redirect == responce_link).first()
    if link is None:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "already exists"}), 402


@app.route('/api/create_link', methods=['POST'])
def create_link():
    form = request.form
    redirect_link = form.get('redirect', None)
    source = form.get('source', None)
    link = Link(source=source, redirect=redirect_link)
    db.session.add(link)
    db.session.commit()
    return jsonify({
        "status": "success",
        "link": f"{BASE_URL}/{redirect_link}"
    }, 201)


@app.route('/<link>', methods=['GET'])
def redirect_link(link):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_info = get_info_by_ip(ip)
    logger.debug(f"{link} - {ip}")
    source_link = Link.query.filter_by(redirect=link).first()
    if source_link is None:
        logger.debug(f"{link} Forbidden")
        return "Forbidden", 403
    logger.debug(f"{source_link.source}")

    #  checking if exist
    link_in_db = db.session.query(LinkData).filter_by(ip=ip, link_id=source_link.id).first()
    logger.warning(link_in_db)
    if link_in_db is None:
        link_data = LinkData(link_id=source_link.id,
                             ip=ip,
                             provider=ip_info.get("provider", None),
                             org=ip_info.get("org", None),
                             country=ip_info.get("country", None),
                             region=ip_info.get("region", None),
                             city=ip_info.get("city", None),
                             zip=ip_info.get("zip", None),
                             lat=ip_info.get("lat", None),
                             lon=ip_info.get("lon", None),
                             )
        db.session.add(link_data)
        logger.info(f"{link_data} added")
        db.session.commit()
    return redirect(source_link.source)


@app.route('/api/link_info/<int:link_id>', methods=['GET'])
def show_link_info(link_id):
    data = LinkData.query.filter_by(id=link_id).all()
    return [i.json() for i in data]


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    logger.info("Starting app")
    #app.run(port=6575, debug=True)
    serve(app, port=6575)


