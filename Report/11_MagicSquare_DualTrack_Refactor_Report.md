# 4×4 Magic Square — Dual-Track 클린 리팩토링 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square — 두 빈칸 완성 시스템 |
| **보고서 유형** | Dual-Track 클린 리팩토링 작업 보고서 |
| **작성일** | 2026-04-28 |
| **작업 기준** | Dual-Track Refactor Skill (커밋 1개 단위) |
| **목적** | 동작 유지 전제하에 Magic Number 제거(R-L3) 및 합산 헬퍼 추출(R-L2)로 Logic Track 가독성 개선 |
| **최종 상태** | 57 passed (GREEN 유지), 린터 오류 없음 |

---

## 목차

1. [작업 배경](#1-작업-배경)
2. [기준선 확인](#2-기준선-확인)
3. [Code Smell 탐지 결과](#3-code-smell-탐지-결과)
4. [리팩토링 목표 선택](#4-리팩토링-목표-선택)
5. [보호 테스트 점검](#5-보호-테스트-점검)
6. [리팩토링 상세](#6-리팩토링-상세)
7. [테스트 재실행 결과](#7-테스트-재실행-결과)
8. [주요 변경 파일](#8-주요-변경-파일)
9. [위험 요소 및 롤백 포인트](#9-위험-요소-및-롤백-포인트)
10. [커밋 메시지 제안](#10-커밋-메시지-제안)
11. [품질 게이트 체크리스트](#11-품질-게이트-체크리스트)

---

## 1. 작업 배경

GREEN 구현 및 `src/` 구조 리팩토링이 완료된 상태(보고서 #10)에서,  
내부 구조의 추가적인 개선을 위해 **Dual-Track Refactor Skill** 워크플로우를 적용했다.

- 작업 원칙: **동작 유지 + 출력 계약 고정 + 단일 커밋**
- 적용 범위: Logic Track (Domain 레이어) 2개 항목
- UI Track(Boundary 레이어): 이번 커밋에서 변경 없음

---

## 2. 기준선 확인

리팩토링 시작 전 전체 테스트를 실행하여 GREEN 기준선을 확보했다.

```
명령: .venv\Scripts\python.exe -m pytest --tb=short -q
결과: 57 passed in 0.23s  ✅ GREEN
```

---

## 3. Code Smell 탐지 결과

1차 스캔에서 발견된 후보 목록:

| # | Smell 종류 | 위치 | 징후 |
|---|-----------|------|------|
| S1 | **Magic Number** | `src/entity/constants.py:6` | `MAGIC_CONSTANT: int = 34` — 4×4 마방진 상수를 공식 없이 하드코딩 |
| S2 | **Mysterious Name** | `src/entity/services/magic_square_validator.py:30` | 열 합산 제너레이터 안에서 외부 for-loop 변수명 `row`를 재사용 → 이름 충돌 |
| S3 | **Long Method (inline)** | `src/entity/services/magic_square_validator.py:29–35` | 열·대각선 합 계산이 인라인 제너레이터로 중복 패턴 반복 |
| S4 | **Duplicated Logic** | `src/entity/services/solving_strategy.py:29–35` | `preferred_order + list(permutations(...))` 조합이 항상 4개(중복 2개)를 생성 후 `tried` set으로 걸러내는 불필요한 순환 |

---

## 4. 리팩토링 목표 선택

2차 우선순위 기준(위험도 낮음 / 범위 좁음 / 개선 효율 높음)으로 2개 선택:

| ID | 선택 | 이유 |
|----|------|------|
| **R-L3** | ✅ 선택 | Magic Number 제거 — 1줄 수정, 위험 최저, 의도 가독성 즉각 향상 |
| **R-L2** | ✅ 선택 | 합산 헬퍼 추출 — 변수명 충돌 해소 + 각 합산 의도를 함수명으로 명시 |
| S4 | 보류 | 동작 의도 변경 위험 존재, 다음 커밋으로 이월 |

---

## 5. 보호 테스트 점검

대상 영역(`magic_square_validator`, `entity/constants`)에 대한 계약 테스트가 충분히 존재함을 확인했다.

| 보호 테스트 | 파일 | 상태 |
|------------|------|------|
| 행 합 불일치 False 반환 | `test_magic_square_validator_red.py` | ✅ 존재 |
| 열 합 불일치 False 반환 | `test_magic_square_validator_red.py` | ✅ 존재 |
| 주 대각선 합 불일치 False 반환 | `test_magic_square_validator_red.py` | ✅ 존재 |
| 역 대각선 합 불일치 False 반환 | `test_magic_square_validator_red.py` | ✅ 존재 |
| MAGIC_CONSTANT 값 검증 | `test_domain_constants.py` | ✅ 존재 |

보강 불필요 — 기존 테스트로 충분히 보호됨.

---

## 6. 리팩토링 상세

### 6.1 R-L3: MAGIC_CONSTANT 하드코딩 제거

**대상 파일**: `src/entity/constants.py`

#### 변경 전

```python
MAGIC_CONSTANT: int = 34
```

#### 변경 후

```python
MAGIC_CONSTANT: int = GRID_SIZE * (GRID_SIZE * GRID_SIZE + 1) // 2
```

**개선 포인트**

- n×n 마방진 상수 공식 `n(n²+1)/2` 이 코드 자체에서 드러남
- `GRID_SIZE`가 바뀌어도 `MAGIC_CONSTANT`가 자동으로 연동됨
- 34라는 숫자가 어디서 왔는지 주석 없이도 추론 가능

---

### 6.2 R-L2: is_magic_square 합산 헬퍼 추출

**대상 파일**: `src/entity/services/magic_square_validator.py`

#### 변경 전 (문제 구간)

```python
for col in range(GRID_SIZE):
    if sum(grid[row][col] for row in range(GRID_SIZE)) != MAGIC_CONSTANT:
        return False

main_diagonal = sum(grid[idx][idx] for idx in range(GRID_SIZE))
anti_diagonal = sum(grid[idx][GRID_SIZE - 1 - idx] for idx in range(GRID_SIZE))
return main_diagonal == MAGIC_CONSTANT and anti_diagonal == MAGIC_CONSTANT
```

- `row`가 외부 `for row in grid` 루프와 내부 제너레이터 양쪽에서 사용 → Mysterious Name
- 3가지 합산 방식(열/주대각선/역대각선)이 인라인 제너레이터로 혼재 → 독자가 패턴을 직접 해석해야 함

#### 변경 후

```python
def _sum_col(grid: list[list[int]], col: int) -> int:
    return sum(grid[r][col] for r in range(GRID_SIZE))


def _sum_main_diag(grid: list[list[int]]) -> int:
    return sum(grid[i][i] for i in range(GRID_SIZE))


def _sum_anti_diag(grid: list[list[int]]) -> int:
    return sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE))


# is_magic_square 내부
if any(_sum_col(grid, col) != MAGIC_CONSTANT for col in range(GRID_SIZE)):
    return False

return (
    _sum_main_diag(grid) == MAGIC_CONSTANT
    and _sum_anti_diag(grid) == MAGIC_CONSTANT
)
```

**개선 포인트**

- `_sum_col`, `_sum_main_diag`, `_sum_anti_diag` — 의도가 함수명에서 명확히 드러남
- 제너레이터 내 변수 `r`, `i` — 외부 루프와의 이름 충돌 완전 해소
- `is_magic_square` 본문이 "무엇을 검사하는가"의 흐름으로 읽힘

---

## 7. 테스트 재실행 결과

```
명령: .venv\Scripts\python.exe -m pytest --tb=short -q
결과: 57 passed in 0.33s  ✅ ALL GREEN
```

| 테스트 파일 | 결과 |
|------------|------|
| `tests/entity/test_domain_constants.py` | PASS |
| `tests/entity/test_blank_finder_red.py` | PASS |
| `tests/entity/test_magic_square_validator_red.py` | PASS |
| `tests/entity/test_solving_strategy_red.py` | PASS |
| `tests/boundary/test_input_validator_red.py` | PASS |
| `tests/boundary/test_solution_contract_red.py` | PASS |
| `tests/gui/test_app.py` | PASS |

린터 진단(`ReadLints`): 변경 파일 기준 오류 없음.

---

## 8. 주요 변경 파일

| 파일 | 구분 | Track |
|------|------|-------|
| `src/entity/constants.py` | 수정 | Logic Track |
| `src/entity/services/magic_square_validator.py` | 수정 | Logic Track |

---

## 9. 위험 요소 및 롤백 포인트

| 항목 | 내용 |
|------|------|
| **위험 수준** | 최저 — 외부 계약(입출력/예외) 변경 없음 |
| **롤백 방법** | `entity/constants.py`의 수식을 `34`로 되돌리고, `magic_square_validator.py`의 헬퍼 3개 삭제 후 원래 인라인 제너레이터 복원 |
| **보류 항목** | S4 (`solving_strategy.py` 중복 순환) — 다음 커밋에서 검토 |

---

## 10. 커밋 메시지 제안

```
refactor(domain): derive MAGIC_CONSTANT from GRID_SIZE and extract sum helpers
```

> `entity/constants.py`: 하드코딩된 `34`를 `n(n²+1)/2` 공식으로 교체  
> `magic_square_validator.py`: 열·대각선 합 계산을 `_sum_col` / `_sum_main_diag` / `_sum_anti_diag` 헬퍼로 분리

---

## 11. 품질 게이트 체크리스트

| 항목 | 상태 |
|------|------|
| 기능 변화 없음 | ✅ |
| 출력 포맷 변화 없음 | ✅ |
| 예외 계약 변화 없음 | ✅ |
| 테스트 전체 PASS (57 passed) | ✅ |
| 변경 범위가 단일 커밋으로 설명 가능 | ✅ |
| 린터 오류 없음 | ✅ |

---

*본 보고서는 Dual-Track Refactor Skill 워크플로우에 따라 수행한 Magic Number 제거 및 합산 헬퍼 추출 작업의 결과를 기록한다.*
