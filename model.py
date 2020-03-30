from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, String, Integer, Numeric

Base = declarative_base()


class Metadata(Base): 
    __tablename__ = 'metadata'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    Tag = Column(String)
    Frequency = Column(String)
    Title = Column(String)
    Date = Column(String)
    Url = Column(String)
    Description = Column(String)
    img_URL = Column(String)

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