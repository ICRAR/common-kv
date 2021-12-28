#
#  ICRAR - International Centre for Radio Astronomy Research
#  UWA - The University of Western Australia
#
#  Copyright (c) 2021.
#  Copyright by UWA (in the framework of the ICRAR)
#  All rights reserved
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#  MA 02111-1307  USA
#
import os
from typing import Optional, List

import psutil
import time
from humanfriendly import format_size
from tabulate import tabulate


def monitor(
    sleep: int = 5,
    log_function=print,
    table_format: str = "psql",
    iterations: Optional[int] = None,
    cpu_interval=1,
    process_parent=0,
    monitor_options: List[str] = ("battery", "network", "memory", "cpu", "processes"),
):  # sourcery no-metrics
    # Run an infinite loop to constantly monitor the system
    while iterations is None or iterations > 0:
        log_string = f"{os.linesep}============================Process Monitor============================{os.linesep}"

        if "battery" in monitor_options:
            # Fetch the battery information
            battery = psutil.sensors_battery().percent
            log_string += (
                f"----Battery Available----{os.linesep}{battery:.1f}%{os.linesep}"
            )

        if "network" in monitor_options:
            # Fetch the Network information
            log_string += f"----Networks----{os.linesep}"
            table = []
            for key in psutil.net_if_stats().keys():
                name = key
                up = "Up" if psutil.net_if_stats()[key].isup else "Down"
                speed = psutil.net_if_stats()[key].speed
                table.append([name, up, format_size(speed)])
            log_string += (
                tabulate(
                    table, headers=["Network", "Status", "Speed"], tablefmt=table_format
                )
                + os.linesep
            )

        if "memory" in monitor_options:
            # Fetch the memory information
            log_string += f"----Memory----{os.linesep}"
            vm = psutil.virtual_memory()
            log_string += (
                tabulate(
                    [
                        [
                            format_size(vm.total),
                            format_size(vm.used),
                            format_size(vm.available),
                            f"{vm.percent}%",
                        ]
                    ],
                    headers=["Total", "Used", "Available", "Percentage"],
                    tablefmt=table_format,
                )
                + os.linesep
            )

        if "cpu" in monitor_options:
            # Fetch the CPU information
            log_string += f"----CPU----{os.linesep}"
            cpu = [
                [
                    f"{cpu_}%"
                    for cpu_ in psutil.cpu_percent(interval=cpu_interval, percpu=True)
                ]
            ]
            log_string += (
                tabulate(
                    cpu,
                    headers=[f"CPU{i+1:02d}" for i in range(len(cpu[0]))],
                    tablefmt=table_format,
                )
                + os.linesep
            )

        if "processes" in monitor_options:
            # Fetch all the processes associated with me.
            process = psutil.Process()
            process_name = process.name()
            process_parent_ = process_parent
            while process_parent_ > 0:
                process = process.parent()
                process_parent_ -= 1

            processes = [
                process_.pid
                for process_ in process.children(recursive=True)
                if process_.name() == process_name
            ]
            if process_parent > 0:
                processes.append(process.pid)

            log_string += f"----Processes----{os.linesep}"

            process_table = []
            for process in processes:
                # While fetching the processes, some of the subprocesses may exit
                # Hence we need to put this code in try-except block
                try:
                    p = psutil.Process(process)
                    process_table.append(
                        [
                            str(process),
                            p.name(),
                            p.status(),
                            str(p.cpu_percent()) + "%",
                            p.num_threads(),
                        ]
                    )

                except Exception as e:
                    pass

            log_string += (
                tabulate(
                    process_table,
                    headers=["PID", "PNAME", "STATUS", "CPU", "NUM THREADS"],
                    tablefmt=table_format,
                )
                + os.linesep
            )

        # Log it
        log_function(log_string)

        if iterations is not None:
            if iterations == 1:
                break
            else:
                iterations -= 1

        # Create a delay
        time.sleep(sleep)
