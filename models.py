from database import db

class WhatsAppUserInformation(db.Model):
    __tablename__ = 'whatsapp_user_information_tab'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), default=None)
    whatsapp_number = db.Column(db.String(20), default=None)
    app_id = db.Column(db.String(100), nullable=False)
    # Define a unique constraint for user_id and app_id
    __table_args__ = (db.UniqueConstraint('user_id', 'app_id', name='user_id__app_id_index'),)
