import os
from datetime import datetime
from langchain_community.agent_toolkits import GmailToolkit
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

# ✅ Gmail API credentials
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="D:/Holmes_Criminal_Detection_Platform-main/core/cred.json",
)

api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)
tools = toolkit.get_tools()

llm = ChatGroq(
    model="gemma2-9b-it",
    api_key="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"
)

agent_executor = create_react_agent(llm, tools)

def send_criminal_alert_email(officer_email, profile):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = f"""
    Compose and send an email to {officer_email} notifying that a criminal has been identified 
    by the facial recognition system. Include the following details:

    - Full Name: {profile.first_name} {profile.last_name}
    - Profile ID: {profile.id}
    - Gender: {profile.gender}
    - Age: {profile.age}
    - Identification Mark: {profile.identi}
    - Crimes: {profile.crime}
    - Nationality: {profile.nationality}
    - Time of Detection: {timestamp}

    Use a professional and concise tone. Alert the officer to verify in the database and take necessary action.
    Ensure the email is sent automatically.
    """

    try:
        events = agent_executor.stream(
            {"messages": [("user", query)]},
            stream_mode="values",
        )
        for event in events:
            print(event["messages"][-1])  # Optional: logs the response
    except Exception as e:
        print("❌ Email sending failed:", e)
