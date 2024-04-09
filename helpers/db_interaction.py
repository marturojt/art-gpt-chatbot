from .db_connection import db_session
from models.asistant_models import Users, ChatLog, AsistantRoles
from sqlalchemy import desc

db_session = db_session()

users = db_session.query(Users).all()
print(users)

# USER OPERATIONS

# Search for a user in the database
def search_user(user_id):
    user = db_session.query(Users).filter(Users.telegram_id == user_id).first()
    db_session.close()
    return user

# Create a new user in the database
def new_user(telegram_id, name):
    new_user = Users(telegram_id=telegram_id, name=name)
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

# Update user name
def update_user(telegram_id, name):
    existing_user = db_session.query(Users).filter(Users.telegram_id == telegram_id).first()
    if (existing_user):
        existing_user.name = name
        db_session.commit()
    db_session.close()

# CHAT CONFIG OPERATIONS

# Get asistant role by id
def get_asistant_role_by_id(asistant_role_id):
    asistant_role = db_session.query(AsistantRoles).filter(AsistantRoles.idAsistantRole == asistant_role_id).first()
    db_session.close()
    return asistant_role

# Get a list of AsistantRoles Descriptions paired with id
def get_asistant_role_descriptions_with_id():
    asistant_roles = db_session.query(WaifuRoles).all()
    asistant_roles_descriptions = []
    for asistant_role in asistant_roles:
        asistant_roles_descriptions.append([asistant_role.AsistantRoleDescription, asistant_role.idAsistantRole])
    db_session.close()
    return waifu_roles_descriptions

# Get a list of WaifuRoles Descriptions
def get_waifu_role_descriptions():
    waifu_roles = db_session.query(WaifuRoles).all()
    waifu_roles_descriptions = []
    for waifu_role in waifu_roles:
        waifu_roles_descriptions.append(waifu_role.WaifuRoleDescription)
    db_session.close()
    return waifu_roles_descriptions

# CHAT LOG OPERATIONS

# def get_chat_log_user(user_id):
#     chat_log = db_session.query(ChatLog).filter(ChatLog.relIdUser == user_id).all()
#     chat_log_parsed = []
#     for chat in chat_log:
#         chat_log_parsed.append([chat.text])
#     db_session.close()
#     return chat_log_parsed

# Obtain the chat log for a user
def get_chat_log_user(user_id):
    # Subquery to get the last 20 rows in descending order
    subquery = db_session.query(ChatLog).filter(ChatLog.relIdUser == user_id).order_by(desc(ChatLog.idChatLog)).limit(20).subquery()

    # Query to sort the subquery result in ascending order
    chat_log = db_session.query(subquery.c.text).order_by(subquery.c.idChatLog.asc()).all()
    chat_log_parsed = []

    for chat in chat_log:
        chat_log_parsed.append([chat.text])
    
    return chat_log_parsed

# Add a new chat log entry
def new_chat_log_entry(user_id, text, timestamp):
    new_chat_log_entry = ChatLog(relIdUser=user_id, text=text, timestamp=timestamp)
    db_session.add(new_chat_log_entry)
    db_session.commit()
    db_session.close()