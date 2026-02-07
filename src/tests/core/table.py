from typing import Dict, List

from i13c.core.table import draw_table


def can_draw_empty_table():
    headers = {"name": "Name", "age": "Age"}
    rows: List[Dict[str, str]] = []

    draw_table(headers, rows).equals("""
        | ---- | --- |
        | Name | Age |
        | ---- | --- |
        | ---- | --- |
    """)


def can_draw_table_with_rows():
    headers = {"name": "Name", "age": "Age"}
    rows = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]

    draw_table(headers, rows).equals("""
        | ----- | --- |
        | Name  | Age |
        | ----- | --- |
        | Alice | 30  |
        | Bob   | 25  |
        | ----- | --- |
    """)
