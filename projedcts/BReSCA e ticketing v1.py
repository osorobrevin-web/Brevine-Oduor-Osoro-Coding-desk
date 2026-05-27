# ============================================================
#  BReSCA e-TICKETING SYSTEM
#  Version 2 — MVP Terminal (Phase 1) + Cancellation System
#  Powered by BReSCA — Brevine e-Systems Consultancy Agency
#  Kisumu, Kenya
#  Founded by: Brevine Oduor Osoro
#  Date: 25th May 2026
#  Intellectual Property of BReSCA
# ============================================================

import csv
import os
import datetime
import getpass

# ── CONSTANTS ────────────────────────────────────────────────
CSV_FILE    = "bresca_tickets.csv"
CLIENT_CODE = "DALA"           # Dala Comedy Club — pioneer client
YEAR        = datetime.datetime.now().strftime("%Y")

TICKET_PRICES = {
    "VVVIP":        5000,
    "VIP":          2000,
    "Regular":       500,
    "Honour Pass":     0,
}

WRISTBANDS = {
    "VVVIP":        "Gold",
    "VIP":          "Blue",
    "Regular":      "Green",
    "Honour Pass":  "White",
}

CSV_HEADERS = [
    "TicketNo", "Client", "EventName", "EventDate", "CancellationDeadline",
    "CustomerName", "Phone", "IDNumber", "Category",
    "Amount", "PaymentStatus", "WristbandColor",
    "FirstEntry", "EntryTime", "Attended",
    "CancelStatus", "CancelRequestedBy", "CancelRequestTime",
    "ClientApproval", "ClientApprovalTime",
    "AdminApproval", "AdminApprovalTime",
    "RefundAmount", "ClientShare", "BReSCAShare", "RefundStatus", "DOA"
]

# ── COMMISSION CALCULATOR ────────────────────────────────────
def calculate_commission(amount):
    if amount == 0:
        return 0
    elif amount <= 500:
        return 50
    elif amount <= 2000:
        return round(amount * 0.08)
    elif amount <= 5000:
        return round(amount * 0.07)
    else:
        return round(amount * 0.06)

# ── TICKET NUMBER GENERATOR ──────────────────────────────────
def generate_ticket_number():
    tickets = read_tickets()
    next_num = len(tickets) + 1
    return f"BReSCA-{YEAR}-{CLIENT_CODE}-{next_num:04d}"

# ── FILE SETUP ───────────────────────────────────────────────
def create_file():
    if os.path.exists(CSV_FILE):
        print(f"Ticket database already exists.")
    else:
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
        print("Ticket database created successfully!")

# ── READ ALL TICKETS ─────────────────────────────────────────
def read_tickets():
    tickets = []
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tickets.append(row)
    return tickets

# ── SAVE UPDATED TICKETS ─────────────────────────────────────
def save_tickets(tickets):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(tickets)

