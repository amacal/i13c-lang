from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.controlflows import ControlFlowListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_controlflows():
    artifacts = prepare_artifacts("""
        fn main() { foo(); bar(); }
    """)

    draw_list(ControlFlowListExtractor, artifacts).equals("""
        | --------- | ----------- | ------------- | ----- | ----- |
        | Reference | Function ID | Function Name | Nodes | Edges |
        | --------- | ----------- | ------------- | ----- | ----- |
        | 12:18     | function#1  | main          | 4     | 3     |
        | --------- | ----------- | ------------- | ----- | ----- |
    """)
