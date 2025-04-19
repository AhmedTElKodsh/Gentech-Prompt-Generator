#!/usr/bin/env python3
"""
Streamlit launcher for the AI Prompt Generator application.
"""

import os
import logging
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Set page config as the first Streamlit command
st.set_page_config(
    page_title="AI Prompt Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import the Streamlit app
from promptgen.web.app import main

# Add a banner at the top of the app
def add_banner():
    st.markdown(
        """
        <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;margin-bottom:10px;">
        <h4 style="color:#4b778d;margin-bottom:0;">AI Prompt Generator</h4>
        <p style="margin-top:0;font-size:0.9em;color:#555;">
        Inspired by <a href="https://github.com/lim-hyo-jeong/Prompt-Enhancer" target="_blank">Prompt-Enhancer</a>, 
        <a href="https://github.com/dair-ai/Prompt-Engineering-Guide" target="_blank">Prompt-Engineering-Guide</a>,
        and other open-source prompt engineering repositories.
        </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    logger.info("Starting Prompt Generator Streamlit application")
    add_banner()
    main() 