# ── SELL A TICKET ────────────────────────────────────────────
def sell_ticket():
    print("\n" + "="*50)
    print("  SELL TICKET — BReSCA e-Ticketing")
    print("="*50)

    event_name  = input("Event name: ").strip()
    event_date  = input("Event date (DD/MM/YYYY): ").strip()
    cancel_deadline = input("Cancellation deadline (DD/MM/YYYY HH:MM): ").strip()

    print("\nTicket categories:")
    categories = list(TICKET_PRICES.keys())
    for i, cat in enumerate(categories, 1):
        price = TICKET_PRICES[cat]
        print(f"  {i}. {cat} — KES {price:,}")

    while True:
        choice = input("\nSelect category (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            category = categories[int(choice) - 1]
            break
        print("Invalid choice. Try again.")

    print("\nCustomer details:")
    name  = input("Full name: ").strip()
    phone = input("Phone number (MPESA): ").strip()
    id_no = input("ID number: ").strip()

    amount    = TICKET_PRICES[category]
    ticket_no = generate_ticket_number()
    doa       = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    print(f"\n{'='*50}")
    print(f"  ORDER SUMMARY")
    print(f"{'='*50}")
    print(f"  Ticket No : {ticket_no}")
    print(f"  Event     : {event_name} — {event_date}")
    print(f"  Cancel by : {cancel_deadline}")
    print(f"  Customer  : {name}")
    print(f"  Phone     : {phone}")
    print(f"  ID        : {id_no}")
    print(f"  Category  : {category} ({WRISTBANDS[category]} wristband)")
    print(f"  Amount    : KES {amount:,}")
    print(f"{'='*50}")

    if amount == 0:
        print("\n  Honour Pass — no payment required.")
        payment_status = "Honour Pass"
    else:
        confirm = input(f"\nSend MPESA STK Push to {phone}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Ticket sale cancelled.")
            return

        print(f"\n  [MPESA] STK Push sent to {phone}...")
        print(f"  [MPESA] Waiting for customer to enter PIN...")
        pin_confirm = input("  Simulate: customer entered PIN (press Enter): ")
        print(f"  [MPESA] Payment of KES {amount:,} confirmed!")
        payment_status = "Paid"

    commission = calculate_commission(amount)
    net        = amount - commission

    new_ticket = {
        "TicketNo":           ticket_no,
        "Client":             CLIENT_CODE,
        "EventName":          event_name,
        "EventDate":          event_date,
        "CancellationDeadline": cancel_deadline,
        "CustomerName":       name,
        "Phone":              phone,
        "IDNumber":           id_no,
        "Category":           category,
        "Amount":             amount,
        "PaymentStatus":      payment_status,
        "WristbandColor":     WRISTBANDS[category],
        "FirstEntry":         "False",
        "EntryTime":          "",
        "Attended":           "False",
        "CancelStatus":       "Active",
        "CancelRequestedBy":  "",
        "CancelRequestTime":  "",
        "ClientApproval":     "",
        "ClientApprovalTime": "",
        "AdminApproval":      "",
        "AdminApprovalTime":  "",
        "RefundAmount":       0,
        "ClientShare":        0,
        "BReSCAShare":        0,
        "RefundStatus":       "N/A",
        "DOA":                doa,
    }

    tickets = read_tickets()
    tickets.append(new_ticket)
    save_tickets(tickets)

    print(f"\n  TICKET ISSUED SUCCESSFULLY!")
    print(f"  Ticket No : {ticket_no}")
    print(f"  Category  : {category} — {WRISTBANDS[category]} wristband")
    print(f"  Commission: KES {commission:,} (BReSCA)")
    print(f"  Net to you: KES {net:,}")
    print(f"  SMS confirmation would be sent to {phone}")

# ── SCAN ENTRY ───────────────────────────────────────────────
def scan_entry():
    print("\n" + "="*50)
    print("  GATE ENTRY SCAN — BReSCA e-Ticketing")
    print("="*50)

    ticket_no = input("Scan / enter ticket number: ").strip()
    tickets   = read_tickets()

    found = None
    index = None
    for i, t in enumerate(tickets):
        if t["TicketNo"].upper() == ticket_no.upper():
            found = t
            index = i
            break

    if not found:
        print("\n  ENTRY DENIED — Ticket not found!")
        return

    print(f"\n  Ticket    : {found['TicketNo']}")
    print(f"  Customer  : {found['CustomerName']}")
    print(f"  Event     : {found['EventName']} — {found['EventDate']}")
    print(f"  Category  : {found['Category']} ({found['WristbandColor']} wristband)")
    print(f"  Payment   : {found['PaymentStatus']}")

    if found["Attended"] == "True":
        print("\n  ENTRY DENIED — Ticket already used!")
        return

    if found["PaymentStatus"] not in ["Paid", "Honour Pass"]:
        print("\n  ENTRY DENIED — Payment not confirmed!")
        return

    entry_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    tickets[index]["FirstEntry"] = "True"
    tickets[index]["EntryTime"]  = entry_time
    tickets[index]["Attended"]   = "True"
    save_tickets(tickets)

    print(f"\n  ENTRY GRANTED!")
    print(f"  Issue {found['WristbandColor'].upper()} WRISTBAND to customer")
    print(f"  Entry time: {entry_time}")

# ── VIEW ALL TICKETS ─────────────────────────────────────────
def view_tickets():
    print("\n" + "="*50)
    print("  ALL TICKETS — BReSCA e-Ticketing")
    print("="*50)

    tickets = read_tickets()
    if not tickets:
        print("  No tickets sold yet.")
        return

    for t in tickets:
        attended = "ATTENDED" if t["Attended"] == "True" else "NOT ATTENDED"
        print(f"\n  {t['TicketNo']}")
        print(f"  {t['CustomerName']} | {t['Category']} | KES {int(t['Amount']):,}")
        print(f"  Event: {t['EventName']} — {t['EventDate']}")
        print(f"  Status: {t['PaymentStatus']} | {attended}")
        if t["EntryTime"]:
            print(f"  Entered: {t['EntryTime']}")

# ── CANCELLATION SYSTEM ──────────────────────────────────────
# Step 1: Customer requests cancellation
def request_cancellation():
    print("\n" + "="*50)
    print("  STEP 1 — CUSTOMER CANCELLATION REQUEST")
    print("="*50)
    print("  WARNING: Cancellations are subject to 50% penalty.")
    print("  Customer receives 50% | Client keeps 25% | BReSCA keeps 25%")
    print("  Honour Pass tickets cannot be cancelled.")
    print("  Tickets cannot be cancelled after the deadline.")

    ticket_no = input("\nEnter ticket number to cancel: ").strip()
    tickets   = read_tickets()

    found = None
    index = None
    for i, t in enumerate(tickets):
        if t["TicketNo"].upper() == ticket_no.upper():
            found = t
            index = i
            break

    if not found:
        print("\n  ERROR — Ticket not found!")
        return

    print(f"\n  Ticket    : {found['TicketNo']}")
    print(f"  Customer  : {found['CustomerName']}")
    print(f"  Event     : {found['EventName']} — {found['EventDate']}")
    print(f"  Category  : {found['Category']}")
    print(f"  Amount    : KES {int(found['Amount']):,}")
    print(f"  Cancel by : {found['CancellationDeadline']}")

    if found["PaymentStatus"] == "Honour Pass":
        print("\n  DENIED — Honour Pass tickets cannot be cancelled.")
        return

    if found["CancelStatus"] != "Active":
        print(f"\n  DENIED — Ticket status is already: {found['CancelStatus']}")
        return

    if found["Attended"] == "True":
        print("\n  DENIED — Ticket has already been used for entry.")
        return

    now = datetime.datetime.now()
    try:
        deadline = datetime.datetime.strptime(found["CancellationDeadline"], "%d/%m/%Y %H:%M")
        if now > deadline:
            print(f"\n  DENIED — Cancellation deadline has passed ({found['CancellationDeadline']}).")
            print("  No refunds after the deadline. Contact event client if you have concerns.")
            return
    except ValueError:
        print("\n  WARNING — Could not verify deadline. Proceeding with caution.")

    amount        = int(found["Amount"])
    refund_amount = amount // 2
    client_share  = amount // 4
    bresca_share  = amount // 4

    print(f"\n  CANCELLATION BREAKDOWN:")
    print(f"  Ticket price       : KES {amount:,}")
    print(f"  Customer refund    : KES {refund_amount:,} (50%)")
    print(f"  Client keeps       : KES {client_share:,} (25%)")
    print(f"  BReSCA keeps       : KES {bresca_share:,} (25%)")

    confirm = input("\n  Customer confirms cancellation request? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Cancellation request abandoned.")
        return

    requested_by   = input("  Customer name confirming: ").strip()
    request_time   = now.strftime("%d/%m/%Y %H:%M")

    tickets[index]["CancelStatus"]      = "Pending Client Approval"
    tickets[index]["CancelRequestedBy"] = requested_by
    tickets[index]["CancelRequestTime"] = request_time
    tickets[index]["RefundAmount"]      = refund_amount
    tickets[index]["ClientShare"]       = client_share
    tickets[index]["BReSCAShare"]       = bresca_share
    save_tickets(tickets)

    print(f"\n  CANCELLATION REQUEST SUBMITTED.")
    print(f"  Status    : Pending Client Approval")
    print(f"  Submitted : {request_time}")
    print(f"  Next step : Event client must approve before BReSCA processes refund.")

# Step 2: Client approves cancellation
def client_approve_cancellation():
    print("\n" + "="*50)
    print("  STEP 2 — CLIENT APPROVAL")
    print("="*50)
    print("  Review pending cancellation requests and approve or reject.")

    tickets  = read_tickets()
    pending  = [(i, t) for i, t in enumerate(tickets)
                if t["CancelStatus"] == "Pending Client Approval"]

    if not pending:
        print("\n  No cancellation requests pending client approval.")
        return

    print(f"\n  {len(pending)} request(s) awaiting your approval:\n")
    for i, t in pending:
        print(f"  Ticket    : {t['TicketNo']}")
        print(f"  Customer  : {t['CustomerName']} | {t['Category']}")
        print(f"  Requested : {t['CancelRequestTime']} by {t['CancelRequestedBy']}")
        print(f"  Refund    : KES {int(t['RefundAmount']):,} to customer")
        print(f"  You keep  : KES {int(t['ClientShare']):,}")
        print()

    ticket_no = input("Enter ticket number to action: ").strip()
    found = None
    idx   = None
    for i, t in pending:
        if t["TicketNo"].upper() == ticket_no.upper():
            found = t
            idx   = i
            break

    if not found:
        print("\n  Ticket not found in pending list.")
        return

    decision = input("Approve or Reject? (approve/reject): ").strip().lower()
    action_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    if decision == "approve":
        tickets[idx]["CancelStatus"]      = "Pending Admin Approval"
        tickets[idx]["ClientApproval"]    = "Approved"
        tickets[idx]["ClientApprovalTime"]= action_time
        save_tickets(tickets)
        print(f"\n  APPROVED. Forwarded to BReSCA admin for final confirmation.")
        print(f"  Approved at: {action_time}")

    elif decision == "reject":
        tickets[idx]["CancelStatus"]      = "Active"
        tickets[idx]["ClientApproval"]    = "Rejected"
        tickets[idx]["ClientApprovalTime"]= action_time
        tickets[idx]["CancelRequestedBy"] = ""
        tickets[idx]["CancelRequestTime"] = ""
        tickets[idx]["RefundAmount"]      = 0
        tickets[idx]["ClientShare"]       = 0
        tickets[idx]["BReSCAShare"]       = 0
        save_tickets(tickets)
        print(f"\n  REJECTED. Ticket remains active.")
        print(f"  Rejected at: {action_time}")
    else:
        print("\n  Invalid input. No action taken.")

# Step 3: BReSCA admin confirms and triggers refund
def admin_confirm_cancellation():
    print("\n" + "="*50)
    print("  STEP 3 — BReSCA ADMIN FINAL CONFIRMATION")
    print("="*50)
    print("  WARNING: This step triggers the actual MPESA refund.")
    print("  Verify all details carefully before confirming.")

    tickets  = read_tickets()
    pending  = [(i, t) for i, t in enumerate(tickets)
                if t["CancelStatus"] == "Pending Admin Approval"]

    if not pending:
        print("\n  No cancellation requests pending admin approval.")
        return

    print(f"\n  {len(pending)} request(s) awaiting BReSCA admin approval:\n")
    for i, t in pending:
        print(f"  Ticket    : {t['TicketNo']}")
        print(f"  Customer  : {t['CustomerName']} | Phone: {t['Phone']}")
        print(f"  Category  : {t['Category']} | KES {int(t['Amount']):,}")
        print(f"  Requested : {t['CancelRequestTime']} by {t['CancelRequestedBy']}")
        print(f"  Client OK : {t['ClientApproval']} at {t['ClientApprovalTime']}")
        print(f"  Refund    : KES {int(t['RefundAmount']):,} → {t['Phone']}")
        print(f"  Client    : KES {int(t['ClientShare']):,}")
        print(f"  BReSCA    : KES {int(t['BReSCAShare']):,}")
        print()

    ticket_no = input("Enter ticket number to action: ").strip()
    found = None
    idx   = None
    for i, t in pending:
        if t["TicketNo"].upper() == ticket_no.upper():
            found = t
            idx   = i
            break

    if not found:
        print("\n  Ticket not found in pending list.")
        return

    decision = input("Confirm and send refund? (confirm/reject): ").strip().lower()
    action_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    if decision == "confirm":
        refund = int(found["RefundAmount"])
        print(f"\n  [MPESA] Sending KES {refund:,} to {found['Phone']}...")
        print(f"  [MPESA] Refund of KES {refund:,} sent successfully!")

        tickets[idx]["CancelStatus"]     = "Cancelled"
        tickets[idx]["PaymentStatus"]    = "Cancelled"
        tickets[idx]["AdminApproval"]    = "Confirmed"
        tickets[idx]["AdminApprovalTime"]= action_time
        tickets[idx]["RefundStatus"]     = "Refunded"
        save_tickets(tickets)

        print(f"\n  CANCELLATION COMPLETE.")
        print(f"  Ticket {found['TicketNo']} voided permanently.")
        print(f"  Refund KES {refund:,} sent to {found['Phone']}")
        print(f"  Client share  : KES {int(found['ClientShare']):,}")
        print(f"  BReSCA share  : KES {int(found['BReSCAShare']):,}")
        print(f"  Confirmed at  : {action_time}")

    elif decision == "reject":
        tickets[idx]["CancelStatus"]     = "Active"
        tickets[idx]["AdminApproval"]    = "Rejected by Admin"
        tickets[idx]["AdminApprovalTime"]= action_time
        tickets[idx]["ClientApproval"]   = ""
        tickets[idx]["CancelRequestedBy"]= ""
        tickets[idx]["RefundAmount"]     = 0
        tickets[idx]["ClientShare"]      = 0
        tickets[idx]["BReSCAShare"]      = 0
        save_tickets(tickets)
        print(f"\n  REJECTED by BReSCA admin. Ticket restored to Active.")
    else:
        print("\n  Invalid input. No action taken.")


# ── SUMMARY REPORT ───────────────────────────────────────────
def summary():
    print("\n" + "="*50)
    print("  SUMMARY REPORT — BReSCA e-Ticketing")
    print("="*50)

    tickets       = read_tickets()
    total_tickets = len(tickets)
    total_revenue = 0
    total_commission = 0
    attended_count   = 0
    cancelled_count  = 0
    honour_count     = 0
    total_refunds    = 0
    total_client_share  = 0
    total_bresca_share  = 0
    category_count = {cat: 0 for cat in TICKET_PRICES}

    for t in tickets:
        amount     = int(t["Amount"])
        commission = calculate_commission(amount)
        total_revenue    += amount
        total_commission += commission

        category_count[t["Category"]] = category_count.get(t["Category"], 0) + 1

        if t["Attended"] == "True":
            attended_count += 1

        if t["PaymentStatus"] == "Honour Pass":
            honour_count += 1

        if t["CancelStatus"] == "Cancelled":
            cancelled_count     += 1
            total_refunds       += int(t["RefundAmount"])
            total_client_share  += int(t["ClientShare"])
            total_bresca_share  += int(t["BReSCAShare"])

    net_revenue = total_revenue - total_commission - total_refunds

    print(f"\n  Total tickets sold : {total_tickets}")
    print(f"  Attended           : {attended_count}")
    print(f"  Cancelled          : {cancelled_count}")
    print(f"  Honour Passes      : {honour_count}")
    print(f"\n  Ticket breakdown:")
    for cat, count in category_count.items():
        if count > 0:
            print(f"    {cat}: {count}")
    print(f"\n  Gross revenue      : KES {total_revenue:,}")
    print(f"  BReSCA commission  : KES {total_commission:,}")
    print(f"  Cancellation refunds: KES {total_refunds:,}")
    print(f"    Client share     : KES {total_client_share:,}")
    print(f"    BReSCA share     : KES {total_bresca_share:,}")
    print(f"  NET revenue        : KES {net_revenue:,}")

# ── LOGIN ────────────────────────────────────────────────────
def login():
    print("\n" + "="*50)
    print("  BReSCA e-TICKETING SYSTEM")
    print("  Powered by Brevine e-Systems Consultancy Agency")
    print("  Kisumu, Kenya")
    print("="*50)
    user     = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    if user == "BRESCA" and password == "Dala2026":
        return True
    return False

# ── MENU ─────────────────────────────────────────────────────
def show_menu():
    print("\n" + "="*50)
    print("  BReSCA e-TICKETING — DALA COMEDY CLUB")
    print("="*50)
    print("  1. Sell a ticket")
    print("  2. Scan entry (gate)")
    print("  3. View all tickets")
    print("  4. Cancellations:")
    print("     4a. Customer requests cancellation")
    print("     4b. Client approves cancellation")
    print("     4c. Admin confirms & triggers refund")
    print("  5. Summary report")
    print("  6. Exit")
    print("="*50)

def run_menu():
    while True:
        show_menu()
        choice = input("Enter choice (1-6 or 4a/4b/4c): ").strip().lower()

        if choice == "1":
            sell_ticket()
        elif choice == "2":
            scan_entry()
        elif choice == "3":
            view_tickets()
        elif choice == "4a":
            request_cancellation()
        elif choice == "4b":
            client_approve_cancellation()
        elif choice == "4c":
            admin_confirm_cancellation()
        elif choice == "5":
            summary()
        elif choice == "6":
            print("\n  Thank you for using BReSCA e-Ticketing!")
            print("  Powered by BReSCA — Kisumu, Kenya")
            break
        else:
            print("\n  Invalid choice. Enter a number between 1 and 6.")

        input("\nPress Enter to continue...")

# ── PROGRAM START ────────────────────────────────────────────
if __name__ == "__main__":
    create_file()
    attempts = 0

    while attempts < 3:
        if login():
            print("\n  Login successful. Welcome to BReSCA e-Ticketing!")
            run_menu()
            break
        else:
            attempts += 1
            remaining = 3 - attempts
            if attempts == 3:
                print("\n  Access denied. System locked. Contact BReSCA admin.")
            else:
                print(f"\n  Wrong credentials. {remaining} attempt(s) remaining.")