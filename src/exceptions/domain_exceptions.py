"""도메인 예외 정의."""


class InvalidBlankCountError(ValueError):
    """빈칸(0) 개수가 2개가 아닐 때 발생한다."""


class NoSolutionError(ValueError):
    """주어진 입력으로 마방진을 완성할 수 없을 때 발생한다."""
