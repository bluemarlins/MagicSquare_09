# Magic Square (4×4) — Dual-Track TDD + Clean Architecture 설계 문서

> **목적:** 구현 없이, 레이어 분리 · 계약 기반 테스트 · 리팩토링 훈련  
> **날짜:** 2026-04-27  
> **제약:** 구현 코드 작성 금지 / UI는 Boundary로 정의 / Data Layer는 저장·로드 인터페이스 수준

---

## 사전 공통 정의

| 항목 | 값 |
|---|---|
| 격자 크기 | 4 × 4 |
| 사용 숫자 | 1 ~ 16 (정수, 중복 없음) |
| Magic Constant | (1+2+…+16) / 4 = **34** |
| 빈칸 표기 | `0` |
| 빈칸 개수 | **정확히 2개** |
| 좌표계 | **1-index** (행 1~4, 열 1~4) |

**출력 배열 의미 (int[6])**

```
[r1, c1, n1,  r2, c2, n2]
  └첫빈칸 행  └첫빈칸 열  └첫빈칸에 채울 숫자
                          └둘째빈칸 행  └둘째빈칸 열  └둘째빈칸에 채울 숫자
```

**숫자 배치 우선순위 규칙 (계약 고정)**  
`(작은수→첫빈칸, 큰수→둘째빈칸)` 조합이 마방진을 만족하면 그 순서로,  
만족하지 않으면 반대 순서 `(큰수→첫빈칸, 작은수→둘째빈칸)`로 반환.

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

### Entities

| 이름 | 설명 | 책임 (SRP) |
|---|---|---|
| `MagicSquare` | 4×4 int 배열을 감싸는 핵심 엔티티 | 격자 데이터 보유 및 불변 조건 자가 검증 |

### Value Objects

| 이름 | 설명 | 책임 (SRP) |
|---|---|---|
| `Cell` | (row, col) 좌표 쌍. 불변. | 좌표 범위 검증 (`1 ≤ row ≤ 4`, `1 ≤ col ≤ 4`) |
| `CellValue` | 0 또는 1~16 범위의 정수. 불변. | 값 범위 검증 |
| `SolveResult` | `int[6]` 배열 래퍼. 불변. | 반환 포맷 표준화 및 좌표 1-index 보장 |
| `MissingPair` | 누락된 두 숫자 쌍 `(smaller, larger)`. 불변. | 두 숫자 순서 정규화 (smaller < larger 보장) |

### Domain Services

| 이름 | 책임 (SRP) |
|---|---|
| `BlankFinder` | 격자에서 0인 셀 2개의 위치를 순서대로 반환 |
| `MissingNumberFinder` | 1~16 중 격자에 없는 숫자 2개 탐색 |
| `MagicSquareValidator` | 4개 행 + 4개 열 + 2개 대각선 합이 모두 34인지 검증 |
| `SolvingStrategy` | 두 숫자·두 빈칸 조합 2가지 시도 후 우선순위 규칙에 따라 결과 선택 |

---

## 1.2 도메인 불변조건 (Invariants)

| # | 불변조건 이름 | 내용 | 검증 시점 |
|---|---|---|---|
| INV-01 | Magic Constant | 모든 행·열·대각선의 합 = 34 | 마방진 판정 시 |
| INV-02 | 숫자 집합 완전성 | 1~16 각각 정확히 1회 등장 | 솔루션 완성 후 |
| INV-03 | 격자 크기 | 행 4개, 각 행 열 4개 | 입력 수신 즉시 |
| INV-04 | 빈칸 개수 | 0의 개수 = 정확히 2 | 입력 수신 즉시 |
| INV-05 | 값 범위 | 모든 셀 값 ∈ {0, 1, 2, …, 16} | 입력 수신 즉시 |
| INV-06 | 비영 중복 없음 | 0 제외, 동일 숫자 2회 이상 등장 금지 | 입력 수신 즉시 |
| INV-07 | 해 유일성 전제 | 두 빈칸에 대해 유효 조합은 정확히 1가지 | 솔루션 반환 전 |
| INV-08 | 출력 좌표 범위 | r1, c1, r2, c2 ∈ {1,2,3,4} | 출력 생성 시 |
| INV-09 | 출력 숫자 범위 | n1, n2 ∈ {1,…,16}, n1 ≠ n2 | 출력 생성 시 |

---

## 1.3 핵심 유스케이스 (도메인 관점)

