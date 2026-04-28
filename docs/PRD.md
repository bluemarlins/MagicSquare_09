# PRD — 4×4 Magic Square: Dual-Track TDD 훈련 시스템

---

| 항목 | 내용 |
|------|------|
| **프로젝트명** | Magic Square (4×4) |
| **문서 유형** | Product Requirements Document (PRD) |
| **버전** | 1.1.0 |
| **작성일** | 2026-04-28 |
| **목적** | Dual-Track TDD + Clean Architecture 훈련 — Concept-to-Code Traceability 포함 (MLOps 방법론 적용) |
| **방법론** | MLOps 과정 Dual-Track UI + Logic TDD — UX Contract / Logic Rule 이중 언어 체계 |
| **참조 문서** | Report/01 (문제 정의) · Report/02 (TDD + Clean Architecture) · Report/03 (.cursorrules) · Report/04 (Epic + User Journey) · MLOps 과정 6~7교시 슬라이드 |

---

## 목차

1. [배경 및 목적](#1-배경-및-목적)
   - 1.4 [PRD 5조건 체크](#14-prd-5조건-체크)
2. [Epic — 훈련 목표](#2-epic--훈련-목표)
3. [도메인 불변조건](#3-도메인-불변조건)
4. [입출력 계약 (고정)](#4-입출력-계약-고정)
5. [Concept → Rule → Use Case → Contract → Test → Component 추적성](#5-concept--rule--use-case--contract--test--component-추적성)
6. [기능 요구사항 — Dual-Track 분리](#6-기능-요구사항--dual-track-분리)
   - 6.6 [Dual-Track 언어 체계 & 3단 매핑 표](#66-dual-track-언어-체계--3단-매핑-표)
7. [에러 정책](#7-에러-정책)
8. [아키텍처 제약 (ECB)](#8-아키텍처-제약-ecb)
9. [Gherkin 시나리오 (L0~L3)](#9-gherkin-시나리오-l0l3)
10. [테스트 계획](#10-테스트-계획)
11. [비기능 요구사항 및 개발 원칙](#11-비기능-요구사항-및-개발-원칙)
12. [성공 기준](#12-성공-기준)
13. [범위 (In-Scope / Out-of-Scope)](#13-범위-in-scope--out-of-scope)
14. [Traceability Matrix](#14-traceability-matrix)

---

## 1. 배경 및 목적

### 1.1 프로젝트 동기

> **마방진은 훈련의 재료다. 이 프로젝트의 진짜 목적은 Invariant 기반 사고 훈련이다.**

개발 학습에서 가장 흔한 실수는 **문제를 받자마자 코드를 작성하는 것**이다.  
이 프로젝트는 그 관성을 의도적으로 차단하고, 다음 능력을 체화하는 데 집중한다.

| 사고 능력 | 훈련 내용 |
|-----------|----------|
| 조건의 완전한 명세 | 자연어 규칙을 빠짐없이 열거하고, 각 조건의 독립성·종속성을 구분한다 |
| 실패 조건 선행 정의 | "언제 성공인가"보다 "언제 실패인가"를 먼저 묻는다 |
| 불변조건과 가변조건의 분리 | 항상 참이어야 하는 조건(Invariant)과 구현 방식에 따라 달라지는 조건(Variable)을 구분한다 |
| 검증 가능한 단위 분해 | 하나의 큰 문제를 독립적으로 참/거짓을 판별할 수 있는 단위로 나눈다 |
| 미정의 상태 허용 금지 | 모든 가능한 상태를 열거하고, 각 상태에 이름을 붙인다 |

### 1.2 왜 4×4인가

| 크기 | 특성 |
|------|------|
| 3×3 | 해가 본질적으로 1가지(회전·반전 제외). 탐색 난이도가 낮아 훈련 효과 미흡 |
| **4×4** | 탐색 공간이 충분히 크고, 다중 제약 조건이 동시 작용. 완전 탐색과 최적화 전략 사이의 균형점 |
| 5×5 이상 | 해의 수가 폭발적으로 증가하여 초기 학습 및 설계 검증에 부적합 |

**수학적 특성:**
- 1~16의 합 = **136**, 목표 합(Magic Constant) = **34**
- 행 4개 + 열 4개 + 대각선 2개 = **총 10개의 합산 조건이 동시에 성립**해야 한다

### 1.3 Why 체인 요약

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

---

### 1.4 PRD 5조건 체크

> **MLOps 과정 기준 — 좋은 PRD의 5조건: 명확성 · 측정 가능성 · 달성 가능성 · 관련성 · 완결성**

| 조건 | 이 PRD의 근거 | 판정 |
|------|-------------|------|
| **명확성** | UX Contract("보인다/안 보인다") + Logic Rule("허용한다/거부한다") 이중 언어 체계로 표현 | ✅ |
| **측정 가능성** | SC-01~SC-09 수치 목표 + 응답 시간 < 100ms + 테스트 71개 GREEN | ✅ |
| **달성 가능성** | Python 단일 스택, InMemory 저장소, 4×4 고정 범위 | ✅ |
| **관련성** | INV-01~INV-09 → 테스트 ID → 컴포넌트 수직 추적 체인 완비 | ✅ |
| **완결성** | L0(초기화) ~ L3(실패) 전 레벨 시나리오 + 에러 코드 7종 전수 커버 | ✅ |

---

## 2. Epic — 훈련 목표

### 2.1 Epic 명칭

> **"Invariant 기반 사고 훈련 시스템 구축"**

*"마방진 풀이 프로그램 개발"이 아닌 이유: 결과물(구현)이 아니라 훈련 목적(사고)이 본질이기 때문이다.*

### 2.2 훈련 목표 4가지

| # | 훈련 목표 | 핵심 질문 | 연관 설계 결정 |
|---|-----------|-----------|----------------|
| ① | Invariant 중심 설계 사고 | "절대 위반할 수 없는 조건은?" | INV-01~INV-09 도출 |
| ② | Dual-Track TDD 적용 | "UI와 Domain을 병렬로 RED→GREEN→REFACTOR 할 수 있는가?" | Track A/B 분리 |
| ③ | 입력/출력 계약 명확화 | "계약은 코드에 어떻게 표현되는가?" | 에러 코드 7종, `int[6]` 출력 |
| ④ | 설계→테스트→구현→리팩토링 흐름 체화 | "각 단계 진입·완료 기준을 지키는가?" | TDD 단계별 규칙 |

### 2.3 학습자 Persona

| 항목 | 내용 |
|------|------|
| 역할 | 소프트웨어 개발 학습자 |
| 현재 상태 | TDD 훈련 중, Clean Architecture 이해 중 |
| 핵심 어려움 | **"구현부터 시작하는 관성"** — 이 훈련이 극복하려는 습관 |
| 목표 | Invariant 도출 → 계약 정의 → Domain 분리 → Dual-Track TDD → 회귀 보호 순서 체화 |

---

## 3. 도메인 불변조건

> **이 9개 불변조건은 변경 금지 규칙이다. 모든 테스트는 아래 조건 중 하나 이상을 보호한다.**

| ID | 불변조건 | 내용 | 위반 시 처리 |
|----|----------|------|-------------|
| **INV-01** | Magic Constant | 모든 행·열·대각선의 합 = **34** | NoSolutionError |
| **INV-02** | 숫자 집합 완전성 | 1~16 각각 정확히 1회 등장 | 검증 실패 |
| **INV-03** | 격자 크기 | 행 4개, 각 행 열 4개 | INVALID_GRID_SIZE |
| **INV-04** | 빈칸 개수 | 0의 개수 = 정확히 2 | INVALID_BLANK_COUNT |
| **INV-05** | 값 범위 | 모든 셀 값 ∈ {0, 1, …, 16} | INVALID_CELL_VALUE |
| **INV-06** | 비영 중복 없음 | 0 제외 동일 숫자 2회 이상 금지 | DUPLICATE_VALUE |
| **INV-07** | 해 유일성 전제 | 두 빈칸 조합 중 유효한 것은 정확히 1가지 | NoSolutionError |
| **INV-08** | 출력 좌표 범위 | r, c ∈ {1, 2, 3, 4} (1-index) | 검증 실패 |
| **INV-09** | 출력 숫자 범위 | n1, n2 ∈ {1,…,16}, n1 ≠ n2 | 검증 실패 |

---

## 4. 입출력 계약 (고정)

> **이 계약은 변경 금지다. 모든 구현은 아래 계약을 준수해야 한다.**

### 4.1 입력 계약

```
타입:    int[4][4]  (4×4 정수 행렬)
빈칸 표기: 0
빈칸 수:  정확히 2개
값 범위:  각 셀 ∈ {0, 1, 2, ..., 16}
중복 금지: 0을 제외한 나머지 숫자는 중복 등장 금지
첫 번째 빈칸 정의: row-major(행 우선) 스캔 시 먼저 발견되는 0
```

**입력 검증 순서 (고정 — 첫 번째 실패 즉시 반환):**

```
1단계: 격자 크기 검증     → 행 수 ≠ 4 또는 각 행의 열 수 ≠ 4  → INVALID_GRID_SIZE
2단계: 셀 값 범위 검증    → 셀 값 ∉ {0, 1, ..., 16}           → INVALID_CELL_VALUE
3단계: 빈칸(0) 수 검증    → 0의 개수 ≠ 2                       → INVALID_BLANK_COUNT
4단계: 비영 중복 검증     → 0 제외 동일 숫자 2회 이상 등장      → DUPLICATE_VALUE
```

> **다중 오류 동시 반환 금지 — 첫 번째 실패 규칙 엄수**

### 4.2 출력 계약

```
타입:    int[6]
포맷:    [r1, c1, n1, r2, c2, n2]
좌표계:  1-index (r, c ∈ {1, 2, 3, 4})
의미:
  r1, c1 — 첫 번째 빈칸의 행, 열 (row-major 기준 첫 번째 0)
  n1     — 첫 번째 빈칸에 채울 숫자
  r2, c2 — 두 번째 빈칸의 행, 열
  n2     — 두 번째 빈칸에 채울 숫자
```

**배치 우선순위 규칙 (결정론적 출력 보장):**

```
시도 A: 작은 수(smaller) → 첫 번째 빈칸, 큰 수(larger) → 두 번째 빈칸
        → 마방진 조건 만족 시: 이 순서로 반환 (n1 < n2)

시도 B: 큰 수(larger) → 첫 번째 빈칸, 작은 수(smaller) → 두 번째 빈칸
        → 마방진 조건 만족 시: 이 순서로 반환 (n1 > n2)

두 시도 모두 실패: NoSolutionError 발생 → errorCode "NO_SOLUTION" 반환
```

### 4.3 마방진 완성 검증 조건 (10개 — 전체 동시 성립 필수)

```
행 합산 (4개):  grid[0] 합 = 34, grid[1] 합 = 34, grid[2] 합 = 34, grid[3] 합 = 34
열 합산 (4개):  col[0] 합 = 34, col[1] 합 = 34, col[2] 합 = 34, col[3] 합 = 34
대각선 (2개):   주대각선 합 = 34, 반대각선 합 = 34
```

---

## 5. Concept → Rule → Use Case → Contract → Test → Component 추적성

> 이 섹션은 개념에서 컴포넌트까지의 **수직 추적 체인**을 확립한다.  
> 아래 표의 각 행은 하나의 훈련 개념이 어떻게 규칙, 유스케이스, 계약, 테스트, 컴포넌트로 이어지는지 보여준다.

| Concept | Rule (Invariant) | Use Case | Contract | Test ID | Component |
|---------|-----------------|----------|----------|---------|-----------|
| 빈칸 탐색 | INV-03, INV-04 | UC-D01: 격자에서 빈칸 2개 위치를 row-major 순서로 추출 | `findBlanks(grid) → Cell[2]` / 빈칸 ≠ 2 → `InvalidBlankCountError` | BF-T01~T06 | `BlankFinder` |
| 누락 숫자 탐색 | INV-02, INV-06 | UC-D02: 1~16 중 격자에 없는 숫자 2개를 탐색 | `findMissing(grid) → MissingPair` / 누락 ≠ 2 → `InvalidMissingCountError` | MF-T01~T05 | `MissingNumberFinder` |
| 마방진 검증 | INV-01 | UC-D03: 완성된 격자의 10개 합산 조건 검증 | `isValid(grid) → bool` / 0 포함 → `IncompleteGridError` | MV-T01~T07 | `MagicSquareValidator` |
| 조합 선택 전략 | INV-07, INV-09 | UC-D04: 시도 A → 시도 B 순으로 마방진 완성 조합 결정 | `solve(grid, blanks, missing) → SolveResult` / 두 조합 실패 → `NoSolutionError` | SS-T01~T05 | `SolvingStrategy` |
| 결과 포맷화 | INV-08, INV-09 | UC-D05: `int[6]` 형식으로 결과를 1-index 좌표로 포맷 | `SolveResult(r1,c1,n1,r2,c2,n2)` 불변 VO | SR-T01~T06 | `SolveResult` VO |
| 입력 검증 | INV-03~INV-06 | UC-B01: 4단계 순서 검증 후 Domain 호출 | 에러 코드 7종 + 표준 메시지 문구 | UI-T01~T19 | `InputValidator` |
| 저장/로드 추상화 | INV-03 | UC-R01: 격자 저장·로드·존재 여부·삭제 계약 | `save/load/exists/delete` Protocol | DT-T01~T13 | `MatrixRepository`, `InMemoryRepository` |
| End-to-End 정상 흐름 | INV-01~INV-09 전체 | UC-I01: 입력 → 검증 → 풀이 → 결과 반환 전체 통합 | 전체 레이어 계약 조합 | IT-S01~S04 | 전체 컴포넌트 |
| End-to-End 실패 흐름 | INV-03~INV-07 | UC-I02: 각 레이어별 실패 경로 처리 | 에러 코드 7종 반환 계약 | IT-F01~F06 | 전체 컴포넌트 |

---

## 6. 기능 요구사항 — Dual-Track 분리

### 6.1 Dual-Track 개요

```
Track A (UI Boundary)                  Track B (Domain Logic)
─────────────────────────────          ─────────────────────────────
대상: 입력 검증 + 응답 포맷            대상: 순수 도메인 로직
격리: Domain을 Mock으로 대체           격리: 외부 의존 없음 (순수 Python)
테스트: UI-T01~T19 (19개)              테스트: BF/MF/MV/SS/SR (29개)
                                       
        ↘                                       ↙
              Integration (IT-S01~S04, IT-F01~F06, 10개)
                    Data Layer (DT-T01~T13, 13개)
```

> **두 Track은 Mock 경계로 완전히 격리된다. Track A 테스트에서 실제 Domain 로직에 의존하는 것은 금지다.**

---

### 6.2 Track A — UI Boundary 기능 요구사항

#### FR-B01: 4단계 순서 입력 검증

- **요구사항:** `InputValidator`는 아래 순서대로 검증을 수행하고, 첫 번째 실패 지점에서 즉시 에러 응답을 반환한다.
- **순서:** 격자 크기 → 셀 값 범위 → 빈칸 수 → 비영 중복
- **제약:** 다중 오류를 동시에 반환하지 않는다.
- **검증 가능 여부:** UI-T01~T15 전체 통과로 확인 가능

#### FR-B02: 표준 에러 응답 포맷

- **요구사항:** `ResponseFormatter`는 모든 오류를 `{errorCode, message}` 형식으로 반환한다.
- **제약:** 에러 메시지 문구는 [에러 정책 섹션](#7-에러-정책)에 명시된 표준 문구와 정확히 일치해야 한다.
- **검증 가능 여부:** UI-T01~T19 내 메시지 문자열 비교로 확인 가능

#### FR-B03: 정상 응답 포맷

- **요구사항:** 풀이 성공 시 `{result: [r1, c1, n1, r2, c2, n2]}` 형식으로 반환한다.
- **제약:** 좌표는 반드시 1-index이고, 리스트 길이는 항상 6이다.
- **검증 가능 여부:** UI-T16~T19 + IT-S01~S04 통과로 확인 가능

#### FR-B04: Domain 예외 → 에러 응답 변환

- **요구사항:** `MagicSquareController`는 Domain에서 발생한 `NoSolutionError`를 `{errorCode: "NO_SOLUTION", message: "..."}` 응답으로 변환한다.
- **제약:** Domain 예외를 호출자에게 그대로 노출하지 않는다.
- **검증 가능 여부:** IT-F05 통과로 확인 가능

---

### 6.3 Track B — Domain Logic 기능 요구사항

#### FR-D01: 빈칸 위치 탐색 (BlankFinder)

- **요구사항:** 격자에서 0인 셀을 row-major 순서로 탐색하여 두 셀의 (row, col) 좌표를 1-index로 반환한다.
- **제약:** 빈칸이 정확히 2개가 아니면 `InvalidBlankCountError`를 발생시킨다.
- **검증 가능 여부:** BF-T01~T06 전체 통과로 확인 가능

#### FR-D02: 누락 숫자 탐색 (MissingNumberFinder)

- **요구사항:** 1~16 중 격자에 등장하지 않는 숫자 2개를 찾아 `MissingPair(smaller, larger)`로 반환한다.
- **제약:** 누락 숫자가 정확히 2개가 아니면 `InvalidMissingCountError`를 발생시킨다. `smaller < larger`는 항상 보장된다.
- **검증 가능 여부:** MF-T01~T05 전체 통과로 확인 가능

#### FR-D03: 마방진 합산 조건 검증 (MagicSquareValidator)

- **요구사항:** 완성된 격자(0 없음)에 대해 10개의 합산 조건(행 4개 + 열 4개 + 대각선 2개)을 검증하고, 모두 34이면 `True`를 반환한다.
- **제약:** 0을 포함한 격자는 `IncompleteGridError`를 발생시킨다.
- **검증 가능 여부:** MV-T01~T07 전체 통과로 확인 가능

#### FR-D04: 조합 선택 전략 (SolvingStrategy)

- **요구사항:** `MissingPair`의 두 숫자를 두 빈칸에 배치하는 두 가지 조합을 아래 순서로 시도한다.
  - **시도 A:** smaller → 첫 번째 빈칸, larger → 두 번째 빈칸
  - **시도 B:** larger → 첫 번째 빈칸, smaller → 두 번째 빈칸
- **제약:** 시도 A가 성공하면 시도 B를 수행하지 않는다. 두 시도 모두 실패하면 `NoSolutionError`를 발생시킨다.
- **검증 가능 여부:** SS-T01~T05 전체 통과로 확인 가능

#### FR-D05: 결과 값 객체 (SolveResult)

- **요구사항:** `[r1, c1, n1, r2, c2, n2]` 형식의 불변(immutable) Value Object를 생성한다.
- **제약:** 좌표값 r, c ∈ {1,2,3,4}, 숫자값 n ∈ {1,...,16}, n1 ≠ n2 조건 위반 시 생성에서 예외를 발생시킨다.
- **검증 가능 여부:** SR-T01~T06 전체 통과로 확인 가능

---

### 6.4 Data Layer 기능 요구사항

#### FR-R01: 격자 저장 계약 (MatrixRepository Protocol)

| 메서드 | 시그니처 | 정상 동작 | 실패 조건 |
|--------|----------|-----------|-----------|
| `save` | `save(id: str, grid: list[list[int]]) → None` | 지정 id로 격자 저장 | 중복 id → `DuplicateIdError` |
| `load` | `load(id: str) → list[list[int]]` | 저장된 격자 반환 | 없는 id → `NotFoundError` |
| `exists` | `exists(id: str) → bool` | 존재 여부 반환 | — |
| `delete` | `delete(id: str) → None` | 지정 id 삭제 | 없는 id → `NotFoundError` |

- **제약:** `InMemoryRepository`는 `MatrixRepository` Protocol을 완전히 구현해야 한다.
- **제약:** `save` 시 반드시 격자를 deep copy하여 저장 — 원본 격자 변경이 저장된 데이터에 영향을 주어서는 안 된다.
- **검증 가능 여부:** DT-T01~T13 전체 통과로 확인 가능

---

### 6.5 핵심 유스케이스 흐름

```
[정상 흐름 — UC-I01]
호출자
  → InputValidator (4단계 검증) ──[실패]──→ ErrorResponse 반환
  → MagicSquareSolver.solve(grid)
      → BlankFinder.findBlanks(grid)     → Cell[2]
      → MissingNumberFinder.findMissing(grid) → MissingPair
      → SolvingStrategy.solve(grid, blanks, missing)
          → 시도 A: MagicSquareValidator.isValid(grid_with_A) → True  → SolveResult 반환
          → (A 실패 시) 시도 B: MagicSquareValidator.isValid(grid_with_B) → True → SolveResult 반환
          → (B도 실패) → NoSolutionError 발생
  → ResponseFormatter.format_success(result) → {result: int[6]}

[실패 흐름 — UC-I02]
  → 각 레이어에서 발생한 예외 → 에러 코드 + 표준 메시지 반환
```

---

### 6.6 Dual-Track 언어 체계 & 3단 매핑 표

> **MLOps 방법론 핵심 원칙:** UI Track과 Logic Track은 서로 다른 언어로 RED를 작성한다.  
> UI 테스트는 로직을 모르고, Logic 테스트는 UI를 모른다.

#### 언어 체계 정의

| UX Contract 언어 (UI Track — Boundary 검증) | Logic Rule 언어 (Logic Track — Control+Entity 검증) |
|--------------------------------------------|---------------------------------------------------|
| 보인다 / 안 보인다 | 허용한다 / 거부한다 |
| 가능하다 / 불가능하다 | 유지한다 / 중단한다 |
| 활성화 / 비활성화 | 반환한다 / 차단한다 |
| 포함한다 / 포함하지 않는다 | 계산한다 / 저장한다 |

> ⚠ **동사로 끝나지 않는 To-Do는 테스트로 변환하지 말 것 — 판단(Decision)을 포함한 것만 변환 대상**

---

#### 3단 매핑 표 — Scenario → UX Contract → Logic Rule

| Scenario | Gherkin 레벨 | UX Contract | Logic Rule |
|----------|------------|-------------|------------|
| MagicSquare 객체 초기화 | **L0** | — | 격자 구조가 유지된다 |
| InMemoryRepository 초기화 | **L0** | — | 저장소가 준비된다 |
| 조합 A로 마방진 완성 (n1 < n2) | **L1** | `"result"` 키가 포함된 응답이 보인다 | 해가 반환된다 |
| 조합 B로 마방진 완성 (n1 > n2) | **L1** | n1 > n2인 응답이 보인다 | 두 번째 조합이 허용된다 |
| 두 빈칸이 같은 행에 위치 | **L2** | r1 = r2인 응답이 보인다 | row-major 순서가 유지된다 |
| 두 빈칸이 같은 열에 위치 | **L2** | c1 = c2인 응답이 보인다 | row-major 순서가 유지된다 |
| 두 빈칸이 대각선에 위치 | **L2** | 정상 응답이 보인다 | 해가 반환된다 |
| 누락 숫자가 1과 16인 극단값 | **L2** | 정상 응답이 보인다 | 극단값 쌍이 허용된다 |
| 격자 저장 후 로드하여 재솔빙 | **L2** | 동일한 응답이 보인다 | 저장/로드가 유지된다 |
| `None` 입력 | **L3** | `"INVALID_INPUT"` 오류가 보인다 | 입력이 차단된다 |
| 격자가 4×4 아닌 경우 | **L3** | `"INVALID_GRID_SIZE"` 오류가 보인다 | 크기 검증이 거부된다 |
| 셀 값이 0~16 범위 초과 | **L3** | `"INVALID_CELL_VALUE"` 오류가 보인다 | 값 범위 검증이 차단된다 |
| 빈칸이 2개 아닌 경우 | **L3** | `"INVALID_BLANK_COUNT"` 오류가 보인다 | 탐색이 중단된다 |
| 0 제외 중복 숫자 존재 | **L3** | `"DUPLICATE_VALUE"` 오류가 보인다 | 중복 탐지가 거부된다 |
| 두 조합 모두 마방진 불만족 | **L3** | `"NO_SOLUTION"` 오류가 보인다 | 풀이가 중단된다 |
| 크기 오류 + 값 오류 동시 존재 | **L3** | `"INVALID_GRID_SIZE"` 오류만 보인다 | 첫 번째 실패에서 검증이 중단된다 |
| 값 오류 + 빈칸 오류 동시 존재 | **L3** | `"INVALID_CELL_VALUE"` 오류만 보인다 | 첫 번째 실패에서 검증이 중단된다 |

---

## 7. 에러 정책

### 7.1 에러 코드 7종 및 표준 메시지 (변경 금지)

| errorCode | 발생 조건 | 메시지 문구 | 처리 레이어 |
|-----------|----------|------------|------------|
| `INVALID_INPUT` | 입력이 `None` | `"입력 행렬이 null입니다."` | UI Boundary |
| `INVALID_GRID_SIZE` | 행 수 ≠ 4 또는 열 수 ≠ 4 | `"행렬 크기는 4×4이어야 합니다."` | UI Boundary |
| `INVALID_CELL_VALUE` | 셀 값 ∉ {0,…,16} | `"셀 값은 0 또는 1~16이어야 합니다. 위치: (행{r}, 열{c}), 값: {v}"` | UI Boundary |
| `INVALID_BLANK_COUNT` | 빈칸 수 ≠ 2 | `"빈칸(0)은 정확히 2개이어야 합니다. 현재: {count}개"` | UI Boundary |
| `DUPLICATE_VALUE` | 0 제외 동일 숫자 2회 이상 | `"중복된 값이 있습니다. 값: {v}"` | UI Boundary |
| `NO_SOLUTION` | 두 조합 모두 마방진 불만족 | `"입력된 행렬로 마방진을 완성할 수 없습니다."` | Domain → Boundary 변환 |
| `INTERNAL_ERROR` | 예상치 못한 예외 | `"내부 오류가 발생했습니다."` | UI Boundary (최후 방어) |

> **위치는 1-index 기준. 메시지 끝 마침표(`.`) 필수. 문구 변경 금지.**

### 7.2 에러 처리 원칙

- UI Boundary는 Domain 예외를 표준 `ErrorResponse`로 변환한다. Domain 예외를 호출자에게 직접 노출하지 않는다.
- Control(Domain) 레이어는 예외를 변환하지 않고 그대로 전파한다.
- `bare except` 사용 금지 — 반드시 `except Exception as e:` 또는 구체적 예외 타입 명시.

---

## 8. 아키텍처 제약 (ECB)

### 8.1 ECB 레이어 구조

```
[Boundary Layer]          외부 입출력 담당 — 호출자와의 계약 이행
  InputValidator
  ResponseFormatter
  MagicSquareController
       │ 의존 (단방향)
       ▼
[Control Layer]           비즈니스 흐름 조율
  MagicSquareSolver
  SolvingStrategy
       │ 의존 (단방향)
       ▼
[Entity Layer]            도메인 순수 로직 — 외부 의존 없음
  MagicSquare (Entity)
  Cell, CellValue, MissingPair, SolveResult (Value Objects)
  BlankFinder, MissingNumberFinder, MagicSquareValidator (Domain Services)

[Data Layer]              저장소 추상화 (Protocol 수준)
  MatrixRepository (Protocol)
  InMemoryRepository (구현체)
```

### 8.2 의존성 방향 (절대 불변)

```
허용:  Boundary → Control → Entity
허용:  Control → Data (Facade 경유)
금지:  Entity → Control
금지:  Entity → Boundary
금지:  Control → Boundary
금지:  Boundary → Data 직접 호출 (Facade 경유 필수)
```

### 8.3 레이어별 절대 금지 행위

| 레이어 | 절대 금지 |
|--------|----------|
| **Entity** | 저장소(Repository) 의존 / UI·입출력 관련 코드 / 외부 라이브러리 |
| **Control** | 입력 유효성 검증 수행 / 저장·로드 직접 수행 |
| **Boundary** | Domain 객체 직접 생성 / 로직 수행 / Data Layer 직접 호출 |

### 8.4 파일 구조 (ECB 기준)

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
│   │   ├── cell.py
│   │   ├── cell_value.py
│   │   ├── missing_pair.py
│   │   └── solve_result.py
│   └── services/
│       ├── blank_finder.py
│       ├── missing_number_finder.py
│       ├── magic_square_validator.py
│       └── solving_strategy.py
├── data/
│   ├── matrix_repository.py
│   └── in_memory_repository.py
├── exceptions/
│   ├── domain_exceptions.py
│   └── boundary_exceptions.py
└── tests/
    ├── entity/
    ├── boundary/
    ├── data/
    └── integration/
```

---

## 9. Gherkin 시나리오 (L0~L3)

> 아래 시나리오는 **검증 가능한 인수 조건**을 정의한다.  
> 각 시나리오는 테스트 ID, 보호하는 Invariant, **Gherkin 레벨(L0~L3)** 에 매핑된다.

**레벨 정의:**

| 레벨 | 의미 | 대응 시나리오 그룹 |
|------|------|-----------------|
| **L0** | 시스템 초기화 / 사전 조건 설정 | Scenario Group 0 |
| **L1** | Happy Path — 정상 동작 | Scenario Group 1, 4 일부 |
| **L2** | 경계값 / 엣지 케이스 | Scenario Group 5 |
| **L3** | 실패 / 오류 케이스 | Scenario Group 2, 3, 4 일부 |

---

### Feature: 4×4 마방진 두 빈칸 채우기

```gherkin
Feature: 4×4 마방진 두 빈칸 채우기
  배경:
    Given 마방진 Magic Constant는 34이다
    And   격자는 정확히 4행 4열이다
    And   빈칸은 정확히 2개이다
    And   1~16은 각각 정확히 1회 등장한다
```

---

#### Scenario Group 0: 시스템 초기화 시나리오 (L0)

```gherkin
  # IT-L0-01 — INV-03
  # UX Contract: —  /  Logic Rule: 격자 구조가 유지된다
  Scenario: MagicSquare 객체 초기화 (L0)
    Given 4행 4열의 정수 배열이 준비되어 있다
    When  MagicSquare 객체를 생성한다
    Then  객체가 정상적으로 생성된다
    And   격자 크기는 4×4이다

  # IT-L0-02 — INV-03
  # UX Contract: —  /  Logic Rule: 저장소가 준비된다
  Scenario: InMemoryRepository 초기화 (L0)
    Given InMemoryRepository 인스턴스를 생성한다
    When  아무 격자도 저장되지 않은 상태이다
    Then  exists("any-id")는 False를 반환한다

  # IT-L0-03 — INV-01, INV-02, INV-03, INV-04
  # UX Contract: —  /  Logic Rule: 도메인 상수가 유지된다
  Scenario: 도메인 상수 초기값 검증 (L0)
    Given 도메인 상수 모듈이 로드된다
    Then  MAGIC_CONSTANT는 34이다
    And   GRID_SIZE는 4이다
    And   VALUE_RANGE_MAX는 16이다
    And   BLANK_COUNT는 2이다
```

---

#### Scenario Group 1: 정상 동작 시나리오 (L1)

```gherkin
  # IT-S01 — INV-01, INV-02, INV-07, INV-08, INV-09
  # UX Contract: "result" 키가 포함된 응답이 보인다  /  Logic Rule: 해가 반환된다
  Scenario: 조합 A(작은 수 → 첫 빈칸)로 마방진이 완성되는 경우 (L1)
    Given 유효한 4×4 격자에 빈칸 2개가 있다
    And   누락 숫자 두 개 중 작은 수를 첫 번째 빈칸에 배치하면 마방진 조건을 만족한다
    When  solve(grid)를 호출한다
    Then  결과 포맷은 [r1, c1, n1, r2, c2, n2] 이다
    And   n1 < n2 이다
    And   r1, c1, r2, c2 는 모두 1 이상 4 이하의 정수이다
    And   완성된 격자의 모든 행, 열, 대각선의 합은 34이다

  # IT-S02 — INV-01, INV-07, INV-09
  # UX Contract: n1 > n2인 응답이 보인다  /  Logic Rule: 두 번째 조합이 허용된다
  Scenario: 조합 A 실패 후 조합 B(큰 수 → 첫 빈칸)로 마방진이 완성되는 경우 (L1)
    Given 유효한 4×4 격자에 빈칸 2개가 있다
    And   작은 수를 첫 번째 빈칸에 배치하면 마방진 조건을 만족하지 않는다
    And   큰 수를 첫 번째 빈칸에 배치하면 마방진 조건을 만족한다
    When  solve(grid)를 호출한다
    Then  결과 포맷은 [r1, c1, n1, r2, c2, n2] 이다
    And   n1 > n2 이다
    And   완성된 격자의 모든 행, 열, 대각선의 합은 34이다

  # IT-S03 — INV-04, INV-08
  # UX Contract: r1 = r2인 응답이 보인다  /  Logic Rule: row-major 순서가 유지된다
  Scenario: 두 빈칸이 같은 행에 위치하는 경우 (L2)
    Given 유효한 4×4 격자에서 두 빈칸이 동일한 행에 있다
    When  solve(grid)를 호출한다
    Then  r1 = r2 이다
    And   c1 < c2 이다 (row-major 순서 보장)

  # IT-S04 — INV-03
  # UX Contract: 동일한 응답이 보인다  /  Logic Rule: 저장/로드가 유지된다
  Scenario: 격자를 저장한 후 로드하여 재솔빙하면 동일한 결과가 나오는 경우 (L2)
    Given 유효한 4×4 격자 grid_a를 repository에 id "test-01"로 저장한다
    When  repository에서 id "test-01"로 로드한 격자로 solve를 호출한다
    Then  원본 grid_a로 solve를 호출한 결과와 동일한 int[6]이 반환된다
```

---

#### Scenario Group 2: 입력 검증 실패 시나리오 (L3)

```gherkin
  # IT-F01 — INV-03
  # UX Contract: "INVALID_GRID_SIZE" 오류가 보인다  /  Logic Rule: 크기 검증이 거부된다
  Scenario: 격자 크기가 4×4가 아닌 경우 (L3)
    Given 3행 4열 격자를 입력으로 준다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_GRID_SIZE" 이다
    And   message는 "행렬 크기는 4×4이어야 합니다." 이다

  # IT-F01 (변형) — INV-03
  # UX Contract: "INVALID_INPUT" 오류가 보인다  /  Logic Rule: 입력이 차단된다
  Scenario: None을 입력으로 전달하는 경우 (L3)
    Given 입력으로 None을 전달한다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_INPUT" 이다
    And   message는 "입력 행렬이 null입니다." 이다

  # IT-F02 — INV-04
  # UX Contract: "INVALID_BLANK_COUNT" 오류가 보인다  /  Logic Rule: 탐색이 중단된다
  Scenario: 빈칸이 3개인 경우 (L3)
    Given 4×4 격자에 0이 3개 존재한다
    And   셀 값 범위는 모두 유효하다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_BLANK_COUNT" 이다
    And   message는 "빈칸(0)은 정확히 2개이어야 합니다. 현재: 3개" 이다

  # IT-F02 (변형) — INV-04
  # UX Contract: "INVALID_BLANK_COUNT" 오류가 보인다  /  Logic Rule: 탐색이 중단된다
  Scenario: 빈칸이 0개인 경우 (L3)
    Given 4×4 격자에 0이 없다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_BLANK_COUNT" 이다
    And   message는 "빈칸(0)은 정확히 2개이어야 합니다. 현재: 0개" 이다

  # IT-F03 — INV-05
  # UX Contract: "INVALID_CELL_VALUE" 오류가 보인다  /  Logic Rule: 값 범위 검증이 차단된다
  Scenario: 셀 값이 허용 범위를 초과하는 경우 (L3)
    Given 4×4 격자의 (행2, 열3) 위치에 값 17이 있다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_CELL_VALUE" 이다
    And   message는 "셀 값은 0 또는 1~16이어야 합니다. 위치: (행2, 열3), 값: 17" 이다

  # IT-F03 (변형) — INV-05
  # UX Contract: "INVALID_CELL_VALUE" 오류가 보인다  /  Logic Rule: 값 범위 검증이 차단된다
  Scenario: 셀 값이 음수인 경우 (L3)
    Given 4×4 격자에 셀 값 -1이 존재한다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_CELL_VALUE" 이다

  # IT-F04 — INV-06
  # UX Contract: "DUPLICATE_VALUE" 오류가 보인다  /  Logic Rule: 중복 탐지가 거부된다
  Scenario: 0을 제외한 숫자가 중복된 경우 (L3)
    Given 4×4 격자에 숫자 5가 2회 등장한다
    And   격자 크기와 빈칸 수는 유효하다
    When  solve(grid)를 호출한다
    Then  errorCode는 "DUPLICATE_VALUE" 이다
    And   message는 "중복된 값이 있습니다. 값: 5" 이다

  # IT-F05 — INV-07
  # UX Contract: "NO_SOLUTION" 오류가 보인다  /  Logic Rule: 풀이가 중단된다
  Scenario: 두 조합 모두 마방진 조건을 만족하지 않는 경우 (L3)
    Given 유효한 형식의 4×4 격자가 있다
    And   어떤 조합으로도 마방진을 완성할 수 없다
    When  solve(grid)를 호출한다
    Then  errorCode는 "NO_SOLUTION" 이다
    And   message는 "입력된 행렬로 마방진을 완성할 수 없습니다." 이다
```

---

#### Scenario Group 3: 입력 검증 순서 시나리오 (L3)

```gherkin
  # UI-T 복합 — 첫 번째 실패 즉시 반환 규칙 검증
  # UX Contract: "INVALID_GRID_SIZE" 오류만 보인다  /  Logic Rule: 첫 번째 실패에서 검증이 중단된다
  Scenario: 크기 오류와 값 오류가 동시에 존재하는 경우 (L3)
    Given 3행 4열 격자에 셀 값 17도 포함되어 있다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_GRID_SIZE" 이다
    And   "INVALID_CELL_VALUE" errorCode는 반환되지 않는다

  # UX Contract: "INVALID_CELL_VALUE" 오류만 보인다  /  Logic Rule: 첫 번째 실패에서 검증이 중단된다
  Scenario: 값 범위 오류와 빈칸 오류가 동시에 존재하는 경우 (L3)
    Given 4×4 격자에 셀 값 17이 있고 빈칸이 3개이다
    When  solve(grid)를 호출한다
    Then  errorCode는 "INVALID_CELL_VALUE" 이다
    And   "INVALID_BLANK_COUNT" errorCode는 반환되지 않는다
```

---

#### Scenario Group 4: 도메인 서비스 단위 시나리오 (L1 / L3)

```gherkin
  # BF-T01 — INV-04, INV-08
  # UX Contract: —  /  Logic Rule: row-major 순서가 유지된다
  Scenario: BlankFinder — 빈칸 2개를 row-major 순서로 반환하는 경우 (L1)
    Given 4×4 격자에서 (행2, 열3)과 (행4, 열1)이 빈칸이다
    When  BlankFinder.findBlanks(grid)를 호출한다
    Then  반환값은 [Cell(2,3), Cell(4,1)] 이다 (row-major 순서)

  # BF-T03 — INV-04
  # UX Contract: —  /  Logic Rule: 탐색이 중단된다
  Scenario: BlankFinder — 빈칸이 3개인 격자가 전달되는 경우 (L3)
    Given 4×4 격자에 빈칸(0)이 3개 존재한다
    When  BlankFinder.findBlanks(grid)를 호출한다
    Then  InvalidBlankCountError가 발생한다

  # MF-T01 — INV-02, INV-09
  # UX Contract: —  /  Logic Rule: 극단값 쌍이 허용된다
  Scenario: MissingNumberFinder — 누락 숫자 2개를 (smaller, larger) 쌍으로 반환하는 경우 (L1)
    Given 1~16 중 3과 11이 격자에 없다
    When  MissingNumberFinder.findMissing(grid)를 호출한다
    Then  반환값은 MissingPair(smaller=3, larger=11) 이다

  # MV-T01 — INV-01
  # UX Contract: —  /  Logic Rule: 합 검증이 허용된다
  Scenario: MagicSquareValidator — 모든 합산 조건이 34인 완성 격자를 검증하는 경우 (L1)
    Given 10개 합산 조건이 모두 34인 완성된 4×4 격자가 있다
    When  MagicSquareValidator.isValid(grid)를 호출한다
    Then  True를 반환한다

  # MV-T02 — INV-01
  # UX Contract: —  /  Logic Rule: 합 검증이 거부된다
  Scenario: MagicSquareValidator — 하나의 행 합이 34가 아닌 경우 (L3)
    Given 1행의 합이 33인 격자가 있다
    When  MagicSquareValidator.isValid(grid)를 호출한다
    Then  False를 반환한다

  # SS-T03 — INV-07
  # UX Contract: —  /  Logic Rule: 풀이가 중단된다
  Scenario: SolvingStrategy — 두 조합 모두 실패하는 경우 (L3)
    Given 유효한 격자와 빈칸 위치, 누락 쌍이 주어졌다
    And   시도 A도 시도 B도 마방진 조건을 만족하지 않는다
    When  SolvingStrategy.solve(grid, blanks, missing)를 호출한다
    Then  NoSolutionError가 발생한다
```

---

#### Scenario Group 5: 엣지 케이스 시나리오 (L2)

```gherkin
  # UX Contract: c1 = c2인 응답이 보인다  /  Logic Rule: row-major 순서가 유지된다
  Scenario: 두 빈칸이 같은 열에 위치하는 경우 (L2)
    Given 유효한 격자에서 두 빈칸이 동일한 열에 있다
    When  solve(grid)를 호출한다
    Then  c1 = c2 이다
    And   r1 < r2 이다 (row-major 순서 보장)

  # UX Contract: 정상 응답이 보인다  /  Logic Rule: 해가 반환된다
  Scenario: 두 빈칸이 같은 대각선에 위치하는 경우 (L2)
    Given 유효한 격자에서 두 빈칸이 주대각선 위에 있다
    When  solve(grid)를 호출한다
    Then  정상적으로 int[6]이 반환된다

  # UX Contract: 정상 응답이 보인다  /  Logic Rule: 극단값 쌍이 허용된다
  Scenario: 누락 숫자가 1과 16인 경우 (극단값) (L2)
    Given 1~16 중 1과 16이 격자에 없다
    When  MissingNumberFinder.findMissing(grid)를 호출한다
    Then  반환값은 MissingPair(smaller=1, larger=16) 이다
```

---

## 10. 테스트 계획

### 10.1 전체 테스트 분포 (71개)

| 레이어 | 테스트 ID 범위 | 케이스 수 | 커버리지 목표 |
|--------|--------------|----------|-------------|
| Domain — BlankFinder | BF-T01~T06 | 6개 | |
| Domain — MissingNumberFinder | MF-T01~T05 | 5개 | |
| Domain — MagicSquareValidator | MV-T01~T07 | 7개 | |
| Domain — SolvingStrategy | SS-T01~T05 | 5개 | |
| Domain — SolveResult VO | SR-T01~T06 | 6개 | |
| **Domain 소계** | | **29개** | **≥ 95%** |
| UI Boundary | UI-T01~T19 | 19개 | **≥ 85%** |
| Data Layer | DT-T01~T13 | 13개 | **≥ 80%** |
| Integration — 정상 | IT-S01~S04 | 4개 | |
| Integration — 실패 | IT-F01~F06 | 6개 | |
| **통합 소계** | | **10개** | |
| **전체 합계** | | **71개** | |

### 10.2 테스트 세부 분류

**UI Boundary (UI-T01~T19)**

| 분류 | 테스트 ID | 케이스 수 |
|------|----------|---------|
| 크기 오류 | UI-T01~T04 | 4개 |
| 빈칸 오류 | UI-T05~T07 | 3개 |
| 값 범위 오류 | UI-T08~T11 | 4개 |
| 중복 오류 | UI-T12~T15 | 4개 |
| 반환 포맷 검증 | UI-T16~T19 | 4개 |

**Data Layer (DT-T01~T13)**

| 분류 | 테스트 ID | 케이스 수 |
|------|----------|---------|
| 저장/로드 정합성 | DT-T01~T05 | 5개 |
| 예외 처리 | DT-T06~T11 | 6개 |
| 불변조건 (4×4 유지) | DT-T12~T13 | 2개 |

### 10.3 TDD 단계별 진입·완료 기준

| 단계 | 진입 조건 | 완료 기준 |
|------|-----------|-----------|
| **RED** | 없음 (첫 단계) | 새 테스트가 `AssertionError` 또는 `ImportError`로 실패 확인 |
| **GREEN** | RED 확인 완료 | 해당 테스트만 통과 + 기존 GREEN 테스트 전체 유지 |
| **REFACTOR** | 모든 테스트 GREEN | 커버리지 목표 유지 + 회귀(regression) 없음 확인 |

> **TDD 사이클 위반 금지:**
> - GREEN 없이 RED→RED 연속 추가 금지
> - GREEN 단계에서 리팩터링·추상화 수행 금지
> - 테스트가 RED인 상태에서 리팩터링 시작 금지

### 10.4 Mock 정책

- **UI Boundary 테스트:** Domain은 반드시 `Mock`으로 대체. 실제 Domain 로직에 의존하는 UI 테스트 작성 금지.
- **Domain 테스트:** 외부 의존 없음. 순수 Python — `pytest`만 사용.
- **Data 테스트:** `InMemoryRepository` 사용. 실제 파일 I/O 또는 네트워크 호출 금지.
- **Mock 라이브러리:** `pytest-mock` 또는 `unittest.mock`

### 10.5 회귀 보호 실행 명령

```bash
# 전체 테스트 실행
pytest tests/ -v

# 레이어별 커버리지 측정
pytest tests/ --cov=entity --cov=boundary --cov=data --cov-report=term-missing

# 매직 넘버(하드코딩 상수) 스캔 — REFACTOR 단계 이후 0건 목표
rg --type py '[^A-Z_"'"'"'(]\b(34|16|4)\b[^)]' entity/ control/

# ECB 역방향 import 검사 (수동)
# entity/ 내에서 boundary 또는 control import 여부 확인
```

---

## 11. 비기능 요구사항 및 개발 원칙

### 11.0 성능 · 보안 · 확장성

| 분류 | 요구사항 | 목표값 | 측정 방법 |
|------|---------|--------|-----------|
| **성능** | 입력 검증 + 풀이 전체 처리 시간 | < 100ms | `pytest-benchmark` |
| **보안** | 입력 유효성 검증 — 4단계 순서 고정 필수 | 100% 검증 통과율 | `pytest tests/boundary/` |
| **확장성** | 5×5 마방진 지원 (Phase 2) 대비 설계 | Protocol 수준 분리 유지 | 레이어 의존 방향 검토 |
| **테스트 격리** | 테스트 간 상태 공유 금지 | fixture scope=function 전수 적용 | pytest 수동 검토 |

### 11.1 코드 스타일

| 항목 | 기준 |
|------|------|
| 언어 | Python 3.10+ |
| 포매터 | Black (max_line_length: 88) |
| 스타일 가이드 | PEP8 엄격 준수 |
| 타입힌트 | 모든 함수 파라미터와 반환값에 필수 |
| Docstring | Google 스타일, 모든 public 메서드에 필수 (Args / Returns / Raises 포함) |
| Import 순서 | stdlib → third-party → local (isort 기준) |
| 명명 규칙 | 클래스 PascalCase / 함수·메서드 snake_case / 상수 UPPER_SNAKE_CASE |

**개발 환경:**

| 항목 | 기준 |
|------|------|
| 버전 관리 | Git Flow (main / develop / feature 브랜치 전략) |
| AI 보조 도구 | Cursor AI — `.cursorrules` 기준 준수 |
| 성능 측정 | pytest-benchmark |
| 의존성 관리 | `requirements.txt` 버전 고정 |

### 11.2 금지 패턴 (forbidden)

| # | 금지 패턴 | 이유 | 대안 |
|---|----------|------|------|
| 1 | `print()` 직접 사용 | 테스트 결과 오염 | `logging` 모듈 또는 `capsys` fixture |
| 2 | 하드코딩 상수 (REFACTOR 단계 이후) | 도메인 상수 분산 | `constants.py`에 선언 후 참조 |
| 3 | `bare except` 사용 | 치명적 예외 무시 | `except Exception as e:` 또는 구체적 타입 |
| 4 | `Domain → Boundary` import | ECB 의존 방향 위반 | 의존성 역전(DI), 인터페이스에만 의존 |
| 5 | `isinstance()` 레이어 간 타입 분기 | 암묵적 결합 | 추상 메서드 오버라이드 또는 Protocol |
| 6 | 테스트 파일 내 실제 파일 I/O / 네트워크 호출 | 테스트 격리 위반 | `InMemoryRepository` 또는 pytest fixtures |
| 7 | `type: ignore` 남용 | 타입 안전성 훼손 | 올바른 타입 선언 또는 `Union`/`Optional` |

> **예외:** GREEN 단계에서는 최소 구현을 위해 하드코딩 일시적 허용 (단, REFACTOR 단계에서 반드시 제거).

### 11.3 도메인 상수 (단일 진실 공급원)

```python
MAGIC_CONSTANT: int = 34
GRID_SIZE: int = 4
VALUE_RANGE_MAX: int = 16
BLANK_MARKER: int = 0
BLANK_COUNT: int = 2
```

> 모든 구현 코드에서 위 상수를 직접 참조한다. 34, 4, 16을 리터럴로 코드에 직접 사용하는 것은 REFACTOR 단계 이후 금지다.

### 11.4 테스트 패턴

- **패턴:** AAA (Arrange-Act-Assert)
- **fixture scope:** `function`이 기본값. `module`·`session` scope는 테스트 간 상태 오염 위험으로 금지.
- **예외 검증:** `pytest.raises()` 사용 필수
- **단일 검증 원칙:** 하나의 테스트에 검증 포인트는 1~3개 이내
- **테스트 ID 명시:** 각 테스트 함수에 테스트 ID(예: `BF-T01`)와 보호 Invariant(예: `INV-04`) 주석 필수

---

## 12. 성공 기준

| 기준 ID | 항목 | 목표값 | 측정 방법 |
|---------|------|--------|-----------|
| **SC-01** | Domain Logic 테스트 커버리지 | ≥ 95% | `pytest --cov=entity` |
| **SC-02** | 입력 검증 계약 테스트 통과율 | 100% | `pytest tests/boundary/` |
| **SC-03** | 하드코딩(매직 넘버) 잔존 여부 | 0건 | `rg` 패턴 스캔 |
| **SC-04** | Invariant → Test 추적 가능성 | INV-01~INV-09 전체 커버 | 테스트 주석 `INV-xx` 확인 |
| **SC-05** | UI Boundary 테스트 커버리지 | ≥ 85% | `pytest --cov=boundary` |
| **SC-06** | Data Layer 테스트 커버리지 | ≥ 80% | `pytest --cov=data` |
| **SC-07** | 전체 테스트 케이스 통과 | 71개 전체 GREEN | `pytest tests/ -v` |
| **SC-08** | ECB 레이어 의존성 방향 위반 | 0건 | import 방향 수동 검토 |
| **SC-09** | 입력 검증 + 풀이 응답 시간 | < 100ms | `pytest-benchmark` |

---

## 13. 범위 (In-Scope / Out-of-Scope)

### In-Scope

| 항목 | 설명 |
|------|------|
| 4×4 격자 두 빈칸 채우기 | 입력 `int[4][4]`, 출력 `int[6]` |
| ECB 레이어 분리 구현 | Boundary / Control / Entity / Data |
| Dual-Track TDD 71개 테스트 | Track A(UI) + Track B(Domain) + Integration + Data |
| Repository Pattern (InMemory) | Protocol 정의 + InMemoryRepository 구현 |
| 에러 코드 7종 처리 | 표준 메시지 문구 포함 |
| 커버리지 목표 달성 검증 | Domain ≥ 95% / UI ≥ 85% / Data ≥ 80% |

### Out-of-Scope

| 항목 | 배제 근거 |
|------|-----------|
| GUI / Web UI | Boundary는 입출력 계약 경계 — 실제 화면은 이 훈련의 대상 외 |
| 데이터베이스 영속성 | Data Layer는 Protocol 수준으로 충분 |
| 5×5 이상 마방진 | INV-03 위반 — 별도 Epic으로 분리 필요 (Phase 2) |
| 빈칸 수 변형 케이스 | INV-04 위반 — 이 훈련 범위 외 |
| 성능 최적화 (비교·벤치마크) | 알고리즘 난이도보다 TDD 훈련이 목적 |
| 등가 해 열거 | INV-07(해 유일성 전제)에 의해 범위 외 |
| 네트워크 기능 (API 서버, HTTP) | 순수 Python 함수 계약으로 충분 |
| 다중 사용자 동시 접속 | InMemoryRepository는 단일 인스턴스 — Phase 2 이상에서 고려 |

---

## 14. Traceability Matrix

> **개념 → Invariant → 테스트 ID → 컴포넌트** 전체 수직 추적 체인

| 개념 | Invariant | 에러 코드 | 테스트 범위 | 담당 컴포넌트 |
|------|-----------|----------|------------|--------------|
| 격자 크기 검증 | INV-03 | `INVALID_GRID_SIZE` | UI-T01~T03, DT-T11~T13 | `InputValidator`, `MatrixRepository` |
| 빈칸 개수 검증 | INV-04 | `INVALID_BLANK_COUNT` | BF-T03~T05, UI-T05~T07 | `BlankFinder`, `InputValidator` |
| 셀 값 범위 검증 | INV-05 | `INVALID_CELL_VALUE` | UI-T08~T11 | `InputValidator` |
| 비영 중복 검증 | INV-06 | `DUPLICATE_VALUE` | MF-T05, UI-T12~T15 | `InputValidator`, `MissingNumberFinder` |
| Magic Constant 검증 | INV-01 | `NO_SOLUTION` | MV-T01~T07, IT-S01~S02 | `MagicSquareValidator` |
| 숫자 집합 완전성 | INV-02 | — | MF-T01~T04 | `MissingNumberFinder` |
| 해 유일성 | INV-07 | `NO_SOLUTION` | SS-T01~T03, IT-F05 | `SolvingStrategy` |
| 출력 좌표 범위 | INV-08 | — | SS-T04, SR-T01~T03, UI-T17 | `SolveResult`, `InputValidator` |
| 출력 숫자 범위·유일성 | INV-09 | — | SR-T04~T06, MF-T02 | `SolveResult`, `MissingNumberFinder` |
| 배치 우선순위 규칙 | (출력 결정론) | — | SS-T01~T02, IT-S01~S02 | `SolvingStrategy` |
| 저장/로드 불변성 | INV-03 | — | DT-T12~T13 | `InMemoryRepository` |
| End-to-End 정상 흐름 | INV-01~INV-09 전체 | — | IT-S01~S04 | 전체 컴포넌트 |
| End-to-End 실패 흐름 | INV-03~INV-07 | 7종 전체 | IT-F01~F06 | 전체 컴포넌트 |

---

## 부록 A — 5단계 User Journey 요약

| 단계 | 핵심 활동 | 완료 기준 | 보호 Invariant |
|------|-----------|-----------|----------------|
| **Step 1** — 문제 인식 | INV-01~INV-09 도출 및 문서화 | 9개 불변조건 전체 명문화 | INV-01~INV-09 |
| **Step 2** — 계약 정의 | 입력·출력·예외 3개 계약 스키마 작성 | 에러 코드 7종 + `int[6]` 포맷 확정 | INV-03~INV-09 |
| **Step 3** — Domain 분리 | SRP 기반 컴포넌트 4종 설계 | 각 컴포넌트의 책임과 역설계 예방 확인 | INV-01~INV-04 |
| **Step 4** — Dual-Track TDD | Track A/B 병렬 RED→GREEN→REFACTOR | 71개 전체 GREEN + 커버리지 목표 달성 | INV-01~INV-09 전체 |
| **Step 5** — 회귀 보호 | 엣지·오류·실패 케이스 추가 | 매직 넘버 0건 + ECB 위반 0건 | INV-01~INV-09 전체 |

---

## 부록 B — 변경 금지 항목 (Change Freeze)

> 아래 항목은 이 PRD 범위 내에서 절대 변경 금지다.

| 항목 | 변경 금지 이유 |
|------|--------------|
| 출력 포맷 `int[6]` 및 원소 순서 | 호출자 계약 위반 |
| 좌표 1-index 기준 | INV-08 위반 |
| 에러 메시지 문구 7종 | UI 계약 위반 |
| Magic Constant = 34 | 수학적 불변 |
| 배치 우선순위 규칙 (A→B 순서) | 출력 결정론 보장 |
| INV-01~INV-09 번호 체계 | 테스트 ID와 1:1 연결 |
| TDD 사이클 순서 (RED→GREEN→REFACTOR) | 훈련 목적 핵심 |

---

*이 PRD는 구현 코드를 포함하지 않는다. 모든 요구사항은 테스트/검증 가능하게 작성되었으며, MLOps 과정 Dual-Track UI + Logic TDD 방법론(UX Contract / Logic Rule 이중 언어 체계, L0~L3 Gherkin 레벨)을 적용하였다. 새로운 기능은 추가되지 않았다.*
