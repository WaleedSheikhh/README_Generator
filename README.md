# README Generator
[![GitHub](https://img.shields.io/badge/GitHub-100%25%20Code-blue.svg)](https://github.com/WaleedSheikhh/README_Generator)
[![Python](https://img.shields.io/badge/Python-3.12%20and%20above-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT%202024-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Title & Tagline
README Generator - Automate Your Documentation

## Description
The README Generator is a powerful tool designed to automatically create professional, modern, and engaging README files for your GitHub repositories. Leveraging the capabilities of Large Language Models (LLMs), this project simplifies the process of generating high-quality documentation, making it easier for developers to showcase their work.

## Features
- **README Generation from GitHub URL**: Paste your GitHub repository URL and generate a README file tailored to your project.
- **README Generation from ZIP File**: Upload a ZIP file of your project and receive a custom README.
- **Customizable Sections**: Choose which sections to include in your README, such as Features, Installation, Usage, and more.
- **Tech Stack Identification**: Automatically identifies and lists the tech stack used in your project.

## Tech Stack
- **Backend**: FastAPI, GitPython, Groq
- **Frontend**: Streamlit
- **Dependencies**: httpx, requests

## Installation
To run the README Generator locally, ensure you have Python 3.12 or higher installed. Then, clone the repository:

```bash
git clone https://github.com/WaleedSheikhh/README_Generator.git
cd README_Generator
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Start the application:

```bash
python main.py
```

Navigate to `http://localhost:8000` in your web browser to access the README Generator API.

### API Endpoints
- **`/generate`**: Generate a README from a GitHub repository URL.
- **`/uploadZIPfile`**: Generate a README from a ZIP file.

## Thanks for Reading
