import streamlit as st
import json
import requests
import os
import subprocess
from datetime import datetime
from urllib.parse import urljoin
from logo_fetcher import get_company_logo

def download_from_backblaze():
    """Download today's interview data from Backblaze B2"""
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{today}.json"

    # B2 credentials from Streamlit secrets or environment variables
    try:
        b2_key_id = st.secrets["backblaze"]["key_id"]
        b2_app_key = st.secrets["backblaze"]["application_key"]
        b2_bucket = st.secrets["backblaze"]["bucket_name"]
    except KeyError:
        # Fallback to environment variables or hardcoded values
        b2_key_id = os.getenv("B2_KEY_ID", "0054b0b4d778a7e0000000002")
        b2_app_key = os.getenv("B2_APPLICATION_KEY", "K005OrQQbrEh9C/9n/NvPnaunWmLCFk")
        b2_bucket = os.getenv("B2_BUCKET_NAME", "interview-questions")

    try:
        # Set environment variables for B2
        env = os.environ.copy()
        env['B2_KEY_ID'] = b2_key_id
        env['B2_APPLICATION_KEY'] = b2_app_key
        env['B2_BUCKET_NAME'] = b2_bucket

        # Check if b2 is available
        try:
            subprocess.run(['b2', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Install b2 if not available
            subprocess.run(['pip', 'install', 'b2'], check=True)

        # Authorize account (suppress warnings)
        auth_result = subprocess.run(
            ['b2', 'account', 'authorize', b2_key_id, b2_app_key],
            capture_output=True,
            text=True,
            env=env
        )

        if auth_result.returncode != 0:
            st.error(f"Failed to authenticate with Backblaze: {auth_result.stderr}")
            return None

        # Download the file
        download_result = subprocess.run(
            ['b2', 'file', 'download', b2_bucket, filename, filename],
            capture_output=True,
            text=True,
            env=env
        )

        if download_result.returncode == 0:
            st.success(f"Downloaded {filename} from Backblaze")
            return filename
        else:
            st.warning(f"File {filename} not found in Backblaze. Error: {download_result.stderr}")
            return None

    except Exception as e:
        st.error(f"Error downloading from Backblaze: {str(e)}")
        return None

def load_interview_data():
    """Load interview data from JSON file, downloading from Backblaze if needed"""
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{today}.json"

    # Check if today's file exists locally
    if not os.path.exists(filename):
        st.info(f"Downloading today's data ({filename}) from Backblaze...")
        downloaded_file = download_from_backblaze()
        if not downloaded_file:
            # Fallback to any existing JSON file
            json_files = [f for f in os.listdir('.') if f.endswith('.json')]
            if json_files:
                filename = sorted(json_files)[-1]  # Use the most recent file
                st.warning(f"Using fallback file: {filename}")
            else:
                st.error("No interview data files found.")
                return []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        st.info(f"Loaded {len(data)} interviews from {filename}")
        return data
    except FileNotFoundError:
        st.error(f"Interview data file {filename} not found.")
        return []
    except json.JSONDecodeError:
        st.error(f"Invalid JSON format in {filename}.")
        return []

def main():
    st.set_page_config(
        page_title="Interview Questions & Answers",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("💼 Interview Questions & Answers")
    st.markdown("---")

    # Load data
    interview_data = load_interview_data()

    if not interview_data:
        st.stop()

    # Sidebar for filtering
    st.sidebar.header("🔍 Filters")

    # Get unique companies and roles
    companies = sorted(list(set([item['company'] for item in interview_data])))
    roles = sorted(list(set([item['role'] for item in interview_data])))

    # Filter options
    selected_companies = st.sidebar.multiselect(
        "Select Companies",
        companies,
        default=companies
    )

    selected_roles = st.sidebar.multiselect(
        "Select Roles",
        roles,
        default=roles
    )

    # Filter data
    filtered_data = [
        item for item in interview_data
        if item['company'] in selected_companies and item['role'] in selected_roles
    ]

    st.sidebar.markdown(f"**Showing {len(filtered_data)} of {len(interview_data)} interviews**")

    # Main content
    if not filtered_data:
        st.warning("No interviews match the selected filters.")
        return

    # Display interviews
    for i, item in enumerate(filtered_data):
        with st.container():
            # Create columns for logo and header info
            col1, col2 = st.columns([1, 5])

            with col1:
                # Company logo
                logo_url = get_company_logo(item['company'], size=128)
                if logo_url:
                    try:
                        st.image(logo_url, width=80)
                    except:
                        st.write("🏢")
                else:
                    st.write("🏢")

            with col2:
                st.subheader(f"{item['company']}")
                st.write(f"**Role:** {item['role']}")
                st.write(f"**Location:** {item['location']}")
                st.write(f"**Rating:** {item['company_rating']}")
                st.write(f"**Interview Date:** {item['interview_date']}")

            # Question section
            st.markdown("### ❓ Question")
            with st.expander("View Question", expanded=True):
                st.write(item['question'])

            # Answer section
            st.markdown("### ✅ Answer")
            with st.expander("View Answer", expanded=False):
                st.write(item['answer'])

            # Metadata
            col3, col4 = st.columns(2)
            with col3:
                st.caption(f"Scraped: {item['scraped_at']}")
            with col4:
                st.caption(f"Answer Generated: {item['answer_generated_at']}")

            # URL link
            if 'url' in item and item['url']:
                st.markdown(f"[🔗 Source URL]({item['url']})")

            st.markdown("---")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Data Summary:**")
    st.sidebar.write(f"• {len(companies)} Companies")
    st.sidebar.write(f"• {len(roles)} Different Roles")
    st.sidebar.write(f"• Data from: {interview_data[0]['interview_date'] if interview_data else 'N/A'}")

if __name__ == "__main__":
    main()