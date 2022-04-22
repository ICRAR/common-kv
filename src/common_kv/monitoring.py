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

import GPUtil
import psutil
import time
from humanfriendly import format_size
from tabulate import tabulate


def monitor(
    sleep: int = 5,
    log_function=print,
    table_format: str = "psql",
    iterations: Optional[int] = None,
    process_parent=0,
    monitor_options: List[str] = (
        "battery",
        "network",
        "memory",
        "cpu",
        "processes",
        "gpu",
    ),
):  # sourcery no-metrics
    process_dictionary = {}
    gpu_available = False

    if "gpu" in monitor_options:
        try:
            GPUtil.getAvailable(order="first", limit=1)
            gpu_available = True
        except ValueError:
            pass

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
            cpu = [[f"{cpu_}%" for cpu_ in psutil.cpu_percent(percpu=True)]]
            log_string += (
                tabulate(
                    cpu,
                    headers=[f"CPU{i+1:02d}" for i in range(len(cpu[0]))],
                    tablefmt=table_format,
                )
                + os.linesep
            )

        if "gpu" in monitor_options:
            log_string += f"----GPU----{os.linesep}"
            if gpu_available:
                gpu_data = [
                    [
                        gpu.id,
                        f"{gpu.load * 100:.1f}%",
                        format_size(gpu.memoryUsed * 1000**2),
                        format_size(gpu.memoryFree * 1000**2),
                        format_size(gpu.memoryTotal * 1000**2),
                        f"{gpu.temperature:.1f}C",
                    ]
                    for gpu in GPUtil.getGPUs()
                ]

                log_string += (
                    tabulate(
                        gpu_data,
                        headers=[
                            "ID",
                            "Load",
                            "Memory Used",
                            "Memory Free",
                            "Memory Total",
                            "Temperature",
                        ],
                        tablefmt=table_format,
                    )
                    + os.linesep
                )

            else:
                log_string += f"No GPU data found{os.linesep}"

        if "processes" in monitor_options:
            # Fetch all the processes associated with me.
            process = process_dictionary.get(os.getpid(), psutil.Process())
            process_name = process.name()
            process_parent_ = process_parent
            while process_parent_ > 0:
                process = process.parent()
                process_parent_ -= 1

            process_ids = [process.pid] + [
                process_.pid
                for process_ in process.children(recursive=True)
                if process_.name() == process_name
            ]

            # Remove dead processes from the map
            for key in process_dictionary:
                if key not in process_ids:
                    del process_dictionary[key]

            log_string += f"----Processes----{os.linesep}"

            process_table = []
            for process_id in process_ids:
                # While fetching the processes, some of the subprocesses may exit
                # Hence we need to put this code in try-except block
                try:
                    if process_id in process_dictionary:
                        p = process_dictionary[process_id]
                    else:
                        p = psutil.Process(process_id)
                        process_dictionary[process_id] = p

                    with p.oneshot():
                        process_table.append(
                            [
                                p.pid,
                                p.ppid(),
                                p.name(),
                                p.status(),
                                f"{str(p.cpu_percent())}%",
                                p.num_threads(),
                            ]
                        )

                except Exception as e:
                    del process_dictionary[process_id]

            log_string += (
                tabulate(
                    process_table,
                    headers=["PID", "PPID", "PNAME", "STATUS", "CPU", "NUM THREADS"],
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
