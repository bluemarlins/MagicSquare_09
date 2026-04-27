# Magic Square (4×4) — Epic · User Journey 설계 문서

> **목적:** 사용자 여정(Epic → User Story → Task) 구조를 통해 훈련 목표와 실행 흐름을 명확히 정의한다  
> **날짜:** 2026-04-27  
> **연관 문서:** 보고서 01 (문제 정의) · 보고서 02 (TDD + Clean Architecture 설계) · `.cursorrules`

---

## 목차

1. [Level 1 — Epic (비즈니스 목표)](#1-level-1--epic-비즈니스-목표)
2. [Level 2 — User Journey (사용자 여정)](#2-level-2--user-journey-사용자-여정)

---

## 1. Level 1 — Epic (비즈니스 목표)

### Epic: "Invariant(불변조건) 기반 사고 훈련 시스템 구축"

---

### 1.1 목적

4×4 Magic Square 문제를 활용하여 아래 4가지 사고 능력을 체계적으로 훈련한다.

| # | 훈련 목표 | 핵심 질문 |
|---|-----------|-----------|
| ① | **Invariant 중심 설계 사고** | "이 시스템이 절대 위반해서는 안 되는 조건은 무엇인가?" |
| ② | **Dual-Track TDD 적용** | "UI 계약과 Domain 로직을 동시에 RED → GREEN → REFACTOR로 진행할 수 있는가?" |
| ③ | **입력/출력 계약 명확화** | "호출자와 구현자가 동의한 계약(Contract)은 코드에 어떻게 표현되는가?" |
| ④ | **설계 → 테스트 → 구현 → 리팩토링 흐름 체화** | "각 단계의 진입 조건과 완료 기준을 지키며 진행하고 있는가?" |

> 이 훈련의 본질은 **"마방진을 푼다"가 아니라**  
> **"불변조건으로부터 계약을 도출하고, 계약으로부터 테스트를 작성하고,  
> 테스트로부터 구현을 추출하는 사고 근육을 기른다"**이다.

---

### 1.2 성공 기준

| 기준 ID | 항목 | 목표값 | 측정 방법 |
|---------|------|--------|-----------|
| SC-01 | Domain Logic 테스트 커버리지 | **≥ 95%** | `pytest --cov=entity` |
| SC-02 | 입력 검증 계약 테스트 통과율 | **100%** | `pytest tests/boundary/` |
| SC-03 | 하드코딩 (매직 넘버) 잔존 여부 | **0건** | 코드 리뷰 + `rg '[^A-Z_][0-9]{1,2}[^0-9]'` |
| SC-04 | Invariant → Test 추적 가능성 | **INV-01~INV-09 전체** | 테스트 주석의 `INV-xx` 태그 확인 |
| SC-05 | UI Boundary 테스트 커버리지 | **≥ 85%** | `pytest --cov=boundary` |
| SC-06 | Data Layer 테스트 커버리지 | **≥ 80%** | `pytest --cov=data` |
| SC-07 | 전체 테스트 케이스 통과 | **71개 전체 GREEN** | `pytest tests/ -v` |
| SC-08 | ECB 레이어 의존성 방향 위반 | **0건** | import 방향 수동 검토 |

---

### 1.3 Epic 범위 (In-Scope / Out-of-Scope)

| 구분 | 항목 |
|------|------|
| **In-Scope** | 4×4 마방진 두 빈칸 풀이 로직 |
| **In-Scope** | ECB 레이어 분리 (Entity / Control / Boundary / Data) |
| **In-Scope** | 71개 테스트 케이스 (Domain · Boundary · Data · Integration) |
| **In-Scope** | 입력 검증 4단계 계약 (크기 → 값 범위 → 빈칸 수 → 중복) |
| **In-Scope** | 에러 코드 7종 정의 및 응답 포맷 표준화 |
| **Out-of-Scope** | GUI / Web UI 구현 |
| **Out-of-Scope** | 데이터베이스 영속성 (파일 저장 / DB) |
| **Out-of-Scope** | 5×5 이상 마방진 확장 |
| **Out-of-Scope** | 빈칸이 2개가 아닌 케이스의 풀이 |

---

### 1.4 도메인 불변조건 (Invariant) 요약

Epic의 모든 User Story는 아래 9가지 불변조건을 기반으로 도출된다.

| ID | 불변조건 | 관련 레이어 |
|----|----------|-------------|
| INV-01 | 모든 행·열·대각선 합 = **34** | Entity |
| INV-02 | 1~16 각각 정확히 1회 등장 | Entity |
| INV-03 | 격자 크기 = **4×4** | Boundary, Entity |
| INV-04 | 빈칸(0) 개수 = **정확히 2** | Boundary, Entity |
| INV-05 | 셀 값 ∈ {0, 1, …, 16} | Boundary, Entity |
| INV-06 | 0 제외 중복 없음 | Boundary, Entity |
| INV-07 | 유효 조합 = **정확히 1가지** | Control, Entity |
| INV-08 | 출력 좌표 r, c ∈ {1, 2, 3, 4} | Boundary |
| INV-09 | 출력 숫자 n1, n2 ∈ {1,…,16}, n1 ≠ n2 | Boundary |

---

## 2. Level 2 — User Journey (사용자 여정)

### Persona

| 항목 | 내용 |
|------|------|
| **역할** | 소프트웨어 개발 학습자 |
| **현재 상태** | TDD 훈련 중, Clean Architecture 이해 중 |
| **목표** | 불변조건 기반 설계 사고와 Dual-Track TDD 흐름을 실제 코드로 체화 |
| **어려움** | "구현부터 시작"하는 관성, 테스트 없이 코드를 작성하는 습관 |

---

### Journey Map

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4 ──→ Step 5
문제 인식   계약 정의   Domain 분리  Dual-Track  회귀 보호
```

---

### Step 1 — 문제 인식

> "마방진을 구현한다"가 아니라 **"어떤 불변조건을 만족시켜야 하는가"** 를 먼저 묻는다.

| 사고 전환 | Before (관성적 접근) | After (Invariant 기반 접근) |
|----------|----------------------|-----------------------------|
| 시작점 | "4×4 배열에 숫자를 채우자" | "이 시스템이 절대 어겨서는 안 될 규칙은 무엇인가?" |
| 질문 | "어떻게 구현할까?" | "무엇이 참이어야 하는가?" |
| 결과 | 구현에 종속된 테스트 | 불변조건에서 도출된 테스트 |

**이 단계에서 확립해야 할 것:**

- 마방진의 수학적 속성 → INV-01, INV-02
- 문제 제약 조건 → INV-03, INV-04, INV-05, INV-06
- 해의 유일성 전제 → INV-07
- 출력 포맷 계약 → INV-08, INV-09

**체크포인트:**

- [ ] 9개 불변조건을 모두 명문화했는가?
- [ ] 각 불변조건이 어느 레이어에서 검증되는지 식별했는가?
- [ ] "무엇을 구현할지"보다 "무엇이 참이어야 하는지"를 먼저 서술했는가?

---

### Step 2 — 계약 정의

> 코드를 작성하기 전에 **호출자와 구현자 사이의 계약(Contract)** 을 명문화한다.

#### 2-A. 입력 스키마 정의

| 항목 | 타입 | 제약 | 관련 Invariant |
|------|------|------|----------------|
| `grid` | `list[list[int]]` | 4행 × 4열 | INV-03 |
| 셀 값 | `int` | 0 또는 1~16 | INV-05 |
| 빈칸 수 | `int` | 정확히 2 | INV-04 |
| 비영 값 중복 | — | 없음 | INV-06 |

#### 2-B. 출력 스키마 정의

```
[r1, c1, n1, r2, c2, n2]  →  int[6], 1-index
```

| 항목 | 타입 | 제약 | 관련 Invariant |
|------|------|------|----------------|
| `r1`, `c1`, `r2`, `c2` | `int` | 1 ≤ 값 ≤ 4 | INV-08 |
| `n1`, `n2` | `int` | 1 ≤ 값 ≤ 16, n1 ≠ n2 | INV-09 |
| 순서 규칙 | — | 작은 수 → 첫 번째 빈칸 우선 | INV-07 |

#### 2-C. 예외 정책 정의

| 에러 코드 | 발생 조건 | 처리 레이어 |
|-----------|-----------|-------------|
| `INVALID_GRID_SIZE` | 행 또는 열이 4가 아님 | Boundary |
| `INVALID_CELL_VALUE` | 셀 값이 0~16 범위 외 | Boundary |
| `INVALID_BLANK_COUNT` | 빈칸이 2개가 아님 | Boundary |
| `DUPLICATE_VALUE` | 0 제외 중복 값 존재 | Boundary |
| `NO_SOLUTION` | 유효 조합 없음 | Control → Boundary |
| `INVALID_INPUT` | 입력 자체가 None / 비배열 | Boundary |
| `INTERNAL_ERROR` | 예상치 못한 예외 | Boundary |

**체크포인트:**

- [ ] 입력 검증 4단계(크기 → 값 범위 → 빈칸 수 → 중복)를 순서대로 명세했는가?
- [ ] 출력 포맷이 `int[6]`으로 고정되어 있는가?
- [ ] 에러 코드 7종이 모두 식별되었는가?
- [ ] "첫 번째 실패 즉시 반환" 정책이 명시되었는가?

---

### Step 3 — Domain 분리

> 하나의 큰 함수 대신 **단일 책임(SRP)을 가진 Domain 서비스**로 분리한다.

#### 3-A. 컴포넌트 책임 분리

| 컴포넌트 | 레이어 | 단일 책임 | 관련 Invariant |
|----------|--------|-----------|----------------|
| `BlankFinder` | Entity | 격자에서 0인 셀 2개의 위치를 행 우선(row-major) 순서로 반환 | INV-04 |
| `MissingNumberFinder` | Entity | 1~16 중 격자에 없는 숫자 2개 탐색 | INV-02 |
| `MagicSquareValidator` | Entity | 4행 + 4열 + 2대각선 합이 모두 34인지 검증 | INV-01 |
| `SolvingStrategy` | Control | 두 조합(작은수 우선 / 큰수 우선)을 시도하고 유효한 결과 선택 | INV-07 |

#### 3-B. ECB 레이어 의존성 방향

```
Boundary ──→ Control ──→ Entity
   │              │           │
InputValidator  Solver    BlankFinder
ResponseFormatter          MissingFinder
Controller                 Validator
                           SolvingStrategy
```

> 화살표 방향의 **역방향 import는 절대 금지**한다.

#### 3-C. 분리 기준 — "이 책임을 다른 컴포넌트가 가지면 어떻게 되는가?" 테스트

| 잘못된 설계 | 문제점 |
|-------------|--------|
| `Solver`가 입력 검증을 수행 | Control이 Boundary 책임 흡수 → 레이어 붕괴 |
| `Validator`가 빈칸을 직접 채움 | Entity가 Control 책임 흡수 → SRP 위반 |
| `Controller`가 도메인 로직 수행 | Boundary가 Entity에 직접 의존 → ECB 붕괴 |

**체크포인트:**

- [ ] 각 컴포넌트의 public 메서드가 하나의 책임만 수행하는가?
- [ ] `entity/` → `boundary/` 또는 `entity/` → `control/` 방향의 import가 없는가?
- [ ] 각 Domain Service가 독립적으로 단위 테스트 가능한가?

---

### Step 4 — Dual-Track 진행

> UI 계약 테스트(Boundary)와 Domain 로직 테스트(Entity)를 **병렬로** RED → GREEN → REFACTOR 한다.

#### 4-A. Dual-Track 구조

```
Track A (UI Boundary)          Track B (Domain Logic)
─────────────────────          ──────────────────────
UI-T01~T19                     BF-T01~T06  (BlankFinder)
  입력 검증 19케이스             MF-T01~T05  (MissingFinder)
  에러 응답 포맷                 MV-T01~T07  (Validator)
  Mock으로 Domain 격리           SS-T01~T05  (SolvingStrategy)
                                SR-T01~T06  (SolveResult VO)
```

#### 4-B. RED 단계 — 실패 확인 후 진행

| 규칙 | 설명 |
|------|------|
| 테스트 우선 | 구현 코드보다 테스트 코드가 반드시 먼저 존재해야 한다 |
| RED 확인 필수 | 새 테스트는 반드시 `AssertionError` 또는 `ImportError`로 실패해야 한다 |
| 단일 사이클 | GREEN 없이 RED→RED 연속 추가 금지 |
| ID 명시 | 테스트 주석에 `# BF-T01 / INV-04` 형식으로 추적 태그를 작성한다 |

#### 4-C. GREEN 단계 — 최소 구현

| 규칙 | 설명 |
|------|------|
| 최소 코드 원칙 | 해당 테스트 하나만 통과시키는 최소 코드만 작성한다 |
| 하드코딩 허용 | GREEN 단계에서 일반화는 금지 — 리팩토링은 다음 단계에서 |
| 기존 GREEN 보호 | 새 코드가 이미 통과한 테스트를 깨뜨리면 안 된다 |

#### 4-D. REFACTOR 단계 — 구조 개선

| 규칙 | 설명 |
|------|------|
| GREEN 상태 전제 | 모든 테스트가 GREEN인 상태에서만 시작한다 |
| 기능 불변 | 리팩토링 중 새 기능 추가 금지 |
| 커버리지 유지 | Domain ≥ 95% / Boundary ≥ 85% / Data ≥ 80% |
| 회귀 검증 | 리팩토링 후 `pytest tests/ -v`로 전체 재실행 |

#### 4-E. 테스트 배분 계획 (71개)

| 레이어 | 파일 | 테스트 ID | 개수 |
|--------|------|-----------|------|
| Domain | `test_blank_finder.py` | BF-T01~T06 | 6 |
| Domain | `test_missing_number_finder.py` | MF-T01~T05 | 5 |
| Domain | `test_magic_square_validator.py` | MV-T01~T07 | 7 |
| Domain | `test_solving_strategy.py` | SS-T01~T05 | 5 |
| Domain | `test_solve_result.py` | SR-T01~T06 | 6 |
| Boundary | `test_input_validator.py` | UI-T01~T19 | 19 |
| Data | `test_in_memory_repository.py` | DT-T01~T13 | 13 |
| Integration | `test_integration.py` | IT-S01~S04, IT-F01~F06 | 10 |
| **합계** | | | **71** |

**체크포인트:**

- [ ] Track A와 Track B가 서로 다른 Mock 경계로 격리되어 있는가?
- [ ] 각 테스트에 `# TEST-ID / INV-xx` 주석이 있는가?
- [ ] RED → GREEN → REFACTOR 순서를 건너뛰지 않았는가?
- [ ] GREEN 단계에서 리팩토링을 시도하지 않았는가?

---

### Step 5 — 회귀 보호

> 핵심 기능이 완성된 후 **엣지 케이스 · 오류 케이스**를 추가하여 회귀(Regression)를 방지한다.

#### 5-A. 엣지 케이스 추가

| 케이스 유형 | 예시 | 대응 테스트 |
|-------------|------|-------------|
| 빈칸이 같은 행에 있는 경우 | `row=2, col=1` & `row=2, col=3` | BF-T03 |
| 빈칸이 같은 열에 있는 경우 | `row=1, col=4` & `row=3, col=4` | BF-T04 |
| 빈칸이 대각선 위에 있는 경우 | `(1,1)` & `(4,4)` | BF-T05 |
| 누락 숫자가 1과 16인 경우 | 최솟값·최댓값 경계 | MF-T04 |
| 순서가 반전되어야 하는 조합 | 큰 수 → 첫 번째 빈칸 | SS-T04 |

#### 5-B. 입력 오류 케이스 추가

| 케이스 유형 | 에러 코드 | 대응 테스트 |
|-------------|-----------|-------------|
| `None` 입력 | `INVALID_INPUT` | UI-T01 |
| 3×4 격자 (행 부족) | `INVALID_GRID_SIZE` | UI-T03 |
| 셀 값이 17 | `INVALID_CELL_VALUE` | UI-T06 |
| 셀 값이 음수 (-1) | `INVALID_CELL_VALUE` | UI-T07 |
| 빈칸이 3개 | `INVALID_BLANK_COUNT` | UI-T09 |
| 빈칸이 없음 | `INVALID_BLANK_COUNT` | UI-T10 |
| 숫자 5가 두 번 등장 | `DUPLICATE_VALUE` | UI-T12 |

#### 5-C. 조합 실패 케이스 추가

| 케이스 유형 | 에러 코드 | 대응 테스트 |
|-------------|-----------|-------------|
| 두 조합 모두 합산 조건 불만족 | `NO_SOLUTION` | IT-F05 |
| 빈칸 위치가 유효하지 않은 조합 | `NO_SOLUTION` | IT-F06 |

#### 5-D. 회귀 보호 실행 체크리스트

```bash
# 전체 테스트 실행
pytest tests/ -v

# 커버리지 측정
pytest tests/ --cov=entity --cov=boundary --cov=data --cov-report=term-missing

# 매직 넘버 스캔
rg --type py '[^A-Z_"'"'"'(]\b(34|16|4)\b[^)]' entity/ control/
```

**체크포인트:**

- [ ] 경계값 케이스(최솟값, 최댓값, 경계±1)가 모두 포함되었는가?
- [ ] 에러 코드 7종에 대응하는 테스트가 각각 1개 이상 존재하는가?
- [ ] 전체 71개 테스트가 모두 GREEN인가?
- [ ] 커버리지 목표(Domain ≥ 95%, Boundary ≥ 85%, Data ≥ 80%)를 달성했는가?

---

## 여정 전체 요약

| Step | 이름 | 핵심 질문 | 완료 기준 |
|------|------|-----------|-----------|
| 1 | 문제 인식 | 어떤 불변조건을 만족시켜야 하는가? | INV-01~INV-09 명문화 |
| 2 | 계약 정의 | 입력·출력·예외 계약이 코드와 일치하는가? | 에러 코드 7종 + 스키마 확정 |
| 3 | Domain 분리 | 각 컴포넌트가 단일 책임을 갖는가? | ECB 레이어 의존성 방향 검증 |
| 4 | Dual-Track 진행 | RED → GREEN → REFACTOR 순서를 지키며 진행하는가? | 71개 테스트 작성 + 커버리지 달성 |
| 5 | 회귀 보호 | 엣지·오류·실패 케이스를 모두 포함했는가? | 전체 테스트 GREEN + 매직 넘버 0건 |

---

> **다음 단계:** Level 3 — User Story (사용자 스토리) 상세 작성  
> 각 Step을 `As a [Persona], I want to [Goal], so that [Benefit]` 형식의 User Story로 분해한다.
