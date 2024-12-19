import os
from abc import ABC, abstractmethod


class IdentifierStore(ABC):
    @abstractmethod
    def get_last_identifier(self) -> str:
        pass

    @abstractmethod
    def store_identifier(self, identifier: str):
        pass


class LatestOnlyIdentifierStore(IdentifierStore):

    def __init__(self, filename: str):
        self.filename = filename

    def get_last_identifier(self) -> str:
        try:
            with open(self.filename, "r", encoding="ascii") as f:
                return f.readline().strip()
        except FileNotFoundError:
            return ""

    def store_identifier(self, identifier: str):
        with open(self.filename, "w", encoding="ascii") as f:
            f.write(f"{identifier}\n")


class FullLogIdentifierStore(IdentifierStore):
    def __init__(self, filename: str):
        self.filename = filename

    def get_last_identifier(self) -> str:
        try:
            with open(self.filename, "r", encoding="ascii") as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()
                buffer = bytearray()
                for i in range(file_size - 1, -1, -1):
                    f.seek(i)
                    char = f.read(1)
                    if char == "\n" and buffer:
                        break
                    buffer.append(ord(char))
                last_line = buffer[::-1].decode("ascii").strip()
                return last_line
        except FileNotFoundError:
            return ""

    def store_identifier(self, identifier: str):
        with open(self.filename, "a", encoding="ascii") as f:
            f.write(f"{identifier}\n")
