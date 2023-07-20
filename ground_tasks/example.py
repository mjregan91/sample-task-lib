import json
import os
import tempfile

from pydantic import constr, conint
from quindar import Spacecrafts
from quindar_tdk.core.tasks import BaseGroundTask

from ground_utils.time_utils import get_now


class Task(BaseGroundTask):
    description = "This is an example ground task using quindar-tdk"
    required_parameter: constr(max_length=10)
    required_int: conint(ge=0, le=90)

    default_string: str = "I have a default value"

    def execute(self):
        self.ctx.log.info(
            f"Starting task with parameters: {self.required_parameter}, {self.required_int}, {self.default_string}"
        )
        sc_client = Spacecrafts(api_client=self.ctx.api_client)
        sc_in_the_system = [sc.name for sc in sc_client.get().response]
        sc_dict = [sc.dict(include={"name", "norad_id", "commanding_enabled"}) for sc in sc_client.get().response]

        self.ctx.log.info(f"System is currently managing {len(sc_in_the_system)} spacecrafts: {sc_in_the_system}")

        self.ctx.log.info(f"Current time is: {get_now()}")

        # NOTE: YOU ARE ONLY ALLOWED TO WRITE TO /tmp
        fd, path = tempfile.mkstemp()
        with open(fd, "w") as sc_file:
            sc_file.write(json.dumps(sc_dict, indent=2))

        self.ctx.write_file(source_file_path=path, destination_file_name="spacecraft.json")
