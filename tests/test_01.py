#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2021
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#
from common_kv.yaml_to_kwargs import read_yaml, get_children


def test_01():
    config = read_yaml("test_01.yaml")

    assert "test1" in config
    assert "test1/files_directory" in config


def test_02():
    config = read_yaml("test_01.yaml")

    assert "common" in config
    assert "test2" in config
    assert "test2/node1" in config


def test_03a():
    config = read_yaml("test_01.yaml")

    children = get_children("test3", **config)

    assert len(children) == 4

    assert "test3" in config
    assert "test3/child1" in config
    assert "test3/child2" in config
    assert "test3/child3" in config
    assert "test3/child4" in config

    assert "child1" in children
    assert "child2" in children
    assert "child3" in children
    assert "child4" in children


def test_03b():
    config = read_yaml("test_01.yaml")

    children = get_children("not a tag", **config)

    assert children is None


def test_03c():
    config = read_yaml("test_01.yaml")

    children = get_children("test3/child4", **config)

    assert children is None


def test_03d():
    config = read_yaml("test_01.yaml")

    children = get_children("", **config)

    assert len(children) == 4
    assert "test1" in children
    assert "common" in children
    assert "test2" in children
    assert "test3" in children
