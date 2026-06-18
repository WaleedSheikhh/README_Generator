import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="README Generator", page_icon="📄", layout="wide")

st.title("📄 README Generator")
st.caption("Generate a professional README from a GitHub repo or a ZIP file.")

# --- Sidebar ---
st.sidebar.header("⚙️ Options")

sections = st.sidebar.multiselect(
    "Sections to include",
    options=[
        "Project Title & Tagline",
        "Description",
        "Features",
        "Tech Stack",
        "Installation",
        "Usage",
        "API Reference",
        "Contributing",
        "License"
    ],
    default=["Description", "Features", "Tech Stack", "Installation", "Usage", "Contributing", "License"]
)

prompt = st.sidebar.text_area(
    "Custom instructions (optional)",
    placeholder="e.g. Make it beginner friendly, focus on async features..."
)

# --- Tabs ---
tab1, tab2 = st.tabs(["🔗 GitHub URL", "📦 Upload ZIP"])


# --- Tab 1: GitHub URL ---
with tab1:
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repo")

    if st.button("Generate README", key="url_btn"):
        if not repo_url:
            st.warning("Please enter a GitHub URL.")
        else:
            with st.spinner("Cloning repo and generating README..."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate",
                        json={
                            "repo_url": repo_url,
                            "selected_sections": sections,
                            "prompt": prompt or None
                        }
                    )

                    if response.status_code == 200:
                        data = response.json()
                        markdown = data["markdown"]

                        st.success(f"Generated using `{data['model_used']}`")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Preview")
                            st.markdown(markdown)
                        with col2:
                            st.subheader("Raw Markdown")
                            st.code(markdown, language="markdown")

                        st.download_button(
                            label="⬇️ Download README.md",
                            data=markdown,
                            file_name="README.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Something went wrong.')}")

                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the backend. Make sure it is running on localhost:8000.")


# --- Tab 2: ZIP Upload ---
with tab2:
    uploaded_file = st.file_uploader("Upload your project as a .zip file", type=["zip"])

    if st.button("Generate README", key="zip_btn"):
        if not uploaded_file:
            st.warning("Please upload a ZIP file.")
        else:
            with st.spinner("Extracting and generating README..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/zip")}
                    data = {
                        "prompt": prompt or "",
                        "selected_sections": json.dumps(sections)
                    }

                    response = requests.post(
                        f"{API_URL}/uploadZIPfile",
                        files=files,
                        data=data
                    )

                    if response.status_code == 200:
                        result = response.json()
                        markdown = result["markdown"]

                        st.success(f"Generated using `{result['model_used']}`")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Preview")
                            st.markdown(markdown)
                        with col2:
                            st.subheader("Raw Markdown")
                            st.code(markdown, language="markdown")

                        st.download_button(
                            label="⬇️ Download README.md",
                            data=markdown,
                            file_name="README.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error(f"Error: {result.json().get('detail', 'Something went wrong.')}")

                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the backend. Make sure it is running on localhost:8000.")