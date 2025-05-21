# Utility functions (encryption, load/save, refresh_page, etc.)

import os
import pandas as pd
from cryptography.fernet import Fernet
import streamlit as st
import streamlit.components.v1 as components
from io import StringIO
from config import DATA_FILE, ENV_OPTIONS
from config import DATA_FILE, KEY_FILE, ENV_OPTIONS



# --------- Encryption Utilities ---------
def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

fernet = Fernet(load_key())

# --------- Data Persistence ---------
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if "Password" in df.columns:
            df["Password"] = df["Password"].apply(lambda x: fernet.decrypt(x.encode()).decode() if pd.notna(x) else "")
        return df
    else:
        return pd.DataFrame(columns=["Environment", "Application", "URL", "Username", "Password"])


def save_data(df):
    df_copy = df.copy()
    df_copy["Password"] = df_copy["Password"].apply(lambda x: fernet.encrypt(x.encode()).decode())
    df_copy.to_csv(DATA_FILE, index=False)


# --------- Delete All Entries Utility ---------
def delete_all_entries():
    empty_df = pd.DataFrame(columns=["Environment", "Application", "URL", "Username", "Password"])
    save_data(empty_df)
    st.session_state.url_data = empty_df


# --------- Page/Form Reset Utility ---------
def refresh_page():
    st.session_state.form_env = "TEST"
    st.session_state.form_system = ""
    st.session_state.form_url = ""
    st.session_state.form_username = ""
    st.session_state.form_password = ""
    st.session_state.edit_index = None
    st.session_state.pending_delete = None
    st.session_state.form_key = str(os.urandom(8))  # New form key to reset widget state
    st.rerun()

# --------- Bookmark Folder Utility ---------
def generate_bookmark_html(df):
    html = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">",
        "<TITLE>DoE Apps</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
        "    <DT><H3 ADD_DATE=\"0\">DoE Apps</H3>",
        "    <DL><p>"
    ]

    if not df.empty:
        grouped = df.groupby("Environment")
        for env, env_df in grouped:
            sorted_env_df = env_df.sort_values("Application", key=lambda x: x.str.lower())
            html.append(f"        <DT><H3>{env} Environment</H3>")
            html.append("        <DL><p>")
            for _, row in sorted_env_df.iterrows():
                app = row['Application']
                url = row['URL']
                username = row['Username']
                password = row['Password']
                tooltip = f"Username: {username} | Password: {password}"
                html.append(f'            <DT><A HREF="{url}" ADD_DATE="0" LAST_MODIFIED="0" TITLE="{tooltip}">{app}</A>')
            html.append("        </DL><p>")

    html.append("    </DL><p>")
    html.append("</DL><p>")

    return "\n".join(html)

# --------- Initialize session state ---------
def init_session_state():
    if "url_data" not in st.session_state:
        st.session_state.url_data = load_data()

    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None

    if "pending_delete" not in st.session_state:
        st.session_state.pending_delete = None

    if "form_key" not in st.session_state:
        st.session_state.form_key = "initial"

    if "form_env" not in st.session_state:
        st.session_state.form_env = "TEST"

    if "form_system" not in st.session_state:
        st.session_state.form_system = ""

    if "form_url" not in st.session_state:
        st.session_state.form_url = ""

    if "form_username" not in st.session_state:
        st.session_state.form_username = ""

    if "form_password" not in st.session_state:
        st.session_state.form_password = ""

    if "upload_success_message" not in st.session_state:
        st.session_state.upload_success_message = ""