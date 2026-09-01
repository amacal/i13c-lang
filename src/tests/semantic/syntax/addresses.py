from tests.semantic.syntax import parse_syntax_graph


def can_visit_a_base_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { jmp qword [rax + 0x1234]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1


def can_visit_an_indexed_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { jmp qword [rax + rbx + 0x1234]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1


def can_visit_a_rip_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { jmp qword [rip + 0x1234]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1


def can_visit_a_scaled_index_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { jmp qword [rax + 2 * rbx + 0x1234]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1


def can_visit_a_qword_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { push qword [rax]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1


def can_visit_a_dword_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { push dword [rax]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1


def can_visit_a_word_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { push word [rax]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1


def can_visit_a_byte_address() -> None:
    visitor = parse_syntax_graph("""
            asm main() { push byte [rax]; }
        """)

    assert len(list(visitor.graph.snippet.addresses.items())) == 1
