from models import db
from sqlalchemy import func

class DataBarang(db.Model):
    __tablename__ = 'data_barang'

    no = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(255), nullable=False)
    stok = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori_barang.no'), nullable=False)

    @property
    def data(self):
        return {
            'no': self.no,
            'nama_kategori': self.kategori.nama_kategori if self.kategori else None,
            'nama_barang': self.nama_barang,
            'stok': self.stok,
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
    def get_total_barang(cls):
        return cls.query.count()