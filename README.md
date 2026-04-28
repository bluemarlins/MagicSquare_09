# Magic Square (4×4) — 두 빈칸 완성 시스템

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.10+ |
| 아키텍처 | ECB (Entity–Control–Boundary) |
| 방법론 | Dual-Track TDD · Concept-to-Code Traceability |
| 테스트 | 74개 목표 (Domain 29 · Control 3 · UI 19 · Data 13 · Integration 10) |
| 상세 요구 | [PRD.md](PRD.md) (v1.1.0) |
| 에이전트 규칙 | [../.cursorrules](../.cursorrules) |

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [도메인 규칙 요약](#2-도메인-규칙-요약)
3. [ECB 아키텍처](#3-ecb-아키텍처)
4. [방법론 — Dual-Track TDD](#4-방법론--dual-track-tdd)
5. [C2C Traceability — Requirements Traceability Matrix](#5-c2c-traceability--requirements-traceability-matrix)
6. [Epic & User Story](#6-epic--user-story)
7. [구현 To-Do 리스트](#7-구현-to-do-리스트)
8. [에러 코드 7종](#8-에러-코드-7종)
9. [개발 환경](#9-개발-환경)
10. [성공 기준](#10-성공-기준)
11. [참고 문서](#11-참고-문서)

---

## 1. 프로젝트 개요

> **마방진은 훈련의 재료다. 이 프로젝트의 진짜 목적은 Invariant 기반 사고 훈련이다.**

### 1.1 왜 이 프로젝트인가 — Why 체인

```
Why #1: "완성"의 기준이 먼저 정의되어야 한다
    ↓
Why #2: 설계 오류는 프로그램도 막을 수 없다
    ↓
Why #3: TDD는 그 설계 오류를 코드 이전에 잡는 방법이다
    ↓
핵심: "무엇을 만들 것인가"가 아니라
      "어떤 조건이 성립할 때 성공인가"를 먼저 정의해야 한다
```

### 1.2 훈련 목표 4가지

| # | 훈련 목표 | 핵심 질문 | 연관 설계 결정 |
|---|-----------|-----------|----------------|
| ① | Invariant 중심 설계 사고 | "절대 위반할 수 없는 조건은?" | INV-01~INV-09 도출 |
| ② | Dual-Track TDD 적용 | "UI와 Domain을 병렬로 RED→GREEN→REFACTOR 할 수 있는가?" | Track A/B 분리 |
| ③ | 입력/출력 계약 명확화 | "계약은 코드에 어떻게 표현되는가?" | 에러 코드 7종, `int[6]` 출력 |
| ④ | 설계→테스트→구현→리팩토링 흐름 체화 | "각 단계 진입·완료 기준을 지키는가?" | TDD 단계별 규칙 |

---

## 2. 도메인 규칙 요약

### 2.1 불변조건 INV-01~INV-09 (변경 금지)

| ID | 불변조건 | 내용 | 위반 시 |
|----|----------|------|---------|
| **INV-01** | Magic Constant | 모든 행·열·대각선의 합 = **34** | `NoSolutionError` |
| **INV-02** | 숫자 집합 완전성 | 1~16 각각 정확히 1회 등장 | 검증 실패 |
| **INV-03** | 격자 크기 | 행 4개, 각 행 열 4개 | `INVALID_GRID_SIZE` |
| **INV-04** | 빈칸 개수 | 0의 개수 = 정확히 2 | `INVALID_BLANK_COUNT` |
| **INV-05** | 값 범위 | 모든 셀 값 ∈ {0, 1, …, 16} | `INVALID_CELL_VALUE` |
| **INV-06** | 비영 중복 없음 | 0 제외 동일 숫자 2회 이상 금지 | `DUPLICATE_VALUE` |
| **INV-07** | 해 유일성 전제 | 두 빈칸 조합 중 유효한 것은 정확히 1가지 | `NoSolutionError` |
| **INV-08** | 출력 좌표 범위 | r, c ∈ {1, 2, 3, 4} (1-index) | 검증 실패 |
| **INV-09** | 출력 숫자 범위 | n1, n2 ∈ {1,…,16}, n1 ≠ n2 | 검증 실패 |

### 2.2 입출력 계약 (변경 금지)

**입력:** `int[4][4]` — 빈칸은 `0`, 빈칸 수 정확히 2, 각 셀 ∈ {0~16}

**입력 검증 순서 (첫 번째 실패 즉시 반환):**

```
1단계: 격자 크기 검증  → INVALID_GRID_SIZE
2단계: 셀 값 범위 검증 → INVALID_CELL_VALUE
3단계: 빈칸(0) 수 검증 → INVALID_BLANK_COUNT
4단계: 비영 중복 검증  → DUPLICATE_VALUE
```

**출력:** `int[6]` = `[r1, c1, n1, r2, c2, n2]` (1-index 좌표)

**배치 우선순위:**

```
시도 A: smaller → 첫 번째 빈칸, larger → 두 번째 빈칸 (n1 < n2)
시도 B: larger  → 첫 번째 빈칸, smaller → 두 번째 빈칸 (n1 > n2)
두 시도 모두 실패 → NO_SOLUTION
```

---

## 3. ECB 아키텍처

### 3.1 레이어 구조

```
┌─────────────────────────────────────────────────────────┐
│  Boundary Layer  ── 외부 입출력 · 계약 이행             │
│  InputValidator · ResponseFormatter · MagicSquareController │
└───────────────────────┬─────────────────────────────────┘
                        │ 의존 (단방향)
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Control Layer   ── 비즈니스 흐름 조율                  │
│  MagicSquareSolver                                      │
└───────────────────────┬─────────────────────────────────┘
                        │ 의존 (단방향)
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Entity Layer    ── 도메인 순수 로직 (외부 의존 없음)   │
│  MagicSquare · Cell · CellValue · MissingPair · SolveResult │
│  BlankFinder · MissingNumberFinder · MagicSquareValidator   │
│  SolvingStrategy                                        │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Data Layer      ── 저장소 추상화 (Protocol)            │
│  MatrixRepository (Protocol) · InMemoryRepository      │
└─────────────────────────────────────────────────────────┘
```

### 3.2 의존성 규칙

| 방향 | 허용 여부 |
|------|-----------|
| `Boundary → Control → Entity` | ✅ 허용 |
| `Control → Data` (Facade 경유) | ✅ 허용 |
| `Entity → Control` | ❌ 금지 |
| `Entity → Boundary` | ❌ 금지 |
| `Control → Boundary` | ❌ 금지 |
| `Boundary → Data` 직접 | ❌ 금지 (Facade 경유 필수) |

### 3.3 파일 구조

```
magic_square/
├── boundary/
│   ├── input_validator.py
│   ├── response_formatter.py
│   └── magic_square_controller.py
├── control/
│   └── magic_square_solver.py
├── entity/
│   ├── magic_square.py
│   ├── value_objects/
│   │   ├── cell.py · cell_value.py · missing_pair.py · solve_result.py
│   └── services/
│       ├── blank_finder.py · missing_number_finder.py
│       ├── magic_square_validator.py · solving_strategy.py
├── data/
│   ├── matrix_repository.py       ← Protocol 정의
│   └── in_memory_repository.py
├── exceptions/
│   ├── domain_exceptions.py       ← MagicSquareError · NoSolutionError
│   │                                 InvalidBlankCountError · InvalidMissingCountError
│   │                                 IncompleteGridError
│   ├── data_exceptions.py         ← DataLayerError · DuplicateIdError · NotFoundError
│   └── boundary_exceptions.py     ← 에러코드 7종 상수 · SuccessResponse · ErrorResponse
└── tests/
    ├── entity/   ← BF / MF / MV / SS / SR
    ├── boundary/ ← UI-T01~T19
    ├── control/  ← SV-T01~T03
    ├── data/     ← DT-T01~T13
    └── integration/ ← IT-S01~S04, IT-F01~F06
```

---

## 4. 방법론 — Dual-Track TDD

### 4.1 Track 구조

```
Track A (UI Boundary)                  Track B (Domain Logic)
──────────────────────────             ────────────────────────
대상: 입력 검증 + 응답 포맷            대상: 순수 도메인 로직
격리: Domain을 Mock으로 대체           격리: 외부 의존 없음
테스트: UI-T01~T19 (19개)             테스트: BF/MF/MV/SS/SR (29개)
                                       ← SolvingStrategy 포함

        ↘                                      ↙
          Integration (IT-S01~S04, IT-F01~F06)
               Data Layer (DT-T01~T13)
               Control Layer (SV-T01~T03)
```

> Track A 테스트에서 실제 Domain 로직에 의존하는 것은 **금지**다.

### 4.2 TDD 단계 진입·완료 기준

| 단계 | 진입 조건 | 완료 기준 |
|------|-----------|-----------|
| **[RED]** | 없음 (첫 단계) | 새 테스트가 `AssertionError` 또는 `ImportError`로 실패 확인 |
| **[GREEN]** | RED 확인 완료 | 해당 테스트만 통과 + 기존 GREEN 테스트 전체 유지 |
| **[REFACTOR]** | 모든 테스트 GREEN | 커버리지 목표 유지 + 회귀(regression) 없음 확인 |

### 4.3 Scenario Level 정의

| 레벨 | 의미 | 해당 시나리오 |
|------|------|--------------|
| **L0** | 시스템 초기화 · 사전 조건 | 도메인 상수, 객체 생성, 저장소 초기화 |
| **L1** | 정상 흐름 (Happy Path) | 조합 A·B 성공, row-major 순서 |
| **L2** | 경계값 · 엣지 케이스 | 같은 행/열 빈칸, 극단값 쌍, 저장-재솔빙 |
| **L3** | 실패 · 오류 케이스 | 모든 에러 코드, 첫 실패 즉시 반환 |

---

## 5. C2C Traceability — Requirements Traceability Matrix

> **Concept → Invariant(REQ) → Scenario → Test → Code** 수직 추적 체인  
> 이 연결고리가 Concept-to-Code Traceability의 실천이다.

### 5.1 REQ ID ↔ Invariant 매핑

| REQ ID | Invariant | 핵심 내용 |
|--------|-----------|-----------|
| REQ-001 | INV-01 | Magic Constant = 34 (10개 합산 조건) |
| REQ-002 | INV-02 | 숫자 집합 완전성 (1~16 각 1회) |
| REQ-003 | INV-03 | 격자 크기 4×4 고정 |
| REQ-004 | INV-04 | 빈칸 개수 정확히 2 |
| REQ-005 | INV-05 | 셀 값 범위 {0~16} |
| REQ-006 | INV-06 | 비영 중복 금지 |
| REQ-007 | INV-07 | 해 유일성 (시도 A→B) |
| REQ-008 | INV-08 | 출력 좌표 1-index |
| REQ-009 | INV-09 | 출력 숫자 범위·유일성 |

### 5.2 Requirements Traceability Matrix

| Task ID | REQ ID | Scenario Level | Test ID | 컴포넌트 (ECB) | 상태 |
|---------|--------|---------------|---------|---------------|------|
| TASK-001 | REQ-003 | L0 | `test_domain_constants` | Entity | ⬜ TODO |
| TASK-002 | REQ-003 | L0 | `test_magic_square_initializes_4x4` | Entity | ⬜ TODO |
| TASK-003 | REQ-003 | L0 | `test_cell_value_objects` | Entity | ⬜ TODO |
| TASK-004 | REQ-001 | L3 | MV-T02 `test_validator_rejects_invalid_row` | Entity | ⬜ TODO |
| TASK-005 | REQ-001 | L1 | MV-T01 `test_validator_accepts_valid_magic_square` | Entity | ⬜ TODO |
| TASK-006 | REQ-001 | L2 | MV-T03~T07 `test_validator_columns_diagonals` | Entity | ⬜ TODO |
| TASK-007 | REQ-004 | L3 | BF-T03 `test_blank_finder_three_blanks` | Entity | ⬜ TODO |
| TASK-008 | REQ-004 | L1 | BF-T01 `test_blank_finder_two_cells_ordered` | Entity | ⬜ TODO |
| TASK-009 | REQ-004 | L2/L3 | BF-T04~T06 `test_blank_finder_invalid_counts` | Entity | ⬜ TODO |
| TASK-010 | REQ-002·REQ-009 | L1 | MF-T01 `test_missing_finder_ordered_pair` | Entity | ⬜ TODO |
| TASK-011 | REQ-002 | L3 | MF-T02~T05 `test_missing_finder_invalid_count` | Entity | ⬜ TODO |
| TASK-012 | REQ-009 | L2 | `test_missing_pair_extremes` | Entity | ⬜ TODO |
| TASK-013 | REQ-007 | L3 | SS-T03 `test_strategy_no_solution` | Entity | ⬜ TODO |
| TASK-014 | REQ-007 | L1 | SS-T01~T02 `test_strategy_combination_a_and_b` | Entity | ⬜ TODO |
| TASK-015 | REQ-008·REQ-009 | L1 | SR-T01~T06 `test_solve_result_to_list_six` | Entity | ⬜ TODO |
| TASK-016 | REQ-001~REQ-009 | L1 | `test_solver_happy_path` | Control | ⬜ TODO |
| TASK-017 | REQ-007 | L3 | `test_solver_propagates_no_solution` | Control | ⬜ TODO |
| TASK-018 | REQ-007 | L2 | `test_solver_injected_strategy` | Control | ⬜ TODO |
| TASK-019 | REQ-003~REQ-006 | L3 | UI-T계열 `test_input_validator_none` | Boundary | ⬜ TODO |
| TASK-020 | REQ-003~REQ-006 | L3 | IT-F01~F04 `test_validation_order_and_first_failure` | Boundary | ⬜ TODO |
| TASK-021 | REQ-007 | L3 | UI-T09~T19 `test_response_formatter_error_codes` | Boundary | ⬜ TODO |
| TASK-022 | REQ-001~REQ-009 | L1/L3 | `test_controller_success_and_errors` | Boundary | ⬜ TODO |
| TASK-023 | REQ-001~REQ-009 | L1/L2 | IT-S01~S03 `test_solve_happy_and_layout` | 통합 | ⬜ TODO |
| TASK-024 | REQ-003~REQ-007 | L3 | IT-F01~F06 `test_solve_failures` | 통합 | ⬜ TODO |
| TASK-025 | REQ-003 | L2 | IT-S04 `test_save_load_solve` | Data | ⬜ TODO |
| TASK-026 | REQ-004·REQ-008 | L2 | `test_integration_edge_blanks` | 통합 | ⬜ TODO |
| TASK-027 | REQ-001~REQ-009 | L0~L3 | Traceability 대조 | 품질 게이트 | ⬜ TODO |
| TASK-028 | REQ-001~REQ-009 | L0~L3 | `pytest` 74개 전체 GREEN | 품질 게이트 | ⬜ TODO |
| TASK-029 | — | — | ECB import 방향 점검 | 품질 게이트 | ⬜ TODO |
| TASK-030 | REQ-001~REQ-009 | L1~L3 | UX Contract 단언 | Boundary+통합 | ⬜ TODO |

> **상태 표기:** ⬜ TODO · 🔴 RED · 🟡 GREEN · ✅ PASS · ♻️ REFACTOR

---

## 6. Epic & User Story

### Epic-001 — Invariant 기반 4×4 마방진 두 빈칸 완성 시스템

**목표:** 유효한 입력에 대해 두 빈칸을 채워 Magic Constant 34를 만족시키고 `int[6]`을 반환한다.  
무효 입력·무해는 PRD에 정의된 `errorCode`로 응답한다.

### User Story 개요

| ID | 제목 | 핵심 산출물 | REQ |
|----|------|-------------|-----|
| **US-001** | 도메인 보드 표현 및 초기화 | `MagicSquare`, 상수, VO | REQ-003 |
| **US-002** | 보드 유효성 검사 (완성 격자) | `MagicSquareValidator` | REQ-001 |
| **US-003** | 빈칸 탐지 | `BlankFinder` | REQ-004 |
| **US-004** | 후보(누락 숫자) | `MissingNumberFinder`, `MissingPair` | REQ-002·REQ-009 |
| **US-005** | 완성 로직 | `SolvingStrategy`, `SolveResult` | REQ-007·REQ-008 |
| **US-006** | 솔버 조율 | `MagicSquareSolver` | REQ-001~REQ-009 |
| **US-007** | Boundary 입력·응답 | `InputValidator`, `ResponseFormatter`, `MagicSquareController` | REQ-003~REQ-007 |
| **US-008** | 통합·Data | 통합 테스트, `InMemoryRepository` | REQ-003 |
| **US-009** | 커버리지·품질 게이트 | Traceability, pytest GREEN, ECB 점검 | 전체 |

---

## 7. 구현 To-Do 리스트

> **구조:** `Epic → US → TASK → [RED] → [GREEN] → [REFACTOR]`  
> **표기:** `(<<<layer>>>)` — ECB 레이어 · `> [Checkpoint]` — 진행 관문 · `> [Validate]` — 품질 검증

---

### US-001 — 도메인 보드 표현 및 초기화 · L0

```
REQ: REQ-003 (INV-03 격자 크기)
```

- [ ] **TASK-001** · 도메인 상수 검증 · **L0** · `(<<<entity>>>)`
  - [ ] TASK-001-1: `[RED]` `test_domain_constants` 테스트 작성 — MAGIC_CONSTANT, GRID_SIZE, BLANK_COUNT 실패 확인
  - [ ] TASK-001-2: `[GREEN]` `entity/constants.py` 최소 구현 — MAGIC_CONSTANT=34, GRID_SIZE=4, BLANK_COUNT=2
  - [ ] TASK-001-3: `[REFACTOR]` 타입힌트 · 독스트링 추가
  > [Checkpoint] MAGIC_CONSTANT=34, GRID_SIZE=4, VALUE_RANGE_MAX=16, BLANK_COUNT=2 전부 통과 확인 후 진행

- [ ] **TASK-002** · `MagicSquare` 4×4 초기화 · **L0** · `(<<<entity>>>)`
  - [ ] TASK-002-1: `[RED]` `test_magic_square_initializes_4x4` 테스트 작성
  - [ ] TASK-002-2: `[GREEN]` `entity/magic_square.py` 최소 구현 — 4×4 행렬 보유
  - [ ] TASK-002-3: `[REFACTOR]` `constants.py` 상수 참조 확인 (리터럴 4 제거)
  > [Checkpoint] MagicSquare 객체 생성 + grid.shape == (4,4) 통과 확인

- [ ] **TASK-003** · `Cell`, `CellValue` VO · **L0** · `(<<<entity>>>)`
  - [ ] TASK-003-1: `[RED]` `test_cell_value_objects` 테스트 작성 — Cell(row, col), CellValue 불변 확인
  - [ ] TASK-003-2: `[GREEN]` `entity/value_objects/cell.py`, `cell_value.py` 최소 구현
  - [ ] TASK-003-3: `[REFACTOR]` 불변(Immutable) 보장 · `__eq__`, `__hash__` 구현
  > [Validate] `Cell(2,3) == Cell(2,3)` · `Cell` 수정 시 예외 발생 확인

---

### US-002 — 보드 유효성 검사 (Domain) · L1/L2/L3

```
REQ: REQ-001 (INV-01 Magic Constant = 34)
```

- [ ] **TASK-004** · 행 합 실패 검증 · **L3** · `(<<<entity>>>)`
  - [ ] TASK-004-1: `[RED]` MV-T02 `test_validator_rejects_invalid_row` 테스트 작성 — 행 합 ≠ 34 시 False 확인
  - [ ] TASK-004-2: `[GREEN]` `entity/services/magic_square_validator.py` 최소 구현 — 행 합산만
  - [ ] TASK-004-3: `[REFACTOR]` 열·대각선 합산 추가
  > [Checkpoint] MV-T02 RED 확인 후 진행 · GREEN 후 MV-T01 자동 통과 확인

- [ ] **TASK-005** · 10개 합산 조건 전부 통과 · **L1** · `(<<<entity>>>)`
  - [ ] TASK-005-1: `[RED]` MV-T01 `test_validator_accepts_valid_magic_square` 테스트 작성
  - [ ] TASK-005-2: `[GREEN]` 행 4 + 열 4 + 대각선 2 = 10개 조건 구현
  - [ ] TASK-005-3: `[REFACTOR]` `MAGIC_CONSTANT` 상수 참조 · 리터럴 34 제거
  > [Validate] 커버리지 ≥ 95% (entity/) 확인

- [ ] **TASK-006** · 열·대각선 엣지 · **L2** · `(<<<entity>>>)`
  - [ ] TASK-006-1: `[RED]` MV-T03~T07 `test_validator_columns_diagonals` 테스트 작성
  - [ ] TASK-006-2: `[GREEN]` 열 합·주대각선·반대각선 조건 완성
  - [ ] TASK-006-3: `[REFACTOR]` `IncompleteGridError` (0 포함 격자 거부) 추가
  > [Checkpoint] MV-T01~T07 전체 GREEN 확인

---

### US-003 — 빈칸 탐지 · L1/L2/L3

```
REQ: REQ-004 (INV-04 빈칸 개수 = 2)
```

- [ ] **TASK-007** · 빈칸 3개 시 예외 · **L3** · `(<<<entity>>>)`
  - [ ] TASK-007-1: `[RED]` BF-T03 `test_blank_finder_three_blanks` 테스트 작성 — `InvalidBlankCountError` 발생 확인
  - [ ] TASK-007-2: `[GREEN]` `entity/services/blank_finder.py` 최소 구현 — 개수 검증
  - [ ] TASK-007-3: `[REFACTOR]` 예외 메시지 · 타입힌트 정리
  > [Checkpoint] BF-T03 RED → GREEN 순서 준수 확인

- [ ] **TASK-008** · row-major 두 빈칸 반환 · **L1** · `(<<<entity>>>)`
  - [ ] TASK-008-1: `[RED]` BF-T01 `test_blank_finder_two_cells_ordered` 테스트 작성 — `Cell[2]` 반환 확인
  - [ ] TASK-008-2: `[GREEN]` row-major 스캔 구현 — 첫 번째 0이 `Cell[0]`, 두 번째 0이 `Cell[1]`
  - [ ] TASK-008-3: `[REFACTOR]` `Cell` VO 적용 · 좌표 1-index 변환 확인
  > [Validate] `Cell(r1,c1)`, `Cell(r2,c2)` — r1*4+c1 < r2*4+c2 (row-major 순서) 보장

- [ ] **TASK-009** · 빈칸 0·1개 변형 · **L2/L3** · `(<<<entity>>>)`
  - [ ] TASK-009-1: `[RED]` BF-T04~T06 `test_blank_finder_invalid_counts` 테스트 작성 — 0개, 1개 케이스
  - [ ] TASK-009-2: `[GREEN]` 0개·1개 모두 `InvalidBlankCountError` 처리
  - [ ] TASK-009-3: `[REFACTOR]` BF-T01~T06 전체 GREEN + 중복 코드 제거
  > [Checkpoint] BF-T01~T06 전체 GREEN 확인

---

### US-004 — 후보값(누락 숫자) · L1/L2/L3

```
REQ: REQ-002 (INV-02 숫자 집합 완전성) · REQ-009 (INV-09 출력 숫자 범위)
```

- [ ] **TASK-010** · `MissingPair(smaller, larger)` · **L1** · `(<<<entity>>>)`
  - [ ] TASK-010-1: `[RED]` MF-T01 `test_missing_finder_ordered_pair` 테스트 작성 — `MissingPair(3,11)` 확인
  - [ ] TASK-010-2: `[GREEN]` `missing_number_finder.py`, `missing_pair.py` 최소 구현 — 1~16 집합 차이 계산
  - [ ] TASK-010-3: `[REFACTOR]` `smaller < larger` 불변 보장 · `MissingPair` VO 불변 처리
  > [Checkpoint] MF-T01 통과 · `smaller < larger` 항상 보장 확인

- [ ] **TASK-011** · 누락 개수 오류 · **L3** · `(<<<entity>>>)`
  - [ ] TASK-011-1: `[RED]` MF-T02~T05 `test_missing_finder_invalid_count` 테스트 작성 — 누락 ≠ 2 케이스
  - [ ] TASK-011-2: `[GREEN]` `InvalidMissingCountError` 발생 구현
  - [ ] TASK-011-3: `[REFACTOR]` MF-T01~T05 전체 GREEN 확인
  > [Validate] 중복 있는 입력 → 누락 ≠ 2 → 예외 경로 확인

- [ ] **TASK-012** · 극단값 쌍 (1, 16) · **L2** · `(<<<entity>>>)`
  - [ ] TASK-012-1: `[RED]` `test_missing_pair_extremes` 테스트 작성 — `MissingPair(1,16)` 확인
  - [ ] TASK-012-2: `[GREEN]` 극단값 처리 — 별도 분기 없이 일반 로직으로 통과 확인
  - [ ] TASK-012-3: `[REFACTOR]` `VALUE_RANGE_MAX` 상수 참조 확인 (리터럴 16 제거)

---

### US-005 — 완성 로직 · L1/L3

```
REQ: REQ-007 (INV-07 해 유일성) · REQ-008 (INV-08 출력 좌표) · REQ-009 (INV-09 출력 숫자)
```

- [ ] **TASK-013** · 두 조합 실패 → `NoSolutionError` · **L3** · `(<<<entity>>>)`
  - [ ] TASK-013-1: `[RED]` SS-T03 `test_strategy_no_solution` 테스트 작성 — `NoSolutionError` 확인
  - [ ] TASK-013-2: `[GREEN]` `solving_strategy.py`, `solve_result.py` 최소 구현 — A·B 실패 경로
  - [ ] TASK-013-3: `[REFACTOR]` 예외 타입 명시 · bare except 금지 확인
  > [Checkpoint] SS-T03 RED 먼저 확인 후 GREEN 진행

- [ ] **TASK-014** · 시도 A/B 성공 경로 · **L1** · `(<<<entity>>>)`
  - [ ] TASK-014-1: `[RED]` SS-T01~T02 `test_strategy_combination_a_and_b` 테스트 작성
  - [ ] TASK-014-2: `[GREEN]` 시도 A(smaller→첫 빈칸) → 시도 B(larger→첫 빈칸) 순서 구현
  - [ ] TASK-014-3: `[REFACTOR]` `MagicSquareValidator` 주입 가능 구조 · IT-S01~S02 통과 확인
  > [Validate] 시도 A 성공 시 시도 B 미실행 확인 (SS-T01 통과 후 SS-T02 별도 검증)

- [ ] **TASK-015** · `SolveResult` → `int[6]` 1-index · **L1** · `(<<<entity>>>)`
  - [ ] TASK-015-1: `[RED]` SR-T01~T06 `test_solve_result_to_list_six` 테스트 작성
  - [ ] TASK-015-2: `[GREEN]` `SolveResult.to_list()` — `[r1,c1,n1,r2,c2,n2]` 반환 구현
  - [ ] TASK-015-3: `[REFACTOR]` 좌표 유효성(INV-08) · 숫자 유효성(INV-09) 생성자 검증 추가
  > [Checkpoint] SR-T01~T06 전체 GREEN · r,c ∈ {1~4}, n ∈ {1~16}, n1≠n2 모두 보장 확인

---

### US-006 — Control (솔버 조율) · L1/L2/L3

```
REQ: REQ-001~REQ-009 (전체 불변조건)
```

- [ ] **TASK-016** · 유효 격자 E2E와 동일 결과(단위) · **L1** · `(<<<control>>>)`
  - [ ] TASK-016-1: `[RED]` `test_solver_happy_path` 테스트 작성 — `InputValidator` 미호출 확인 필수
  - [ ] TASK-016-2: `[GREEN]` `control/magic_square_solver.py` 구현 — BlankFinder→MissingFinder→Strategy 조율
  - [ ] TASK-016-3: `[REFACTOR]` 의존성 주입(DI) 구조 — Strategy 교체 가능 확인
  > [Checkpoint] Control이 InputValidator를 직접 호출하지 않음 확인 (ECB 규칙)

- [ ] **TASK-017** · `NoSolutionError` 전파(변환 없음) · **L3** · `(<<<control>>>)`
  - [ ] TASK-017-1: `[RED]` `test_solver_propagates_no_solution` 테스트 작성
  - [ ] TASK-017-2: `[GREEN]` Control에서 예외 변환 없이 그대로 전파 구현
  - [ ] TASK-017-3: `[REFACTOR]` 예외 타입 주석 · Raises 독스트링 추가
  > [Validate] `NoSolutionError`가 Boundary까지 도달하는지 통합 테스트로 확인

- [ ] **TASK-018** · Strategy 주입 가능 · **L2** · `(<<<control>>>)`
  - [ ] TASK-018-1: `[RED]` `test_solver_injected_strategy` 테스트 작성 — Mock Strategy 주입 확인
  - [ ] TASK-018-2: `[GREEN]` 생성자 DI 또는 Protocol 기반 Strategy 주입 구현
  - [ ] TASK-018-3: `[REFACTOR]` `isinstance()` 레이어 간 타입 분기 금지 확인
  > [Checkpoint] Strategy Mock 교체 후 동일 인터페이스 통과 확인

---

### US-007 — Boundary (입력 검증 · 응답 포맷) · L1/L3

```
REQ: REQ-003~REQ-007 (INV-03~INV-07 — 4단계 검증 순서)
```

- [ ] **TASK-019** · `None` → `INVALID_INPUT` · **L3** · `(<<<boundary>>>)`
  - [ ] TASK-019-1: `[RED]` UI-T계열 `test_input_validator_none` 테스트 작성 — `errorCode: "INVALID_INPUT"` 확인
  - [ ] TASK-019-2: `[GREEN]` `boundary/input_validator.py` — None 처리 (0단계) 구현
  - [ ] TASK-019-3: `[REFACTOR]` 메시지 문구 상수 정의 · 변경 금지 주석 추가
  > [Checkpoint] `message == "입력 행렬이 null입니다."` 정확히 일치 확인

- [ ] **TASK-020** · 4단계 검증 순서·첫 실패만 · **L3** · `(<<<boundary>>>)`
  - [ ] TASK-020-1: `[RED]` IT-F01~F04 `test_validation_order_and_first_failure` 테스트 작성 — 복합 오류 시 첫 번째만 반환 확인
  - [ ] TASK-020-2: `[GREEN]` 1→2→3→4단계 순서 검증 · 첫 실패 즉시 반환 구현
  - [ ] TASK-020-3: `[REFACTOR]` 검증 순서 변경 금지 주석 · `bare except` 금지 확인
  > [Checkpoint] 크기+값 동시 오류 → `INVALID_GRID_SIZE`만 반환 · 값+빈칸 → `INVALID_CELL_VALUE`만 반환

- [ ] **TASK-021** · Domain 예외 → `ErrorResponse` · **L3** · `(<<<boundary>>>)`
  - [ ] TASK-021-1: `[RED]` UI-T09~T19 `test_response_formatter_error_codes` 테스트 작성 — 7종 에러코드 매핑
  - [ ] TASK-021-2: `[GREEN]` `boundary/response_formatter.py` — `NoSolutionError` → `{errorCode: "NO_SOLUTION"}` 변환
  - [ ] TASK-021-3: `[REFACTOR]` 모든 Domain 예외 → 표준 `ErrorResponse` 변환 확인
  > [Validate] Domain 예외가 호출자에게 직접 노출되지 않음 확인

- [ ] **TASK-022** · `MagicSquareController` 단일 진입점 · **L1/L3** · `(<<<boundary>>>)`
  - [ ] TASK-022-1: `[RED]` `test_controller_success_and_errors` 테스트 작성 — 성공/실패 모든 경로 확인
  - [ ] TASK-022-2: `[GREEN]` `boundary/magic_square_controller.py` — InputValidator → Solver → ResponseFormatter 조율
  - [ ] TASK-022-3: `[REFACTOR]` Repository 직접 호출 금지 확인 · ECB 의존성 방향 검토
  > [Checkpoint] Controller가 Data Layer를 직접 호출하지 않음 확인 (Facade 경유 필수)

---

### US-008 — 통합 · Data · L1/L2/L3

```
REQ: REQ-001~REQ-009 (전체 통합)
```

- [ ] **TASK-023** · IT-S01~S03 통합 시나리오 · **L1/L2** · `(<<<통합>>>)`
  - [ ] TASK-023-1: `[RED]` `tests/integration/test_solve_happy_and_layout` 테스트 작성 — 조합 A/B, 같은 행 빈칸
  - [ ] TASK-023-2: `[GREEN]` 전 스택 조율 — 실제 컴포넌트로 통과
  - [ ] TASK-023-3: `[REFACTOR]` Mock 없는 E2E 경로 · fixture scope=function 확인
  > [Checkpoint] IT-S01~S03 전체 GREEN 확인 후 TASK-024 진행

- [ ] **TASK-024** · IT-F01~F06 실패·복합 순서 · **L3** · `(<<<통합>>>)`
  - [ ] TASK-024-1: `[RED]` `tests/integration/test_solve_failures` 테스트 작성 — 에러 코드 7종 E2E 확인
  - [ ] TASK-024-2: `[GREEN]` `controller`, `input_validator` 통합 실패 경로 완성
  - [ ] TASK-024-3: `[REFACTOR]` IT-F01~F06 전체 GREEN · Boundary+Control 연결 확인
  > [Validate] 에러 코드 7종 전체 E2E 통과 확인

- [ ] **TASK-025** · 저장·로드·재솔빙 · **L2** · `(<<<data>>>)`
  - [ ] TASK-025-1: `[RED]` IT-S04 `test_save_load_solve` 테스트 작성 — 저장 후 로드한 격자 재솔빙 동일 결과 확인
  - [ ] TASK-025-2: `[GREEN]` `data/in_memory_repository.py` — save/load/exists/delete + deep copy 구현
  - [ ] TASK-025-3: `[REFACTOR]` DT-T01~T13 전체 GREEN · deep copy 불변성 확인
  > [Checkpoint] 원본 격자 수정 후 저장된 격자 불변 확인 (DT-T12~T13)

- [ ] **TASK-026** · L2 엣지 (동일 열·대각선 빈칸) · **L2** · `(<<<통합>>>)`
  - [ ] TASK-026-1: `[RED]` `test_integration_edge_blanks` 테스트 작성 — 같은 열/대각선 빈칸 케이스
  - [ ] TASK-026-2: `[GREEN]` 엣지 케이스 통합 테스트 통과
  - [ ] TASK-026-3: `[REFACTOR]` row-major 순서 보장 재확인 (c1=c2 일 때 r1 < r2)
  > [Validate] IT-S01~S04 + 엣지 전체 GREEN 확인

---

### US-009 — 테스트 커버리지 · 품질 게이트

```
REQ: REQ-001~REQ-009 (전체 추적성 검증)
```

- [ ] **TASK-027** · PRD §14 Traceability 대조 · **L0~L3**
  - [ ] TASK-027-1: INV-01~INV-09 각각에 대응하는 테스트 ID 주석 확인 (`# INV-0x`)
  - [ ] TASK-027-2: 테스트 함수 내 `# BF-T01 — INV-04` 형식 주석 전수 확인
  - [ ] TASK-027-3: Traceability Matrix (§5.2) 빠진 항목 없음 확인
  > [Checkpoint] INV-01~INV-09 전부 테스트 ID와 1:1 연결 확인

- [ ] **TASK-028** · `pytest` 74개 전체 GREEN
  - [ ] TASK-028-1: `pytest tests/ -v` 실행 — 74개 전체 GREEN 확인
  - [ ] TASK-028-2: `pytest tests/ --cov=entity --cov=boundary --cov=data --cov-report=term-missing` — 커버리지 목표 달성 확인
  > [Validate] Domain ≥ 95% · UI ≥ 85% · Data ≥ 80%

- [ ] **TASK-029** · ECB 의존성 위반 여부 점검
  - [ ] TASK-029-1: `entity/` 내에서 `boundary` 또는 `control` import 없음 확인
  - [ ] TASK-029-2: `control/` 내에서 `boundary` import 없음 확인
  - [ ] TASK-029-3: `boundary/` 내에서 `data/` 직접 import 없음 확인
  > [Checkpoint] ECB 위반 0건 · 매직 넘버(34, 4, 16 리터럴) 0건

- [ ] **TASK-030** · Dual-Track UX Contract 단언 · **L1~L3**
  - [ ] TASK-030-1: Track A 테스트에서 실제 Domain 로직 의존 없음 확인 (Mock 100%)
  - [ ] TASK-030-2: 통합/Boundary에서 `{"result": [...]}` 응답 스키마 단언 확인
  - [ ] TASK-030-3: `{"errorCode": "...", "message": "..."}` 에러 스키마 단언 확인
  > [Validate] 응답 스키마 계약 위반 0건 확인

---

## 8. 에러 코드 7종

| errorCode | 발생 조건 | 메시지 문구 (변경 금지) | 처리 레이어 |
|-----------|----------|------------------------|------------|
| `INVALID_INPUT` | 입력이 `None` | `"입력 행렬이 null입니다."` | Boundary |
| `INVALID_GRID_SIZE` | 행 수 ≠ 4 또는 열 수 ≠ 4 | `"행렬 크기는 4×4이어야 합니다."` | Boundary |
| `INVALID_CELL_VALUE` | 셀 값 ∉ {0,…,16} | `"셀 값은 0 또는 1~16이어야 합니다. 위치: (행{r}, 열{c}), 값: {v}"` | Boundary |
| `INVALID_BLANK_COUNT` | 빈칸 수 ≠ 2 | `"빈칸(0)은 정확히 2개이어야 합니다. 현재: {count}개"` | Boundary |
| `DUPLICATE_VALUE` | 0 제외 동일 숫자 2회 이상 | `"중복된 값이 있습니다. 값: {v}"` | Boundary |
| `NO_SOLUTION` | 두 조합 모두 마방진 불만족 | `"입력된 행렬로 마방진을 완성할 수 없습니다."` | Domain → Boundary 변환 |
| `INTERNAL_ERROR` | 예상치 못한 예외 | `"내부 오류가 발생했습니다."` | Boundary (최후 방어) |

> 위치는 1-index 기준. 메시지 끝 마침표(`.`) 필수. **문구 변경 금지.**

---

## 9. 개발 환경

> `pyproject.toml` / 패키지 추가 후 아래 경로를 저장소에 맞게 조정하세요.

```bash
# 환경 설정
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[dev]"         # 또는 pip install -r requirements.txt

# 테스트 실행
pytest tests/ -v                # 전체 실행
pytest tests/ --cov=entity --cov=boundary --cov=data --cov-report=term-missing

# 코드 품질
black . --check                 # 포매터 검사
isort . --check-only            # import 순서 검사

# 매직 넘버 스캔 (REFACTOR 단계 이후 0건 목표)
rg --type py "[^A-Z_\"'(]\b(34|16|4)\b[^)]" entity/ control/

# ECB 역방향 import 검사
rg --type py "from boundary|import boundary" entity/ control/
rg --type py "from control|import control" entity/
```

---

## 10. 성공 기준

| 기준 ID | 항목 | 목표값 | 측정 방법 |
|---------|------|--------|-----------|
| **SC-01** | Domain Logic 테스트 커버리지 | ≥ 95% | `pytest --cov=entity` |
| **SC-02** | 입력 검증 계약 테스트 통과율 | 100% | `pytest tests/boundary/` |
| **SC-03** | 하드코딩(매직 넘버) 잔존 여부 | 0건 | `rg` 패턴 스캔 |
| **SC-04** | Invariant → Test 추적 가능성 | INV-01~INV-09 전체 커버 | 테스트 주석 `INV-xx` 확인 |
| **SC-05** | UI Boundary 테스트 커버리지 | ≥ 85% | `pytest --cov=boundary` |
| **SC-06** | Data Layer 테스트 커버리지 | ≥ 80% | `pytest --cov=data` |
| **SC-07** | 전체 테스트 케이스 통과 | 74개 전체 GREEN | `pytest tests/ -v` |
| **SC-08** | ECB 레이어 의존성 방향 위반 | 0건 | import 방향 수동 검토 |
| **SC-09** | 입력 검증 + 풀이 응답 시간 | < 100ms | `pytest-benchmark` |

---

## 11. 참고 문서

| 문서 | 용도 |
|------|------|
| [PRD.md](PRD.md) | 불변조건, 입출력 계약, Gherkin(L0~L3), 테스트 ID, Traceability (원본) |
| `Report/05` ~ `Report/06` | PRD 작성 및 README 작성 보고 |

---

*To-Do → Scenario → Test → Code의 C2C Traceability가 이 문서의 핵심 구조입니다.  
구현 세부 및 Gherkin 시나리오 전문은 항상 [PRD.md](PRD.md)를 우선합니다.*
