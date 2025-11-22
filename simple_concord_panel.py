import streamlit as st
import json

# Load accounts
def load_accounts():
    with open("accounts.json", "r") as f:
        return json.load(f)

def save_accounts(data):
    with open("accounts.json", "w") as f:
        json.dump(data, f, indent=4)

st.title("🌟 Custodian–Heirs Concord Panel")

accounts = load_accounts()

# Tabs for Custodian, Heir, Customer
tab1, tab2, tab3 = st.tabs(["Custodians", "Heirs", "Customers"])

with tab1:
    st.header("Custodians")
    for c in accounts["custodians"]:
        st.write(f"🛡 {c['name']} — {c['status']}")

with tab2:
    st.header("Heirs")
    for h in accounts["heirs"]:
        st.write(f"🌱 {h['name']} — {h['status']}")
    new_heir = st.text_input("Add New Heir")
    if st.button("Induct Heir"):
        accounts["heirs"].append({"id": f"HEIR{len(accounts['heirs'])+1:03}", "name": new_heir, "role": "Heir", "status": "inducted"})
        save_accounts(accounts)
        st.success(f"Heir {new_heir} inducted!")

with tab3:
    st.header("Customers")
    for cu in accounts["customers"]:
        st.write(f"🌍 {cu['name']} — {cu['status']}")
    new_customer = st.text_input("Add New Customer")
    if st.button("Welcome Customer"):
        accounts["customers"].append({"id": f"CUSTM{len(accounts['customers'])+1:03}", "name": new_customer, "role": "Customer", "status": "welcomed"})
        save_accounts(accounts)
        st.success(f"Customer {new_customer} welcomed!")