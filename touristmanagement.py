import streamlit as st
import mysql.connector
import pandas as pd
import hashlib

# 🎨 Sidebar theme
st.sidebar.header("🎨 Customize Theme")
text_color = st.sidebar.color_picker("Pick text color", "#FFFFFF")
background_image_url = "https://i.pinimg.com/736x/e1/d2/8d/e1d28d807962765a81a2a12e476ae2d5.jpg"

# 💅 Styling
st.markdown(f"""
<style>
.stApp {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-attachment: fixed;
    color: {text_color};
    font-weight: bold;
}}
h1 {{ font-size: 40px; font-weight: 900; }}
h2 {{ font-size: 32px; font-weight: 800; }}
h3 {{ font-size: 26px; font-weight: 700; }}
p, span, div, label {{ font-size: 18px; font-weight: 600; }}
.stButton>button {{
    font-size: 20px;
    font-weight: 800;
    padding: 10px 18px;
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)


# ✅ Database Connection
def create_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Adarsh@2005",
            database="tourism_management"
        )
    except:
        st.error("❌ Database connection failed.")
        return None


# ✅ Password Hash
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


# ✅ Logout
def logout():
    st.session_state.clear()
    st.success("👋 Logged out successfully!")
    st.rerun()


# ✅ Login & Signup (Admin + Customer)
def login_signup():
    st.title("🔐 Login / Signup Portal")
    role = st.radio("Select Role", ["Admin", "Customer"])
    action = st.radio("Action", ["Login", "Signup"])

    username = st.text_input("Username / Email")
    password = st.text_input("Password", type="password")

    conn = create_connection()
    cur = conn.cursor()

    # ─────────────── ADMIN LOGIN/SIGNUP ───────────────
    if role == "Admin":
        if action == "Login":
            if st.button("Login"):
                cur.execute("SELECT * FROM Admin WHERE username=%s AND password=%s",
                            (username, hash_password(password)))
                user = cur.fetchone()
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "admin"
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("❌ Invalid Admin credentials")
        else:
            if st.button("Signup"):
                try:
                    cur.execute("INSERT INTO Admin(username,password) VALUES(%s,%s)",
                                (username, hash_password(password)))
                    conn.commit()
                    st.success("✅ Admin registered successfully! Please login.")
                except mysql.connector.Error as e:
                    st.error(f"❌ {e}")

    # ─────────────── CUSTOMER LOGIN/SIGNUP ───────────────
    else:
        if action == "Login":
            if st.button("Login"):
                cur.execute("SELECT * FROM Customer WHERE email=%s AND nationality=%s", (username, password))
                user = cur.fetchone()
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "customer"
                    st.session_state["username"] = user[1]
                    st.session_state["customer_id"] = user[0]
                    st.rerun()
                else:
                    st.error("❌ Invalid Customer credentials (email/nationality)")
        else:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            nationality = st.text_input("Nationality (used as password)")
            if st.button("Signup"):
                try:
                    cur.execute("INSERT INTO Customer(name,email,nationality) VALUES(%s,%s,%s)",
                                (name, email, nationality))
                    conn.commit()
                    st.success("✅ Customer registered successfully! Use email & nationality to log in.")
                except mysql.connector.Error as e:
                    st.error(f"❌ {e}")


# ✅ Stored Procedure: Add Booking
def add_booking_ui():
    st.subheader("🛏️ Add Booking (Procedure)")
    cin = st.date_input("Check-in Date")
    cout = st.date_input("Check-out Date")
    price = st.number_input("Price", min_value=0.0)
    cid = st.number_input("Customer ID", min_value=1)
    hid = st.number_input("Homestay ID", min_value=1)

    if st.button("Add Booking"):
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.callproc("add_booking", (cin, cout, price, cid, hid))
            conn.commit()
            st.success("✅ Booking Added Successfully!")
        except mysql.connector.Error as e:
            st.error(f"❌ {e}")


# ✅ Stored Procedure: Register Payment
def register_payment_ui():
    st.subheader("💳 Register Payment (Procedure)")
    bid = st.number_input("Booking ID", min_value=1)
    pay_type = st.selectbox("Payment Type", ["UPI", "Credit Card", "Debit Card", "Net Banking"])
    amt = st.number_input("Amount", min_value=0.0)
    txn = st.text_input("Transaction ID")

    if st.button("Record Payment"):
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.callproc("register_payment", (bid, pay_type, amt, txn))
            conn.commit()
            st.success("✅ Payment Recorded Successfully!")
        except mysql.connector.Error as e:
            st.error(f"❌ {e}")


# ✅ Function: Stay Duration
def stay_duration_ui():
    st.subheader("📆 Stay Duration Calculator")
    cin = st.date_input("Check-in Date")
    cout = st.date_input("Check-out Date")
    if st.button("Calculate Duration"):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT get_stay_duration(%s,%s)", (cin, cout))
        days = cur.fetchone()[0]
        st.info(f"⏳ Duration: {days} days")


# ✅ Function: Total Payment
def total_payment_ui():
    st.subheader("💰 Total Payment by Customer")
    cid = st.number_input("Customer ID", min_value=1)
    if st.button("Get Total"):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT total_payment_by_customer(%s)", (cid,))
        total = cur.fetchone()[0]
        st.success(f"💸 Total Paid: ₹{total}")


# ✅ Function: Total Revenue by Place
def revenue_by_place_ui():
    st.subheader("🌍 Total Revenue by Tourist Place")
    pid = st.number_input("Place ID", min_value=1)
    if st.button("Get Revenue"):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT total_revenue_by_place(%s)", (pid,))
        rev = cur.fetchone()[0]
        st.success(f"📊 Total Revenue: ₹{rev}")


# ✅ Analytics / Reports
def analytics_ui():
    st.subheader("📊 Reports (Join / Nested / Aggregate)")
    report = st.selectbox("Choose Report", [
        "Top Homestays by Revenue",
        "Customers Above Avg Spending",
        "Bookings + Customer + Homestay + Place"
    ])

    conn = create_connection()
    cur = conn.cursor()

    if report == "Top Homestays by Revenue":
        sql = """
        SELECT h.name AS Homestay, SUM(p.price) AS Total_Revenue
        FROM Homestays h
        JOIN Booking b ON h.homestay_id=b.homestay_id
        JOIN Payment p ON b.booking_id=p.booking_id
        GROUP BY h.name ORDER BY Total_Revenue DESC;
        """
    elif report == "Customers Above Avg Spending":
        sql = """
        SELECT c.name AS Customer, t.total_spent AS Total_Spent
        FROM (
            SELECT b.customer_id, SUM(p.price) AS total_spent
            FROM Booking b JOIN Payment p ON b.booking_id=p.booking_id
            GROUP BY b.customer_id
        ) t
        JOIN Customer c ON c.customer_id=t.customer_id
        WHERE t.total_spent > (
            SELECT AVG(total) FROM (
                SELECT SUM(p2.price) AS total
                FROM Booking b2 JOIN Payment p2 ON b2.booking_id=p2.booking_id
                GROUP BY b2.customer_id
            ) sub
        )
        ORDER BY t.total_spent DESC;
        """
    else:
        sql = """
        SELECT 
            b.booking_id AS Booking_ID,
            c.name AS Customer_Name,
            h.name AS Homestay_Name,
            tp.place_name AS Place_Name,
            b.checkin_date AS CheckIn,
            b.checkout_date AS CheckOut,
            b.price AS Booking_Price
        FROM Booking b
        JOIN Customer c ON b.customer_id=c.customer_id
        JOIN Homestays h ON b.homestay_id=h.homestay_id
        LEFT JOIN Tourist_Place tp ON h.place_id=tp.place_id
        ORDER BY b.booking_id;
        """

    cur.execute(sql)
    data = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    st.dataframe(pd.DataFrame(data, columns=cols), use_container_width=True)


# ✅ CRUD (Admin)
def manage_table(table):
    st.subheader(f"🗂 Manage Table: {table}")
    conn = create_connection()
    cur = conn.cursor()

    action = st.selectbox("Action", ["View", "Add", "Update", "Delete"])

    cur.execute("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA='tourism_management' AND TABLE_NAME=%s
        ORDER BY ORDINAL_POSITION
    """, (table,))
    cols = [c[0] for c in cur.fetchall()]

    cur.execute("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA='tourism_management' AND TABLE_NAME=%s AND CONSTRAINT_NAME='PRIMARY'
    """, (table,))
    pk = cur.fetchone()[0]

    if action == "View":
        cur.execute(f"SELECT * FROM {table}")
        st.dataframe(pd.DataFrame(cur.fetchall(), columns=cols))
    elif action == "Add":
        vals = {c: st.text_input(f"{c}") for c in cols if c != pk}
        if st.button("Insert"):
            q = f"INSERT INTO {table} ({','.join(vals.keys())}) VALUES ({','.join(['%s']*len(vals))})"
            cur.execute(q, list(vals.values()))
            conn.commit()
            st.success("✅ Record Added")
    elif action == "Update":
        idv = st.text_input(f"Enter {pk}")
        vals = {c: st.text_input(f"New {c}") for c in cols if c != pk}
        if st.button("Update"):
            sets = ", ".join([f"{k}=%s" for k, v in vals.items() if v])
            params = [v for v in vals.values() if v]
            cur.execute(f"UPDATE {table} SET {sets} WHERE {pk}=%s", params + [idv])
            conn.commit()
            st.success("✅ Updated Successfully")
    elif action == "Delete":
        idv = st.text_input(f"Enter {pk}")
        if st.button("Delete"):
            cur.execute(f"DELETE FROM {table} WHERE {pk}=%s", (idv,))
            conn.commit()
            st.warning("🚮 Record Deleted")


# ✅ DB Object Viewer (Admin)
def show_db_objects():
    st.subheader("🧠 Database Objects")
    conn = create_connection()
    cur = conn.cursor()
    choice = st.selectbox("Select Type", ["Triggers", "Procedures", "Functions"])
    if choice == "Triggers":
        cur.execute("SHOW TRIGGERS")
    elif choice == "Procedures":
        cur.execute("SHOW PROCEDURE STATUS WHERE Db='tourism_management'")
    else:
        cur.execute("SHOW FUNCTION STATUS WHERE Db='tourism_management'")
    st.dataframe(pd.DataFrame(cur.fetchall()))


# ✅ CUSTOMER HOME
def customer_home():
    st.title(f"🌍 Welcome {st.session_state['username']} (Customer)")
    st.sidebar.button("🚪 Logout", on_click=logout)
    conn = create_connection()
    cur = conn.cursor()

    # ─────────────── Tourist Places ───────────────
    st.subheader("🏞️ Available Tourist Places")
    cur.execute("SELECT place_id, place_name, location, entry_fee FROM Tourist_Place")
    st.dataframe(pd.DataFrame(cur.fetchall(),
                              columns=["Place ID", "Place Name", "Location", "Entry Fee"]),
                 use_container_width=True)

    pid = st.number_input("Enter Place ID to View Homestays", min_value=1)
    if st.button("Show Homestays"):
        cur.execute("""
            SELECT homestay_id, name, price_per_night, rating
            FROM Homestays WHERE place_id=%s
        """, (pid,))
        st.dataframe(pd.DataFrame(cur.fetchall(),
                                  columns=["Homestay ID", "Homestay", "Price/Night", "Rating"]),
                     use_container_width=True)

    # ─────────────── Booking Section ───────────────
    st.subheader("🛏️ Book a Homestay")

    hid = st.number_input("Homestay ID", min_value=1)

    # Fetch price per night
    cur.execute("SELECT price_per_night FROM Homestays WHERE homestay_id=%s", (hid,))
    price_data = cur.fetchone()

    if not price_data:
        st.warning("⚠️ Invalid Homestay ID. Please enter a valid one.")
        return

    price_per_night = float(price_data[0])
    st.info(f"💰 Price per night: ₹{price_per_night}")

    checkin = st.date_input("Check-in Date")
    checkout = st.date_input("Check-out Date")

    # Calculate stay duration
    if checkout <= checkin:
        st.error("❌ Checkout date must be after check-in date.")
        return

    days = (checkout - checkin).days
    total_price = round(price_per_night * days, 2)

    st.write(f"📆 Stay Duration: **{days} nights**")
    st.write(f"💵 Total Price: **₹{total_price}**")

    # ─────────────── Confirm Booking ───────────────
    if st.button("Confirm Booking"):
        try:
            cur.callproc("add_booking", (checkin, checkout, total_price, st.session_state["customer_id"], hid))
            conn.commit()
            st.success(f"✅ Booking Confirmed for ₹{total_price} ({days} nights)")
        except mysql.connector.Error as e:
            st.error(f"❌ {e}")



# ✅ ADMIN HOME
def admin_home():
    st.title(f"👑 Admin Dashboard — {st.session_state['username']}")
    st.sidebar.button("🚪 Logout", on_click=logout)
    menu = st.selectbox("Select Menu", [
        "Tables", "Add Booking (Proc)", "Register Payment (Proc)",
        "Stay Duration (Func)", "Total Payment (Func)",
        "Revenue by Place (Func)", "Analytics / Reports", "DB Objects Viewer"
    ])
    if menu == "Tables":
        t = st.selectbox("Select Table", [
            "Admin","Travel_agents","Packages","Customer","Cust_phone_no",
            "Tourist_Place","Homestays","Booking","Review","Payment"
        ])
        manage_table(t)
    elif menu == "Add Booking (Proc)": add_booking_ui()
    elif menu == "Register Payment (Proc)": register_payment_ui()
    elif menu == "Stay Duration (Func)": stay_duration_ui()
    elif menu == "Total Payment (Func)": total_payment_ui()
    elif menu == "Revenue by Place (Func)": revenue_by_place_ui()
    elif menu == "Analytics / Reports": analytics_ui()
    elif menu == "DB Objects Viewer": show_db_objects()


# ✅ MAIN
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_signup()
else:
    if st.session_state["role"] == "admin":
        admin_home()
    else:
        customer_home()
