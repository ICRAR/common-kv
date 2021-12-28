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
from common_kv.monitoring import monitor


def test_01():
    log_string = []

    def logger(string):
        log_string.append(string)

    monitor(iterations=1, log_function=logger)

    assert log_string is not None
    assert len(log_string) == 1
    assert "----Battery Available----" in log_string[0]
    assert "----Networks----" in log_string[0]
    assert "----Memory----" in log_string[0]
    assert "----CPU----" in log_string[0]
    assert "----Processes----" in log_string[0]


def test_02():
    log_string = []

    def logger(string):
        log_string.append(string)

    monitor(iterations=1, log_function=logger, monitor_options=["battery"])

    assert log_string is not None
    assert len(log_string) == 1
    assert "----Battery Available----" in log_string[0]
    assert "----Networks----" not in log_string[0]
    assert "----Memory----" not in log_string[0]
    assert "----CPU----" not in log_string[0]
    assert "----Processes----" not in log_string[0]


def test_03():
    log_string = []

    def logger(string):
        log_string.append(string)

    monitor(
        sleep=1, iterations=5, log_function=logger, monitor_options=["cpu", "processes"]
    )

    assert log_string is not None
    assert len(log_string) == 5
    assert "----Battery Available----" not in log_string[0]
    assert "----Networks----" not in log_string[0]
    assert "----Memory----" not in log_string[0]
    assert "----CPU----" in log_string[0]
    assert "----Processes----" in log_string[0]
