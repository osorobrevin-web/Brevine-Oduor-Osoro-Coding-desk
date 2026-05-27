"""
╔══════════════════════════════════════════════════════════════════╗
║          TICKETZETU — Powered by BReSCA                          ║
║          CLIENT DASHBOARD                                        ║
║          Brevine e-Systems Consultancy Agency, Kisumu Kenya      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import csv
import os
import uuid
import hashlib
from datetime import datetime, date

# ─────────────────────────────────────────────
#  FILE PATHS  (all dashboards share these)
# ─────────────────────────────────────────────
CLIENTS_FILE        = "clients.csv"
EVENTS_FILE         = "events.csv"
TICKETS_FILE        = "tickets.csv"
CANCELLATIONS_FILE  = "cancellations.csv"

# ─────────────────────────────────────────────
#  BRESCA COMMISSION RULES
# ─────────────────────────────────────────────
MPESA_TRANSACTION_COST = 10   # KES — always non-refundable

def bresca_commission(price: float) -> float:
    """Return BReSCA commission for a given ticket price."""
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
    """Create CSV file with headers if it does not exist."""
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def read_csv(filepath: str) -> list:
    """Read all rows from a CSV and return list of dicts."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(filepath: str, rows: list, headers: list):
    """Overwrite entire CSV with given rows."""
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def append_csv(filepath: str, row: dict, headers: list):
    """Append a single row to a CSV file."""
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# ══════════════════════════════════════════════
#  CSV HEADERS
# ══════════════════════════════════════════════

CLIENT_HEADERS = [
    "client_id", "business_name", "owner_name", "phone",
    "email", "password_hash", "plan", "status", "joined_date"
]