| # | 유스케이스 | 입력 | 출력 | 관련 Domain Service |
|---|---|---|---|---|
| UC-D01 | 빈칸 찾기 | 4×4 int[][] | `Cell[]` (크기 2, 행 우선 탐색 순서) | `BlankFinder` |
| UC-D02 | 누락 숫자 찾기 | 4×4 int[][] | `MissingPair` (smaller, larger) | `MissingNumberFinder` |
| UC-D03 | 마방진 판정 | 완성된 4×4 int[][] | `boolean` | `MagicSquareValidator` |
| UC-D04 | 두 조합 시도 | `Cell[]`(2), `MissingPair`, 원본 격자 | `SolveResult` | `SolvingStrategy` |
| UC-D05 | 전체 솔루션 흐름 | 4×4 int[][] | `SolveResult` | 모든 Domain Service 조합 |

**UC-D04 조합 시도 세부 흐름:**

```
조합 A: Cell[0]←smaller,  Cell[1]←larger  → MagicSquareValidator 판정
조합 B: Cell[0]←larger,   Cell[1]←smaller → MagicSquareValidator 판정

if (조합 A 성공) → SolveResult(Cell[0], smaller, Cell[1], larger)
elif (조합 B 성공) → SolveResult(Cell[0], larger, Cell[1], smaller)
else → 예외 발생 (NoSolutionException)
```

---

## 1.4 Domain API (내부 계약)

> 코드 작성 금지 — 메서드 시그니처 및 계약 명세만 기술

### `BlankFinder`

| 항목 | 내용 |
|---|---|
| 메서드 | `findBlanks(grid: int[][]) → Cell[2]` |
| 전제조건 | grid는 4×4, 0의 개수 = 2 |
| 반환 | 행 우선(row-major) 순서로 첫 번째·두 번째 빈칸의 `Cell` 배열 |
| 실패조건 | 0의 개수 ≠ 2 → `InvalidBlankCountException` |

### `MissingNumberFinder`

| 항목 | 내용 |
|---|---|
| 메서드 | `findMissing(grid: int[][]) → MissingPair` |
| 전제조건 | grid는 4×4, 값 범위·중복 조건 만족, 0은 2개 |
| 반환 | `MissingPair(smaller, larger)` — smaller < larger 보장 |
| 실패조건 | 누락 숫자 수 ≠ 2 → `InvalidMissingCountException` |

### `MagicSquareValidator`

| 항목 | 내용 |
|---|---|
| 메서드 | `isValid(grid: int[][]) → boolean` |
| 전제조건 | grid는 0이 없는 완성된 4×4 |
| 반환 | 모든 행(4) + 모든 열(4) + 주대각선(1) + 반대각선(1) = 합계 10개가 전부 34이면 `true` |
| 실패조건 | grid에 0 포함 → `IncompleteGridException` |

### `SolvingStrategy`

| 항목 | 내용 |
|---|---|
| 메서드 | `solve(grid: int[][], blanks: Cell[2], missing: MissingPair) → SolveResult` |
| 전제조건 | blanks.length = 2, missing.smaller < missing.larger |
| 반환 | `SolveResult([r1,c1,n1,r2,c2,n2])` — 우선순위 규칙 적용 |
| 실패조건 | 두 조합 모두 마방진 불만족 → `NoSolutionException` |

### `SolveResult`

| 항목 | 내용 |
|---|---|
| 생성자 | `SolveResult(r1, c1, n1, r2, c2, n2: int)` |
| 검증 | r1,r2,c1,c2 ∈ {1,2,3,4} / n1,n2 ∈ {1,…,16} / n1 ≠ n2 |
| 접근자 | `toArray() → int[6]` |
| 실패조건 | 범위 위반 → `IllegalSolveResultException` |

---

## 1.5 Domain 단위 테스트 설계 (RED 우선)

### BlankFinder 테스트

| # | 테스트 이름 | 시나리오 | 기대 결과 | 보호 Invariant |
|---|---|---|---|---|
| BF-T01 | 첫째·둘째 빈칸 행 우선 순서 반환 | 0이 (1,3)과 (3,2)에 위치 | `Cell(1,3), Cell(3,2)` 순 | INV-04 |
| BF-T02 | 같은 행에 두 빈칸 | 0이 (2,1)과 (2,4)에 위치 | `Cell(2,1), Cell(2,4)` 순 | INV-04 |
| BF-T03 | 빈칸 0개 → 예외 | 모든 셀이 1~16 | `InvalidBlankCountException` | INV-04 |
| BF-T04 | 빈칸 1개 → 예외 | 0이 1개 | `InvalidBlankCountException` | INV-04 |
| BF-T05 | 빈칸 3개 → 예외 | 0이 3개 | `InvalidBlankCountException` | INV-04 |
| BF-T06 | 빈칸이 마지막 셀(4,4) | 0이 (4,3)과 (4,4)에 위치 | `Cell(4,3), Cell(4,4)` 순 | INV-08 |

