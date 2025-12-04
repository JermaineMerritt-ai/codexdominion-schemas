# apps/dashboard/system_optimizer.py
import os
import sys

import streamlit as st

sys.path.append("..")
sys.path.append("../..")
from core.memory_optimizer import (monitor_memory_usage, optimize_memory,
                                   optimize_streamlit_memory)

st.set_page_config(page_title="System Optimizer", layout="wide", page_icon="⚡")
st.title("⚡ Codex System Optimizer")

col1, col2 = st.columns(2)

with col1:
    st.header("🧠 Memory Optimization")

    if st.button("🔥 Optimize Memory", type="primary"):
        with st.spinner("Optimizing memory..."):
            result = optimize_memory()
            optimize_streamlit_memory()

        st.success("Memory optimization complete!")
        st.metric("Memory Saved", f"{result['saved_mb']} MB")
        st.metric("Modules Cleared", result["modules_cleared"])
        st.metric("Cache Cleaned", result["cache_dirs_cleaned"])

    if st.button("📊 Memory Report"):
        memory_stats = monitor_memory_usage()

        st.subheader("System Memory")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total RAM", f"{memory_stats['total_gb']} GB")
        with col_b:
            st.metric("Available", f"{memory_stats['available_gb']} GB")
        with col_c:
            st.metric("Usage", f"{memory_stats['percent']:.1f}%")

        st.subheader("Top Memory Consumers")
        for proc in memory_stats["top_processes"][:8]:
            st.write(
                f"**{proc['name']}**: {proc['memory_mb']} MB ({proc['memory_percent']}%)"
            )

with col2:
    st.header("🧹 System Cleanup")

    if st.button("Clear Streamlit Cache"):
        optimize_streamlit_memory()
        st.success("Streamlit cache cleared!")

    if st.button("Clean Python Cache"):
        import shutil
        from pathlib import Path

        cleaned = 0
        for pycache in Path("../../").rglob("__pycache__"):
            try:
                shutil.rmtree(pycache, ignore_errors=True)
                cleaned += 1
            except:
                pass

        st.success(f"Cleaned {cleaned} cache directories!")

    if st.button("Force Garbage Collection"):
        import gc

        collected = gc.collect()
        st.success(f"Collected {collected} objects!")

st.divider()
st.header("⚙️ Performance Tips")
st.markdown(
    """
**Memory Optimization Strategies:**
- 🔄 Regular garbage collection
- 🧹 Clear unused module cache
- 📦 Optimize large data structures
- ⏱️ Use generators for large datasets
- 🎯 Profile memory usage regularly

**System Performance:**
- Close unused browser tabs
- Restart VS Code instances periodically
- Monitor background processes
- Use virtual environments efficiently
"""
)

# Auto-refresh every 30 seconds for memory monitoring
if st.checkbox("Auto-refresh (30s)"):
    st.rerun()
