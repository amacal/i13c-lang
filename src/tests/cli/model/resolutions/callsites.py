from i13c.cli.model import draw_list
from i13c.cli.model.resolutions.callsites import (
    BindingsOfCallSiteResolutionListExtractor,
    CallSiteResolutionListExtractor,
)
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_callsite_resolutions():
    artifacts = prepare_artifacts(
        """
            fn foo() {}
            fn foo(x: u16) {}
            fn main() { foo(0x123); }
        """
    )

    draw_list(CallSiteResolutionListExtractor, artifacts).equals(
        """
            | --------- | ----------- | ----------- | --------- | -------- | -------- |
            | Reference | CallSite ID | Callee Name | Arguments | Accepted | Rejected |
            | --------- | ----------- | ----------- | --------- | -------- | -------- |
            | 79:89     | callsite#5  | foo         | 1         | 1        | 1        |
            | --------- | ----------- | ----------- | --------- | -------- | -------- |
        """
    )


def can_draw_a_table_with_callsite_resolutions_bindings():
    artifacts = prepare_artifacts(
        """
            fn foo() {}
            fn foo(x: u16) {}
            fn main() { foo(0x123); }
        """
    )

    draw_list(BindingsOfCallSiteResolutionListExtractor, artifacts).equals(
        """
            | --------- | ----------- | ----------- | ------------- | ------------ |
            | Reference | CallSite ID | Callee Name | Binding Index | Binding Kind |
            | --------- | ----------- | ----------- | ------------- | ------------ |
            | 79:89     | callsite#5  | foo         | 0             | argument     |
            | --------- | ----------- | ----------- | ------------- | ------------ |
        """
    )
