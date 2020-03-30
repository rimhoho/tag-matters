from app import db
# from sqlalchemy.dialects.postgresql import JSON


class Metadata(db.Model): 
    __tablename__ = 'metadata'
    __table_args__ = {'extend_existing': True}

    # result
    # [{'Tag': '', 'Frequency': '', 'Title': '', 'Date': '', 'Url': '', 'Description': '', 'img_URL': ''},{...}]

    id = db.Column(db.Integer, primary_key=True)
    Tag = db.Column(db.String())
    Frequency = db.Column(db.String())
    Title = db.Column(db.String())
    Date = db.Column(db.String())
    Url = db.Column(db.String())
    Description = db.Column(db.String())
    img_URL = db.Column(db.String())

    def __init__(self, url, result_all, result_no_stop_words):
        self.Tag = Tag

        self.title = title
        self.pub_date = pub_date
        self.Url = Url
        self.description = description
        self.thm_img = thm_img

    def __repr__(self):
        return '<id {}>'.format(self.id)