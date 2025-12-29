import streamlit as st
import re
import pandas as pd
from datetime import datetime
from io import StringIO
import time

# Page setup
st.set_page_config(
    page_title="Email Verifier Pro",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for better look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0D47A1;
        transform: translateY(-2px);
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1E88E5;
        background-color: #f8f9fa;
    }
    .dark-mode {
        background-color: #0e1117;
        color: white;
    }
    .dark-mode .result-box {
        background-color: #1e1e1e;
        color: white;
    }
    .feature-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 10px 0;
        background-color: white;
    }
    .dark-mode .feature-card {
        background-color: #1e1e1e;
        border-color: #444;
    }
    .stat-card {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Toggle dark mode
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply dark mode if enabled
if st.session_state.dark_mode:
    st.markdown('<div class="dark-mode">', unsafe_allow_html=True)

# Dark mode toggle in sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    if st.button("🌙 Toggle Dark Mode" if not st.session_state.dark_mode else "☀️ Toggle Light Mode"):
        toggle_dark_mode()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 App Info")
    st.info("""
    **Features Included:**
    1. Single email verification
    2. Bulk email upload (CSV/TXT)
    3. Save/download results
    4. Dark/light mode
    """)

# Main app title
st.markdown('<h1 class="main-header">📧 Advanced Email Verifier Pro</h1>', unsafe_allow_html=True)
st.markdown("### Check email validity, detect temporary addresses, and manage bulk lists")

# Feature selection tabs
tab1, tab2, tab3 = st.tabs(["🔍 Single Email", "📁 Bulk Upload", "📊 Results History"])

# Define disposable domains
DISPOSABLE_DOMAINS = {
    'tempmail.com', 'mailinator.com', '10minutemail.com',
    'throwawaymail.com', 'yopmail.com', 'guerrillamail.com',
    'temp-mail.org', 'fakeinbox.com', 'dispostable.com',
    'getairmail.com', 'maildrop.cc', 'tempail.com',
    'sharklasers.com', 'guerrillamail.net', 'yopmail.net'
}

# Initialize session state for results history
if 'verification_history' not in st.session_state:
    st.session_state.verification_history = []

# Function to verify email
def verify_email(email):
    """Verify a single email address"""
    result = {
        'email': email,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'format_valid': False,
        'disposable': False,
        'status': 'Unknown'
    }
    
    # Check format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        result['status'] = 'Invalid Format'
        return result
    
    result['format_valid'] = True
    
    # Check domain
    domain = email.split('@')[1].lower()
    
    # Check if disposable
    if domain in DISPOSABLE_DOMAINS:
        result['disposable'] = True
        result['status'] = 'Disposable Email'
        return result
    
    result['status'] = 'Valid'
    return result

# Tab 1: Single Email Verification
with tab1:
    st.subheader("Verify Single Email Address")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        email = st.text_input(
            "Enter email address:",
            placeholder="example@gmail.com",
            key="single_email_input",
            label_visibility="collapsed"
        )
    with col2:
        verify_single_btn = st.button("🔍 Verify Email", use_container_width=True)
    
    if verify_single_btn:
        if not email:
            st.warning("⚠️ Please enter an email address")
        else:
            with st.spinner("Verifying..."):
                time.sleep(0.5)  # Small delay for UX
                result = verify_email(email)
                
                # Add to history
                st.session_state.verification_history.append(result)
                
                # Display result
                if result['status'] == 'Valid':
                    st.success(f"""
                    ### ✅ EMAIL VERIFIED SUCCESSFULLY
                    
                    **Email:** {result['email']}  
                    **Status:** {result['status']}  
                    **Time:** {result['timestamp']}
                    """)
                elif result['status'] == 'Disposable Email':
                    st.warning(f"""
                    ### ⚠️ TEMPORARY EMAIL DETECTED
                    
                    **Email:** {result['email']}  
                    **Status:** {result['status']}  
                    **Risk:** High - This is a disposable email service
                    """)
                else:
                    st.error(f"""
                    ### ❌ INVALID EMAIL FORMAT
                    
                    **Email:** {result['email']}  
                    **Status:** {result['status']}  
                    **Issue:** Email format is incorrect
                    """)
                
                # Download button for single result
                result_text = f"""Email Verification Result
================================
Email: {result['email']}
Status: {result['status']}
Format Valid: {result['format_valid']}
Disposable: {result['disposable']}
Timestamp: {result['timestamp']}
Verified By: Email Verifier Pro
================================
Note: This is a basic verification. For business use, consider professional services."""
                
                st.download_button(
                    label="📥 Download This Result",
                    data=result_text,
                    file_name=f"email_verification_{result['email'].replace('@', '_at_')}.txt",
                    mime="text/plain"
                )

# Tab 2: Bulk Email Upload
with tab2:
    st.subheader("Bulk Email Verification")
    
    uploaded_file = st.file_uploader(
        "Upload CSV or TXT file with emails",
        type=['csv', 'txt'],
        help="CSV should have 'email' column or one email per line in TXT"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                if 'email' in df.columns:
                    emails = df['email'].dropna().astype(str).tolist()
                else:
                    emails = df.iloc[:, 0].dropna().astype(str).tolist()
            else:  # TXT file
                content = uploaded_file.read().decode("utf-8")
                emails = [line.strip() for line in content.split('\n') if line.strip()]
            
            st.success(f"📁 File loaded successfully! Found {len(emails)} email(s)")
            
            if st.button("🚀 Start Bulk Verification", type="primary"):
                if len(emails) > 100:
                    st.warning(f"⚠️ Large file detected ({len(emails)} emails). Only first 100 will be processed.")
                    emails = emails[:100]
                
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, email in enumerate(emails):
                    result = verify_email(email)
                    results.append(result)
                    
                    # Update progress
                    progress = (i + 1) / len(emails)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing: {i + 1}/{len(emails)} emails")
                
                # Add to history
                st.session_state.verification_history.extend(results)
                
                # Show summary
                st.success(f"✅ Verification complete! Processed {len(results)} emails")
                
                # Create summary
                valid_count = sum(1 for r in results if r['status'] == 'Valid')
                disposable_count = sum(1 for r in results if r['status'] == 'Disposable Email')
                invalid_count = sum(1 for r in results if r['status'] == 'Invalid Format')
                
                # Display stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'<div class="stat-card"><h3>{valid_count}</h3><p>Valid</p></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="stat-card"><h3>{disposable_count}</h3><p>Disposable</p></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="stat-card"><h3>{invalid_count}</h3><p>Invalid</p></div>', unsafe_allow_html=True)
                
                # Create CSV for download
                results_df = pd.DataFrame(results)
                csv_data = results_df.to_csv(index=False)
                
                # Download button for bulk results
                st.download_button(
                    label="📥 Download All Results as CSV",
                    data=csv_data,
                    file_name=f"bulk_email_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Show sample results
                with st.expander("View Sample Results (First 10)"):
                    st.dataframe(results_df.head(10))
                    
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("Make sure your file is properly formatted. For CSV, include an 'email' column.")

# Tab 3: Results History
with tab3:
    st.subheader("Verification History")
    
    if not st.session_state.verification_history:
        st.info("No verification history yet. Verify some emails first!")
    else:
        # Show statistics
        total_verifications = len(st.session_state.verification_history)
        recent_count = len([r for r in st.session_state.verification_history 
                          if datetime.strptime(r['timestamp'], "%Y-%m-%d %H:%M:%S") > 
                          datetime.now().replace(hour=0, minute=0, second=0)])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Verifications", total_verifications)
        with col2:
            st.metric("Today's Verifications", recent_count)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            show_valid = st.checkbox("Show Valid", value=True)
        with col2:
            show_disposable = st.checkbox("Show Disposable", value=True)
        with col3:
            show_invalid = st.checkbox("Show Invalid", value=True)
        
        # Filter history
        filtered_history = []
        for result in st.session_state.verification_history:
            if result['status'] == 'Valid' and show_valid:
                filtered_history.append(result)
            elif result['status'] == 'Disposable Email' and show_disposable:
                filtered_history.append(result)
            elif result['status'] == 'Invalid Format' and show_invalid:
                filtered_history.append(result)
        
        # Display filtered results
        if filtered_history:
            # Convert to DataFrame for display
            history_df = pd.DataFrame(filtered_history)
            
            # Sort by timestamp (newest first)
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            history_df = history_df.sort_values('timestamp', ascending=False)
            
            # Display table
            st.dataframe(
                history_df[['email', 'status', 'timestamp']],
                use_container_width=True,
                column_config={
                    "email": "Email Address",
                    "status": "Status",
                    "timestamp": "Verification Time"
                }
            )
            
            # Download full history
            if st.button("📥 Download Complete History"):
                full_history_df = pd.DataFrame(st.session_state.verification_history)
                csv_history = full_history_df.to_csv(index=False)
                
                st.download_button(
                    label="Click to Download History CSV",
                    data=csv_history,
                    file_name=f"email_verification_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No results match your filter criteria.")

# Sidebar information
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    
    with st.expander("Single Email Check"):
        st.write("""
        1. Enter any email address
        2. Click 'Verify Email'
        3. View results instantly
        4. Download individual report
        """)
    
    with st.expander("Bulk Upload"):
        st.write("""
        1. Prepare CSV/TXT file
        2. Upload via drag & drop
        3. Click 'Start Bulk Verification'
        4. Download all results
        """)
    
    with st.expander("Results History"):
        st.write("""
        1. All verifications are saved
        2. Filter by status
        3. View statistics
        4. Export complete history
        """)
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Tips")
    st.info("""
    - **Max 100 emails** per bulk upload
    - **History saves** until page refresh
    - **Dark mode** saves eye strain
    - **All features are 100% free**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 20px;'>
    <p>🚀 <strong>Advanced Email Verifier Pro</strong> | Built with Streamlit</p>
    <p>✅ 3-in-1 Features | 💯 Free to Use | 🔒 No Data Stored</p>
    <p>Last updated: December 2023 | Version 2.0</p>
</div>
""", unsafe_allow_html=True)

# Close dark mode div if enabled
if st.session_state.dark_mode:
    st.markdown('</div>', unsafe_allow_html=True)