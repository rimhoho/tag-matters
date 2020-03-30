from app import db


class Metadata(db.Model): 
    __tablename__ = 'metadata'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    Tag = db.Column(db.String(255))
    Frequency = db.Column(db.String(255))
    Title = db.Column(db.String(255))
    Date = db.Column(db.String(25))
    Url = db.Column(db.String(255))
    Description = db.Column(db.String())
    img_URL = db.Column(db.String(255))

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