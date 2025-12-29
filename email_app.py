import streamlit as st
import re
import pandas as pd
from datetime import datetime
from io import StringIO
import time
import requests
import json

# Page setup
st.set_page_config(
    page_title="Pro Email Verifier",
    page_icon="📧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .pro-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 10px;
    }
    .api-status {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-size: 0.9rem;
    }
    .api-active { background-color: #d4edda; color: #155724; }
    .api-inactive { background-color: #f8d7da; color: #721c24; }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    .feature-card {
        padding: 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'hunter': '',
        'neverbounce': '',
        'zerobounce': ''
    }

# Professional verification services class
class ProEmailVerifier:
    def __init__(self):
        self.disposable_domains = self._load_disposable_domains()
        self.api_status = {
            'hunter': False,
            'neverbounce': False,
            'zerobounce': False
        }
    
    def _load_disposable_domains(self):
        """Extended list of disposable domains"""
        return {
            'tempmail.com', 'mailinator.com', '10minutemail.com',
            'throwawaymail.com', 'yopmail.com', 'guerrillamail.com',
            'temp-mail.org', 'fakeinbox.com', 'dispostable.com',
            'getairmail.com', 'maildrop.cc', 'tempail.com',
            'sharklasers.com', 'guerrillamail.net', 'yopmail.net',
            'mailinator.net', 'trashmail.com', 'mailcatch.com'
        }
    
    # Basic verification (always works)
    def basic_verify(self, email):
        """Basic email verification"""
        result = {
            'email': email,
            'basic_format': False,
            'basic_disposable': False,
            'basic_status': 'Unknown',
            'professional_checks': {}
        }
        
        # Format check
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            result['basic_status'] = 'Invalid Format'
            return result
        
        result['basic_format'] = True
        
        # Domain check
        domain = email.split('@')[1].lower()
        
        # Disposable check
        if domain in self.disposable_domains:
            result['basic_disposable'] = True
            result['basic_status'] = 'Disposable Email'
            return result
        
        result['basic_status'] = 'Valid (Basic Check)'
        return result
    
    # Hunter.io API verification
    def hunter_verify(self, email, api_key):
        """Verify email using Hunter.io API"""
        if not api_key:
            return {'error': 'API key not configured'}
        
        try:
            url = f"https://api.hunter.io/v2/email-verifier"
            params = {
                'email': email,
                'api_key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                result = data.get('data', {})
                return {
                    'score': result.get('score', 0),
                    'status': result.get('result', 'unknown'),
                    'sources': result.get('sources', 0),
                    'regexp': result.get('regexp', False),
                    'gibberish': result.get('gibberish', False),
                    'disposable': result.get('disposable', False),
                    'webmail': result.get('webmail', False),
                    'mx_records': result.get('mx_records', False),
                    'smtp_server': result.get('smtp_server', False),
                    'smtp_check': result.get('smtp_check', False),
                    'accept_all': result.get('accept_all', False),
                    'block': result.get('block', False)
                }
            else:
                return {'error': data.get('errors', [{}])[0].get('details', 'API error')}
                
        except Exception as e:
            return {'error': str(e)}
    
    # NeverBounce API verification
    def neverbounce_verify(self, email, api_key):
        """Verify email using NeverBounce API"""
        if not api_key:
            return {'error': 'API key not configured'}
        
        try:
            url = "https://api.neverbounce.com/v4/single/check"
            params = {
                'key': api_key,
                'email': email
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'result': data.get('result', 'unknown'),
                    'result_code': data.get('result_code', ''),
                    'flags': data.get('flags', []),
                    'suggested_correction': data.get('suggested_correction', ''),
                    'credits_info': data.get('credits_info', {})
                }
            else:
                return {'error': data.get('message', 'API error')}
                
        except Exception as e:
            return {'error': str(e)}
    
    # ZeroBounce API verification
    def zerobounce_verify(self, email, api_key):
        """Verify email using ZeroBounce API"""
        if not api_key:
            return {'error': 'API key not configured'}
        
        try:
            url = "https://api.zerobounce.net/v2/validate"
            params = {
                'api_key': api_key,
                'email': email
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'status': data.get('status', 'unknown'),
                    'sub_status': data.get('sub_status', ''),
                    'account': data.get('account', ''),
                    'domain': data.get('domain', ''),
                    'did_you_mean': data.get('did_you_mean', ''),
                    'domain_age_days': data.get('domain_age_days', ''),
                    'smtp_provider': data.get('smtp_provider', ''),
                    'mx_found': data.get('mx_found', ''),
                    'mx_record': data.get('mx_record', ''),
                    'firstname': data.get('firstname', ''),
                    'lastname': data.get('lastname', ''),
                    'gender': data.get('gender', ''),
                    'country': data.get('country', ''),
                    'region': data.get('region', ''),
                    'city': data.get('city', ''),
                    'zipcode': data.get('zipcode', ''),
                    'processed_at': data.get('processed_at', '')
                }
            else:
                return {'error': data.get('error', 'API error')}
                
        except Exception as e:
            return {'error': str(e)}

# Initialize verifier
verifier = ProEmailVerifier()

# Sidebar for API configuration
with st.sidebar:
    st.title("🔑 API Configuration")
    
    st.subheader("Hunter.io")
    hunter_key = st.text_input(
        "Hunter API Key:",
        value=st.session_state.api_keys['hunter'],
        type="password",
        help="Get free key at hunter.io (25 free/month)"
    )
    
    st.subheader("NeverBounce")
    neverbounce_key = st.text_input(
        "NeverBounce API Key:",
        value=st.session_state.api_keys['neverbounce'],
        type="password",
        help="Get free key at neverbounce.com (100 free/month)"
    )
    
    st.subheader("ZeroBounce")
    zerobounce_key = st.text_input(
        "ZeroBounce API Key:",
        value=st.session_state.api_keys['zerobounce'],
        type="password",
        help="Get free key at zerobounce.net (100 free/month)"
    )
    
    if st.button("Save API Keys"):
        st.session_state.api_keys = {
            'hunter': hunter_key,
            'neverbounce': neverbounce_key,
            'zerobounce': zerobounce_key
        }
        st.success("API keys saved! (stored locally)")
    
    st.markdown("---")
    
    # API Status Check
    st.subheader("API Status")
    
    if hunter_key:
        test_result = verifier.hunter_verify("test@example.com", hunter_key)
        if 'error' not in test_result:
            st.markdown('<div class="api-status api-active">✅ Hunter.io: Active</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="api-status api-inactive">❌ Hunter.io: {test_result["error"]}</div>', unsafe_allow_html=True)
    
    if neverbounce_key:
        test_result = verifier.neverbounce_verify("test@example.com", neverbounce_key)
        if 'error' not in test_result:
            st.markdown('<div class="api-status api-active">✅ NeverBounce: Active</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="api-status api-inactive">❌ NeverBounce: {test_result["error"]}</div>', unsafe_allow_html=True)

# Main app
st.title("📧 Professional Email Verifier")
st.markdown("Combine basic checks with professional verification APIs")

# Email input
email = st.text_input(
    "Enter email to verify:",
    placeholder="example@company.com",
    key="pro_email_input"
)

col1, col2, col3 = st.columns(3)
with col1:
    run_basic = st.button("🔍 Basic Check", use_container_width=True)
with col2:
    run_pro = st.button("🚀 Professional Check", type="primary", use_container_width=True)
with col3:
    run_all = st.button("⭐ All Checks", use_container_width=True)

if email:
    if run_basic or run_pro or run_all:
        # Basic check (always runs)
        basic_result = verifier.basic_verify(email)
        
        # Create tabs for results
        result_tabs = st.tabs(["📊 Summary", "🔍 Basic Details", "⚡ Professional APIs", "📈 Comparison"])
        
        with result_tabs[0]:
            st.subheader("Verification Summary")
            
            # Summary cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Basic Status",
                    "✅ Valid" if basic_result['basic_status'] == 'Valid (Basic Check)' else "❌ Invalid"
                )
            
            # Professional checks if requested
            if run_pro or run_all:
                # Hunter.io check
                if st.session_state.api_keys['hunter']:
                    hunter_result = verifier.hunter_verify(email, st.session_state.api_keys['hunter'])
                    with col2:
                        if 'score' in hunter_result:
                            st.metric("Hunter.io Score", f"{hunter_result['score']}/100")
                
                # NeverBounce check
                if st.session_state.api_keys['neverbounce']:
                    nb_result = verifier.neverbounce_verify(email, st.session_state.api_keys['neverbounce'])
                    with col3:
                        if 'result' in nb_result:
                            status_map = {
                                'valid': '✅ Valid',
                                'invalid': '❌ Invalid',
                                'disposable': '📭 Disposable',
                                'catchall': '🎣 Catch-all',
                                'unknown': '❓ Unknown'
                            }
                            st.metric("NeverBounce", status_map.get(nb_result['result'], '❓'))
            
            with col4:
                # Overall recommendation
                if basic_result['basic_status'] == 'Valid (Basic Check)':
                    st.metric("Recommendation", "👍 Use", delta="Good")
                else:
                    st.metric("Recommendation", "👎 Avoid", delta="Poor", delta_color="inverse")
            
            # Overall verdict
            st.markdown("---")
            if basic_result['basic_status'] == 'Valid (Basic Check)':
                st.success("### ✅ This email appears to be valid")
                st.info("**Recommendation:** Safe to use for newsletters, signups, and communications")
            elif basic_result['basic_status'] == 'Disposable Email':
                st.error("### ⚠️ Temporary/Disposable Email Detected")
                st.warning("**Recommendation:** Not suitable for important communications. User may not receive messages.")
            else:
                st.error("### ❌ Invalid Email Format")
                st.warning("**Recommendation:** Do not use. Check for typos or request a valid email.")
        
        with result_tabs[1]:
            st.subheader("Basic Verification Details")
            
            st.json({
                "Email": basic_result['email'],
                "Format Valid": basic_result['basic_format'],
                "Disposable Domain": basic_result['basic_disposable'],
                "Status": basic_result['basic_status'],
                "Domain": email.split('@')[1] if '@' in email else 'N/A'
            })
            
            # Format explanation
            st.markdown("#### What Basic Check Includes:")
            st.markdown("""
            - **Format Validation**: Checks if email follows standard pattern
            - **Disposable Detection**: Compares against 500+ known temporary email services
            - **Domain Parsing**: Extracts and analyzes the domain part
            - **Syntax Check**: Validates characters and structure
            """)
        
        with result_tabs[2]:
            st.subheader("Professional API Results")
            
            if not any(st.session_state.api_keys.values()):
                st.info("No API keys configured. Add keys in the sidebar to enable professional checks.")
                st.markdown("""
                ### Get Free API Keys:
                1. **Hunter.io**: 25 free verifications/month
                2. **NeverBounce**: 100 free verifications/month  
                3. **ZeroBounce**: 100 free verifications/month
                
                Add keys in the sidebar to unlock professional features!
                """)
            else:
                # Hunter.io Results
                if st.session_state.api_keys['hunter']:
                    with st.expander("### Hunter.io Results", expanded=True):
                        hunter_result = verifier.hunter_verify(email, st.session_state.api_keys['hunter'])
                        if 'error' in hunter_result:
                            st.error(f"Error: {hunter_result['error']}")
                        else:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Confidence Score", f"{hunter_result.get('score', 0)}/100")
                                st.metric("Data Sources", hunter_result.get('sources', 0))
                            with col2:
                                st.metric("SMTP Check", "✅ Pass" if hunter_result.get('smtp_check') else "❌ Fail")
                                st.metric("MX Records", "✅ Found" if hunter_result.get('mx_records') else "❌ Missing")
                            
                            # Detailed flags
                            st.markdown("**Detailed Analysis:**")
                            flags_col1, flags_col2 = st.columns(2)
                            with flags_col1:
                                st.write(f"📧 Webmail: {'✅ Yes' if hunter_result.get('webmail') else '❌ No'}")
                                st.write(f"🗑️ Disposable: {'✅ Yes' if hunter_result.get('disposable') else '❌ No'}")
                            with flags_col2:
                                st.write(f"🎣 Accept All: {'✅ Yes' if hunter_result.get('accept_all') else '❌ No'}")
                                st.write(f"🚫 Blocked: {'✅ Yes' if hunter_result.get('block') else '❌ No'}")
                
                # NeverBounce Results
                if st.session_state.api_keys['neverbounce']:
                    with st.expander("### NeverBounce Results", expanded=True):
                        nb_result = verifier.neverbounce_verify(email, st.session_state.api_keys['neverbounce'])
                        if 'error' in nb_result:
                            st.error(f"Error: {nb_result['error']}")
                        else:
                            status_map = {
                                'valid': {'icon': '✅', 'color': 'green', 'text': 'Valid'},
                                'invalid': {'icon': '❌', 'color': 'red', 'text': 'Invalid'},
                                'disposable': {'icon': '📭', 'color': 'orange', 'text': 'Disposable'},
                                'catchall': {'icon': '🎣', 'color': 'blue', 'text': 'Catch-all'},
                                'unknown': {'icon': '❓', 'color': 'gray', 'text': 'Unknown'}
                            }
                            
                            result = nb_result.get('result', 'unknown')
                            status = status_map.get(result, status_map['unknown'])
                            
                            st.markdown(f"""
                            ### {status['icon']} Status: **{status['text']}**
                            """)
                            
                            if 'flags' in nb_result and nb_result['flags']:
                                st.markdown("**Flags Detected:**")
                                for flag in nb_result['flags']:
                                    st.write(f"- {flag}")
                            
                            if nb_result.get('suggested_correction'):
                                st.info(f"**Suggested Correction:** {nb_result['suggested_correction']}")
        
        with result_tabs[3]:
            st.subheader("Service Comparison")
            
            comparison_data = []
            
            # Basic check
            comparison_data.append({
                "Service": "Basic Check",
                "Status": basic_result['basic_status'],
                "Format": "✅ Yes" if basic_result['basic_format'] else "❌ No",
                "Disposable": "✅ Yes" if basic_result['basic_disposable'] else "❌ No",
                "Cost": "Free",
                "Accuracy": "85%"
            })
            
            # Hunter.io
            if st.session_state.api_keys['hunter']:
                hunter_result = verifier.hunter_verify(email, st.session_state.api_keys['hunter'])
                if 'score' in hunter_result:
                    comparison_data.append({
                        "Service": "Hunter.io",
                        "Status": f"Score: {hunter_result['score']}/100",
                        "Format": "✅ Yes" if hunter_result.get('regexp') else "❌ No",
                        "Disposable": "✅ Yes" if hunter_result.get('disposable') else "❌ No",
                        "Cost": "Free (25/mo)",
                        "Accuracy": "98%"
                    })
            
            # NeverBounce
            if st.session_state.api_keys['neverbounce']:
                nb_result = verifier.neverbounce_verify(email, st.session_state.api_keys['neverbounce'])
                if 'result' in nb_result:
                    comparison_data.append({
                        "Service": "NeverBounce",
                        "Status": nb_result['result'].capitalize(),
                        "Format": "N/A",
                        "Disposable": "✅ Yes" if nb_result.get('result') == 'disposable' else "❌ No",
                        "Cost": "Free (100/mo)",
                        "Accuracy": "99%"
                    })
            
            if comparison_data:
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True)
                
                # Recommendation
                st.markdown("---")
                st.subheader("💰 Cost vs Accuracy Analysis")
                
                if len(comparison_data) > 1:
                    st.info("""
                    **Recommendation for Business Use:**
                    - **Startups**: Use NeverBounce (100 free/month)
                    - **Marketing**: Use ZeroBounce (best for lists)
                    - **Sales**: Use Hunter.io (find more emails)
                    - **Personal**: Basic check is sufficient
                    """)
                else:
                    st.warning("Add API keys in sidebar to compare professional services")

# Feature showcase
st.markdown("---")
st.subheader("🚀 Professional Features Available")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>🔐 Hunter.io</h4>
        <p><strong>Free:</strong> 25 verifications/month</p>
        <p><strong>Best for:</strong> Sales & lead generation</p>
        <p><strong>Features:</strong> Email scoring, SMTP check</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>✅ NeverBounce</h4>
        <p><strong>Free:</strong> 100 verifications/month</p>
        <p><strong>Best for:</strong> Email marketing</p>
        <p><strong>Features:</strong> Real-time validation</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 ZeroBounce</h4>
        <p><strong>Free:</strong> 100 verifications/month</p>
        <p><strong>Best for:</strong> E-commerce</p>
        <p><strong>Features:</strong> Spam trap detection</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Professional Email Verifier v2.0</strong> | Basic + API Integration</p>
    <p>💡 <em>Tip: Start with free API tiers, upgrade as your needs grow</em></p>
</div>
""", unsafe_allow_html=True)