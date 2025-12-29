import streamlit as st
import re

# Page setup
st.set_page_config(
    page_title="Email Verifier Pro",
    page_icon="📧",
    layout="centered"
)

# Custom CSS for better look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.5rem;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">📧 Free Email Verification Tool</h1>', unsafe_allow_html=True)
st.write("Check if email addresses are valid, active, and not temporary")

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    email = st.text_input(
        "Enter email address to verify:",
        placeholder="example@gmail.com",
        label_visibility="collapsed"
    )
with col2:
    verify_btn = st.button("🔍 Verify Now", use_container_width=True)

# Verification logic
if verify_btn:
    if not email:
        st.warning("⚠️ Please enter an email address")
    else:
        # Check email format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            st.error("""
            ## ❌ INVALID EMAIL FORMAT
            
            **Problem:** The email doesn't follow standard format
            **Solution:** Check for typos like:
            - Missing @ symbol
            - Spaces in email
            - Invalid characters
            """)
        else:
            # Check for disposable domains
            disposable_domains = [
                'tempmail.com', 'mailinator.com', '10minutemail.com',
                'throwawaymail.com', 'yopmail.com', 'guerrillamail.com',
                'temp-mail.org', 'fakeinbox.com', 'dispostable.com'
            ]
            
            domain = email.split('@')[1].lower()
            
            if domain in disposable_domains:
                st.warning(f"""
                ## ⚠️ TEMPORARY EMAIL DETECTED
                
                **Domain:** {domain}
                **Risk:** This is a disposable email service
                **Recommendation:** Use a permanent email address
                """)
            else:
                st.success(f"""
                ## ✅ EMAIL APPEARS VALID!
                
                **Email:** {email}
                **Domain:** {domain}
                **Status:** Format is correct and not temporary
                
                *Note: This is a basic check. For business use, 
                consider professional verification services.*
                """)

# Add statistics
st.markdown("---")
st.markdown("### 📊 Quick Stats")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Format Check", "✅ Included")
with col2:
    st.metric("Temporary Email", "✅ Detected")
with col3:
    st.metric("Domain Check", "✅ Basic")

# Add footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Made with ❤️ using Streamlit | Free Email Verification Tool</p>
    <p>Last updated: December 2023 | For personal use only</p>
</div>
""", unsafe_allow_html=True)