EVENT_HEADERS = [
    "event_id", "client_id", "event_name", "event_date",
    "event_time", "venue", "description", "poster",
    "status",                        # ACTIVE / INACTIVE / COMPLETED
    # ── Ticket categories ──
    "vvvip_price", "vvvip_seats",
    "vip_price",   "vip_seats",
    "regular_price","regular_seats",
    # ── Cancellation policy ──
    "cancel_by_date",                # Last date customer can cancel
    "refund_percent",                # 0–100
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
    "status",                        # PENDING / CLIENT_APPROVED / CLIENT_REJECTED / ADMIN_APPROVED / ADMIN_REJECTED / REFUNDED
    "client_action_date", "client_note",
    "admin_action_date",  "admin_note",
    "request_date"
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
    print("   CLIENT DASHBOARD")
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


def generate_ticket_no(client_id: str, event_id: str) -> str:
    """Generate unique ticket number: TZ-2026-CLIENTCODE-XXXX"""
    tickets = read_csv(TICKETS_FILE)
    # Count tickets for this event
    event_tickets = [t for t in tickets if t["event_id"] == event_id]
    seq = str(len(event_tickets) + 1).zfill(4)
    # Use first 4 chars of client_id as code
    client_code = client_id[:4].upper()
    year = date.today().year
    return f"TZ-{year}-{client_code}-{seq}"


# ══════════════════════════════════════════════
#  INITIALISE ALL CSV FILES
# ══════════════════════════════════════════════

def init_files():
    ensure_file(CLIENTS_FILE,       CLIENT_HEADERS)
    ensure_file(EVENTS_FILE,        EVENT_HEADERS)
    ensure_file(TICKETS_FILE,       TICKET_HEADERS)
    ensure_file(CANCELLATIONS_FILE, CANCELLATION_HEADERS)


# ══════════════════════════════════════════════
#  AUTH — REGISTER & LOGIN
# ══════════════════════════════════════════════

def register_client():
    clear()
    banner()
    print("\n  NEW CLIENT REGISTRATION\n")
    divider()

    business_name = input("Business / Organisation Name: ").strip()
    owner_name    = input("Owner / Contact Person Name: ").strip()
    phone         = input("Phone Number (07XXXXXXXX): ").strip()
    email         = input("Email Address: ").strip()

    # Check phone not already registered
    clients = read_csv(CLIENTS_FILE)
    for c in clients:
        if c["phone"] == phone:
            print("\n⚠  A client with this phone number already exists.")
            pause()
            return

    print("\nChoose Subscription Plan:")
    print("  1. Starter  — KES 2,000/month (up to 3 events)")
    print("  2. Growth   — KES 5,000/month (up to 10 events)")
    print("  3. Pro      — KES 10,000/month (unlimited events)")
    plan_choice = input("Select plan (1-3): ").strip()
    plans = {"1": "Starter", "2": "Growth", "3": "Pro"}
    plan = plans.get(plan_choice, "Starter")

    password  = input("\nCreate Password: ").strip()
    password2 = input("Confirm Password: ").strip()
    if password != password2:
        print("\n⚠  Passwords do not match.")
        pause()
        return

    client_id = str(uuid.uuid4())[:8].upper()

    new_client = {
        "client_id":     client_id,
        "business_name": business_name,
        "owner_name":    owner_name,
        "phone":         phone,
        "email":         email,
        "password_hash": hash_password(password),
        "plan":          plan,
        "status":        "ACTIVE",
        "joined_date":   today_str()
    }

    append_csv(CLIENTS_FILE, new_client, CLIENT_HEADERS)
    print(f"\n✅ Registration successful!")
    print(f"   Your Client ID: {client_id}")
    print(f"   Plan: {plan}")
    print("\n   Note: BReSCA admin will review and activate your account.")
    pause()


def login_client() -> dict | None:
    clear()
    banner()
    print("\n  CLIENT LOGIN\n")
    divider()

    phone    = input("Phone Number: ").strip()
    password = input("Password: ").strip()

    clients = read_csv(CLIENTS_FILE)
    for c in clients:
        if c["phone"] == phone and c["password_hash"] == hash_password(password):
            if c["status"] != "ACTIVE":
                print(f"\n⚠  Your account status is: {c['status']}")
                print("   Please contact BReSCA support.")
                pause()
                return None
            print(f"\n✅ Welcome back, {c['owner_name']} — {c['business_name']}!")
            pause()
            return c

    print("\n⚠  Invalid phone number or password.")
    pause()
    return None


# ══════════════════════════════════════════════
#  EVENT MANAGEMENT
# ══════════════════════════════════════════════

def create_event(client: dict):
    clear()
    banner()
    print(f"\n  CREATE NEW EVENT — {client['business_name']}\n")
    divider()

    event_name  = input("Event Name: ").strip()
    event_date  = input("Event Date (YYYY-MM-DD): ").strip()
    if not valid_date(event_date):
        print("⚠  Invalid date format.")
        pause()
        return

    event_time  = input("Event Time (e.g. 7:00 PM): ").strip()
    venue       = input("Venue / Location: ").strip()
    description = input("Event Description: ").strip()
    poster      = input("Poster filename or URL (leave blank if none): ").strip()

    print("\n  TICKET CATEGORIES")
    print("  Enter price 0 to disable a category.\n")

    def get_category(name):
        price = input(f"  {name} Ticket Price (KES): ").strip()
        seats = input(f"  {name} Total Seats: ").strip()
        try:
            return float(price), int(seats)
        except ValueError:
            return 0.0, 0

    vvvip_price,   vvvip_seats   = get_category("VVVIP")
    vip_price,     vip_seats     = get_category("VIP")
    regular_price, regular_seats = get_category("Regular")

    print("\n  CANCELLATION POLICY")
    cancel_by_date = input("  Cancel-by Date (YYYY-MM-DD): ").strip()
    if not valid_date(cancel_by_date):
        print("⚠  Invalid date. Setting cancel-by date to today.")
        cancel_by_date = today_str()

    while True:
        try:
            refund_percent = int(input("  Refund Percentage (0–100): ").strip())
            if 0 <= refund_percent <= 100:
                break
            print("  ⚠  Must be between 0 and 100.")
        except ValueError:
            print("  ⚠  Enter a number.")

    event_id = str(uuid.uuid4())[:8].upper()

    new_event = {
        "event_id":      event_id,
        "client_id":     client["client_id"],
        "event_name":    event_name,
        "event_date":    event_date,
        "event_time":    event_time,
        "venue":         venue,
        "description":   description,
        "poster":        poster,
        "status":        "ACTIVE",
        "vvvip_price":   vvvip_price,
        "vvvip_seats":   vvvip_seats,
        "vip_price":     vip_price,
        "vip_seats":     vip_seats,
        "regular_price": regular_price,
        "regular_seats": regular_seats,
        "cancel_by_date":cancel_by_date,
        "refund_percent":refund_percent,
        "created_date":  today_str()
    }

    append_csv(EVENTS_FILE, new_event, EVENT_HEADERS)
    print(f"\n✅ Event created successfully!")
    print(f"   Event ID: {event_id}")
    print(f"   Cancellation policy: {refund_percent}% refund if cancelled by {cancel_by_date}")
    pause()


def view_my_events(client: dict):
    clear()
    banner()
    print(f"\n  MY EVENTS — {client['business_name']}\n")
    divider()

    events = [e for e in read_csv(EVENTS_FILE) if e["client_id"] == client["client_id"]]
    if not events:
        print("  No events found. Create your first event!")
        pause()
        return

    for i, e in enumerate(events, 1):
        tickets = [t for t in read_csv(TICKETS_FILE) if t["event_id"] == e["event_id"]]
        sold = len(tickets)
        gross = sum(float(t["price"]) for t in tickets)
        print(f"\n  [{i}] {e['event_name']}")
        print(f"       Date   : {e['event_date']} at {e['event_time']}")
        print(f"       Venue  : {e['venue']}")
        print(f"       Status : {e['status']}")
        print(f"       Tickets Sold : {sold}  |  Gross Sales: KES {gross:,.0f}")
        print(f"       Cancel By: {e['cancel_by_date']}  |  Refund: {e['refund_percent']}%")
    pause()


def edit_event(client: dict):
    clear()
    banner()
    print(f"\n  EDIT EVENT — {client['business_name']}\n")
    divider()

    events = [e for e in read_csv(EVENTS_FILE) if e["client_id"] == client["client_id"]]
    if not events:
        print("  No events found.")
        pause()
        return

    for i, e in enumerate(events, 1):
        print(f"  [{i}] {e['event_name']} — {e['event_date']} [{e['status']}]")

    choice = input("\nSelect event number to edit: ").strip()
    try:
        selected = events[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Editing: {selected['event_name']}")
    print("  Press ENTER to keep current value.\n")

    def update_field(label, key, current):
        val = input(f"  {label} [{current}]: ").strip()
        return val if val else current

    selected["event_name"]    = update_field("Event Name",    "event_name",    selected["event_name"])
    selected["event_date"]    = update_field("Event Date",    "event_date",    selected["event_date"])
    selected["event_time"]    = update_field("Event Time",    "event_time",    selected["event_time"])
    selected["venue"]         = update_field("Venue",         "venue",         selected["venue"])
    selected["description"]   = update_field("Description",   "description",   selected["description"])
    selected["cancel_by_date"]= update_field("Cancel By Date","cancel_by_date",selected["cancel_by_date"])

    rp = input(f"  Refund Percent [{selected['refund_percent']}]: ").strip()
    if rp:
        try:
            rp_int = int(rp)
            if 0 <= rp_int <= 100:
                selected["refund_percent"] = rp_int
        except ValueError:
            pass

    print("\n  Status options: ACTIVE / INACTIVE / COMPLETED")
    st = input(f"  Status [{selected['status']}]: ").strip().upper()
    if st in ["ACTIVE", "INACTIVE", "COMPLETED"]:
        selected["status"] = st

    # Save back
    all_events = read_csv(EVENTS_FILE)
    updated = [selected if e["event_id"] == selected["event_id"] else e for e in all_events]
    write_csv(EVENTS_FILE, updated, EVENT_HEADERS)

    print("\n✅ Event updated successfully!")
    pause()


# ══════════════════════════════════════════════
#  HONOUR PASS — ISSUE COMPLIMENTARY TICKET
# ══════════════════════════════════════════════

def issue_honour_pass(client: dict):
    clear()
    banner()
    print(f"\n  ISSUE HONOUR PASS — {client['business_name']}\n")
    divider()

    events = [e for e in read_csv(EVENTS_FILE)
              if e["client_id"] == client["client_id"] and e["status"] == "ACTIVE"]
    if not events:
        print("  No active events found.")
        pause()
        return

    for i, e in enumerate(events, 1):
        print(f"  [{i}] {e['event_name']} — {e['event_date']}")

    choice = input("\nSelect event: ").strip()
    try:
        event = events[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print("\n  Pass Type:")
    pass_types = {
        "1": "Organiser Pass",
        "2": "Partner Pass",
        "3": "Press Pass",
        "4": "Staff Pass",
        "5": "Complimentary Pass",
        "6": "Promotional Pass"
    }
    for k, v in pass_types.items():
        print(f"  [{k}] {v}")

    pt = input("Select pass type: ").strip()
    pass_type = pass_types.get(pt, "Complimentary Pass")

    print("\n  Recipient Details:")
    name   = input("  Full Name: ").strip()
    phone  = input("  Phone Number: ").strip()
    id_no  = input("  ID Number: ").strip()
    email  = input("  Email (optional): ").strip()

    ticket_no = generate_ticket_no(client["client_id"], event["event_id"])
    wristband_qr = f"WB-{ticket_no}"

    ticket = {
        "ticket_no":        ticket_no,
        "client_id":        client["client_id"],
        "event_id":         event["event_id"],
        "event_name":       event["event_name"],
        "customer_name":    name,
        "phone":            phone,
        "id_number":        id_no,
        "email":            email,
        "category":         f"Honour Pass ({pass_type})",
        "price":            0,
        "commission":       0,
        "transaction_cost": 0,
        "payment_status":   "COMPLIMENTARY",
        "wristband_qr":     wristband_qr,
        "first_entry":      "False",
        "entry_time":       "",
        "attended":         "False",
        "refund_amount":    0,
        "refund_status":    "N/A",
        "purchase_date":    today_str()
    }

    append_csv(TICKETS_FILE, ticket, TICKET_HEADERS)
    print(f"\n✅ Honour Pass issued!")
    print(f"   Ticket No  : {ticket_no}")
    print(f"   Recipient  : {name}")
    print(f"   Pass Type  : {pass_type}")
    print(f"   Wristband  : {wristband_qr}")
    pause()


# ══════════════════════════════════════════════
#  TICKET MANAGEMENT
# ══════════════════════════════════════════════

def view_sold_tickets(client: dict):
    clear()
    banner()
    print(f"\n  SOLD TICKETS — {client['business_name']}\n")
    divider()

    events = [e for e in read_csv(EVENTS_FILE) if e["client_id"] == client["client_id"]]
    if not events:
        print("  No events found.")
        pause()
        return

    # Let client filter by event
    for i, e in enumerate(events, 1):
        print(f"  [{i}] {e['event_name']} — {e['event_date']}")
    print("  [A] All events")

    choice = input("\nFilter by event (number or A): ").strip().upper()
    if choice == "A":
        tickets = [t for t in read_csv(TICKETS_FILE) if t["client_id"] == client["client_id"]]
    else:
        try:
            event = events[int(choice) - 1]
            tickets = [t for t in read_csv(TICKETS_FILE) if t["event_id"] == event["event_id"]]
        except (ValueError, IndexError):
            print("⚠  Invalid selection.")
            pause()
            return

    if not tickets:
        print("\n  No tickets found.")
        pause()
        return

    print(f"\n  {'TICKET NO':<25} {'CUSTOMER':<20} {'CATEGORY':<12} {'PRICE':>8} {'STATUS':<12}")
    divider()
    for t in tickets:
        print(f"  {t['ticket_no']:<25} {t['customer_name']:<20} {t['category']:<12} "
              f"KES {float(t['price']):>6,.0f}  {t['payment_status']:<12}")

    print(f"\n  Total tickets: {len(tickets)}")
    print(f"  Gross sales  : KES {sum(float(t['price']) for t in tickets):,.0f}")
    pause()


def blacklist_ticket(client: dict):
    clear()
    banner()
    print(f"\n  BLACKLIST TICKET — {client['business_name']}\n")
    divider()

    ticket_no = input("Enter Ticket Number to blacklist: ").strip().upper()
    tickets = read_csv(TICKETS_FILE)

    found = False
    updated = []
    for t in tickets:
        if t["ticket_no"] == ticket_no and t["client_id"] == client["client_id"]:
            t["payment_status"] = "BLACKLISTED"
            found = True
            print(f"\n  Ticket   : {t['ticket_no']}")
            print(f"  Customer : {t['customer_name']}")
            print(f"  Category : {t['category']}")
            confirm = input("\n  Confirm blacklist? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("  Cancelled.")
                pause()
                return
        updated.append(t)

    if not found:
        print("⚠  Ticket not found or does not belong to your account.")
    else:
        write_csv(TICKETS_FILE, updated, TICKET_HEADERS)
        print("✅ Ticket blacklisted.")
    pause()


# ══════════════════════════════════════════════
#  CANCELLATION MANAGEMENT
# ══════════════════════════════════════════════

def view_cancellation_requests(client: dict):
    clear()
    banner()
    print(f"\n  CANCELLATION REQUESTS — {client['business_name']}\n")
    divider()

    cancellations = [c for c in read_csv(CANCELLATIONS_FILE)
                     if c["client_id"] == client["client_id"]]

    if not cancellations:
        print("  No cancellation requests found.")
        pause()
        return

    # Group by status
    pending  = [c for c in cancellations if c["status"] == "PENDING"]
    approved = [c for c in cancellations if c["status"] == "CLIENT_APPROVED"]
    others   = [c for c in cancellations if c["status"] not in ["PENDING", "CLIENT_APPROVED"]]

    def print_group(label, items):
        if items:
            print(f"\n  ── {label} ──")
            for c in items:
                print(f"\n  Cancel ID  : {c['cancel_id']}")
                print(f"  Ticket No  : {c['ticket_no']}")
                print(f"  Customer   : {c['customer_name']} | {c['phone']}")
                print(f"  Category   : {c['category']}  | Price: KES {float(c['price']):,.0f}")
                print(f"  Refund Due : KES {float(c['refundable_amount']):,.0f} ({c['refund_percent']}%)")
                print(f"  Reason     : {c['reason']}")
                print(f"  Requested  : {c['request_date']}")
                print(f"  Status     : {c['status']}")

    print_group("PENDING YOUR ACTION", pending)
    print_group("AWAITING BRESCA ADMIN", approved)
    print_group("RESOLVED", others)
    pause()


def process_cancellation(client: dict):
    clear()
    banner()
    print(f"\n  PROCESS CANCELLATION — {client['business_name']}\n")
    divider()

    cancellations = read_csv(CANCELLATIONS_FILE)
    pending = [c for c in cancellations
               if c["client_id"] == client["client_id"] and c["status"] == "PENDING"]

    if not pending:
        print("  No pending cancellation requests.")
        pause()
        return

    for i, c in enumerate(pending, 1):
        print(f"\n  [{i}]")
        print(f"       Cancel ID  : {c['cancel_id']}")
        print(f"       Ticket No  : {c['ticket_no']}")
        print(f"       Customer   : {c['customer_name']} — {c['phone']}")
        print(f"       Category   : {c['category']}  | Price: KES {float(c['price']):,.0f}")
        print(f"       Refund Due : KES {float(c['refundable_amount']):,.0f} ({c['refund_percent']}%)")
        print(f"       Reason     : {c['reason']}")
        print(f"       Requested  : {c['request_date']}")

    choice = input("\nSelect request number to process: ").strip()
    try:
        selected = pending[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Processing: {selected['cancel_id']}")
    print("  [1] Approve — forward to BReSCA Admin")
    print("  [2] Reject  — close request")
    action = input("  Your decision (1 or 2): ").strip()

    note = input("  Add a note (optional): ").strip()

    updated = []
    for c in cancellations:
        if c["cancel_id"] == selected["cancel_id"]:
            if action == "1":
                c["status"] = "CLIENT_APPROVED"
                print("\n✅ Approved — forwarded to BReSCA Admin for final approval.")
            elif action == "2":
                c["status"] = "CLIENT_REJECTED"
                # Also update ticket refund status
                tickets = read_csv(TICKETS_FILE)
                t_updated = []
                for t in tickets:
                    if t["ticket_no"] == c["ticket_no"]:
                        t["refund_status"] = "REJECTED"
                    t_updated.append(t)
                write_csv(TICKETS_FILE, t_updated, TICKET_HEADERS)
                print("\n✅ Rejected — customer will be notified.")
            else:
                print("⚠  Invalid choice. No action taken.")
                pause()
                return
            c["client_action_date"] = now_str()
            c["client_note"]        = note
        updated.append(c)

    write_csv(CANCELLATIONS_FILE, updated, CANCELLATION_HEADERS)
    pause()


# ══════════════════════════════════════════════
#  FINANCIAL REPORTS
# ══════════════════════════════════════════════

def financial_report(client: dict):
    clear()
    banner()
    print(f"\n  FINANCIAL REPORT — {client['business_name']}\n")
    divider()

    tickets = [t for t in read_csv(TICKETS_FILE)
               if t["client_id"] == client["client_id"] and t["payment_status"] == "PAID"]
    cancellations = [c for c in read_csv(CANCELLATIONS_FILE)
                     if c["client_id"] == client["client_id"] and c["status"] == "REFUNDED"]

    gross        = sum(float(t["price"]) for t in tickets)
    commissions  = sum(float(t["commission"]) for t in tickets)
    txn_costs    = sum(float(t["transaction_cost"]) for t in tickets)
    refunds_paid = sum(float(c["refundable_amount"]) for c in cancellations)
    net_revenue  = gross - commissions - txn_costs - refunds_paid

    print(f"\n  Gross Ticket Sales    : KES {gross:>12,.2f}")
    print(f"  BReSCA Commission     : KES {commissions:>12,.2f}  (deducted)")
    print(f"  MPESA Transaction Cost: KES {txn_costs:>12,.2f}  (deducted)")
    print(f"  Refunds Paid Out      : KES {refunds_paid:>12,.2f}  (deducted)")
    divider()
    print(f"  NET REVENUE           : KES {net_revenue:>12,.2f}")
    print(f"\n  Total Tickets Sold    : {len(tickets)}")
    print(f"  Refunds Processed     : {len(cancellations)}")
    pause()


def request_payout(client: dict):
    clear()
    banner()
    print(f"\n  REQUEST PAYOUT — {client['business_name']}\n")
    divider()

    tickets = [t for t in read_csv(TICKETS_FILE)
               if t["client_id"] == client["client_id"] and t["payment_status"] == "PAID"]
    cancellations = [c for c in read_csv(CANCELLATIONS_FILE)
                     if c["client_id"] == client["client_id"] and c["status"] == "REFUNDED"]

    gross       = sum(float(t["price"]) for t in tickets)
    commissions = sum(float(t["commission"]) for t in tickets)
    txn_costs   = sum(float(t["transaction_cost"]) for t in tickets)
    refunds     = sum(float(c["refundable_amount"]) for c in cancellations)
    available   = gross - commissions - txn_costs - refunds

    print(f"  Available for payout: KES {available:,.2f}")
    print("\n  Payout method:")
    print("  [1] MPESA")
    print("  [2] Bank Transfer")
    method = input("  Select (1 or 2): ").strip()
    methods = {"1": "MPESA", "2": "Bank Transfer"}
    method_name = methods.get(method, "MPESA")

    amount = input(f"  Amount to withdraw (max KES {available:,.2f}): KES ").strip()
    try:
        amount_f = float(amount)
    except ValueError:
        print("⚠  Invalid amount.")
        pause()
        return

    if amount_f > available:
        print("⚠  Amount exceeds available balance.")
        pause()
        return

    # Simulate payout
    print(f"\n  ── PAYOUT SIMULATION ──")
    print(f"  Method   : {method_name}")
    print(f"  Amount   : KES {amount_f:,.2f}")
    print(f"  Account  : {client['phone']}")
    print(f"\n  [SIMULATED] Payout of KES {amount_f:,.2f} sent via {method_name}.")
    print(f"  Confirmation SMS sent to {client['phone']}.")
    pause()


# ══════════════════════════════════════════════
#  ATTENDANCE MANAGEMENT
# ══════════════════════════════════════════════

def scan_ticket_entry(client: dict):
    """Simulate gate scanning — mark ticket as attended."""
    clear()
    banner()
    print(f"\n  GATE ENTRY SCANNER — {client['business_name']}\n")
    divider()
    print("  Enter ticket number or wristband QR to mark entry.")
    print("  Type 'quit' to exit scanner.\n")

    while True:
        scan = input("  SCAN → ").strip().upper()
        if scan == "QUIT":
            break

        tickets = read_csv(TICKETS_FILE)
        found = False
        updated = []
        for t in tickets:
            if (t["ticket_no"] == scan or t["wristband_qr"] == scan) \
                    and t["client_id"] == client["client_id"]:
                found = True
                if t["payment_status"] == "BLACKLISTED":
                    print("  ❌ BLACKLISTED TICKET — DENY ENTRY")
                elif t["payment_status"] not in ["PAID", "COMPLIMENTARY"]:
                    print(f"  ❌ INVALID PAYMENT STATUS: {t['payment_status']}")
                elif t["first_entry"] == "True":
                    # Wristband re-entry
                    print(f"  ✅ RE-ENTRY — {t['customer_name']} | {t['category']}")
                    t["attended"] = "True"
                else:
                    # First entry
                    t["first_entry"] = "True"
                    t["entry_time"]  = now_str()
                    t["attended"]    = "True"
                    print(f"  ✅ FIRST ENTRY — {t['customer_name']} | {t['category']}")
                    print(f"     Issue {t['category'].split('(')[0].strip()} wristband")
            updated.append(t)

        if not found:
            print("  ❌ TICKET NOT FOUND")

        write_csv(TICKETS_FILE, updated, TICKET_HEADERS)


def view_attendance(client: dict):
    clear()
    banner()
    print(f"\n  ATTENDANCE REPORT — {client['business_name']}\n")
    divider()

    events = [e for e in read_csv(EVENTS_FILE) if e["client_id"] == client["client_id"]]
    if not events:
        print("  No events found.")
        pause()
        return

    for i, e in enumerate(events, 1):
        tickets = [t for t in read_csv(TICKETS_FILE) if t["event_id"] == e["event_id"]]
        attended    = [t for t in tickets if t["attended"] == "True"]
        not_attended= [t for t in tickets if t["attended"] == "False"
                       and t["payment_status"] == "PAID"]
        print(f"\n  [{i}] {e['event_name']} — {e['event_date']}")
        print(f"       Tickets Sold   : {len(tickets)}")
        print(f"       Attended       : {len(attended)}")
        print(f"       Did Not Attend : {len(not_attended)}")
    pause()


# ══════════════════════════════════════════════
#  DOWNLOAD ATTENDEE LIST
# ══════════════════════════════════════════════

def download_attendee_list(client: dict):
    clear()
    banner()
    print(f"\n  DOWNLOAD ATTENDEE LIST — {client['business_name']}\n")
    divider()

    events = [e for e in read_csv(EVENTS_FILE) if e["client_id"] == client["client_id"]]
    if not events:
        print("  No events found.")
        pause()
        return

    for i, e in enumerate(events, 1):
        print(f"  [{i}] {e['event_name']} — {e['event_date']}")

    choice = input("\nSelect event: ").strip()
    try:
        event = events[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    tickets = [t for t in read_csv(TICKETS_FILE) if t["event_id"] == event["event_id"]]
    filename = f"attendees_{event['event_id']}_{today_str()}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TICKET_HEADERS)
        writer.writeheader()
        writer.writerows(tickets)

    print(f"\n✅ Attendee list saved to: {filename}")
    print(f"   {len(tickets)} records exported.")
    pause()


# ══════════════════════════════════════════════
#  CUSTOMER COMMUNICATION (SIMULATED SMS)
# ══════════════════════════════════════════════

def send_sms_blast(client: dict):
    clear()
    banner()
    print(f"\n  SMS BLAST — {client['business_name']}\n")
    divider()

    events = [e for e in read_csv(EVENTS_FILE) if e["client_id"] == client["client_id"]]
    if not events:
        print("  No events found.")
        pause()
        return

    for i, e in enumerate(events, 1):
        print(f"  [{i}] {e['event_name']} — {e['event_date']}")

    choice = input("\nSelect event to message ticket holders: ").strip()
    try:
        event = events[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    message = input("\n  Type your message:\n  > ").strip()
    tickets = [t for t in read_csv(TICKETS_FILE)
               if t["event_id"] == event["event_id"] and t["payment_status"] in ["PAID", "COMPLIMENTARY"]]

    cost_per_sms = 5
    total_cost   = len(tickets) * cost_per_sms

    print(f"\n  Recipients : {len(tickets)}")
    print(f"  SMS Cost   : KES {total_cost} (KES {cost_per_sms}/SMS)")
    confirm = input("\n  Confirm send? (yes/no): ").strip().lower()

    if confirm == "yes":
        print(f"\n  [SIMULATED] Sending SMS to {len(tickets)} recipients...")
        for t in tickets:
            print(f"  → {t['phone']} ({t['customer_name']}): {message[:40]}...")
        print(f"\n✅ SMS blast sent to {len(tickets)} recipients.")
        print(f"   Total cost: KES {total_cost}")
    else:
        print("  Cancelled.")
    pause()


# ══════════════════════════════════════════════
#  ACCOUNT SETTINGS
# ══════════════════════════════════════════════

def view_profile(client: dict):
    clear()
    banner()
    print(f"\n  MY PROFILE\n")
    divider()
    print(f"  Client ID     : {client['client_id']}")
    print(f"  Business Name : {client['business_name']}")
    print(f"  Owner         : {client['owner_name']}")
    print(f"  Phone         : {client['phone']}")
    print(f"  Email         : {client['email']}")
    print(f"  Plan          : {client['plan']}")
    print(f"  Status        : {client['status']}")
    print(f"  Joined        : {client['joined_date']}")
    pause()


def change_password(client: dict) -> dict:
    clear()
    banner()
    print(f"\n  CHANGE PASSWORD\n")
    divider()

    old_pw = input("  Current Password: ").strip()
    if hash_password(old_pw) != client["password_hash"]:
        print("⚠  Incorrect current password.")
        pause()
        return client

    new_pw  = input("  New Password: ").strip()
    new_pw2 = input("  Confirm New Password: ").strip()
    if new_pw != new_pw2:
        print("⚠  Passwords do not match.")
        pause()
        return client

    clients = read_csv(CLIENTS_FILE)
    updated = []
    for c in clients:
        if c["client_id"] == client["client_id"]:
            c["password_hash"] = hash_password(new_pw)
            client = c
        updated.append(c)
    write_csv(CLIENTS_FILE, updated, CLIENT_HEADERS)

    print("✅ Password changed successfully.")
    pause()
    return client


# ══════════════════════════════════════════════
#  MAIN DASHBOARD MENU
# ══════════════════════════════════════════════

def client_dashboard(client: dict):
    while True:
        clear()
        banner()
        print(f"\n  Welcome, {client['owner_name']} — {client['business_name']}")
        print(f"  Plan: {client['plan']}  |  Today: {today_str()}\n")

        # Count pending cancellations
        pending_count = len([c for c in read_csv(CANCELLATIONS_FILE)
                             if c["client_id"] == client["client_id"]
                             and c["status"] == "PENDING"])
        if pending_count > 0:
            print(f"  ⚠  You have {pending_count} pending cancellation request(s)!\n")

        print("  ── EVENT MANAGEMENT ──")
        print("  [1]  Create New Event")
        print("  [2]  View My Events")
        print("  [3]  Edit Event")
        print("  [4]  Issue Honour Pass")
        print()
        print("  ── TICKET MANAGEMENT ──")
        print("  [5]  View Sold Tickets")
        print("  [6]  Blacklist a Ticket")
        print("  [7]  Download Attendee List")
        print()
        print("  ── CANCELLATIONS ──")
        print("  [8]  View Cancellation Requests")
        print("  [9]  Process Cancellation Requests")
        print()
        print("  ── GATE / ATTENDANCE ──")
        print("  [10] Gate Entry Scanner")
        print("  [11] View Attendance Report")
        print()
        print("  ── FINANCIALS ──")
        print("  [12] Financial Report")
        print("  [13] Request Payout")
        print()
        print("  ── COMMUNICATION ──")
        print("  [14] Send SMS Blast")
        print()
        print("  ── ACCOUNT ──")
        print("  [15] View My Profile")
        print("  [16] Change Password")
        print("  [0]  Logout")
        divider()

        choice = input("  Select option: ").strip()

        if   choice == "1":  create_event(client)
        elif choice == "2":  view_my_events(client)
        elif choice == "3":  edit_event(client)
        elif choice == "4":  issue_honour_pass(client)
        elif choice == "5":  view_sold_tickets(client)
        elif choice == "6":  blacklist_ticket(client)
        elif choice == "7":  download_attendee_list(client)
        elif choice == "8":  view_cancellation_requests(client)
        elif choice == "9":  process_cancellation(client)
        elif choice == "10": scan_ticket_entry(client)
        elif choice == "11": view_attendance(client)
        elif choice == "12": financial_report(client)
        elif choice == "13": request_payout(client)
        elif choice == "14": send_sms_blast(client)
        elif choice == "15": view_profile(client)
        elif choice == "16": client = change_password(client)
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
    while True:
        clear()
        banner()
        print("\n  [1]  Login")
        print("  [2]  Register New Client")
        print("  [0]  Exit")
        divider()

        choice = input("  Select option: ").strip()

        if choice == "1":
            client = login_client()
            if client:
                client_dashboard(client)
        elif choice == "2":
            register_client()
        elif choice == "0":
            print("\n  Goodbye! — BReSCA Ticketzetu\n")
            break
        else:
            print("⚠  Invalid option.")
            pause()


if __name__ == "__main__":
    main()
