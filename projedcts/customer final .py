"""
╔══════════════════════════════════════════════════════════════════╗
║          TICKETZETU — Powered by BReSCA                          ║
║          CUSTOMER DASHBOARD                                      ║
║          Brevine e-Systems Consultancy Agency, Kisumu Kenya      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import csv
import os
import uuid
import hashlib
from datetime import datetime, date

# ─────────────────────────────────────────────
#  SHARED FILE PATHS  (same as client.py)
# ─────────────────────────────────────────────
CLIENTS_FILE        = "clients.csv"
EVENTS_FILE         = "events.csv"
TICKETS_FILE        = "tickets.csv"
CANCELLATIONS_FILE  = "cancellations.csv"
CUSTOMERS_FILE      = "customers.csv"
REVIEWS_FILE        = "reviews.csv"

# ─────────────────────────────────────────────
#  BRESCA FEE RULES  (must match client.py)
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

CUSTOMER_HEADERS = [
    "customer_id", "full_name", "phone", "id_number",
    "email", "password_hash", "status", "joined_date"
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

REVIEW_HEADERS = [
    "review_id", "ticket_no", "event_id", "event_name",
    "customer_name", "phone", "rating", "comment", "review_date"
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
    print("   CUSTOMER PORTAL")
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
    tickets = read_csv(TICKETS_FILE)
    event_tickets = [t for t in tickets if t["event_id"] == event_id]
    seq = str(len(event_tickets) + 1).zfill(4)
    client_code = client_id[:4].upper()
    year = date.today().year
    return f"TZ-{year}-{client_code}-{seq}"


def compute_refundable_amount(price: float, refund_percent: int) -> float:
    """
    Refund = (price - commission - transaction_cost) * refund_percent / 100
    Commission and transaction cost are NEVER refunded.
    """
    commission = bresca_commission(price)
    deductible = commission + MPESA_TRANSACTION_COST
    refundable_base = max(price - deductible, 0)
    return round(refundable_base * refund_percent / 100, 2)


def init_files():
    ensure_file(CUSTOMERS_FILE, CUSTOMER_HEADERS)
    ensure_file(TICKETS_FILE,   TICKET_HEADERS)
    ensure_file(CANCELLATIONS_FILE, CANCELLATION_HEADERS)
    ensure_file(REVIEWS_FILE,   REVIEW_HEADERS)


# ══════════════════════════════════════════════
#  AUTH — REGISTER & LOGIN
# ══════════════════════════════════════════════

def register_customer():
    clear()
    banner()
    print("\n  CREATE YOUR ACCOUNT\n")
    divider()

    full_name = input("  Full Name: ").strip()
    phone     = input("  Phone Number (07XXXXXXXX): ").strip()
    id_number = input("  National ID Number: ").strip()
    email     = input("  Email Address (optional): ").strip()

    # Check phone not already registered
    customers = read_csv(CUSTOMERS_FILE)
    for c in customers:
        if c["phone"] == phone:
            print("\n⚠  An account with this phone number already exists.")
            print("   Please login instead.")
            pause()
            return

    password  = input("  Create Password: ").strip()
    password2 = input("  Confirm Password: ").strip()
    if password != password2:
        print("\n⚠  Passwords do not match.")
        pause()
        return

    customer_id = str(uuid.uuid4())[:8].upper()

    new_customer = {
        "customer_id":   customer_id,
        "full_name":     full_name,
        "phone":         phone,
        "id_number":     id_number,
        "email":         email,
        "password_hash": hash_password(password),
        "status":        "ACTIVE",
        "joined_date":   today_str()
    }

    append_csv(CUSTOMERS_FILE, new_customer, CUSTOMER_HEADERS)
    print(f"\n✅ Account created successfully!")
    print(f"   Welcome to Ticketzetu, {full_name}!")
    pause()


def login_customer() -> dict | None:
    clear()
    banner()
    print("\n  CUSTOMER LOGIN\n")
    divider()

    phone    = input("  Phone Number: ").strip()
    password = input("  Password: ").strip()

    customers = read_csv(CUSTOMERS_FILE)
    for c in customers:
        if c["phone"] == phone and c["password_hash"] == hash_password(password):
            if c["status"] != "ACTIVE":
                print(f"\n⚠  Your account is {c['status']}. Contact support.")
                pause()
                return None
            print(f"\n✅ Welcome back, {c['full_name']}!")
            pause()
            return c

    print("\n⚠  Invalid phone number or password.")
    pause()
    return None


# ══════════════════════════════════════════════
#  BROWSE EVENTS
# ══════════════════════════════════════════════

def browse_events():
    clear()
    banner()
    print("\n  AVAILABLE EVENTS\n")
    divider()

    events = read_csv(EVENTS_FILE)
    active = [e for e in events if e["status"] == "ACTIVE"]

    if not active:
        print("  No events available right now. Check back soon!")
        pause()
        return

    for i, e in enumerate(active, 1):
        # Get client business name
        clients = read_csv(CLIENTS_FILE)
        organiser = next((c["business_name"] for c in clients
                          if c["client_id"] == e["client_id"]), "Unknown Organiser")

        print(f"\n  [{i}] {e['event_name'].upper()}")
        print(f"       Organiser  : {organiser}")
        print(f"       Date       : {e['event_date']} at {e['event_time']}")
        print(f"       Venue      : {e['venue']}")
        print(f"       Description: {e['description']}")
        print()

        # Show available categories
        categories = []
        if float(e.get("vvvip_price", 0)) > 0 and int(e.get("vvvip_seats", 0)) > 0:
            categories.append(("VVVIP", float(e["vvvip_price"]), int(e["vvvip_seats"])))
        if float(e.get("vip_price", 0)) > 0 and int(e.get("vip_seats", 0)) > 0:
            categories.append(("VIP", float(e["vip_price"]), int(e["vip_seats"])))
        if float(e.get("regular_price", 0)) > 0 and int(e.get("regular_seats", 0)) > 0:
            categories.append(("Regular", float(e["regular_price"]), int(e["regular_seats"])))

        print(f"       TICKETS:")
        for cat, price, seats in categories:
            # Count remaining seats
            sold = len([t for t in read_csv(TICKETS_FILE)
                        if t["event_id"] == e["event_id"]
                        and t["category"] == cat
                        and t["payment_status"] in ["PAID", "COMPLIMENTARY"]])
            remaining = seats - sold
            status_tag = "✅ Available" if remaining > 0 else "❌ SOLD OUT"
            print(f"         {cat:<10} KES {price:>6,.0f}  |  {remaining} seats left  {status_tag}")

        print(f"\n       Cancellation: Cancel by {e['cancel_by_date']} for {e['refund_percent']}% refund")
        divider()

    pause()


def view_event_details(event_id: str):
    events = read_csv(EVENTS_FILE)
    return next((e for e in events if e["event_id"] == event_id), None)


# ══════════════════════════════════════════════
#  BUY TICKET
# ══════════════════════════════════════════════

def buy_ticket(customer: dict):
    clear()
    banner()
    print("\n  BUY A TICKET\n")
    divider()

    events = read_csv(EVENTS_FILE)
    active = [e for e in events if e["status"] == "ACTIVE"]

    if not active:
        print("  No events available.")
        pause()
        return

    for i, e in enumerate(active, 1):
        print(f"  [{i}] {e['event_name']} — {e['event_date']} | {e['venue']}")

    choice = input("\n  Select event: ").strip()
    try:
        event = active[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    # Check if customer already has a ticket for this event
    existing = [t for t in read_csv(TICKETS_FILE)
                if t["event_id"] == event["event_id"]
                and t["phone"] == customer["phone"]
                and t["payment_status"] in ["PAID", "COMPLIMENTARY"]]
    if existing:
        print(f"\n⚠  You already have a ticket for {event['event_name']}.")
        print(f"   Ticket No: {existing[0]['ticket_no']}")
        pause()
        return

    # Build available categories
    categories = {}
    cat_index  = 1

    def check_seat(cat_name, price_key, seat_key):
        price = float(event.get(price_key, 0))
        seats = int(event.get(seat_key, 0))
        if price > 0 and seats > 0:
            sold = len([t for t in read_csv(TICKETS_FILE)
                        if t["event_id"] == event["event_id"]
                        and t["category"] == cat_name
                        and t["payment_status"] in ["PAID", "COMPLIMENTARY"]])
            remaining = seats - sold
            return price, remaining
        return 0, 0

    print(f"\n  {event['event_name'].upper()} — Select Ticket Category\n")

    vvvip_price, vvvip_left = check_seat("VVVIP", "vvvip_price", "vvvip_seats")
    vip_price,   vip_left   = check_seat("VIP",   "vip_price",   "vip_seats")
    reg_price,   reg_left   = check_seat("Regular","regular_price","regular_seats")

    options = []
    if vvvip_price > 0:
        tag = f"({vvvip_left} left)" if vvvip_left > 0 else "(SOLD OUT)"
        print(f"  [1] VVVIP    — KES {vvvip_price:,.0f}  {tag}")
        options.append(("VVVIP", vvvip_price, vvvip_left))
    else:
        options.append(None)

    if vip_price > 0:
        tag = f"({vip_left} left)" if vip_left > 0 else "(SOLD OUT)"
        print(f"  [2] VIP      — KES {vip_price:,.0f}  {tag}")
        options.append(("VIP", vip_price, vip_left))
    else:
        options.append(None)

    if reg_price > 0:
        tag = f"({reg_left} left)" if reg_left > 0 else "(SOLD OUT)"
        print(f"  [3] Regular  — KES {reg_price:,.0f}  {tag}")
        options.append(("Regular", reg_price, reg_left))
    else:
        options.append(None)

    cat_choice = input("\n  Select category (1/2/3): ").strip()
    try:
        selected = options[int(cat_choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    if selected is None:
        print("⚠  That category is not available for this event.")
        pause()
        return

    cat_name, price, seats_left = selected

    if seats_left <= 0:
        print("⚠  Sorry, this category is SOLD OUT.")
        pause()
        return

    # Customer details (pre-fill from account)
    print(f"\n  Your Details (pre-filled from your account):")
    print(f"  Name  : {customer['full_name']}")
    print(f"  Phone : {customer['phone']}")
    print(f"  ID No : {customer['id_number']}")

    use_account = input("\n  Use these details? (yes/no): ").strip().lower()
    if use_account == "yes":
        name    = customer["full_name"]
        phone   = customer["phone"]
        id_no   = customer["id_number"]
        email   = customer["email"]
    else:
        name  = input("  Full Name: ").strip()
        phone = input("  Phone (MPESA registered): ").strip()
        id_no = input("  ID Number: ").strip()
        email = input("  Email (optional): ").strip()

    # Fee breakdown
    commission   = bresca_commission(price)
    txn_cost     = MPESA_TRANSACTION_COST
    total_charge = price  # Customer pays the ticket price; fees deducted from that on backend

    print(f"\n  ── ORDER SUMMARY ──")
    print(f"  Event    : {event['event_name']}")
    print(f"  Date     : {event['event_date']} at {event['event_time']}")
    print(f"  Venue    : {event['venue']}")
    print(f"  Category : {cat_name}")
    print(f"  Price    : KES {price:,.0f}")
    print(f"\n  ── CANCELLATION POLICY ──")
    print(f"  Cancel by   : {event['cancel_by_date']}")
    print(f"  Refund      : {event['refund_percent']}% of refundable amount")
    refundable = compute_refundable_amount(price, int(event["refund_percent"]))
    print(f"  Max refund  : KES {refundable:,.2f}")
    print(f"  (Commission KES {commission:,.0f} + Transaction KES {txn_cost} are non-refundable)")

    print(f"\n  TOTAL TO PAY : KES {total_charge:,.0f}")

    confirm = input("\n  Proceed to payment? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Purchase cancelled.")
        pause()
        return

    # Simulate MPESA STK Push
    print(f"\n  ── MPESA PAYMENT ──")
    print(f"  Sending STK Push to {phone}...")
    print(f"  [SIMULATED] Enter your MPESA PIN on your phone.")
    mpesa_pin = input("  MPESA PIN (simulated — type anything): ").strip()

    if not mpesa_pin:
        print("⚠  Payment cancelled — no PIN entered.")
        pause()
        return

    # Generate ticket
    ticket_no    = generate_ticket_no(event["client_id"], event["event_id"])
    wristband_qr = f"WB-{ticket_no}"

    ticket = {
        "ticket_no":        ticket_no,
        "client_id":        event["client_id"],
        "event_id":         event["event_id"],
        "event_name":       event["event_name"],
        "customer_name":    name,
        "phone":            phone,
        "id_number":        id_no,
        "email":            email,
        "category":         cat_name,
        "price":            price,
        "commission":       commission,
        "transaction_cost": txn_cost,
        "payment_status":   "PAID",
        "wristband_qr":     wristband_qr,
        "first_entry":      "False",
        "entry_time":       "",
        "attended":         "False",
        "refund_amount":    0,
        "refund_status":    "NONE",
        "purchase_date":    today_str()
    }

    append_csv(TICKETS_FILE, ticket, TICKET_HEADERS)

    print(f"\n✅ PAYMENT CONFIRMED!")
    print(f"{'=' * 50}")
    print(f"  TICKET NO   : {ticket_no}")
    print(f"  EVENT       : {event['event_name']}")
    print(f"  DATE        : {event['event_date']} at {event['event_time']}")
    print(f"  VENUE       : {event['venue']}")
    print(f"  CATEGORY    : {cat_name}")
    print(f"  NAME        : {name}")
    print(f"  PHONE       : {phone}")
    print(f"  AMOUNT PAID : KES {price:,.0f}")
    print(f"  QR CODE     : [■■■■■■■] {ticket_no} [■■■■■■■]")
    print(f"{'=' * 50}")
    print(f"\n  [SIMULATED] SMS confirmation sent to {phone}")
    print(f"  Show this QR code at the gate for entry.")
    pause()


# ══════════════════════════════════════════════
#  MY TICKETS
# ══════════════════════════════════════════════

def my_tickets(customer: dict):
    clear()
    banner()
    print(f"\n  MY TICKETS — {customer['full_name']}\n")
    divider()

    tickets = [t for t in read_csv(TICKETS_FILE)
               if t["phone"] == customer["phone"]]

    if not tickets:
        print("  You have no tickets yet. Buy one from Browse Events!")
        pause()
        return

    for i, t in enumerate(tickets, 1):
        print(f"\n  [{i}] {t['ticket_no']}")
        print(f"       Event    : {t['event_name']}")
        print(f"       Category : {t['category']}")
        print(f"       Price    : KES {float(t['price']):,.0f}")
        print(f"       Status   : {t['payment_status']}")
        print(f"       Entry    : {'✅ Attended' if t['attended'] == 'True' else '⏳ Not yet attended'}")
        print(f"       Refund   : {t['refund_status']}")
        print(f"       Purchased: {t['purchase_date']}")
        if t["payment_status"] == "PAID":
            print(f"       QR CODE  : [■■■■■■■] {t['ticket_no']} [■■■■■■■]")
    pause()


def view_ticket_detail(customer: dict):
    clear()
    banner()
    print(f"\n  TICKET DETAILS\n")
    divider()

    ticket_no = input("  Enter Ticket Number: ").strip().upper()
    tickets   = read_csv(TICKETS_FILE)
    ticket    = next((t for t in tickets
                      if t["ticket_no"] == ticket_no
                      and t["phone"] == customer["phone"]), None)

    if not ticket:
        print("⚠  Ticket not found or does not belong to your account.")
        pause()
        return

    event = next((e for e in read_csv(EVENTS_FILE)
                  if e["event_id"] == ticket["event_id"]), {})

    print(f"\n{'=' * 50}")
    print(f"  TICKET NO   : {ticket['ticket_no']}")
    print(f"  EVENT       : {ticket['event_name']}")
    print(f"  DATE        : {event.get('event_date','N/A')} at {event.get('event_time','')}")
    print(f"  VENUE       : {event.get('venue','N/A')}")
    print(f"  CATEGORY    : {ticket['category']}")
    print(f"  NAME        : {ticket['customer_name']}")
    print(f"  PHONE       : {ticket['phone']}")
    print(f"  ID NO       : {ticket['id_number']}")
    print(f"  PRICE       : KES {float(ticket['price']):,.0f}")
    print(f"  STATUS      : {ticket['payment_status']}")
    print(f"  WRISTBAND   : {ticket['wristband_qr']}")
    print(f"  ATTENDED    : {ticket['attended']}")
    print(f"  ENTRY TIME  : {ticket['entry_time'] or 'Not yet'}")
    print(f"  REFUND      : {ticket['refund_status']}")
    print(f"  PURCHASED   : {ticket['purchase_date']}")
    if ticket["payment_status"] == "PAID":
        print(f"\n  QR CODE     : [■■■■■■■] {ticket['ticket_no']} [■■■■■■■]")
    print(f"{'=' * 50}")
    pause()


# ══════════════════════════════════════════════
#  CANCELLATION REQUEST
# ══════════════════════════════════════════════

def request_cancellation(customer: dict):
    clear()
    banner()
    print(f"\n  REQUEST TICKET CANCELLATION\n")
    divider()

    # Show customer's paid tickets
    tickets = [t for t in read_csv(TICKETS_FILE)
               if t["phone"] == customer["phone"]
               and t["payment_status"] == "PAID"]

    if not tickets:
        print("  You have no paid tickets eligible for cancellation.")
        pause()
        return

    for i, t in enumerate(tickets, 1):
        print(f"  [{i}] {t['ticket_no']} — {t['event_name']} | {t['category']} | KES {float(t['price']):,.0f}")

    choice = input("\n  Select ticket to cancel: ").strip()
    try:
        ticket = tickets[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    # Get event cancellation policy
    event = next((e for e in read_csv(EVENTS_FILE)
                  if e["event_id"] == ticket["event_id"]), None)
    if not event:
        print("⚠  Event not found.")
        pause()
        return

    # Check cancel-by date
    cancel_by = datetime.strptime(event["cancel_by_date"], "%Y-%m-%d").date()
    today     = date.today()

    if today > cancel_by:
        print(f"\n⚠  CANCELLATION WINDOW CLOSED")
        print(f"   The cancel-by date was {event['cancel_by_date']}.")
        print(f"   Today is {today_str()}.")
        print(f"   You can no longer cancel this ticket.")
        pause()
        return

    # Check not already requested
    existing_cancel = [c for c in read_csv(CANCELLATIONS_FILE)
                       if c["ticket_no"] == ticket["ticket_no"]
                       and c["status"] not in ["CLIENT_REJECTED", "ADMIN_REJECTED"]]
    if existing_cancel:
        print(f"\n⚠  A cancellation request already exists for this ticket.")
        print(f"   Status: {existing_cancel[0]['status']}")
        pause()
        return

    # Compute refund
    price          = float(ticket["price"])
    refund_percent = int(event["refund_percent"])
    commission     = bresca_commission(price)
    txn_cost       = MPESA_TRANSACTION_COST
    refundable     = compute_refundable_amount(price, refund_percent)

    print(f"\n  ── CANCELLATION POLICY ──")
    print(f"  Cancel by         : {event['cancel_by_date']}")
    print(f"  Ticket Price      : KES {price:,.0f}")
    print(f"  BReSCA Commission : KES {commission:,.0f}  (non-refundable)")
    print(f"  Transaction Cost  : KES {txn_cost}  (non-refundable)")
    print(f"  Refundable Base   : KES {price - commission - txn_cost:,.2f}")
    print(f"  Refund Percent    : {refund_percent}%")
    print(f"  YOU WILL RECEIVE  : KES {refundable:,.2f}")
    print(f"\n  Note: Refund requires approval from the organiser")
    print(f"        and BReSCA admin before processing.")

    confirm = input("\n  Proceed with cancellation request? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Cancelled.")
        pause()
        return

    reason = input("  Reason for cancellation: ").strip()

    cancel_id = str(uuid.uuid4())[:8].upper()

    cancellation = {
        "cancel_id":          cancel_id,
        "ticket_no":          ticket["ticket_no"],
        "event_id":           ticket["event_id"],
        "client_id":          ticket["client_id"],
        "customer_name":      ticket["customer_name"],
        "phone":              ticket["phone"],
        "category":           ticket["category"],
        "price":              price,
        "refund_percent":     refund_percent,
        "refundable_amount":  refundable,
        "reason":             reason,
        "status":             "PENDING",
        "client_action_date": "",
        "client_note":        "",
        "admin_action_date":  "",
        "admin_note":         "",
        "request_date":       now_str()
    }

    append_csv(CANCELLATIONS_FILE, cancellation, CANCELLATION_HEADERS)

    # Update ticket refund status
    all_tickets = read_csv(TICKETS_FILE)
    updated = []
    for t in all_tickets:
        if t["ticket_no"] == ticket["ticket_no"]:
            t["refund_status"] = "PENDING"
        updated.append(t)
    write_csv(TICKETS_FILE, updated, TICKET_HEADERS)

    print(f"\n✅ Cancellation request submitted!")
    print(f"   Cancel ID  : {cancel_id}")
    print(f"   Status     : PENDING — awaiting organiser review")
    print(f"   If approved, KES {refundable:,.2f} will be refunded to {ticket['phone']}")
    print(f"\n   [SIMULATED] SMS confirmation sent to {customer['phone']}")
    pause()


# ══════════════════════════════════════════════
#  VIEW CANCELLATION STATUS
# ══════════════════════════════════════════════

def my_cancellations(customer: dict):
    clear()
    banner()
    print(f"\n  MY CANCELLATION REQUESTS — {customer['full_name']}\n")
    divider()

    cancellations = [c for c in read_csv(CANCELLATIONS_FILE)
                     if c["phone"] == customer["phone"]]

    if not cancellations:
        print("  You have no cancellation requests.")
        pause()
        return

    status_labels = {
        "PENDING":          "⏳ Pending organiser review",
        "CLIENT_APPROVED":  "✅ Organiser approved — awaiting BReSCA admin",
        "CLIENT_REJECTED":  "❌ Rejected by organiser",
        "ADMIN_APPROVED":   "✅ Approved by BReSCA — refund processing",
        "ADMIN_REJECTED":   "❌ Rejected by BReSCA admin",
        "REFUNDED":         "✅ Refund sent to your MPESA"
    }

    for c in cancellations:
        status_display = status_labels.get(c["status"], c["status"])
        print(f"\n  Cancel ID  : {c['cancel_id']}")
        print(f"  Ticket No  : {c['ticket_no']}")
        print(f"  Event      : ", end="")
        event = next((e for e in read_csv(EVENTS_FILE)
                      if e["event_id"] == c["event_id"]), {})
        print(event.get("event_name", "N/A"))
        print(f"  Category   : {c['category']}  | Price: KES {float(c['price']):,.0f}")
        print(f"  Refund Due : KES {float(c['refundable_amount']):,.2f}")
        print(f"  Reason     : {c['reason']}")
        print(f"  Requested  : {c['request_date']}")
        print(f"  STATUS     : {status_display}")
        if c["client_note"]:
            print(f"  Organiser Note : {c['client_note']}")
        if c["admin_note"]:
            print(f"  BReSCA Note    : {c['admin_note']}")
        divider()
    pause()


# ══════════════════════════════════════════════
#  RATE AN EVENT
# ══════════════════════════════════════════════

def rate_event(customer: dict):
    clear()
    banner()
    print(f"\n  RATE AN EVENT\n")
    divider()

    # Only attended events
    tickets = [t for t in read_csv(TICKETS_FILE)
               if t["phone"] == customer["phone"]
               and t["attended"] == "True"
               and t["payment_status"] in ["PAID", "COMPLIMENTARY"]]

    if not tickets:
        print("  You have no attended events to rate yet.")
        pause()
        return

    # Filter out already reviewed
    reviewed = [r["ticket_no"] for r in read_csv(REVIEWS_FILE)
                if r["phone"] == customer["phone"]]
    unreviewed = [t for t in tickets if t["ticket_no"] not in reviewed]

    if not unreviewed:
        print("  You have already rated all your attended events.")
        pause()
        return

    for i, t in enumerate(unreviewed, 1):
        print(f"  [{i}] {t['event_name']} — {t['category']}")

    choice = input("\n  Select event to rate: ").strip()
    try:
        ticket = unreviewed[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠  Invalid selection.")
        pause()
        return

    print(f"\n  Rating: {ticket['event_name']}")
    print("  Stars: 1 = Poor  2 = Fair  3 = Good  4 = Great  5 = Excellent")

    while True:
        try:
            rating = int(input("  Your Rating (1-5): ").strip())
            if 1 <= rating <= 5:
                break
            print("  ⚠  Enter a number between 1 and 5.")
        except ValueError:
            print("  ⚠  Enter a number.")

    comment = input("  Leave a comment (optional): ").strip()
    stars   = "⭐" * rating

    review = {
        "review_id":     str(uuid.uuid4())[:8].upper(),
        "ticket_no":     ticket["ticket_no"],
        "event_id":      ticket["event_id"],
        "event_name":    ticket["event_name"],
        "customer_name": customer["full_name"],
        "phone":         customer["phone"],
        "rating":        rating,
        "comment":       comment,
        "review_date":   today_str()
    }

    append_csv(REVIEWS_FILE, review, REVIEW_HEADERS)
    print(f"\n✅ Thank you for your review!")
    print(f"   {ticket['event_name']}  —  {stars}")
    if comment:
        print(f"   \"{comment}\"")
    pause()


# ══════════════════════════════════════════════
#  ACCOUNT SETTINGS
# ══════════════════════════════════════════════

def view_profile(customer: dict):
    clear()
    banner()
    print(f"\n  MY PROFILE\n")
    divider()
    print(f"  Customer ID : {customer['customer_id']}")
    print(f"  Full Name   : {customer['full_name']}")
    print(f"  Phone       : {customer['phone']}")
    print(f"  ID Number   : {customer['id_number']}")
    print(f"  Email       : {customer['email'] or 'Not provided'}")
    print(f"  Status      : {customer['status']}")
    print(f"  Member Since: {customer['joined_date']}")

    # Quick stats
    my_tkts = [t for t in read_csv(TICKETS_FILE) if t["phone"] == customer["phone"]]
    attended = [t for t in my_tkts if t["attended"] == "True"]
    print(f"\n  Tickets Purchased : {len(my_tkts)}")
    print(f"  Events Attended   : {len(attended)}")
    pause()


def change_password(customer: dict) -> dict:
    clear()
    banner()
    print(f"\n  CHANGE PASSWORD\n")
    divider()

    old_pw = input("  Current Password: ").strip()
    if hash_password(old_pw) != customer["password_hash"]:
        print("⚠  Incorrect current password.")
        pause()
        return customer

    new_pw  = input("  New Password: ").strip()
    new_pw2 = input("  Confirm New Password: ").strip()
    if new_pw != new_pw2:
        print("⚠  Passwords do not match.")
        pause()
        return customer

    customers = read_csv(CUSTOMERS_FILE)
    updated   = []
    for c in customers:
        if c["customer_id"] == customer["customer_id"]:
            c["password_hash"] = hash_password(new_pw)
            customer = c
        updated.append(c)
    write_csv(CUSTOMERS_FILE, updated, CUSTOMER_HEADERS)

    print("✅ Password changed successfully.")
    pause()
    return customer


# ══════════════════════════════════════════════
#  MAIN DASHBOARD MENU
# ══════════════════════════════════════════════

def customer_dashboard(customer: dict):
    while True:
        clear()
        banner()
        print(f"\n  Welcome, {customer['full_name']}")
        print(f"  Today: {today_str()}\n")

        # Notify of any cancellation updates
        updates = [c for c in read_csv(CANCELLATIONS_FILE)
                   if c["phone"] == customer["phone"]
                   and c["status"] in ["ADMIN_APPROVED", "CLIENT_REJECTED",
                                        "ADMIN_REJECTED", "REFUNDED"]]
        if updates:
            print(f"  🔔 You have {len(updates)} cancellation update(s) — check option [6]\n")


        print("  ── EVENTS ──")
        print("  [1]  Browse Available Events")
        print("  [2]  Buy a Ticket")
        print()
        print("  ── MY TICKETS ──")
        print("  [3]  My Tickets")
        print("  [4]  View Ticket Detail")
        print()
        print("  ── CANCELLATIONS ──")
        print("  [5]  Request Ticket Cancellation")
        print("  [6]  My Cancellation Requests & Status")
        print()
        print("  ── REVIEWS ──")
        print("  [7]  Rate an Event")
        print()
        print("  ── ACCOUNT ──")
        print("  [8]  My Profile")
        print("  [9]  Change Password")
        print("  [0]  Logout")
        divider()

        choice = input("  Select option: ").strip()

        if   choice == "1": browse_events()
        elif choice == "2": buy_ticket(customer)
        elif choice == "3": my_tickets(customer)
        elif choice == "4": view_ticket_detail(customer)
        elif choice == "5": request_cancellation(customer)
        elif choice == "6": my_cancellations(customer)
        elif choice == "7": rate_event(customer)
        elif choice == "8": view_profile(customer)
        elif choice == "9": customer = change_password(customer)
        elif choice == "0":
            print("\n  Logging out... See you at the event! 🎉")
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
        print("  [2]  Create Account")
        print("  [3]  Browse Events (no login required)")
        print("  [0]  Exit")
        divider()

        choice = input("  Select option: ").strip()

        if choice == "1":
            customer = login_customer()
            if customer:
                customer_dashboard(customer)
        elif choice == "2":
            register_customer()
        elif choice == "3":
            browse_events()
        elif choice == "0":
            print("\n  Goodbye! — Ticketzetu by BReSCA\n")
            break
        else:
            print("⚠  Invalid option.")
            pause()


if __name__ == "__main__":
    main()
