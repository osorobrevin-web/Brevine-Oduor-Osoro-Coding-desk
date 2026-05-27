"""
╔══════════════════════════════════════════════════════════════════╗
║          TICKETZETU — Powered by BReSCA                          ║
║          ADMIN DASHBOARD                                         ║
║          Brevine e-Systems Consultancy Agency, Kisumu Kenya      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import csv
import os
import uuid
import hashlib
from datetime import datetime, date

# ─────────────────────────────────────────────
#  SHARED FILE PATHS  (same as client.py & customer.py)
# ─────────────────────────────────────────────
CLIENTS_FILE        = "clients.csv"
EVENTS_FILE         = "events.csv"
TICKETS_FILE        = "tickets.csv"
CANCELLATIONS_FILE  = "cancellations.csv"
CUSTOMERS_FILE      = "customers.csv"
REVIEWS_FILE        = "reviews.csv"
ADMINS_FILE         = "admins.csv"
PAYOUTS_FILE        = "payouts.csv"

# ─────────────────────────────────────────────
#  BRESCA FEE RULES  (must match client.py & customer.py)
# ─────────────────────────────────────────────
MPESA_TRANSACTION_COST = 10

def bresca_commission(price: float) -> float:
    if price == 0:
        return 0
    elif price <= 500:
        return 50
    elif price <= 2000:
        return price * 0.08
    elif price <= 5000:
        return price * 0.07
    else:
        return price * 0.06


# ══════════════════════════════════════════════
#  CSV HELPERS
# ══════════════════════════════════════════════

def ensure_file(filepath: str, headers: list):
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def read_csv(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(filepath: str, rows: list, headers: list):
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def append_csv(filepath: str, row: dict, headers: list):
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# ══════════════════════════════════════════════
#  CSV HEADERS
# ══════════════════════════════════════════════

ADMIN_HEADERS = [
    "admin_id", "full_name", "phone", "email",
    "password_hash", "role", "status", "created_date"
]

CLIENT_HEADERS = [
    "client_id", "business_name", "owner_name", "phone",
    "email", "password_hash", "plan", "status", "joined_date"
]

EVENT_HEADERS = [
    "event_id", "client_id", "event_name", "event_date",
    "event_time", "venue", "description", "poster",
    "status",
    "vvvip_price", "vvvip_seats",
    "vip_price",   "vip_seats",
    "regular_price","regular_seats",
    "cancel_by_date",
    "refund_percent",
    "created_date"
]

TICKET_HEADERS = [
    "ticket_no", "client_id", "event_id", "event_name",
    "customer_name", "phone", "id_number", "email",
    "category", "price", "commission", "transaction_cost",
    "payment_status", "wristband_qr",
    "first_entry", "entry_time", "attended",
    "refund_amount", "refund_status", "purchase_date"
]

CANCELLATION_HEADERS = [
    "cancel_id", "ticket_no", "event_id", "client_id",
    "customer_name", "phone", "category", "price",
    "refund_percent", "refundable_amount",
    "reason",
    "status",
    "client_action_date", "client_note",
    "admin_action_date",  "admin_note",
    "request_date"
]

CUSTOMER_HEADERS = [
    "customer_id", "full_name", "phone", "id_number",
    "email", "password_hash", "status", "joined_date"
]

REVIEW_HEADERS = [
    "review_id", "ticket_no", "event_id", "event_name",
    "customer_name", "phone", "rating", "comment", "review_date"
]

PAYOUT_HEADERS = [
    "payout_id", "client_id", "business_name", "amount",
    "method", "status", "requested_date", "processed_date", "admin_note"
]


# ══════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ══════════════════════════════════════════════

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 60)
    print("   TICKETZETU — Powered by BReSCA")
    print("   ⚙  BRESCA ADMIN DASHBOARD")
    print("   Brevine e-Systems Consultancy Agency | Kisumu, Kenya")
    print("=" * 60)


def divider():
    print("-" * 60)


def pause():
    input("\nPress ENTER to continue...")


def today_str() -> str:
    return date.today().strftime("%Y-%m-%d")


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ══════════════════════════════════════════════
#  INITIALISE ALL CSV FILES
# ══════════════════════════════════════════════

def init_files():
    ensure_file(ADMINS_FILE,        ADMIN_HEADERS)
    ensure_file(CLIENTS_FILE,       CLIENT_HEADERS)
    ensure_file(EVENTS_FILE,        EVENT_HEADERS)
    ensure_file(TICKETS_FILE,       TICKET_HEADERS)
    ensure_file(CANCELLATIONS_FILE, CANCELLATION_HEADERS)
    ensure_file(CUSTOMERS_FILE,     CUSTOMER_HEADERS)
    ensure_file(REVIEWS_FILE,       REVIEW_HEADERS)
    ensure_file(PAYOUTS_FILE,       PAYOUT_HEADERS)


# ══════════════════════════════════════════════
#  SEED DEFAULT SUPER ADMIN
# ══════════════════════════════════════════════

def seed_super_admin():
    """
    Create the default BReSCA super admin on first run if no admins exist.
    Credentials:  Phone: 0700000000  |  Password: bresca2026
    CHANGE PASSWORD immediately after first login!
    """
    admins = read_csv(ADMINS_FILE)
    if admins:
        return  # Already seeded

    super_admin = {
        "admin_id":      "BRESCA-01",
        "full_name":     "BReSCA Super Admin",
        "phone":         "0700000000",
        "email":         "admin@bresca.co.ke",
        "password_hash": hash_password("bresca2026"),
        "role":          "SUPER_ADMIN",
        "status":        "ACTIVE",
        "created_date":  today_str()
    }
    append_csv(ADMINS_FILE, super_admin, ADMIN_HEADERS)
    print("\n  ℹ  Default super admin created.")
    print("     Phone: 0700000000  |  Password: bresca2026")
    print("     ⚠  Change password immediately after login!")
    pause()


# ══════════════════════════════════════════════
#  AUTH — LOGIN
# ══════════════════════════════════════════════

def login_admin() -> dict | None:
    clear()
    banner()
    print("\n  ADMIN LOGIN\n")
    divider()

    phone    = input("  Phone Number: ").strip()
    password = input("  Password: ").strip()

    admins = read_csv(ADMINS_FILE)
    for a in admins:
        if a["phone"] == phone and a["password_hash"] == hash_password(password):
            if a["status"] != "ACTIVE":
                print(f"\n⚠  Your account is {a['status']}. Contact support.")
                pause()
                return None
            print(f"\n✅ Welcome, {a['full_name']} ({a['role']})")
            pause()
            return a

    print("\n⚠  Invalid phone number or password.")
    pause()
    return None


# ══════════════════════════════════════════════
#  ADMIN ACCOUNT MANAGEMENT
# ══════════════════════════════════════════════

def create_admin(admin: dict):
    """SUPER_ADMIN only — create a new admin account."""
    if admin["role"] != "SUPER_ADMIN":
        print("\n⚠  Only Super Admins can create admin accounts.")
        pause()
        return

    clear()
    banner()
    print("\n  CREATE ADMIN ACCOUNT\n")
    divider()

    full_name = input("  Full Name: ").strip()
    phone     = input("  Phone Number: ").strip()
    email     = input("  Email Address: ").strip()

    # Check phone not already registered
    admins = read_csv(ADMINS_FILE)
    for a in admins:
        if a["phone"] == phone:
            print("\n⚠  An admin with this phone number already exists.")
            pause()
            return

    print("\n  Role:")
    print("  [1] ADMIN       — Standard admin access")
    print("  [2] SUPER_ADMIN — Full system access")
    role_choice = input("  Select role (1 or 2): ").strip()
    role = "SUPER_ADMIN" if role_choice == "2" else "ADMIN"

    password  = input("\n  Set Password: ").strip()
    password2 = input("  Confirm Password: ").strip()
    if password != password2:
        print("\n⚠  Passwords do not match.")
        pause()
        return

    admin_id = f"ADM-{str(uuid.uuid4())[:6].upper()}"

    new_admin = {
        "admin_id":      admin_id,
        "full_name":     full_name,
        "phone":         phone,
        "email":         email,
        "password_hash": hash_password(password),
        "role":          role,
        "status":        "ACTIVE",
        "created_date":  today_str()
    }

    append_csv(ADMINS_FILE, new_admin, ADMIN_HEADERS)
    print(f"\n✅ Admin account created!")
    print(f"   Admin ID : {admin_id}")
    print(f"   Role     : {role}")
    pause()


def view_all_admins(admin: dict):
    if admin["role"] != "SUPER_ADMIN":
        print("\n⚠  Access denied.")
        pause()
        return

    clear()
    banner()
    print("\n  ALL ADMIN ACCOUNTS\n")
    divider()

    admins = read_csv(ADMINS_FILE)
    if not admins:
        print("  No admin accounts found.")
        pause()
        return

    for a in admins:
        print(f"\n  Admin ID  : {a['admin_id']}")
        print(f"  Name      : {a['full_name']}")
        print(f"  Phone     : {a['phone']}")
        print(f"  Email     : {a['email']}")
        print(f"  Role      : {a['role']}")
        print(f"  Status    : {a['status']}")
        print(f"  Created   : {a['created_date']}")
        divider()
    pause()


def change_admin_password(admin: dict) -> dict:
    clear()
    banner()
    print(f"\n  CHANGE PASSWORD\n")
    divider()

    old_pw = input("  Current Password: ").strip()
    if hash_password(old_pw) != admin["password_hash"]:
        print("⚠  Incorrect current password.")
        pause()
        return admin

    new_pw  = input("  New Password: ").strip()
    new_pw2 = input("  Confirm New Password: ").strip()
    if new_pw != new_pw2:
        print("⚠  Passwords do not match.")
        pause()
        return admin

    admins  = read_csv(ADMINS_FILE)
    updated = []
    for a in admins:
        if a["admin_id"] == admin["admin_id"]:
            a["password_hash"] = hash_password(new_pw)
            admin = a
        updated.append(a)
    write_csv(ADMINS_FILE, updated, ADMIN_HEADERS)

    print("✅ Password changed successfully.")
    pause()
    return admin


# ══════════════════════════════════════════════
#  CLIENT MANAGEMENT
# ══════════════════════════════════════════════

def view_all_clients():
    clear()
    banner()
    print("\n  ALL REGISTERED CLIENTS\n")
    divider()

    clients = read_csv(CLIENTS_FILE)
    if not clients:
        print("  No clients registered yet.")
        pause()
        return

    for i, c in enumerate(clients, 1):
        events    = [e for e in read_csv(EVENTS_FILE) if e["client_id"] == c["client_id"]]
        tickets   = [t for t in read_csv(TICKETS_FILE) if t["client_id"] == c["client_id"]
                     and t["payment_status"] == "PAID"]
        gross     = sum(float(t["price"]) for t in tickets)
        commission= sum(float(t["commission"]) for t in tickets)

        print(f"\n  [{i}] {c['business_name'].upper()}")
        print(f"       Client ID  : {c['client_id']}")
        print(f"       Owner      : {c['owner_name']}")
        print(f"       Phone      : {c['phone']}")
        print(f"       Email      : {c['email']}")
        print(f"       Plan       : {c['plan']}")
        print(f"       Status     : {c['status']}")
        print(f"       Joined     : {c['joined_date']}")
        print(f"       Events     : {len(events)}")
        print(f"       Tickets    : {len(tickets)}  |  Gross: KES {gross:,.0f}  |  BReSCA Earned: KES {commission:,.0f}")
        divider()
    pause()


def manage_client_status():
    clear()
    banner()
    print("\n  MANAGE CLIENT STATUS\n")
    divider()

    clients = read_csv(CLIENTS_FILE)
    if not clients:
        print("  No clients found.")
        pause()
        return

    for i, c in enumerate(clients, 1):
        print(f"  [{i}] {c['business_name']} — {c['phone']} [{c['status']}]")

    choice = input("\n  Select client: ").strip()
    try:
        selected = clients[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Client  : {selected['business_name']}")
    print(f"  Current : {selected['status']}")
    print("\n  Set Status:")
    print("  [1] ACTIVE")
    print("  [2] SUSPENDED")
    print("  [3] BLACKLISTED")
    action = input("  Select (1/2/3): ").strip()

    status_map = {"1": "ACTIVE", "2": "SUSPENDED", "3": "BLACKLISTED"}
    new_status = status_map.get(action)
    if not new_status:
        print("⚠  Invalid choice.")
        pause()
        return

    updated = []
    for c in clients:
        if c["client_id"] == selected["client_id"]:
            c["status"] = new_status
        updated.append(c)
    write_csv(CLIENTS_FILE, updated, CLIENT_HEADERS)

    print(f"\n✅ {selected['business_name']} status set to {new_status}.")
    print(f"   [SIMULATED] Notification SMS sent to {selected['phone']}.")
    pause()


def manage_client_plan():
    clear()
    banner()
    print("\n  CHANGE CLIENT SUBSCRIPTION PLAN\n")
    divider()

    clients = read_csv(CLIENTS_FILE)
    if not clients:
        print("  No clients found.")
        pause()
        return

    for i, c in enumerate(clients, 1):
        print(f"  [{i}] {c['business_name']} — Plan: {c['plan']} [{c['status']}]")

    choice = input("\n  Select client: ").strip()
    try:
        selected = clients[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Client : {selected['business_name']}")
    print(f"  Current Plan: {selected['plan']}")
    print("\n  Available Plans:")
    print("  [1] Starter   — KES 2,000/month (up to 3 events)")
    print("  [2] Growth    — KES 5,000/month (up to 10 events)")
    print("  [3] Pro       — KES 10,000/month (unlimited events)")
    print("  [4] Enterprise — Custom")
    plan_map = {"1": "Starter", "2": "Growth", "3": "Pro", "4": "Enterprise"}
    plan_choice = input("  Select plan (1-4): ").strip()
    new_plan = plan_map.get(plan_choice)

    if not new_plan:
        print("⚠  Invalid selection.")
        pause()
        return

    updated = []
    for c in clients:
        if c["client_id"] == selected["client_id"]:
            c["plan"] = new_plan
        updated.append(c)
    write_csv(CLIENTS_FILE, updated, CLIENT_HEADERS)

    print(f"\n✅ {selected['business_name']} plan updated to {new_plan}.")
    pause()


# ══════════════════════════════════════════════
#  EVENT OVERSIGHT
# ══════════════════════════════════════════════

def view_all_events():
    clear()
    banner()
    print("\n  ALL EVENTS — PLATFORM-WIDE\n")
    divider()

    events  = read_csv(EVENTS_FILE)
    clients = read_csv(CLIENTS_FILE)

    if not events:
        print("  No events found on the platform.")
        pause()
        return

    for i, e in enumerate(events, 1):
        organiser = next((c["business_name"] for c in clients
                          if c["client_id"] == e["client_id"]), "Unknown")
        tickets   = [t for t in read_csv(TICKETS_FILE) if t["event_id"] == e["event_id"]
                     and t["payment_status"] == "PAID"]
        gross     = sum(float(t["price"]) for t in tickets)

        print(f"\n  [{i}] {e['event_name'].upper()}")
        print(f"       Organiser : {organiser}")
        print(f"       Date      : {e['event_date']} at {e['event_time']}")
        print(f"       Venue     : {e['venue']}")
        print(f"       Status    : {e['status']}")
        print(f"       Tickets   : {len(tickets)}  |  Gross: KES {gross:,.0f}")
        divider()
    pause()


def force_event_status():
    """Admin can override any event status."""
    clear()
    banner()
    print("\n  FORCE EVENT STATUS\n")
    divider()

    events  = read_csv(EVENTS_FILE)
    clients = read_csv(CLIENTS_FILE)

    if not events:
        print("  No events found.")
        pause()
        return

    for i, e in enumerate(events, 1):
        organiser = next((c["business_name"] for c in clients
                          if c["client_id"] == e["client_id"]), "Unknown")
        print(f"  [{i}] {e['event_name']} | {organiser} [{e['status']}]")

    choice = input("\n  Select event: ").strip()
    try:
        selected = events[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Event   : {selected['event_name']}")
    print(f"  Current : {selected['status']}")
    print("\n  Set Status:")
    print("  [1] ACTIVE")
    print("  [2] INACTIVE")
    print("  [3] COMPLETED")
    action = input("  Select (1/2/3): ").strip()
    status_map = {"1": "ACTIVE", "2": "INACTIVE", "3": "COMPLETED"}
    new_status = status_map.get(action)

    if not new_status:
        print("⚠  Invalid choice.")
        pause()
        return

    updated = []
    for e in events:
        if e["event_id"] == selected["event_id"]:
            e["status"] = new_status
        updated.append(e)
    write_csv(EVENTS_FILE, updated, EVENT_HEADERS)

    print(f"\n✅ Event '{selected['event_name']}' status set to {new_status}.")
    pause()


# ══════════════════════════════════════════════
#  CUSTOMER MANAGEMENT
# ══════════════════════════════════════════════

def view_all_customers():
    clear()
    banner()
    print("\n  ALL REGISTERED CUSTOMERS\n")
    divider()

    customers = read_csv(CUSTOMERS_FILE)
    if not customers:
        print("  No customers registered yet.")
        pause()
        return

    print(f"  Total Customers: {len(customers)}\n")
    for i, c in enumerate(customers, 1):
        tickets = [t for t in read_csv(TICKETS_FILE) if t["phone"] == c["phone"]]
        print(f"  [{i}] {c['full_name']}")
        print(f"       Phone   : {c['phone']}  |  ID: {c['id_number']}")
        print(f"       Status  : {c['status']}  |  Joined: {c['joined_date']}")
        print(f"       Tickets : {len(tickets)}")
        divider()
    pause()


def manage_customer_status():
    clear()
    banner()
    print("\n  MANAGE CUSTOMER STATUS\n")
    divider()

    customers = read_csv(CUSTOMERS_FILE)
    if not customers:
        print("  No customers found.")
        pause()
        return

    search = input("  Search by phone or name: ").strip().lower()
    matches = [c for c in customers
               if search in c["phone"].lower() or search in c["full_name"].lower()]

    if not matches:
        print("  No matching customers found.")
        pause()
        return

    for i, c in enumerate(matches, 1):
        print(f"  [{i}] {c['full_name']} — {c['phone']} [{c['status']}]")

    choice = input("\n  Select customer: ").strip()
    try:
        selected = matches[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Customer : {selected['full_name']}")
    print(f"  Current  : {selected['status']}")
    print("\n  Set Status:")
    print("  [1] ACTIVE")
    print("  [2] SUSPENDED")
    print("  [3] BLACKLISTED")
    action = input("  Select (1/2/3): ").strip()
    status_map = {"1": "ACTIVE", "2": "SUSPENDED", "3": "BLACKLISTED"}
    new_status = status_map.get(action)

    if not new_status:
        print("⚠  Invalid choice.")
        pause()
        return

    updated = []
    for c in customers:
        if c["customer_id"] == selected["customer_id"]:
            c["status"] = new_status
        updated.append(c)
    write_csv(CUSTOMERS_FILE, updated, CUSTOMER_HEADERS)

    print(f"\n✅ {selected['full_name']} status set to {new_status}.")
    pause()


# ══════════════════════════════════════════════
#  TICKET MANAGEMENT
# ══════════════════════════════════════════════

def view_all_tickets():
    clear()
    banner()
    print("\n  ALL TICKETS — PLATFORM-WIDE\n")
    divider()

    tickets = read_csv(TICKETS_FILE)
    if not tickets:
        print("  No tickets issued yet.")
        pause()
        return

    print(f"  Total Tickets: {len(tickets)}\n")
    paid         = [t for t in tickets if t["payment_status"] == "PAID"]
    complimentary= [t for t in tickets if t["payment_status"] == "COMPLIMENTARY"]
    blacklisted  = [t for t in tickets if t["payment_status"] == "BLACKLISTED"]

    print(f"  Paid         : {len(paid)}")
    print(f"  Complimentary: {len(complimentary)}")
    print(f"  Blacklisted  : {len(blacklisted)}")
    divider()

    # Show last 20 tickets
    print("  RECENT TICKETS (last 20)\n")
    for t in tickets[-20:]:
        print(f"  {t['ticket_no']}  |  {t['event_name'][:25]:<25}  |  {t['category']:<8}  |  {t['customer_name'][:20]:<20}  |  {t['payment_status']}")
    pause()


def search_ticket():
    clear()
    banner()
    print("\n  SEARCH TICKET\n")
    divider()

    query = input("  Enter Ticket No, Phone or ID Number: ").strip().upper()
    tickets = read_csv(TICKETS_FILE)

    results = [t for t in tickets
               if query in t["ticket_no"].upper()
               or query in t["phone"]
               or query in t["id_number"]]

    if not results:
        print("  No matching tickets found.")
        pause()
        return

    for t in results:
        print(f"\n  Ticket No  : {t['ticket_no']}")
        print(f"  Event      : {t['event_name']}")
        print(f"  Customer   : {t['customer_name']}  |  {t['phone']}")
        print(f"  ID Number  : {t['id_number']}")
        print(f"  Category   : {t['category']}  |  KES {float(t['price']):,.0f}")
        print(f"  Status     : {t['payment_status']}")
        print(f"  Attended   : {t['attended']}  |  Entry: {t['entry_time'] or 'N/A'}")
        print(f"  Refund     : {t['refund_status']}")
        print(f"  Purchased  : {t['purchase_date']}")
        divider()
    pause()


def admin_blacklist_ticket():
    clear()
    banner()
    print("\n  BLACKLIST / UNBLACKLIST TICKET\n")
    divider()

    ticket_no = input("  Enter Ticket Number: ").strip().upper()
    tickets   = read_csv(TICKETS_FILE)
    ticket    = next((t for t in tickets if t["ticket_no"] == ticket_no), None)

    if not ticket:
        print("⚠  Ticket not found.")
        pause()
        return

    print(f"\n  Ticket  : {ticket['ticket_no']}")
    print(f"  Event   : {ticket['event_name']}")
    print(f"  Customer: {ticket['customer_name']} — {ticket['phone']}")
    print(f"  Status  : {ticket['payment_status']}")
    print("\n  [1] Blacklist Ticket")
    print("  [2] Restore to PAID")
    print("  [3] Cancel (no action)")
    action = input("  Select (1/2/3): ").strip()

    if action == "1":
        new_status = "BLACKLISTED"
    elif action == "2":
        new_status = "PAID"
    else:
        print("  No action taken.")
        pause()
        return

    updated = []
    for t in tickets:
        if t["ticket_no"] == ticket_no:
            t["payment_status"] = new_status
        updated.append(t)
    write_csv(TICKETS_FILE, updated, TICKET_HEADERS)

    print(f"\n✅ Ticket {ticket_no} status set to {new_status}.")
    pause()


# ══════════════════════════════════════════════
#  CANCELLATION PROCESSING  (admin final step)
# ══════════════════════════════════════════════

def view_cancellations():
    clear()
    banner()
    print("\n  ALL CANCELLATION REQUESTS\n")
    divider()

    cancellations = read_csv(CANCELLATIONS_FILE)
    if not cancellations:
        print("  No cancellation requests found.")
        pause()
        return

    # Summary counts
    pending_admin = [c for c in cancellations if c["status"] == "CLIENT_APPROVED"]
    all_pending   = [c for c in cancellations if c["status"] == "PENDING"]
    refunded      = [c for c in cancellations if c["status"] == "REFUNDED"]

    print(f"  Awaiting Client Review  : {len(all_pending)}")
    print(f"  Awaiting Admin Approval : {len(pending_admin)}")
    print(f"  Refunded                : {len(refunded)}")
    print(f"  Total Requests          : {len(cancellations)}\n")
    divider()

    for c in cancellations:
        print(f"  Cancel ID  : {c['cancel_id']}")
        print(f"  Ticket No  : {c['ticket_no']}")
        print(f"  Customer   : {c['customer_name']} — {c['phone']}")
        print(f"  Category   : {c['category']}  |  KES {float(c['price']):,.0f}")
        print(f"  Refund Due : KES {float(c['refundable_amount']):,.2f}")
        print(f"  Reason     : {c['reason']}")
        print(f"  Status     : {c['status']}")
        print(f"  Requested  : {c['request_date']}")
        if c["client_note"]:
            print(f"  Client Note: {c['client_note']}")
        if c["admin_note"]:
            print(f"  Admin Note : {c['admin_note']}")
        divider()
    pause()


def process_cancellation():
    """Admin final approval/rejection for CLIENT_APPROVED cancellations."""
    clear()
    banner()
    print("\n  PROCESS CANCELLATIONS — ADMIN FINAL APPROVAL\n")
    divider()

    cancellations = read_csv(CANCELLATIONS_FILE)
    pending = [c for c in cancellations if c["status"] == "CLIENT_APPROVED"]

    if not pending:
        print("  No cancellations awaiting admin approval.")
        print("  (Only requests already approved by the client organiser appear here.)")
        pause()
        return

    for i, c in enumerate(pending, 1):
        print(f"\n  [{i}]")
        print(f"       Cancel ID  : {c['cancel_id']}")
        print(f"       Ticket No  : {c['ticket_no']}")
        print(f"       Customer   : {c['customer_name']} — {c['phone']}")
        print(f"       Category   : {c['category']}  |  KES {float(c['price']):,.0f}")
        print(f"       Refund Due : KES {float(c['refundable_amount']):,.2f}")
        print(f"       Reason     : {c['reason']}")
        print(f"       Requested  : {c['request_date']}")
        if c["client_note"]:
            print(f"       Client Note: {c['client_note']}")

    choice = input("\n  Select request to process: ").strip()
    try:
        selected = pending[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Processing: {selected['cancel_id']}")
    print("  [1] Approve & Trigger Refund")
    print("  [2] Reject")
    action = input("  Your decision (1 or 2): ").strip()
    note   = input("  Admin note (optional): ").strip()

    updated_cancellations = []
    for c in cancellations:
        if c["cancel_id"] == selected["cancel_id"]:
            if action == "1":
                c["status"]            = "REFUNDED"
                c["admin_action_date"] = now_str()
                c["admin_note"]        = note

                # Mark ticket as refunded
                all_tickets = read_csv(TICKETS_FILE)
                t_updated   = []
                for t in all_tickets:
                    if t["ticket_no"] == c["ticket_no"]:
                        t["refund_status"]  = "REFUNDED"
                        t["refund_amount"]  = c["refundable_amount"]
                        t["payment_status"] = "REFUNDED"
                    t_updated.append(t)
                write_csv(TICKETS_FILE, t_updated, TICKET_HEADERS)

                print(f"\n✅ Refund APPROVED.")
                print(f"   [SIMULATED] KES {float(c['refundable_amount']):,.2f} sent via MPESA to {c['phone']}.")
                print(f"   [SIMULATED] Confirmation SMS sent to {c['phone']}.")

            elif action == "2":
                c["status"]            = "ADMIN_REJECTED"
                c["admin_action_date"] = now_str()
                c["admin_note"]        = note

                # Reset ticket refund status
                all_tickets = read_csv(TICKETS_FILE)
                t_updated   = []
                for t in all_tickets:
                    if t["ticket_no"] == c["ticket_no"]:
                        t["refund_status"] = "REJECTED"
                    t_updated.append(t)
                write_csv(TICKETS_FILE, t_updated, TICKET_HEADERS)

                print(f"\n✅ Cancellation REJECTED.")
                print(f"   [SIMULATED] Customer {c['phone']} has been notified.")
            else:
                print("⚠  Invalid choice. No action taken.")
                pause()
                return

        updated_cancellations.append(c)

    write_csv(CANCELLATIONS_FILE, updated_cancellations, CANCELLATION_HEADERS)
    pause()


# ══════════════════════════════════════════════
#  PAYOUT MANAGEMENT
# ══════════════════════════════════════════════

def view_payout_requests():
    clear()
    banner()
    print("\n  PAYOUT REQUESTS\n")
    divider()

    payouts = read_csv(PAYOUTS_FILE)
    if not payouts:
        print("  No payout requests on record.")
        print("\n  Note: Payout requests from the Client Dashboard are simulated")
        print("        in MVP. In production, they will be logged here for admin")
        print("        to process to client MPESA/bank accounts.")
        pause()
        return

    pending   = [p for p in payouts if p["status"] == "PENDING"]
    processed = [p for p in payouts if p["status"] == "PROCESSED"]

    print(f"  Pending   : {len(pending)}")
    print(f"  Processed : {len(processed)}\n")
    divider()

    for p in payouts:
        print(f"  Payout ID : {p['payout_id']}")
        print(f"  Client    : {p['business_name']}  ({p['client_id']})")
        print(f"  Amount    : KES {float(p['amount']):,.2f}")
        print(f"  Method    : {p['method']}")
        print(f"  Status    : {p['status']}")
        print(f"  Requested : {p['requested_date']}")
        if p["admin_note"]:
            print(f"  Admin Note: {p['admin_note']}")
        divider()
    pause()


# ══════════════════════════════════════════════
#  PLATFORM ANALYTICS & REPORTS
# ══════════════════════════════════════════════

def platform_overview():
    clear()
    banner()
    print("\n  PLATFORM OVERVIEW — ALL CLIENTS\n")
    divider()

    clients   = read_csv(CLIENTS_FILE)
    events    = read_csv(EVENTS_FILE)
    tickets   = read_csv(TICKETS_FILE)
    customers = read_csv(CUSTOMERS_FILE)
    cancels   = read_csv(CANCELLATIONS_FILE)

    paid_tickets = [t for t in tickets if t["payment_status"] == "PAID"]
    gross        = sum(float(t["price"]) for t in paid_tickets)
    commissions  = sum(float(t["commission"]) for t in paid_tickets)
    txn_costs    = sum(float(t["transaction_cost"]) for t in paid_tickets)
    refunded     = [c for c in cancels if c["status"] == "REFUNDED"]
    total_refunds= sum(float(c["refundable_amount"]) for c in refunded)

    active_events= len([e for e in events if e["status"] == "ACTIVE"])

    print(f"  CLIENTS")
    print(f"  Total Registered     : {len(clients)}")
    print(f"  Active               : {len([c for c in clients if c['status'] == 'ACTIVE'])}")
    print(f"  Suspended/Blacklisted: {len([c for c in clients if c['status'] != 'ACTIVE'])}")
    divider()

    print(f"  EVENTS")
    print(f"  Total Events         : {len(events)}")
    print(f"  Currently Active     : {active_events}")
    divider()

    print(f"  CUSTOMERS")
    print(f"  Total Registered     : {len(customers)}")
    divider()

    print(f"  TICKETS")
    print(f"  Total Issued         : {len(tickets)}")
    print(f"  Paid                 : {len(paid_tickets)}")
    print(f"  Complimentary        : {len([t for t in tickets if t['payment_status'] == 'COMPLIMENTARY'])}")
    print(f"  Attended             : {len([t for t in tickets if t['attended'] == 'True'])}")
    divider()

    print(f"  FINANCIALS")
    print(f"  Gross Ticket Sales   : KES {gross:>12,.2f}")
    print(f"  BReSCA Commission    : KES {commissions:>12,.2f}")
    print(f"  MPESA Transaction    : KES {txn_costs:>12,.2f}")
    print(f"  Total Refunds Paid   : KES {total_refunds:>12,.2f}")
    print(f"  ─────────────────────────────────────")
    bresca_net = commissions + txn_costs
    print(f"  BReSCA TOTAL EARNED  : KES {bresca_net:>12,.2f}")
    divider()

    print(f"  CANCELLATIONS")
    print(f"  Total Requests       : {len(cancels)}")
    print(f"  Refunded             : {len(refunded)}")
    print(f"  Pending Client Review: {len([c for c in cancels if c['status'] == 'PENDING'])}")
    print(f"  Awaiting Admin       : {len([c for c in cancels if c['status'] == 'CLIENT_APPROVED'])}")
    pause()


def revenue_by_client():
    clear()
    banner()
    print("\n  REVENUE BREAKDOWN BY CLIENT\n")
    divider()

    clients = read_csv(CLIENTS_FILE)
    tickets = read_csv(TICKETS_FILE)

    if not clients:
        print("  No clients found.")
        pause()
        return

    for c in clients:
        client_tickets = [t for t in tickets
                          if t["client_id"] == c["client_id"]
                          and t["payment_status"] == "PAID"]
        gross      = sum(float(t["price"]) for t in client_tickets)
        commission = sum(float(t["commission"]) for t in client_tickets)
        txn        = sum(float(t["transaction_cost"]) for t in client_tickets)

        print(f"\n  {c['business_name']} [{c['plan']}]")
        print(f"  Tickets Sold    : {len(client_tickets)}")
        print(f"  Gross Sales     : KES {gross:>10,.2f}")
        print(f"  BReSCA Earned   : KES {commission + txn:>10,.2f}  (commission + txn)")
        print(f"  Client Net      : KES {gross - commission - txn:>10,.2f}")
        divider()
    pause()


def event_performance_report():
    clear()
    banner()
    print("\n  EVENT PERFORMANCE REPORT\n")
    divider()

    events  = read_csv(EVENTS_FILE)
    clients = read_csv(CLIENTS_FILE)
    tickets = read_csv(TICKETS_FILE)
    reviews = read_csv(REVIEWS_FILE)

    if not events:
        print("  No events found.")
        pause()
        return

    for e in events:
        organiser    = next((c["business_name"] for c in clients
                             if c["client_id"] == e["client_id"]), "Unknown")
        e_tickets    = [t for t in tickets if t["event_id"] == e["event_id"]]
        paid         = [t for t in e_tickets if t["payment_status"] == "PAID"]
        attended     = [t for t in e_tickets if t["attended"] == "True"]
        e_reviews    = [r for r in reviews if r["event_id"] == e["event_id"]]
        avg_rating   = (sum(int(r["rating"]) for r in e_reviews) / len(e_reviews)
                        if e_reviews else 0)
        gross        = sum(float(t["price"]) for t in paid)

        print(f"\n  {e['event_name']} ({e['event_date']})")
        print(f"  Organiser    : {organiser}")
        print(f"  Status       : {e['status']}")
        print(f"  Tickets Sold : {len(paid)}  |  Attended: {len(attended)}")
        print(f"  Gross Sales  : KES {gross:,.0f}")
        if e_reviews:
            stars = "⭐" * round(avg_rating)
            print(f"  Avg Rating   : {avg_rating:.1f}/5  {stars}  ({len(e_reviews)} reviews)")
        else:
            print(f"  Reviews      : None yet")
        divider()
    pause()


def view_all_reviews():
    clear()
    banner()
    print("\n  ALL EVENT REVIEWS\n")
    divider()

    reviews = read_csv(REVIEWS_FILE)
    if not reviews:
        print("  No reviews submitted yet.")
        pause()
        return

    print(f"  Total Reviews: {len(reviews)}\n")
    for r in reviews:
        stars = "⭐" * int(r["rating"])
        print(f"  Event   : {r['event_name']}")
        print(f"  By      : {r['customer_name']} — {r['phone']}")
        print(f"  Rating  : {r['rating']}/5  {stars}")
        if r["comment"]:
            print(f"  Comment : {r['comment']}")
        print(f"  Date    : {r['review_date']}")
        divider()
    pause()


# ══════════════════════════════════════════════
#  EXPORT DATA
# ══════════════════════════════════════════════

def export_data():
    clear()
    banner()
    print("\n  EXPORT PLATFORM DATA\n")
    divider()
    print("  [1] Export All Tickets")
    print("  [2] Export All Clients")
    print("  [3] Export All Customers")
    print("  [4] Export All Cancellations")
    print("  [5] Export All Events")
    print("  [0] Back")
    divider()

    choice = input("  Select: ").strip()

    export_map = {
        "1": (TICKETS_FILE,       TICKET_HEADERS,       "export_tickets"),
        "2": (CLIENTS_FILE,       CLIENT_HEADERS,       "export_clients"),
        "3": (CUSTOMERS_FILE,     CUSTOMER_HEADERS,     "export_customers"),
        "4": (CANCELLATIONS_FILE, CANCELLATION_HEADERS, "export_cancellations"),
        "5": (EVENTS_FILE,        EVENT_HEADERS,        "export_events"),
    }

    if choice not in export_map:
        return

    source_file, headers, prefix = export_map[choice]
    rows = read_csv(source_file)

    if not rows:
        print("  No data to export.")
        pause()
        return

    filename = f"{prefix}_{today_str()}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Exported {len(rows)} records to: {filename}")
    pause()


# ══════════════════════════════════════════════
#  SYSTEM SETTINGS
# ══════════════════════════════════════════════

def system_info():
    clear()
    banner()
    print("\n  SYSTEM INFORMATION\n")
    divider()

    admins    = read_csv(ADMINS_FILE)
    clients   = read_csv(CLIENTS_FILE)
    events    = read_csv(EVENTS_FILE)
    tickets   = read_csv(TICKETS_FILE)
    customers = read_csv(CUSTOMERS_FILE)

    print(f"  Platform    : Ticketzetu by BReSCA")
    print(f"  Version     : MVP 1.0 (CSV Backend)")
    print(f"  Date        : {today_str()}")
    print(f"\n  DATA SUMMARY")
    print(f"  Admins      : {len(admins)}")
    print(f"  Clients     : {len(clients)}")
    print(f"  Events      : {len(events)}")
    print(f"  Tickets     : {len(tickets)}")
    print(f"  Customers   : {len(customers)}")
    print(f"\n  DATA FILES")
    for f in [ADMINS_FILE, CLIENTS_FILE, EVENTS_FILE, TICKETS_FILE,
              CUSTOMERS_FILE, CANCELLATIONS_FILE, REVIEWS_FILE, PAYOUTS_FILE]:
        exists = "✅" if os.path.exists(f) else "❌"
        size   = os.path.getsize(f) if os.path.exists(f) else 0
        print(f"  {exists} {f:<30} {size:>6} bytes")
    pause()


# ══════════════════════════════════════════════
#  MAIN DASHBOARD MENU
# ══════════════════════════════════════════════

def admin_dashboard(admin: dict):
    while True:
        clear()
        banner()
        print(f"\n  Logged in: {admin['full_name']} ({admin['role']})")
        print(f"  Today: {today_str()}\n")

        # Live alerts
        pending_admin  = len([c for c in read_csv(CANCELLATIONS_FILE)
                               if c["status"] == "CLIENT_APPROVED"])
        new_clients    = len([c for c in read_csv(CLIENTS_FILE)
                               if c["status"] == "ACTIVE"])

        if pending_admin > 0:
            print(f"  🔔 {pending_admin} cancellation(s) awaiting your final approval!\n")

        print("  ── CLIENT MANAGEMENT ──")
        print("  [1]  View All Clients")
        print("  [2]  Manage Client Status (Activate / Suspend / Blacklist)")
        print("  [3]  Change Client Plan")
        print()
        print("  ── EVENT OVERSIGHT ──")
        print("  [4]  View All Events")
        print("  [5]  Force Event Status")
        print()
        print("  ── CUSTOMER MANAGEMENT ──")
        print("  [6]  View All Customers")
        print("  [7]  Manage Customer Status")
        print()
        print("  ── TICKET MANAGEMENT ──")
        print("  [8]  View All Tickets")
        print("  [9]  Search Ticket")
        print("  [10] Blacklist / Restore Ticket")
        print()
        print("  ── CANCELLATIONS ──")
        print("  [11] View All Cancellation Requests")
        print("  [12] Process Cancellations (Admin Final Approval)")
        print()
        print("  ── PAYOUTS ──")
        print("  [13] View Payout Requests")
        print()
        print("  ── ANALYTICS & REPORTS ──")
        print("  [14] Platform Overview")
        print("  [15] Revenue Breakdown by Client")
        print("  [16] Event Performance Report")
        print("  [17] View All Reviews")
        print()
        print("  ── DATA & SYSTEM ──")
        print("  [18] Export Data")
        print("  [19] System Information")
        print()
        if admin["role"] == "SUPER_ADMIN":
            print("  ── SUPER ADMIN ──")
            print("  [20] Create Admin Account")
            print("  [21] View All Admin Accounts")
            print()
        print("  ── ACCOUNT ──")
        print("  [22] Change Password")
        print("  [0]  Logout")
        divider()

        choice = input("  Select option: ").strip()

        if   choice == "1":  view_all_clients()
        elif choice == "2":  manage_client_status()
        elif choice == "3":  manage_client_plan()
        elif choice == "4":  view_all_events()
        elif choice == "5":  force_event_status()
        elif choice == "6":  view_all_customers()
        elif choice == "7":  manage_customer_status()
        elif choice == "8":  view_all_tickets()
        elif choice == "9":  search_ticket()
        elif choice == "10": admin_blacklist_ticket()
        elif choice == "11": view_cancellations()
        elif choice == "12": process_cancellation()
        elif choice == "13": view_payout_requests()
        elif choice == "14": platform_overview()
        elif choice == "15": revenue_by_client()
        elif choice == "16": event_performance_report()
        elif choice == "17": view_all_reviews()
        elif choice == "18": export_data()
        elif choice == "19": system_info()
        elif choice == "20":
            if admin["role"] == "SUPER_ADMIN":
                create_admin(admin)
            else:
                print("⚠  Access denied.")
                pause()
        elif choice == "21":
            if admin["role"] == "SUPER_ADMIN":
                view_all_admins(admin)
            else:
                print("⚠  Access denied.")
                pause()
        elif choice == "22": admin = change_admin_password(admin)
        elif choice == "0":
            print("\n  Logging out... Goodbye!")
            break
        else:
            print("⚠  Invalid option.")
            pause()


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

def main():
    init_files()
    seed_super_admin()

    while True:
        clear()
        banner()
        print("\n  [1]  Admin Login")
        print("  [0]  Exit")
        divider()

        choice = input("  Select option: ").strip()

        if choice == "1":
            admin = login_admin()
            if admin:
                admin_dashboard(admin)
        elif choice == "0":
            print("\n  Goodbye! — BReSCA Ticketzetu Admin\n")
            break
        else:
            print("⚠  Invalid option.")
            pause()


if __name__ == "__main__":
    main()
