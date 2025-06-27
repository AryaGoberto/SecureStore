from models import db
from sqlalchemy import func

class KategoriBarang(db.Model):
    __tablename__ = 'kategori_barang'

    no = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    items = db.relationship('DataBarang', backref='kategori', lazy=True)

    @property
    def data(self):
        return {
            'no': self.no,
            'nama_kategori': self.nama_kategori,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.all()
        result =[]
        for i in r:
            result.append(i.data)
        return result
    
    @classmethod
    def get_by_id(cls, no):
        return cls.query.get(no)
    
    @classmethod
    def get_total_kategori(cls):
        return cls.query.count()