### MissingNumberFinder 테스트

| # | 테스트 이름 | 시나리오 | 기대 결과 | 보호 Invariant |
|---|---|---|---|---|
| MF-T01 | 누락 숫자 2개 정상 탐색 | 7과 11 누락 | `MissingPair(7, 11)` | INV-02 |
| MF-T02 | 누락 숫자가 1과 16 (경계값) | 1과 16 누락 | `MissingPair(1, 16)` | INV-02, INV-09 |
| MF-T03 | 연속된 두 숫자 누락 | 8과 9 누락 | `MissingPair(8, 9)` | INV-02 |
| MF-T04 | smaller < larger 보장 | 누락이 15, 3 순 탐색 | `MissingPair(3, 15)` | INV-09 |
| MF-T05 | 중복 값 포함 격자 → 예외 | 숫자 5가 두 번 등장 | `InvalidMissingCountException` | INV-06 |

### MagicSquareValidator 테스트

| # | 테스트 이름 | 시나리오 | 기대 결과 | 보호 Invariant |
|---|---|---|---|---|
| MV-T01 | 알려진 4×4 마방진 | 표준 Dürer 마방진 | `true` | INV-01 |
| MV-T02 | 행 합이 34가 아닌 격자 | 1행 합 = 35 | `false` | INV-01 |
| MV-T03 | 열 합이 34가 아닌 격자 | 2열 합 = 33 | `false` | INV-01 |
| MV-T04 | 주대각선 합 불일치 | 주대각선 합 = 32 | `false` | INV-01 |
| MV-T05 | 반대각선 합 불일치 | 반대각선 합 = 36 | `false` | INV-01 |
| MV-T06 | 0 포함 격자 → 예외 | 셀 중 0 존재 | `IncompleteGridException` | INV-07 |
| MV-T07 | 모든 조건 동시 만족 | 완전한 마방진 | `true` | INV-01, INV-02 |

### SolvingStrategy 테스트

| # | 테스트 이름 | 시나리오 | 기대 결과 | 보호 Invariant |
|---|---|---|---|---|
| SS-T01 | 조합 A(작은수→첫빈칸) 성공 | 작은수 배치 시 마방진 완성 | `SolveResult` n1=smaller, n2=larger | INV-07 |
| SS-T02 | 조합 B(큰수→첫빈칸) 성공 | 조합 A 실패, 조합 B 성공 | `SolveResult` n1=larger, n2=smaller | INV-07 |
| SS-T03 | 두 조합 모두 실패 → 예외 | 어떤 배치도 마방진 불성립 | `NoSolutionException` | INV-07 |
| SS-T04 | 반환 좌표가 1-index | 내부 0-index 셀이 (0,0)인 경우 | r1=1, c1=1 | INV-08 |
| SS-T05 | n1 ≠ n2 보장 | 정상 입력 | n1 ≠ n2 | INV-09 |

### SolveResult VO 테스트

| # | 테스트 이름 | 시나리오 | 기대 결과 | 보호 Invariant |
|---|---|---|---|---|
| SR-T01 | toArray() 길이 = 6 | 정상 생성 | 배열 길이 6 | INV-08, INV-09 |
| SR-T02 | 좌표 0 → 예외 | r1=0 전달 | `IllegalSolveResultException` | INV-08 |
| SR-T03 | 좌표 5 → 예외 | c2=5 전달 | `IllegalSolveResultException` | INV-08 |
| SR-T04 | 숫자 0 → 예외 | n1=0 전달 | `IllegalSolveResultException` | INV-09 |
| SR-T05 | 숫자 17 → 예외 | n2=17 전달 | `IllegalSolveResultException` | INV-09 |
| SR-T06 | n1 = n2 → 예외 | n1=7, n2=7 전달 | `IllegalSolveResultException` | INV-09 |

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오

```
[호출자]
    │
    ▼
① 4×4 int[][] 행렬 전달
    │
    ▼
② UI Boundary: 입력 유효성 검사 (크기 / 빈칸 수 / 값 범위 / 중복)
    │
    ├─── 검사 실패 → ErrorResponse 반환 (즉시 종료)
    │
    ▼
③ Domain Service 호출 (MagicSquareSolver.solve)
    │
    ├─── Domain 예외 → ErrorResponse 변환 후 반환
    │
    ▼
④ int[6] SolveResult 반환
    │
    ▼
[호출자] 결과 수신
```

**검증 순서 (순서가 에러 메시지에 영향):**

1. 격자 크기 검증 (행 수 → 각 행 열 수)
2. 값 범위 검증 (0 또는 1~16)
3. 빈칸(0) 개수 검증 (정확히 2)
4. 비영 중복 검증

---

## 2.2 UI 계약 (외부 계약)

### Input Schema

| 필드 | 타입 | 제약 |
|---|---|---|
| `grid` | `int[4][4]` | 행 수 = 4, 각 행 열 수 = 4 |
| 각 셀 값 | `int` | 값 ∈ {0, 1, 2, …, 16} |
| 0의 개수 | `int` | 정확히 2 |
| 비영 중복 | — | 없음 (0 제외 각 값 1회만) |

### Output Schema (정상)

| 필드 | 타입 | 설명 |
|---|---|---|
| `result` | `int[6]` | `[r1, c1, n1, r2, c2, n2]` |
| `r1`, `r2` | `int` | 빈칸 행 번호 (1-index, 1~4) |
| `c1`, `c2` | `int` | 빈칸 열 번호 (1-index, 1~4) |
| `n1`, `n2` | `int` | 채울 숫자 (1~16, n1 ≠ n2) |

### Error Schema

| 필드 | 타입 | 예시 값 |
|---|---|---|
| `errorCode` | `string` | `"INVALID_GRID_SIZE"` |
| `message` | `string` | `"행렬 크기는 4×4이어야 합니다."` |
| `field` | `string?` | `"grid[2]"` (해당 필드 있으면) |

---

## 2.3 UI 레벨 테스트 (Contract-first, RED 우선)

> Domain은 **Mock**으로 대체. UI 레이어의 검증 로직만 테스트.

### 입력 크기 오류

| # | 테스트 이름 | 입력 | 기대 errorCode | 기대 message |
|---|---|---|---|---|
| UI-T01 | 행이 3개인 격자 | `int[3][4]` | `INVALID_GRID_SIZE` | `"행렬 크기는 4×4이어야 합니다."` |
| UI-T02 | 행이 5개인 격자 | `int[5][4]` | `INVALID_GRID_SIZE` | `"행렬 크기는 4×4이어야 합니다."` |
| UI-T03 | 한 행의 열이 3개 | `int[4][3]` (2번째 행) | `INVALID_GRID_SIZE` | `"행렬 크기는 4×4이어야 합니다."` |
| UI-T04 | null 입력 | `null` | `INVALID_INPUT` | `"입력 행렬이 null입니다."` |

### 빈칸 개수 오류

| # | 테스트 이름 | 입력 | 기대 errorCode | 기대 message |
|---|---|---|---|---|
| UI-T05 | 빈칸 0개 | 모든 셀 1~16 | `INVALID_BLANK_COUNT` | `"빈칸(0)은 정확히 2개이어야 합니다. 현재: 0개"` |
| UI-T06 | 빈칸 1개 | 0이 1개 | `INVALID_BLANK_COUNT` | `"빈칸(0)은 정확히 2개이어야 합니다. 현재: 1개"` |
| UI-T07 | 빈칸 3개 | 0이 3개 | `INVALID_BLANK_COUNT` | `"빈칸(0)은 정확히 2개이어야 합니다. 현재: 3개"` |

### 값 범위 오류

| # | 테스트 이름 | 입력 | 기대 errorCode | 기대 message |
|---|---|---|---|---|
| UI-T08 | 음수 포함 | 셀 중 `-1` 존재 | `INVALID_CELL_VALUE` | `"셀 값은 0 또는 1~16이어야 합니다. 위치: (행2, 열3), 값: -1"` |
| UI-T09 | 17 초과 값 | 셀 중 `17` 존재 | `INVALID_CELL_VALUE` | `"셀 값은 0 또는 1~16이어야 합니다. 위치: (행1, 열4), 값: 17"` |
| UI-T10 | 경계값 16 정상 | 셀에 `16` 존재 | (오류 없음) | — |
| UI-T11 | 경계값 1 정상 | 셀에 `1` 존재 | (오류 없음) | — |

### 중복 값 오류

| # | 테스트 이름 | 입력 | 기대 errorCode | 기대 message |
|---|---|---|---|---|
| UI-T12 | 비영 숫자 중복 | 숫자 `5`가 두 셀에 존재 | `DUPLICATE_VALUE` | `"중복된 값이 있습니다. 값: 5"` |
| UI-T13 | `0` 중복은 허용 | 0이 정확히 2개 | (오류 없음) | — |
| UI-T14 | 경계값(1) 중복 | 숫자 `1`이 두 번 | `DUPLICATE_VALUE` | `"중복된 값이 있습니다. 값: 1"` |
| UI-T15 | 경계값(16) 중복 | 숫자 `16`이 두 번 | `DUPLICATE_VALUE` | `"중복된 값이 있습니다. 값: 16"` |

### 반환 포맷 검증

| # | 테스트 이름 | 시나리오 | 기대 결과 |
|---|---|---|---|
| UI-T16 | 정상 입력 → 배열 길이 6 | Mock이 `[2,3,7,4,1,11]` 반환 | 배열 길이 = 6 |
| UI-T17 | 좌표 1-index 확인 | Mock이 `[1,1,n1,4,4,n2]` 반환 | r1=1, c1=1 (0 아님) |
| UI-T18 | Domain Mock 호출 1회 | 정상 입력 | Mock 호출 횟수 = 1 |
| UI-T19 | 입력 오류 시 Domain Mock 미호출 | 빈칸 3개인 격자 | Mock 호출 횟수 = 0 |

---

## 2.4 UX/출력 규칙

### 에러 메시지 표준 문구 (고정 — 변경 금지)

| errorCode | 메시지 패턴 | 변수 |
|---|---|---|
| `INVALID_INPUT` | `"입력 행렬이 null입니다."` | 없음 |
| `INVALID_GRID_SIZE` | `"행렬 크기는 4×4이어야 합니다."` | 없음 |
| `INVALID_BLANK_COUNT` | `"빈칸(0)은 정확히 2개이어야 합니다. 현재: {count}개"` | `{count}` |
| `INVALID_CELL_VALUE` | `"셀 값은 0 또는 1~16이어야 합니다. 위치: (행{r}, 열{c}), 값: {v}"` | `{r}`, `{c}`, `{v}` |
| `DUPLICATE_VALUE` | `"중복된 값이 있습니다. 값: {v}"` | `{v}` |
| `NO_SOLUTION` | `"입력된 행렬로 마방진을 완성할 수 없습니다."` | 없음 |
| `INTERNAL_ERROR` | `"내부 오류가 발생했습니다."` | 없음 |

**규칙:**
- 위치는 **1-index** 기준으로 표기
- 첫 번째 발견된 오류만 반환 (다중 오류 동시 반환 금지)
- 검증 순서: 크기 → 값 범위 → 빈칸 수 → 중복
- 메시지 문구 끝에 마침표(`.`) 필수
- 숫자 포맷 없음 (소수점·천 단위 구분자 금지)

---

# 3) Data Layer 설계

## 3.1 목적 정의

| 항목 | 내용 |
|---|---|
| 목적 | 입력 행렬과 실행 결과를 저장·로드하여 **재현 가능한 테스트 케이스 관리** 및 **결과 추적** 지원 |
| 학습 범위 | 저장소 추상화 (Repository Pattern) 연습 — DB 불필요 |
| 저장 대상 (필수) | 입력 행렬 (`int[4][4]`) |
| 저장 대상 (선택) | 실행 결과 (`int[6]`) |
| 교체 가능성 | InMemory ↔ File 구현체를 인터페이스 교체만으로 전환 가능 |

---

## 3.2 인터페이스 계약

### `MatrixRepository`

| 메서드 | 시그니처 | 전제조건 | 반환 | 실패조건 |
|---|---|---|---|---|
| `save` | `save(id: string, grid: int[][]) → void` | id 비어 있지 않음, grid는 4×4 | 없음 | id 중복 → `DuplicateIdException` / grid 크기 오류 → `InvalidGridException` |
| `load` | `load(id: string) → int[][]` | id 비어 있지 않음 | 4×4 int[][] | id 없음 → `NotFoundException` |
| `exists` | `exists(id: string) → boolean` | — | `true`/`false` | 없음 |
| `delete` | `delete(id: string) → void` | — | 없음 | id 없음 → `NotFoundException` |
| `listIds` | `listIds() → string[]` | — | 저장된 모든 id 목록 | 없음 |

### `ResultRepository` (선택)

| 메서드 | 시그니처 | 전제조건 | 반환 | 실패조건 |
|---|---|---|---|---|
| `saveResult` | `saveResult(id: string, result: int[6]) → void` | id 존재, result 길이 = 6 | 없음 | `NotFoundException` / `InvalidResultException` |
| `loadResult` | `loadResult(id: string) → int[6]` | id 존재 | int[6] | `NotFoundException` |

---

## 3.3 구현 옵션 비교

| 비교 항목 | 옵션 A: InMemoryRepository | 옵션 B: FileRepository (JSON) |
|---|---|---|
| 구현 복잡도 | 낮음 (Map 사용) | 중간 (직렬화/역직렬화 필요) |
| 테스트 격리 | 매우 쉬움 (인스턴스 교체) | 테스트 후 파일 정리 필요 |
| 재현성 | 프로세스 종료 시 소실 | 파일 유지로 재현 가능 |
| 실패 시나리오 | 구현하기 어려움 | 파일 없음·손상 시나리오 자연 발생 |
| 학습 효과 | Repository 패턴 기초 | 직렬화 + 예외 처리 추가 학습 |
| 인터페이스 교체 비용 | 낮음 | 낮음 (인터페이스 동일) |

**추천안: 옵션 A (InMemoryRepository)**

> **이유:**  
> 1. TDD 학습 초기 단계에서 **저장소 구현 복잡성이 도메인 로직 학습을 방해하지 않아야** 함.  
> 2. 테스트 격리가 완전하여 `@BeforeEach`에서 새 인스턴스 생성만으로 초기화 가능.  
> 3. 인터페이스가 동일하므로 추후 FileRepository로 교체 시 **테스트 코드를 수정하지 않아도 됨** (의존성 역전 원칙 실습).

---

## 3.4 Data 레이어 테스트

### 저장/로드 정합성

| # | 테스트 이름 | 시나리오 | 기대 결과 | 보호 조건 |
|---|---|---|---|---|
| DT-T01 | 저장 후 로드 = 원본 동일 | 격자 A를 저장 후 동일 id로 로드 | 로드된 배열 = 원본 배열 (deep equal) | INV-03 |
| DT-T02 | 로드 후 수정이 원본에 영향 없음 | 로드된 배열 셀 변경 후 재로드 | 재로드 = 최초 저장값 (방어 복사) | INV-03 |
| DT-T03 | 여러 id 독립 저장 | id "A", "B" 각각 저장 | 각각 올바른 격자 반환 | — |
| DT-T04 | exists() 저장 전/후 | 저장 전 → false, 저장 후 → true | 순서대로 `false`, `true` | — |
| DT-T05 | listIds() 반환 순서 | 3개 저장 후 listIds() | 3개 id 포함 (순서 무관) | — |

### 예외 처리

| # | 테스트 이름 | 시나리오 | 기대 예외 |
|---|---|---|---|
| DT-T06 | 없는 id 로드 | 미저장 id로 load() | `NotFoundException` |
| DT-T07 | 없는 id 삭제 | 미저장 id로 delete() | `NotFoundException` |
| DT-T08 | id 중복 저장 | 동일 id로 save() 2회 | `DuplicateIdException` |
| DT-T09 | null id 저장 | `save(null, grid)` | `IllegalArgumentException` |
| DT-T10 | 빈 문자열 id 저장 | `save("", grid)` | `IllegalArgumentException` |
| DT-T11 | 크기 불량 격자 저장 | `save(id, int[3][4])` | `InvalidGridException` |

### 불변조건 (4×4 유지)

| # | 테스트 이름 | 시나리오 | 기대 결과 |
|---|---|---|---|
| DT-T12 | 로드된 배열 행 수 = 4 | 정상 저장 후 로드 | `grid.length == 4` |
| DT-T13 | 로드된 배열 각 행 열 수 = 4 | 정상 저장 후 로드 | 모든 `grid[i].length == 4` |

---

# 4) Integration & Verification (통합 및 검증)

## 4.1 통합 경로 정의

```
[호출자 / 테스트]
       │
       ▼
┌──────────────────┐
│   UI Boundary    │  ← 입력 유효성 검사 (INV-03 ~ INV-06)
│  (InputValidator)│
└────────┬─────────┘
         │ 유효한 int[4][4]
         ▼
┌──────────────────────────────────────────────┐
│              Application Facade              │  ← (선택적 레이어, 얇음)
│          MagicSquareSolverFacade             │
└──┬────────────────────────────────────────┬──┘
   │                                        │
   ▼                                        ▼
┌──────────────────┐              ┌──────────────────┐
│   Domain Layer   │              │   Data Layer     │
│  BlankFinder     │              │ MatrixRepository │
│  MissingFinder   │◄─────────────┤  (선택: 저장)    │
│  Validator       │              └──────────────────┘
│  SolvingStrategy │
└──────────────────┘
         │
         ▼
   SolveResult (int[6])
         │
         ▼
   [호출자 수신]
```

**의존성 방향 규칙:**

| 방향 | 설명 |
|---|---|
| UI → Domain | UI가 Domain 인터페이스에만 의존 (구현체 직접 참조 금지) |
| UI → Data | UI는 Data Layer를 직접 호출하지 않음 |
| Domain → Data | Domain은 Data Layer를 모름 (Data 의존 금지) |
| Application → Domain | Application Facade가 Domain + Data 조율 |
| Data → Domain | Data는 Domain 타입(`int[][]`)만 다룸 (Entity 의존 없음) |

---

## 4.2 통합 테스트 시나리오

### 정상 시나리오

| # | 시나리오 이름 | 입력 | 기대 출력 | 검증 항목 |
|---|---|---|---|---|
| IT-S01 | 조합 A 성공 (작은수→첫빈칸) | 알려진 마방진에서 7(행2,열3), 11(행4,열1) 제거 | `[2,3,7,4,1,11]` | 배열 길이=6, n1<n2, 좌표 1-index, 완성 후 마방진 검증 |
| IT-S02 | 조합 B 성공 (큰수→첫빈칸) | 조합 A 시 마방진 불성립, 조합 B 시 성립 | `[r1,c1,larger,r2,c2,smaller]` | n1>n2, 완성 후 마방진 검증 |
| IT-S03 | 빈칸이 같은 행에 위치 | 동일 행(행3)에 두 빈칸 | 올바른 `int[6]` | 행 우선 순서 좌표 정확성 |
| IT-S04 | 저장 후 로드하여 재솔빙 | 격자 저장 → 로드 → 솔빙 | IT-S01과 동일 결과 | 저장/로드 후 결과 재현성 |

### 실패 시나리오

| # | 시나리오 이름 | 입력 | 기대 결과 | 실패 레이어 |
|---|---|---|---|---|
| IT-F01 | 격자 크기 오류 | `int[3][4]` | `INVALID_GRID_SIZE` 에러 반환 | UI Boundary |
| IT-F02 | 빈칸 3개 | 0이 3개인 4×4 격자 | `INVALID_BLANK_COUNT` 에러 반환 (현재: 3개) | UI Boundary |
| IT-F03 | 범위 초과 값 포함 | 셀 중 값 = 20 | `INVALID_CELL_VALUE` 에러 반환 | UI Boundary |
| IT-F04 | 중복 값 포함 | 숫자 8이 두 곳 | `DUPLICATE_VALUE` 에러 반환 | UI Boundary |
| IT-F05 | 해 없음 (도메인 실패) | 유효 형식이나 두 조합 모두 마방진 불성립 | `NO_SOLUTION` 에러 반환 | Domain Layer |
| IT-F06 | 저장 실패 후 솔빙 진행 여부 | Data Layer save 예외 발생 | 솔빙 결과는 정상 반환, 저장 실패 로그 | Data Layer |

---

## 4.3 회귀 보호 규칙

### 기존 테스트 유지 정책

| # | 규칙 | 내용 |
|---|---|---|
| RG-01 | 테스트 삭제 금지 | 한 번 통과한 테스트는 삭제하지 않는다. 대신 `@Deprecated` 마킹 후 사유 기록. |
| RG-02 | 테스트 수정 제한 | 계약이 변경되지 않는 한 기존 테스트의 기대값을 수정하지 않는다. |
| RG-03 | GREEN 유지 | 모든 PR/커밋 전 기존 테스트 전체 통과 필수. |
| RG-04 | 리팩토링 보호 | 리팩토링 시 테스트를 먼저 통과시킨 상태에서만 내부 구현 변경. |

### 변경 금지 계약

| 변경 금지 항목 | 이유 |
|---|---|
| 출력 배열 포맷 `int[6]` 및 순서 `[r1,c1,n1,r2,c2,n2]` | 호출자 계약 위반 |
| 좌표 1-index 기준 | INV-08, 모든 테스트 좌표 기준 |
| 에러 메시지 문구 (2.4 표 고정) | UI 계약 위반 |
| Magic Constant = 34 | 수학적 불변 |
| 빈칸 개수 = 정확히 2 | 입력 계약 |
| 숫자 배치 우선순위 규칙 (smaller→첫빈칸 우선) | 출력 결정론 보장 |

---

## 4.4 커버리지 목표

| 레이어 | 커버리지 목표 | 측정 대상 | 미달 시 조치 |
|---|---|---|---|
| Domain Logic | **95% 이상** | `BlankFinder`, `MissingNumberFinder`, `MagicSquareValidator`, `SolvingStrategy`, VO | 누락 경로 추가 테스트 작성 |
| UI Boundary | **85% 이상** | `InputValidator`, 에러 메시지 분기, 포맷 변환 | 에러 코드별 테스트 추가 |
| Data Layer | **80% 이상** | `MatrixRepository` 구현체, 예외 경로 | 예외 시나리오 보강 |

**커버리지 측정 기준:**
- **라인 커버리지** 기준 (브랜치 커버리지는 보조 지표)
- 커버리지 측정에서 VO의 getter/setter 자동 생성 코드는 제외 가능
- 테스트 코드 자체는 커버리지 대상에서 제외

---

## 4.5 Traceability Matrix (추적 가능성 매트릭스)

| Concept (개념) | Invariant | Rule (규칙) | Use Case | Contract | Test | Component |
|---|---|---|---|---|---|---|
| 격자 크기 | INV-03 | 행=4, 각 행 열=4 | UC-D05 | Input Schema `int[4][4]` | UI-T01, UI-T02, UI-T03, DT-T11, DT-T12, DT-T13 | `InputValidator`, `MatrixRepository` |
| 빈칸 개수 | INV-04 | 0의 개수 = 정확히 2 | UC-D01 | `findBlanks` 계약 | BF-T03, BF-T04, BF-T05, UI-T05, UI-T06, UI-T07 | `BlankFinder`, `InputValidator` |
| 값 범위 | INV-05 | ∈ {0,1,…,16} | UC-D05 | Input Schema 셀 값 | UI-T08, UI-T09, UI-T10, UI-T11 | `InputValidator` |
| 비영 중복 없음 | INV-06 | 0 제외 각 값 1회 | UC-D02 | `findMissing` 전제조건 | MF-T05, UI-T12, UI-T13, UI-T14, UI-T15 | `InputValidator`, `MissingNumberFinder` |
| Magic Constant | INV-01 | 행/열/대각선 합=34 | UC-D03 | `isValid` 반환 조건 | MV-T01~T07, IT-S01, IT-S02 | `MagicSquareValidator` |
| 숫자 집합 완전성 | INV-02 | 1~16 각 1회 | UC-D02 | `findMissing` 반환 계약 | MF-T01~T04 | `MissingNumberFinder` |
| 해 유일성 | INV-07 | 유효 조합 = 1가지 | UC-D04 | `solve` 반환 계약 | SS-T01, SS-T02, SS-T03 | `SolvingStrategy` |
| 출력 좌표 범위 | INV-08 | r,c ∈ {1,2,3,4} | UC-D04, UC-D05 | Output Schema / `SolveResult` | SS-T04, SR-T01~T03, UI-T17 | `SolveResult`, `InputValidator` |
| 출력 숫자 범위 | INV-09 | n ∈ {1,…,16}, n1≠n2 | UC-D04, UC-D05 | Output Schema / `SolveResult` | SR-T04~T06, MF-T02, UI-T16 | `SolveResult`, `MissingNumberFinder` |
| 배치 우선순위 | (규칙) | smaller→첫빈칸 우선 | UC-D04 | `solve` 우선순위 계약 | SS-T01, SS-T02, IT-S01, IT-S02 | `SolvingStrategy` |
| 저장/로드 정합성 | (Data) | 저장 = 로드 | UC-Data | `MatrixRepository` 계약 | DT-T01, DT-T02, DT-T03 | `MatrixRepository` |
| 에러 메시지 표준 | (UI) | 2.4 표 고정 문구 | — | Error Schema | UI-T01~T15 | `InputValidator`, ErrorResponse |

---

## 부록: 예외 계층 정의

| 예외 클래스 | 발생 레이어 | 발생 조건 |
|---|---|---|
| `InvalidGridSizeException` | UI / Data | 격자가 4×4가 아님 |
| `InvalidBlankCountException` | UI / Domain | 빈칸 수 ≠ 2 |
| `InvalidCellValueException` | UI | 셀 값 ∉ {0,1,…,16} |
| `DuplicateValueException` | UI | 비영 중복 값 존재 |
| `IncompleteGridException` | Domain | 완성 판정 시 0 존재 |
| `InvalidMissingCountException` | Domain | 누락 숫자 수 ≠ 2 |
| `NoSolutionException` | Domain | 두 조합 모두 마방진 불성립 |
| `IllegalSolveResultException` | Domain (VO) | SolveResult 범위 위반 |
| `NotFoundException` | Data | 해당 id 없음 |
| `DuplicateIdException` | Data | 동일 id 중복 저장 |
| `InvalidResultException` | Data | int[6] 길이 ≠ 6 |
| `IllegalArgumentException` | Data | null/빈 id |

---

## 부록: 테스트 전체 체크리스트

- [ ] **BF-T01 ~ BF-T06** (BlankFinder — 6개)
- [ ] **MF-T01 ~ MF-T05** (MissingNumberFinder — 5개)
- [ ] **MV-T01 ~ MV-T07** (MagicSquareValidator — 7개)
- [ ] **SS-T01 ~ SS-T05** (SolvingStrategy — 5개)
- [ ] **SR-T01 ~ SR-T06** (SolveResult VO — 6개)
- [ ] **UI-T01 ~ UI-T19** (UI Boundary — 19개)
- [ ] **DT-T01 ~ DT-T13** (Data Layer — 13개)
- [ ] **IT-S01 ~ IT-S04** (통합 정상 — 4개)
- [ ] **IT-F01 ~ IT-F06** (통합 실패 — 6개)

**총 테스트 케이스: 71개**
