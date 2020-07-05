import pytest
import os
from src.file_service import *

file_service = FileService()


def test_generate_file():
    file = file_service.generate_file(2.0)

    assert file.writable() == True
    assert file.name == "particle_timeline_2.0.txt"

    os.remove(file.name)


def test_append_particle_position():
    file = file_service.generate_file(2.0)
    file_service.append_particle_position(file, 1, 2)
    file.seek(0)

    assert file.readline() == '1 2\n'

    file_service.append_particle_position(file, 3, 4)
    file.seek(4)

    assert file.readline() == '3 4\n'

    os.remove(file.name)
