class TestDomainConstantsRed:
    def test_magic_constant_grid_size_blank_count_constants(self) -> None:
        from tests.red_helpers import load_attr

        magic_constant = load_attr("entity.constants", "MAGIC_CONSTANT")
        grid_size = load_attr("entity.constants", "GRID_SIZE")
        blank_count = load_attr("entity.constants", "BLANK_COUNT")

        assert magic_constant == 34
        assert grid_size == 4
        assert blank_count == 2
