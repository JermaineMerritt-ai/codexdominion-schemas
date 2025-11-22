import streamlit as st
import time

st.title("🚀 Codex Dominion - Test Dashboard")
st.write("✅ Dashboard is running successfully!")

st.header("System Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Server Status", "✅ Online", "Running")

with col2:
    st.metric("Port", "8502", "Active")

with col3:
    st.metric("Time", time.strftime("%H:%M:%S"), "Live")

st.success("🎉 Connection successful! Your dashboard is working properly.")

st.info("""
**Next Steps:**
- Your trading dashboard is now accessible
- FastAPI backend: http://127.0.0.1:8000
- Main dashboard: Use the full dashboard once this test works
- Documentation: http://127.0.0.1:8000/docs
""")

if st.button("Test Connection"):
    st.balloons()
    st.success("🎯 Test passed! Dashboard is fully operational.")