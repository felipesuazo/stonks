from . import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.String(), primary_key=True)
    streamer_name = db.Column(db.String())
    event_type = db.Column(db.String())
    viewer_name = db.Column(db.String())
    created_at = db.Column(db.DateTime())

    _idx_streamer_name = db.Index('events_idx_streamer_name', 'streamer_name')

    def as_dict(self):
        return {
            'id': self.id,
            'streamer_name': self.streamer_name,
            'event_type': self.event_type,
            'viewer_name': self.viewer_name,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }