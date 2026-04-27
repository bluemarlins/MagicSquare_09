# 4×4 Magic Square — Dual-Track TDD + Clean Architecture 설계 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square 프로그램 개발 |
| **보고서 유형** | 아키텍처 설계 및 TDD 계약 정의 (Design Report) |
| **작성일** | 2026-04-27 |
| **단계 범위** | Logic Layer 설계 → UI Boundary → Data Layer → 통합 검증 |
| **목적** | 구현 이전에 레이어 분리·계약 기반 테스트·추적 가능성을 확립하여 리팩토링에 안전한 설계 기준을 마련한다 |
| **설계 원문** | `Design/02_MagicSquare_TDD_CleanArchitecture_Design.md` |

---

## 목차

1. [설계 배경 및 제약](#1-설계-배경-및-제약)
2. [공통 계약 기반](#2-공통-계약-기반)
3. [Logic Layer (Domain) 설계 요약](#3-logic-layer-domain-설계-요약)
4. [Screen Layer (UI Boundary) 설계 요약](#4-screen-layer-ui-boundary-설계-요약)
5. [Data Layer 설계 요약](#5-data-layer-설계-요약)
6. [Integration & Verification 요약](#6-integration--verification-요약)
7. [테스트 계획 전체 요약](#7-테스트-계획-전체-요약)
8. [종합 결론 및 다음 단계](#8-종합-결론-및-다음-단계)

---

## 1. 설계 배경 및 제약

이 설계는 이전 단계(보고서 01)에서 확립된 핵심 전제를 이어받는다.

> **"무엇을 만들 것인가"가 아니라 "어떤 조건이 성립할 때 성공인가"를 먼저 정의한다.**

### 설계에 부과된 4가지 제약

| # | 제약 | 이유 |
|---|------|------|
| 1 | **구현 코드 작성 금지** | 계약과 테스트가 구현보다 먼저 결정되어야 함 |
| 2 | **UI는 Boundary로 정의** | 실제 화면이 아니라 입력/출력 경계만 다룸 |
| 3 | **Data Layer는 인터페이스 수준** | DB가 아닌 저장/로드 추상화 수준 — 구현체 교체 가능 |
| 4 | **입력/출력 계약 고정** | 입력 `int[4][4]`, 출력 `int[6]` — 변경 금지 |

### 입력/출력 계약 확정

```
입력:  int[4][4]
       - 0은 빈칸 (정확히 2개)
       - 값 범위: 0 또는 1~16
       - 0 제외 중복 금지

출력:  int[6] = [r1, c1, n1, r2, c2, n2]
       - 좌표는 1-index
       - n1: 첫 번째 빈칸에 채울 숫자
       - n2: 두 번째 빈칸에 채울 숫자
       - 우선순위: (작은수→첫빈칸)이 마방진이면 그 순서, 아니면 반대
```

---

## 2. 공통 계약 기반

모든 레이어가 공유하는 수학적·논리적 불변조건을 먼저 정의한다.
이 조건들은 **변경 금지 규칙**이며, 모든 테스트가 이 조건을 보호한다.

### 도메인 불변조건 (Invariants)

| # | 불변조건 | 내용 | 변경 가능 여부 |
|---|----------|------|---------------|
| INV-01 | Magic Constant | 모든 행·열·대각선의 합 = **34** | ❌ 금지 |
| INV-02 | 숫자 집합 완전성 | 1~16 각각 정확히 1회 등장 | ❌ 금지 |
| INV-03 | 격자 크기 | 행 4개, 각 행 열 4개 | ❌ 금지 |
| INV-04 | 빈칸 개수 | 0의 개수 = 정확히 2 | ❌ 금지 |
| INV-05 | 값 범위 | 모든 셀 값 ∈ {0, 1, …, 16} | ❌ 금지 |
| INV-06 | 비영 중복 없음 | 0 제외 동일 숫자 2회 이상 금지 | ❌ 금지 |
| INV-07 | 해 유일성 전제 | 두 빈칸 조합 중 유효한 것은 정확히 1가지 | ❌ 금지 |
| INV-08 | 출력 좌표 범위 | r, c ∈ {1, 2, 3, 4} | ❌ 금지 |
| INV-09 | 출력 숫자 범위 | n1, n2 ∈ {1,…,16}, n1 ≠ n2 | ❌ 금지 |

> 이 9개 불변조건이 **테스트 케이스의 원천**이다.  
> 불변조건을 위반하는 입력·출력은 모두 예외로 처리된다.

---

## 3. Logic Layer (Domain) 설계 요약

### 3.1 계층 구조

```
[Domain Layer]
├── Entity
│   └── MagicSquare          ← 4×4 격자 보유 + 자가 검증
├── Value Objects
│   ├── Cell                 ← (row, col) 불변, 1-index
│   ├── CellValue            ← 0 또는 1~16 불변
│   ├── MissingPair          ← (smaller, larger), smaller < larger 보장
│   └── SolveResult          ← int[6] 래퍼, 반환 포맷 표준화
└── Domain Services
    ├── BlankFinder          ← 격자에서 빈칸 2개 위치 탐색
    ├── MissingNumberFinder  ← 1~16 중 누락 숫자 2개 탐색
    ├── MagicSquareValidator ← 10개 합산 조건 검증
    └── SolvingStrategy      ← 두 조합 시도 + 우선순위 적용
```

### 3.2 핵심 유스케이스 흐름

```
격자 입력
  → UC-D01: 빈칸 2개 위치 추출 (BlankFinder)
  → UC-D02: 누락 숫자 2개 탐색 (MissingNumberFinder)
  → UC-D04: 조합 A(작은수→첫빈칸) 시도 → 마방진 검증 성공이면 반환
            조합 B(큰수→첫빈칸) 시도 → 마방진 검증 성공이면 반환
            두 조합 모두 실패 → NoSolutionException
  → SolveResult(int[6]) 반환
```

### 3.3 Domain API 핵심 계약 요약

| Domain Service | 메서드 | 주요 실패조건 |
|----------------|--------|-------------|
| `BlankFinder` | `findBlanks(grid) → Cell[2]` | 빈칸 수 ≠ 2 → `InvalidBlankCountException` |
| `MissingNumberFinder` | `findMissing(grid) → MissingPair` | 누락 수 ≠ 2 → `InvalidMissingCountException` |
| `MagicSquareValidator` | `isValid(grid) → boolean` | 0 포함 → `IncompleteGridException` |
| `SolvingStrategy` | `solve(grid, blanks, missing) → SolveResult` | 두 조합 실패 → `NoSolutionException` |

### 3.4 Domain 테스트 케이스 수: **29개**

| 대상 | 케이스 수 |
|------|----------|
| BlankFinder | 6개 (BF-T01~T06) |
| MissingNumberFinder | 5개 (MF-T01~T05) |
| MagicSquareValidator | 7개 (MV-T01~T07) |
| SolvingStrategy | 5개 (SS-T01~T05) |
| SolveResult VO | 6개 (SR-T01~T06) |

---

## 4. Screen Layer (UI Boundary) 설계 요약

### 4.1 UI의 역할

UI Layer는 **실제 화면이 아닌 입력/출력 경계(Boundary)** 로 정의된다.  
Domain을 직접 호출하기 전에 입력을 검증하고, Domain 예외를 표준 에러 포맷으로 변환한다.

```
호출자 → [InputValidator] → Domain.solve() → [ResponseFormatter] → 호출자
              ↑                    ↑
         4단계 검증           Mock 처리(테스트 시)
```

### 4.2 입력 검증 순서 (고정)

| 순서 | 검증 항목 | 실패 시 errorCode |
|------|----------|-----------------|
| 1 | 격자 크기 (4×4) | `INVALID_GRID_SIZE` |
| 2 | 셀 값 범위 (0 또는 1~16) | `INVALID_CELL_VALUE` |
| 3 | 빈칸(0) 개수 (정확히 2) | `INVALID_BLANK_COUNT` |
| 4 | 비영 중복 여부 | `DUPLICATE_VALUE` |

> **첫 번째 실패 즉시 반환 — 다중 오류 동시 반환 금지**

### 4.3 에러 메시지 표준 문구 (변경 금지)

| errorCode | 메시지 패턴 |
|-----------|------------|
| `INVALID_INPUT` | `"입력 행렬이 null입니다."` |
| `INVALID_GRID_SIZE` | `"행렬 크기는 4×4이어야 합니다."` |
| `INVALID_BLANK_COUNT` | `"빈칸(0)은 정확히 2개이어야 합니다. 현재: {count}개"` |
| `INVALID_CELL_VALUE` | `"셀 값은 0 또는 1~16이어야 합니다. 위치: (행{r}, 열{c}), 값: {v}"` |
| `DUPLICATE_VALUE` | `"중복된 값이 있습니다. 값: {v}"` |
| `NO_SOLUTION` | `"입력된 행렬로 마방진을 완성할 수 없습니다."` |
| `INTERNAL_ERROR` | `"내부 오류가 발생했습니다."` |

> 위치는 1-index 기준. 메시지 끝 마침표(`.`) 필수.

### 4.4 UI 테스트 케이스 수: **19개**

| 분류 | 케이스 수 |
|------|----------|
| 크기 오류 | 4개 (UI-T01~T04) |
| 빈칸 오류 | 3개 (UI-T05~T07) |
| 값 범위 오류 | 4개 (UI-T08~T11) |
| 중복 오류 | 4개 (UI-T12~T15) |
| 반환 포맷 검증 | 4개 (UI-T16~T19) |

---

## 5. Data Layer 설계 요약

### 5.1 Data Layer의 학습 목적

Data Layer는 DB 연동이 목적이 아니다.  
**Repository Pattern을 통한 저장소 추상화**를 학습하고,  
추후 구현체 교체(InMemory → File)를 **테스트 코드 수정 없이** 달성하는 것이 목적이다.

### 5.2 인터페이스 계약 핵심

| 메서드 | 시그니처 | 주요 실패조건 |
|--------|----------|-------------|
| `save` | `save(id, grid) → void` | 중복 id → `DuplicateIdException` |
| `load` | `load(id) → int[][]` | 없는 id → `NotFoundException` |
| `exists` | `exists(id) → boolean` | — |
| `delete` | `delete(id) → void` | 없는 id → `NotFoundException` |

### 5.3 구현 방식 결정: InMemoryRepository 채택

| 채택 이유 | 설명 |
|-----------|------|
| **테스트 격리 완전** | `@BeforeEach`에서 새 인스턴스 생성만으로 완전 초기화 가능 |
| **구현 복잡성 최소화** | TDD 초기 단계에서 직렬화 복잡성이 학습을 방해하지 않음 |
| **전환 비용 제로** | 인터페이스가 동일하므로 추후 FileRepository 교체 시 테스트 무수정 |

### 5.4 Data 테스트 케이스 수: **13개**

| 분류 | 케이스 수 |
|------|----------|
| 저장/로드 정합성 | 5개 (DT-T01~T05) |
| 예외 처리 | 6개 (DT-T06~T11) |
| 불변조건 (4×4 유지) | 2개 (DT-T12~T13) |

---

## 6. Integration & Verification 요약

### 6.1 레이어 의존성 방향

```
[UI Boundary]
      │  의존
      ▼
[Application Facade] (선택적 얇은 레이어)
      │  의존
      ▼
[Domain Layer] ←──────────── [Data Layer]
(BlankFinder,                 (MatrixRepository)
 MissingFinder,
 Validator,
 SolvingStrategy)
```

**절대 금지 방향:**

| 금지 사항 | 이유 |
|-----------|------|
| Domain → Data 의존 | Domain은 순수 로직 — 저장소를 몰라야 함 |
| UI → Data 직접 호출 | Application Facade를 통해서만 조율 |
| 구현체 직접 참조 | 항상 인터페이스에만 의존 |

### 6.2 통합 테스트 시나리오: **10개**

**정상 시나리오 (4개)**

| # | 시나리오 | 검증 핵심 |
|---|----------|----------|
| IT-S01 | 조합 A(작은수→첫빈칸) 성공 | n1<n2, 완성 후 마방진 검증, 좌표 1-index |
| IT-S02 | 조합 B(큰수→첫빈칸) 성공 | n1>n2, 완성 후 마방진 검증 |
| IT-S03 | 빈칸이 같은 행에 위치 | 행 우선 좌표 순서 정확성 |
| IT-S04 | 저장 후 로드하여 재솔빙 | 저장/로드 후 결과 재현성 |

**실패 시나리오 (6개)**

| # | 시나리오 | 실패 레이어 | 반환 errorCode |
|---|----------|------------|---------------|
| IT-F01 | 격자 크기 오류 | UI Boundary | `INVALID_GRID_SIZE` |
| IT-F02 | 빈칸 3개 | UI Boundary | `INVALID_BLANK_COUNT` |
| IT-F03 | 범위 초과 값 | UI Boundary | `INVALID_CELL_VALUE` |
| IT-F04 | 중복 값 포함 | UI Boundary | `DUPLICATE_VALUE` |
| IT-F05 | 해 없음 | Domain Layer | `NO_SOLUTION` |
| IT-F06 | Data save 예외 | Data Layer | 솔빙은 정상 반환 |

### 6.3 변경 금지 항목 (회귀 보호)

| 항목 | 금지 이유 |
|------|-----------|
| 출력 포맷 `int[6]` 및 순서 | 호출자 계약 위반 |
| 좌표 1-index 기준 | INV-08 위반 |
| 에러 메시지 문구 (7종) | UI 계약 위반 |
| Magic Constant = 34 | 수학적 불변 |
| 배치 우선순위 규칙 | 출력 결정론 보장 |

### 6.4 커버리지 목표

| 레이어 | 목표 | 기준 |
|--------|------|------|
| Domain Logic | **95% 이상** | 라인 커버리지 |
| UI Boundary | **85% 이상** | 라인 커버리지 |
| Data Layer | **80% 이상** | 라인 커버리지 |

---

## 7. 테스트 계획 전체 요약

### 테스트 케이스 분포

| 레이어 | 범위 | 케이스 수 |
|--------|------|----------|
| Domain — BlankFinder | BF-T01~T06 | 6개 |
| Domain — MissingNumberFinder | MF-T01~T05 | 5개 |
| Domain — MagicSquareValidator | MV-T01~T07 | 7개 |
| Domain — SolvingStrategy | SS-T01~T05 | 5개 |
| Domain — SolveResult VO | SR-T01~T06 | 6개 |
| UI Boundary | UI-T01~T19 | 19개 |
| Data Layer | DT-T01~T13 | 13개 |
| 통합 (정상) | IT-S01~S04 | 4개 |
| 통합 (실패) | IT-F01~F06 | 6개 |
| **합계** | | **71개** |

### Traceability Matrix (요약)

| 개념 | Invariant | 테스트 범위 | 담당 컴포넌트 |
|------|-----------|------------|--------------|
| 격자 크기 | INV-03 | UI-T01~T03, DT-T11~T13 | `InputValidator`, `MatrixRepository` |
| 빈칸 개수 | INV-04 | BF-T03~T05, UI-T05~T07 | `BlankFinder`, `InputValidator` |
| 값 범위 | INV-05 | UI-T08~T11 | `InputValidator` |
| 비영 중복 | INV-06 | MF-T05, UI-T12~T15 | `InputValidator`, `MissingNumberFinder` |
| Magic Constant | INV-01 | MV-T01~T07, IT-S01~S02 | `MagicSquareValidator` |
| 숫자 집합 완전성 | INV-02 | MF-T01~T04 | `MissingNumberFinder` |
| 해 유일성 | INV-07 | SS-T01~T03 | `SolvingStrategy` |
| 출력 좌표 범위 | INV-08 | SS-T04, SR-T01~T03, UI-T17 | `SolveResult`, `InputValidator` |
| 출력 숫자 범위 | INV-09 | SR-T04~T06, MF-T02 | `SolveResult`, `MissingNumberFinder` |
| 배치 우선순위 | (규칙) | SS-T01~T02, IT-S01~S02 | `SolvingStrategy` |

---

## 8. 종합 결론 및 다음 단계

### 이 설계 단계에서 확립된 것

```
문제 정의 단계 (보고서 01)
  → "조건이 성립할 때 성공"을 먼저 정의했다
        ↓
아키텍처 설계 단계 (이 보고서)
  → 그 조건들을 레이어별 계약과 테스트로 변환했다
        ↓
다음: TDD RED 단계
  → 테스트를 먼저 작성하고, 통과시키는 구현을 추가한다
```

### 설계가 해결한 4가지 구조적 문제

| 이전 문제 | 이 설계의 해결 방식 |
|-----------|------------------|
| 검증 기준 미정 | 불변조건 9개 + 에러 코드 7종 고정 |
| 탐색 과정 은폐 | SolvingStrategy의 조합 시도 2가지 명시 |
| 해의 범위 미정 | 유효 조합 = 정확히 1가지 (INV-07) |
| 목적 부재 | 커버리지 목표 + Traceability Matrix로 훈련 목적 구체화 |

### 다음 단계

| 단계 | 내용 | 입력 |
|------|------|------|
| **STEP 6** | RED 단계 — Domain 테스트 29개 작성 (실패 상태) | 이 보고서의 Domain API 계약 |
| **STEP 7** | GREEN 단계 — Domain 구현체 작성 (테스트 통과) | RED 단계 테스트 |
| **STEP 8** | RED 단계 — UI Boundary 테스트 19개 작성 | 이 보고서의 UI 계약 |
| **STEP 9** | GREEN 단계 — UI 구현체 작성 | UI RED 단계 테스트 |
| **STEP 10** | Data Layer 테스트 + 구현 | 이 보고서의 Data 계약 |
| **STEP 11** | 통합 테스트 10개 작성 + 통과 | 모든 하위 레이어 완료 후 |
| **STEP 12** | Refactor — 커버리지 목표 달성 검증 | 전체 71개 테스트 GREEN |
