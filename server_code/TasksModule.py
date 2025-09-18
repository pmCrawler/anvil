import anvil.users
import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def save_task(input):
    app_tables.tasks.add_row(
        event_link=input["event_link"],
        task=input["task"],
        details=input["details"],
        due_date=input["due_date"],
        duration=input["duration"],
        status=int(input["status"]),
    )


@anvil.server.callable
def save_tasks(tasks):
    row = app_tables.tasks.add_row(
        event_id=tasks["event_id"],
        description=tasks["description"],
        by_datetime=tasks["by_datetime"],
        is_done=False,
    )
    return row
