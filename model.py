from app import db


class Metadata(db.Model): 
    __tablename__ = 'metadata'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    Tag = db.Column(db.String(64))
    Frequency = db.Column(db.String(64))
    Title = db.Column(db.String(64))
    Date = db.Column(db.String(64))
    Url = db.Column(db.String(64))
    Description = db.Column(db.String(64))
    img_URL = db.Column(db.String(64))

    @property
    def serialize(self):
        """Returns a python dictionary of Metadata
        """
        return {
            'Tag': self.Tag,
            'Frequency': self.Frequency,
            'Title': self.Title,
            'Date': self.Date,
            'Url': self.Url,
            'Description': self.Description,
            'img_URL': self.img_URL
        }