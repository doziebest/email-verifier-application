import streamlit as st
import re

st.set_page_config(page_title="Email Verifier", page_icon="📧")

st.title("📧 Free Email Verification App")
st.write("Check if email addresses are valid and active")

# Input
email = st.text_input("Enter email address:", placeholder="example@gmail.com")

if st.button("Verify Email"):
    if email:
        # Simple format check
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            st.success("✅ Valid email format!")
            
            # Check for common disposable emails
            disposable_domains = ['tempmail.com', 'mailinator.com', '10minutemail.com']
            domain = email.split('@')[1]
            
            if domain in disposable_domains:
                st.warning("⚠️ This looks like a disposable/temporary email")
            else:
                st.info("📧 Email appears to be valid!")
                st.write("Note: This is a basic check. For 100% accuracy, consider paid services.")
        else:
            st.error("❌ Invalid email format")
    else:
        st.warning("Please enter an email address")

# Add some info
st.markdown("---")
st.markdown("""
### How it works:
1. **Format Check** - Validates email structure
2. **Domain Check** - Identifies temporary email services

### What we DON'T check (free limitations):
- Actual mailbox existence
- Corporate/private email systems
- Real-time delivery verification
""")
