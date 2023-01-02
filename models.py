from app import db


class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    redirect = db.Column(db.String(4096), nullable=False)

    def __repr__(self):
        return f"{self.id}\n{self.source}\n{self.redirect}"

    def json(self):
        return {
            "id": self.id,
            "source": self.source,
            "redirect": self.redirect
        }


class LinkData(db.Model):
    __tablename__ = 'links_data'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey("links.id"), nullable=False)
    ip = db.Column(db.String(30))
    provider = db.Column(db.String(255))
    org = db.Column(db.String(255))
    country = db.Column(db.String(255))
    region = db.Column(db.String(255))
    city = db.Column(db.String(255))
    zip = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def json(self):
        return {
            "id": self.id,
            "link_id": self.link_id,
            "ip": self.ip,
            "provider": self.provider,
            "org": self.org,
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "zip": self.zip,
            "lat": self.lat,
            "lon": self.lon
        }

    def __repr__(self):
        return f"{self.link_id}\n{self.ip}"
