from tests.semantic.syntax import parse_syntax_graph


def can_visit_flags_in_a_snippet() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() noreturn clobbers rax, rbx { call; }
        """
    )

    assert len(list(visitor.graph.snippet.flags.items())) == 1


def can_ignore_flags_in_a_snippet_without_any_flag_specified() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call; }
        """
    )

    assert len(list(visitor.graph.snippet.flags.items())) == 0
