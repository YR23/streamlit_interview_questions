import streamlit as st
import json
import requests
from datetime import datetime
from urllib.parse import urljoin
from logo_fetcher import get_company_logo

def load_interview_data():
    """Load interview data from JSON file"""
    try:
        with open('2025-09-27.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Interview data file not found. Please ensure '2025-09-27.json' exists in the current directory.")
        return []
    except json.JSONDecodeError:
        st.error("Invalid JSON format in the data file.")
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