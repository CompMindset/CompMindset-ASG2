import warnings
# Suppress pkg_resources deprecation warning from Flask-Admin
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

import click
from flask.cli import AppGroup
from App import create_app
from App.database import db
from App.models import *

from App.controllers.user import create_user, list_users
from App.controllers.shift import create_shift, assign_shift, publish_roster, list_all_shifts
from App.controllers.attendance import clock_in, clock_out
from App.controllers.request import make_request, decide_request
from App.controllers.report import generate_weekly_report
from App.controllers.initialize import initialize as initialize_all
from App.controllers.auth import login as auth_login

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()
app = create_app()

# ---- DB init ----
@app.cli.command("init")
def init_db():
    db.create_all()
    console.print(Panel.fit("✅ Database initialized successfully!", style="green bold"))

# ---- initialize (drop+create+seed) ----
@app.cli.command("initialize")
def initialize_cmd():
    msg = initialize_all()
    console.print(Panel.fit("🔄 Database reset and seeded with demo users", style="blue bold"))
    console.print("Demo Users Created:", style="bold yellow")
    console.print("  👤 admin1 / adminpass (Admin)")
    console.print("  👤 staff1 / staffpass (Staff)")  
    console.print("  👤 staff2 / staffpass (Staff)")

# ---- auth (JWT) ----
auth_cli = AppGroup("auth", help="Authentication helpers")

@auth_cli.command("login")
@click.argument("username")
@click.argument("password")
def auth_login_cmd(username, password):
    token = auth_login(username, password)
    if token:
        console.print(f"🔐 Login successful for [bold green]{username}[/bold green]")
        console.print(Panel(f"JWT Token:\n{token}", title="Authentication Token", style="green"))
    else:
        console.print(f"❌ Login failed for [bold red]{username}[/bold red] - Invalid credentials", style="red")

app.cli.add_command(auth_cli)

# ---- users ----
user_cli = AppGroup("user", help="User management")

