import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from cryptography.fernet import Fernet


DATA_FILE = "url_credentials.csv"
KEY_FILE = "secret.key"

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
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Environment", "Application", "URL", "Username", "Password"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

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
from io import StringIO

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



# --------- UI Starts ---------
st.title("🔐 URL and Credential Manager")

# Add an anchor just before the notification placeholder
st.markdown("<a name='notification'></a>", unsafe_allow_html=True)

notification_placeholder = st.empty()

# ---- to display success message on the top, however, it doesn't auto-scrolls to the top. Hence, usind st.toast method instead --- #
# if st.session_state.upload_success_message:
#     notification_placeholder.success(st.session_state.upload_success_message)
#     components.html(
#         """
#         <script>
#             window.parent.location.hash = '#notification';
#         </script>
#         """,
#         height=0,
#     )
#     st.session_state.upload_success_message = ""

if st.session_state.upload_success_message:
    st.toast(st.session_state.upload_success_message)
    st.session_state.upload_success_message = ""


st.subheader("➕ Add or Edit an Entry")

with st.form(key=f"entry_form_{st.session_state.form_key}"):
    env = st.selectbox(
        "Environment", ["TEST", "PRE", "PSUP"],
        index=["TEST", "PRE", "PSUP"].index(st.session_state.form_env)
    )
    system = st.text_input("Application Name", value=st.session_state.form_system)
    url = st.text_input("URL", value=st.session_state.form_url)
    username = st.text_input("**Username**", value=st.session_state.form_username)
    password = st.text_input("Password", type="password", value=st.session_state.form_password)

    submitted = st.form_submit_button("Update Entry" if st.session_state.edit_index is not None else "Add Entry")

    if submitted:
        if st.session_state.edit_index is not None:
            # Update entry
            st.session_state.url_data.loc[
                st.session_state.edit_index,
                ["Environment", "Application", "URL", "Username", "Password"]
            ] = [env, system, url, username, password]
            st.session_state.upload_success_message = "✅ Entry updated"
        else:
            # Add new entry
            new_entry = pd.DataFrame([[env, system, url, username, password]],
                                     columns=["Environment", "Application", "URL", "Username", "Password"])
            st.session_state.url_data = pd.concat([st.session_state.url_data, new_entry], ignore_index=True)
            st.session_state.upload_success_message = "✅ Entry added"

        save_data(st.session_state.url_data)
        refresh_page()


# --------- Download Data ---------
st.subheader("📥 Download Data")

csv_data = st.session_state.url_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📁 Download CSV",
    data=csv_data,
    file_name="url_credentials.csv",
    mime="text/csv"
)

# --------- Upload CSV to Add Entries with Preview + Duplicate Check ---------
st.subheader("📤 Upload CSV to Import Entries")

if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = True

def cancel_upload():
    st.session_state.show_uploader = False
    st.rerun()

if st.session_state.show_uploader:
    uploaded_file = st.file_uploader(
        "Upload a CSV file with columns: Environment, System, URL, Username, Password", 
        type="csv"
    )

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            required_cols = ["Environment", "Application", "URL", "Username", "Password"]

            if all(col in uploaded_df.columns for col in required_cols):
                st.info("🔍 Preview of uploaded data:")
                st.dataframe(uploaded_df)

                # Identify duplicates
                existing_keys = st.session_state.url_data[["Environment", "Application", "Username"]].astype(str)
                new_keys = uploaded_df[["Environment", "Application", "Username"]].astype(str)

                duplicates_mask = new_keys.apply(tuple, axis=1).isin(existing_keys.apply(tuple, axis=1))
                duplicates = uploaded_df[duplicates_mask]
                unique_rows = uploaded_df[~duplicates_mask]

                if not duplicates.empty:
                    st.warning(f"⚠️ {len(duplicates)} duplicate rows found. These will be skipped.")
                    st.dataframe(duplicates)

                if not unique_rows.empty:
                    if st.button("✅ Import Unique Entries"):
                        st.session_state.url_data = pd.concat(
                            [st.session_state.url_data, unique_rows], ignore_index=True
                        )
                        save_data(st.session_state.url_data)
                        st.session_state.upload_success_message = f"✅ {len(unique_rows)} new entries imported successfully!"
                        st.session_state.show_uploader = False
                        st.rerun()

                else:
                    st.info("No new entries to import.")

                if st.button("❌ Cancel Upload"):
                    cancel_upload()

            else:
                st.error(f"❌ CSV is missing required columns: {', '.join(required_cols)}")
        except Exception as e:
            st.error(f"❌ Failed to process file: {e}")
else:
    # Button to re-show uploader if user wants to start again
    if st.button("📁 Upload Another CSV"):
        st.session_state.show_uploader = True
        st.rerun()

# -------- Bookmarks button --------
st.subheader("🔖 Export Bookmarks")

bookmark_html = generate_bookmark_html(st.session_state.url_data)
st.download_button(
    label="📥 Download Bookmark File",
    data=bookmark_html,
    file_name="DoE_Apps_Bookmarks.html",
    mime="text/html"
)

with st.expander("❓ How to Use This File"):
    st.markdown("""
1. Click **Download Bookmark File** above to save `DoE_Apps_Bookmarks.html`.
2. Open your browser and go to the **Import Bookmarks** section:
    - **Chrome**: `Bookmarks > Import Bookmarks and Settings > Bookmarks HTML File`
    - **Firefox**: `Library > Bookmarks > Show All Bookmarks > Import and Backup > Import Bookmarks from HTML`
    - **Edge**: `Settings > Profiles > Import browser data > Favorites or bookmarks HTML file`
3. Select the downloaded file.
4. You’ll see a folder called **"DoE Apps"** with bookmarks grouped by environment and application.
    """)


# --------- Show Entries ---------
st.subheader("📋 Current Entries")

for env in ["TEST", "PRE", "PSUP"]:
    filtered = st.session_state.url_data[st.session_state.url_data["Environment"] == env]
    if not filtered.empty:
        st.markdown(f"### 🌐 {env} Environment")

        for i, row in filtered.iterrows():
            with st.expander(f"🔐 {row['Application']} ({row['Username']})"):
                st.write(f"**URL**: {row['URL']}")
                st.write(f"**Username**: {row['Username']}")
                st.write(f"**Password**: {row['Password']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Edit", key=f"edit_{i}"):
                        st.session_state.edit_index = row.name
                        st.session_state.form_env = row["Environment"]
                        st.session_state.form_system = row["Application"]
                        st.session_state.form_url = row["URL"]
                        st.session_state.form_username = row["Username"]
                        st.session_state.form_password = row["Password"]
                        st.rerun()
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        st.session_state.pending_delete = row.name
                        st.rerun()

                if st.session_state.pending_delete == row.name:
                    st.warning(f"⚠️ Are you sure you want to permanently delete the entry for **{row['Application']} ({row['Username']})**?")
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("✅ Yes, Delete", key=f"confirm_delete_{i}"):
                            st.session_state.url_data.drop(index=row.name, inplace=True)
                            st.session_state.url_data.reset_index(drop=True, inplace=True)
                            save_data(st.session_state.url_data)
                            st.session_state.upload_success_message = f"🗑️ Deleted entry for {row['Application']} ({row['Username']})"
                            refresh_page()
                    with col_cancel:
                        if st.button("❌ Cancel", key=f"cancel_delete_{i}"):
                            st.session_state.pending_delete = None
                            st.info("Deletion cancelled")
                            st.rerun()