@user_cli.command("create")
@click.argument("role")        # ADMIN|STAFF
@click.argument("full_name")
@click.argument("email")
@click.argument("username")
@click.argument("password")
def user_create(role, full_name, email, username, password):
    try:
        u = create_user(role, full_name, email, username, password)
        role_emoji = "👑" if role.upper() == "ADMIN" else "👤"
        console.print(f"✅ {role_emoji} [bold green]{role.title()}[/bold green] user created successfully!")
        
        table = Table(title="User Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("ID", str(u.id))
        table.add_row("Username", u.username)
        table.add_row("Full Name", u.full_name)
        table.add_row("Email", u.email)
        table.add_row("Role", u.role)
        
        console.print(table)
    except Exception as e:
        console.print(f"❌ Failed to create user: [red]{str(e)}[/red]")

@user_cli.command("list")
def user_list():
    """List all users in the system"""
    try:
        users = list_users()
        if not users:
            console.print("👥 No users found in the system")
            return
        
        table = Table(title="📋 All Users")
        table.add_column("ID", style="cyan")
        table.add_column("Username", style="white")
        table.add_column("Full Name", style="green")
        table.add_column("Email", style="blue")
        table.add_column("Role", style="yellow")
        
        for u in users:
            role_emoji = "👑" if u.role == "ADMIN" else "👤"
            table.add_row(
                str(u.id),
                u.username,
                u.full_name,
                u.email,
                f"{role_emoji} {u.role}"
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"❌ Failed to list users: [red]{str(e)}[/red]")

app.cli.add_command(user_cli)

# ---- shifts ----
shift_cli = AppGroup("shift", help="Shift operations")

@shift_cli.command("create")
@click.argument("admin_id", type=int)
@click.argument("start")      # 2025-09-29T09:00
@click.argument("end")        # 2025-09-29T17:00
@click.argument("location")
@click.argument("week_start") # 2025-09-29
def shift_create(admin_id, start, end, location, week_start):
    try:
        s = create_shift(admin_id, start, end, location, week_start)
        console.print(f"✅ [bold green]Shift #{s.id}[/bold green] created successfully!")
        
        table = Table(title="Shift Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Shift ID", str(s.id))
        table.add_row("Location", s.location)
        table.add_row("Start Time", str(s.start_time))
        table.add_row("End Time", str(s.end_time))
        table.add_row("Week Start", str(s.week_start))
        table.add_row("Status", s.status)
        
        console.print(table)
    except Exception as e:
        console.print(f"❌ Failed to create shift: [red]{str(e)}[/red]")

@shift_cli.command("assign")
@click.argument("shift_id", type=int)
@click.argument("staff_id", type=int)
def shift_assign_cmd(shift_id, staff_id):
    try:
        s = assign_shift(shift_id, staff_id)
        console.print(f"✅ [bold green]Shift #{s.id}[/bold green] assigned to [bold blue]Staff #{s.staff_id}[/bold blue]")
        console.print(f"📅 {s.start_time} - {s.end_time} @ {s.location}")
    except Exception as e:
        console.print(f"❌ Failed to assign shift: [red]{str(e)}[/red]")

@shift_cli.command("publish")
@click.argument("week_start")
def shift_publish_cmd(week_start):
    shifts = publish_roster(week_start)
    
    if not shifts:
        console.print(f"📅 No shifts found for week starting [yellow]{week_start}[/yellow]")
        return
    
    table = Table(title=f"📋 Weekly Roster - Week of {week_start}")
    table.add_column("Shift ID", style="cyan")
    table.add_column("Date/Time", style="white")
    table.add_column("Location", style="green")
    table.add_column("Staff ID", style="blue")
    table.add_column("Status", style="yellow")
    
    for s in shifts:
        status_color = "green" if s.status == "ASSIGNED" else "yellow"
        table.add_row(
            str(s.id),
            f"{s.start_time} - {s.end_time}",
            s.location,
            str(s.staff_id) if s.staff_id else "Unassigned",
            f"[{status_color}]{s.status}[/{status_color}]"
        )
    
    console.print(table)

@shift_cli.command("all")
def shift_all_cmd():
    shifts = list_all_shifts()
    
    if not shifts:
        console.print("📅 No shifts found in the system")
        return
    
    table = Table(title="📋 All Shifts")
    table.add_column("ID", style="cyan")
    table.add_column("Week", style="white")
    table.add_column("Date/Time", style="white")
    table.add_column("Location", style="green")
    table.add_column("Staff", style="blue")
    table.add_column("Status", style="yellow")
    
    for s in shifts:
        status_color = "green" if s.status == "ASSIGNED" else "yellow"
        table.add_row(
            str(s.id),
            str(s.week_start),
            f"{s.start_time} - {s.end_time}",
            s.location,
            str(s.staff_id) if s.staff_id else "Unassigned",
            f"[{status_color}]{s.status}[/{status_color}]"
        )
    
    console.print(table)

app.cli.add_command(shift_cli)

# ---- attendance ----
att_cli = AppGroup("att", help="Attendance/time logs")

@att_cli.command("in")
@click.argument("shift_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("ts")  # 2025-09-29T09:04
def att_in_cmd(shift_id, staff_id, ts):
    try:
        rec = clock_in(shift_id, staff_id, ts)
        status_emoji = "✅" if rec.status == "ON_TIME" else "⚠️"
        status_color = "green" if rec.status == "ON_TIME" else "yellow"
        
        console.print(f"{status_emoji} [bold]Clock In Recorded[/bold]")
        console.print(f"👤 Staff #{staff_id} | 🕐 {ts}")
        console.print(f"Status: [{status_color}]{rec.status}[/{status_color}]")
        console.print(f"Attendance ID: {rec.id}")
    except Exception as e:
        console.print(f"❌ Failed to clock in: [red]{str(e)}[/red]")

@att_cli.command("out")
@click.argument("shift_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("ts")
def att_out_cmd(shift_id, staff_id, ts):
    try:
        rec = clock_out(shift_id, staff_id, ts)
        console.print("✅ [bold green]Clock Out Recorded[/bold green]")
        console.print(f"👤 Staff #{staff_id} | 🕐 {ts}")
        console.print(f"Attendance ID: {rec.id}")
        
        if rec.clockIn and rec.clockOut:
            duration = rec.clockOut - rec.clockIn
            hours = duration.total_seconds() / 3600
            console.print(f"⏱️  Total Time: [bold cyan]{hours:.2f} hours[/bold cyan]")
    except Exception as e:
        console.print(f"❌ Failed to clock out: [red]{str(e)}[/red]")

app.cli.add_command(att_cli)

# ---- requests ----
req_cli = AppGroup("req", help="Swap / time-off requests")

@req_cli.command("make")
@click.argument("staff_id", type=int)
@click.argument("admin_id", type=int)
@click.argument("req_type")  # SWAP|TIME-OFF
@click.argument("reason", default="")
@click.option("--shift", "shift_id", type=int, default=None)
def req_make_cmd(staff_id, admin_id, req_type, reason, shift_id):
    try:
        r = make_request(staff_id, admin_id, req_type, reason, shift_id)
        req_emoji = "🔄" if req_type == "SWAP" else "🏖️"
        
        console.print(f"{req_emoji} [bold green]Request Created Successfully![/bold green]")
        
        table = Table(title="Request Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Request ID", str(r.id))
        table.add_row("Type", req_type)
        table.add_row("Staff ID", str(staff_id))
        table.add_row("Admin ID", str(admin_id))
        table.add_row("Reason", reason or "No reason provided")
        table.add_row("Target Shift", str(shift_id) if shift_id else "N/A")
        table.add_row("Status", f"[yellow]{r.status}[/yellow]")
        
        console.print(table)
    except Exception as e:
        console.print(f"❌ Failed to create request: [red]{str(e)}[/red]")

@req_cli.command("decide")
@click.argument("request_id", type=int)
@click.argument("decision")  # APPROVED|REJECTED
def req_decide_cmd(request_id, decision):
    try:
        r = decide_request(request_id, decision)
        decision_emoji = "✅" if decision == "APPROVED" else "❌"
        decision_color = "green" if decision == "APPROVED" else "red"
        
        console.print(f"{decision_emoji} [bold]Request #{r.id}[/bold] has been [{decision_color}]{r.status}[/{decision_color}]")
        console.print(f"Type: {r.type} | Staff: #{r.requestingStaffID}")
    except Exception as e:
        console.print(f"❌ Failed to process request: [red]{str(e)}[/red]")

app.cli.add_command(req_cli)

# ---- reports ----
rep_cli = AppGroup("report", help="Weekly reports")

@rep_cli.command("gen")
@click.argument("week_start")
def rep_gen_cmd(week_start):
    try:
        rpt = generate_weekly_report(week_start)
        
        console.print(f"📊 [bold green]Weekly Report Generated![/bold green]")
        console.print()
        
        # Create a nice report summary
        report_panel = Panel.fit(
            f"Week: [cyan]{rpt.weekStart}[/cyan]\n"
            f"Total Shifts: [yellow]{rpt.totalShifts}[/yellow]\n"  
            f"Total Hours: [green]{rpt.totalHours}[/green]\n"
            f"Generated: [white]{rpt.generatedAt}[/white]",
            title=f"📈 Report #{rpt.id}",
            style="blue"
        )
        
        console.print(report_panel)
        
        # Additional stats if available
        if rpt.totalShifts > 0:
            avg_hours = rpt.totalHours / rpt.totalShifts
            console.print(f"📊 Average hours per shift: [cyan]{avg_hours:.2f}[/cyan]")
            
    except Exception as e:
        console.print(f"❌ Failed to generate report: [red]{str(e)}[/red]")

app.cli.add_command(rep_cli)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
