# 4×4 Magic Square — 테스트 케이스 정의 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square — 두 빈칸 완성 시스템 |
| **보고서 유형** | 테스트 케이스 정의 및 구조 설계 보고서 |
| **작성일** | 2026-04-28 |
| **분석 대상** | `docs/TestCases.md` · `docs/PRD.md` · `README.md` |
| **목적** | PRD Gherkin 시나리오 및 README RTM 기반으로 24개 테스트 케이스를 정의하고 문서화 |
| **산출물** | `docs/TestCases.md` (v1.0) — 24개 TC, 4개 그룹 |

---

## 목차

1. [작성 배경 및 목적](#1-작성-배경-및-목적)
2. [테스트 케이스 설계 원칙](#2-테스트-케이스-설계-원칙)
3. [그룹별 테스트 케이스 현황](#3-그룹별-테스트-케이스-현황)
4. [TC 그룹 A — 빈칸 찾기](#4-tc-그룹-a--빈칸-찾기)
5. [TC 그룹 B — 마방진 검증](#5-tc-그룹-b--마방진-검증)
6. [TC 그룹 C — 솔루션 / 경계값](#6-tc-그룹-c--솔루션--경계값)
7. [TC 그룹 D — 오류 예외](#7-tc-그룹-d--오류-예외)
8. [REQ-TC Traceability](#8-req-tc-traceability)
9. [ECB 레이어별 커버리지 분석](#9-ecb-레이어별-커버리지-분석)
10. [미정의 항목 및 후속 과제](#10-미정의-항목-및-후속-과제)
11. [종합 결론](#11-종합-결론)

---

## 1. 작성 배경 및 목적

### 1.1 배경

README §5.2 Requirements Traceability Matrix(RTM)와 `docs/PRD.md` Gherkin 시나리오(L0~L3)를 기반으로 코드 구현 전 테스트 케이스를 선행 정의한다. TDD Red→Green→Refactor 사이클에서 **[RED] 단계 진입 조건**은 실패 테스트가 먼저 존재해야 한다는 것이며, 이를 위해 구현 전 TC 문서가 필요하다.

### 1.2 목적

| 목적 | 상세 |
|------|------|
| **명세 선행** | 구현 이전에 입출력 계약과 예외 조건을 테스트 형식으로 고정 |
| **추적성 확보** | INV-01~INV-09 → REQ-001~REQ-009 → TC ID 수직 연결 |
| **품질 게이트 준비** | SC-07(74개 GREEN) 달성을 위한 기준선 수립 |
| **Dual-Track TDD 지원** | Track A(Boundary)·Track B(Entity) 병렬 작업 가능하도록 TC 분리 |

---

## 2. 테스트 케이스 설계 원칙

### 2.1 TC ID 체계

```
TC-MS-{그룹}-{번호}

그룹:
  A — find_blank_coords   (Entity: BlankFinder)
  B — is_magic_square     (Entity: MagicSquareValidator)
  C — solution / 경계값   (Entity: SolvingStrategy)
  D — 오류·예외           (Boundary: InputValidator)
```

### 2.2 시나리오 레벨 매핑

| Scenario Level | 정의 | 해당 TC |
|:--------------:|------|---------|
| **L0** | 시스템 초기화·사전조건 | — (별도 단위 테스트로 관리) |
| **L1** | 정상 흐름 (Happy Path) | A-001, A-002, B-001, C-001, C-002 |
| **L2** | 경계값·엣지 케이스 | A-003, A-004, C-003, C-004, C-005, C-006, C-008 |
| **L3** | 실패·오류 케이스 | A-005, B-002~B-005, C-007, D-001~D-006 |

### 2.3 테스트 단계 구조

각 TC는 BDD 형식의 Given/When/Then 단계로 구성한다.

```
Given : 사전 상태 및 입력 데이터 준비
When  : 대상 함수 호출
Then  : 반환값·예외 단언 (assert)
```

### 2.4 입력 데이터 기준

모든 유효 입력 행렬은 뒤러(Dürer) 4×4 마방진을 기준으로 일부 셀을 0(빈칸)으로 치환하여 생성한다.

```python
# 기준 행렬 — 뒤러 마방진 (행·열·대각선 합 = 34)
DÜRER = [
    [16,  3,  2, 13],
    [ 5, 10, 11,  8],
    [ 9,  6,  7, 12],
    [ 4, 15, 14,  1],
]
```

---

## 3. 그룹별 테스트 케이스 현황

| 그룹 | 기능 | TC 수 | L1 | L2 | L3 | 대상 레이어 |
|:----:|------|:-----:|:--:|:--:|:--:|------------|
| **A** | `find_blank_coords` — 빈칸 탐지 | 5 | 2 | 2 | 1 | Entity |
| **B** | `is_magic_square` — 마방진 검증 | 5 | 1 | 0 | 4 | Entity |
| **C** | `solution()` — 솔루션·경계값 | 8 | 2 | 4 | 2 | Entity |
| **D** | `InputValidator` — 오류 예외 | 6 | 0 | 0 | 6 | Boundary |
| **합계** | | **24** | **5** | **6** | **13** | |

> **우선순위:** 전체 P2 (구현 전 확정 필요 최소 집합)

---

## 4. TC 그룹 A — 빈칸 찾기

**대상 컴포넌트:** `entity/services/blank_finder.py` — `BlankFinder`  
**관련 불변조건:** INV-04 (빈칸 개수 = 2), INV-08 (출력 좌표 1-index)

| TC ID | 항목 | Level | 입력 조건 | 예상 결과 |
|-------|------|:-----:|-----------|-----------|
| TC-MS-A-001 | 정상 — 빈칸 2개 | L1 | 뒤러 기반, 빈칸 (1,3)(3,3) | `[(1,3),(3,3)]` |
| TC-MS-A-002 | 정상 — 빈칸 위치 다양 | L1 | 뒤러 기반, 빈칸 (0,0)(3,3) | `[(0,0),(3,3)]` |
| TC-MS-A-003 | 빈칸 0개 | L2 | 완성 격자 (빈칸 없음) | `InvalidBlankCountError` |
| TC-MS-A-004 | 빈칸 1개 | L2 | 뒤러 기반, 빈칸 1개 | `InvalidBlankCountError` |
| TC-MS-A-005 | 빈칸 3개 이상 | L3 | 뒤러 기반, 빈칸 3개 | `InvalidBlankCountError` |

**설계 포인트:**
- row-major 순서 보장: `r1 × 4 + c1 < r2 × 4 + c2` 조건을 Then 단계에서 명시적으로 단언
- 경계값 0·1·3개 모두 동일 예외(`InvalidBlankCountError`)로 처리 — 메시지에 현재 개수 포함

---

## 5. TC 그룹 B — 마방진 검증

**대상 컴포넌트:** `entity/services/magic_square_validator.py` — `MagicSquareValidator`  
**관련 불변조건:** INV-01 (Magic Constant = 34)

| TC ID | 항목 | Level | 입력 조건 | 예상 결과 |
|-------|------|:-----:|-----------|-----------|
| TC-MS-B-001 | 완성 마방진 | L1 | 뒤러 완성 격자 | `True` |
| TC-MS-B-002 | 행합 불일치 | L3 | 행 1의 합 = 35 | `False` |
| TC-MS-B-003 | 열합 불일치 | L3 | 열 3의 합 = 35 | `False` |
| TC-MS-B-004 | 주대각선 합 불일치 | L3 | 주대각선 합 = 35 | `False` |
| TC-MS-B-005 | 반대각선 합 불일치 | L3 | 반대각선 합 = 35 | `False` |

**설계 포인트:**
- 10개 합산 조건(행 4 + 열 4 + 대각선 2) 각각을 독립 TC로 분리
- 변형 방법: 뒤러 격자에서 값 1개만 교체(+1)하여 해당 합산 조건만 위반

---

## 6. TC 그룹 C — 솔루션 / 경계값

**대상 컴포넌트:** `entity/services/solving_strategy.py` — `SolvingStrategy`  
**관련 불변조건:** INV-07 (해 유일성), INV-08 (출력 좌표), INV-09 (출력 숫자)

| TC ID | 항목 | Level | 입력 조건 | 예상 결과 |
|-------|------|:-----:|-----------|-----------|
| TC-MS-C-001 | 정상 — 타입 확인 | L1 | 뒤러 빈칸 {1,8} | `list`, 길이 6 |
| TC-MS-C-002 | 정상 — 값 확인 | L1 | 뒤러 빈칸 {1,8} | `[2,4,8,4,4,1]` |
| TC-MS-C-003 | 이미 완성된 격자 ⭐ | L2 | 빈칸 0개 | `InvalidBlankCountError` |
| TC-MS-C-004 | 경계값 MIN=1 ⭐ | L2 | 뒤러 빈칸 {1,8} | 결과에 `n=1` 포함 |
| TC-MS-C-005 | 경계값 MAX=16 ⭐ | L2 | 뒤러 빈칸 {8,16} | 결과에 `n=16` 포함 |
| TC-MS-C-006 | 완성 후 합 = 34 | L2 | 뒤러 빈칸 {1,8} | 10개 합산 조건 = 34 |
| TC-MS-C-007 | 합 불가 NO_SOLUTION | L3 | 해 없는 행렬 | `NoSolutionError` |
| TC-MS-C-008 | 대각선 합 = 34 | L2 | 뒤러 빈칸 {1,8} | 주·반대각선 합 = 34 |

**설계 포인트:**
- C-001(타입) → C-002(값) 순서로 점진적 검증 — TDD [RED] 단계 분리를 반영
- C-004, C-005는 INV-09 경계값: `n ∈ {1,…,16}`의 최솟값·최댓값 케이스
- C-007 NO_SOLUTION 입력: 시도 A·B 모두 실패하는 행렬 사용

```python
# NO_SOLUTION 케이스 — TC-MS-C-007 입력 행렬
matrix = [
    [ 1,  2,  3,  4],
    [ 5,  6,  7,  0],   # 누락: {8, 16}
    [ 9, 10, 11, 12],
    [13, 14, 15,  0],
]
# 시도 A: (1,3)=8  → 행1 합 = 26 ≠ 34 → 실패
# 시도 B: (1,3)=16 → 행1 합 = 34 ✓, 행3 합 = 50 ≠ 34 → 실패
# → NoSolutionError
```

---

## 7. TC 그룹 D — 오류 예외

**대상 컴포넌트:** `boundary/input_validator.py` — `InputValidator`  
**관련 불변조건:** INV-03~INV-06 (4단계 검증 순서)

| TC ID | 항목 | Level | 입력 조건 | 예상 결과 | 검증 단계 |
|-------|------|:-----:|-----------|-----------|:---------:|
| TC-MS-D-001 | 셀 값 17 초과 | L3 | 셀 값 17 포함 | `INVALID_CELL_VALUE` | 2단계 |
| TC-MS-D-002 | 격자 5열 | L3 | 4행 5열 행렬 | `INVALID_GRID_SIZE` | 1단계 |
| TC-MS-D-003 | 3×3 격자 | L3 | 3×3 행렬 | `INVALID_GRID_SIZE` | 1단계 |
| TC-MS-D-004 | None 입력 | L3 | `matrix = None` | `INVALID_INPUT` | 0단계 |
| TC-MS-D-005 | 문자열 포함 | L3 | 셀 값 `"A"` | `TypeError` / `INVALID_CELL_VALUE` | 2단계 |
| TC-MS-D-006 | 불균형 행렬 | L3 | 행별 열 수 상이 | `INVALID_GRID_SIZE` | 1단계 |

**설계 포인트:**
- **검증 순서 우선순위** 반드시 준수 (README §2.2):

```
0단계: None 검증      → INVALID_INPUT
1단계: 격자 크기 검증 → INVALID_GRID_SIZE
2단계: 셀 값 범위 검증 → INVALID_CELL_VALUE
3단계: 빈칸(0) 수 검증 → INVALID_BLANK_COUNT
4단계: 비영 중복 검증  → DUPLICATE_VALUE
```

- D-004(`None`)는 다른 검증 이전에 처리 — `INVALID_INPUT` 메시지 문구 `"입력 행렬이 null입니다."` 정확히 일치 필요

---

## 8. REQ-TC Traceability

| REQ ID | Invariant | 관련 TC | 커버 여부 |
|--------|-----------|---------|:---------:|
| REQ-001 | INV-01 — Magic Constant = 34 | B-001~005, C-006, C-007, C-008 | ✅ |
| REQ-002 | INV-02 — 숫자 집합 완전성 | C-001~005 (누락 숫자 계산 경로) | ✅ |
| REQ-003 | INV-03 — 격자 크기 4×4 | D-002, D-003, D-006 | ✅ |
| REQ-004 | INV-04 — 빈칸 개수 = 2 | A-001~005, C-003 | ✅ |
| REQ-005 | INV-05 — 셀 값 범위 0~16 | D-001, D-005 | ✅ |
| REQ-006 | INV-06 — 비영 중복 없음 | D-004 (None, 타입 검증 경로) | ⚠️ 직접 TC 없음 |
| REQ-007 | INV-07 — 해 유일성 | C-001~008 | ✅ |
| REQ-008 | INV-08 — 출력 좌표 1-index | C-002, C-004, C-005 | ✅ |
| REQ-009 | INV-09 — 출력 숫자 범위 | C-002, C-004, C-005 | ✅ |

> **⚠️ 갭:** REQ-006(INV-06, 비영 중복 검증)에 대한 전용 TC 미정의.  
> → `DUPLICATE_VALUE` 에러코드 TC를 추후 D-007로 추가 권장

---

## 9. ECB 레이어별 커버리지 분석

| 레이어 | 대상 컴포넌트 | TC 수 | 비고 |
|--------|-------------|:-----:|------|
| **Entity** | `BlankFinder`, `MagicSquareValidator`, `SolvingStrategy` | 18 | 그룹 A·B·C |
| **Boundary** | `InputValidator` | 6 | 그룹 D |
| **Control** | `MagicSquareSolver` | 0 | 별도 단위 테스트(SV-T01~T03)로 관리 |
| **Data** | `InMemoryRepository` | 0 | DT-T01~T13으로 관리 |
| **Integration** | 전체 스택 | 0 | IT-S01~S04, IT-F01~F06으로 관리 |

> 이 문서의 24개 TC는 **Entity·Boundary 레이어 단위 테스트**에 집중한다.  
> Control·Data·Integration TC는 README §7 구현 To-Do 리스트의 후속 단계에서 정의한다.

---

## 10. 미정의 항목 및 후속 과제

| 항목 | 유형 | 우선순위 | 조치 |
|------|------|:--------:|------|
| `DUPLICATE_VALUE` 전용 TC (D-007) | 미정의 | P2 | REQ-006 커버 위해 추가 필요 |
| Control Layer TC (SV-T01~T03) | 미작성 | P1 | TASK-016~018 진행 시 작성 |
| Data Layer TC (DT-T01~T13) | 미작성 | P2 | TASK-025 진행 시 작성 |
| Integration TC (IT-S01~S04, IT-F01~F06) | 미작성 | P1 | TASK-023~024 진행 시 작성 |
| `TestCases.md` 작성자·승인자·테스트일자 | 공란 | P3 | 실제 실행 시 기입 |

---

## 11. 종합 결론

### 11.1 완료 사항

| 항목 | 결과 |
|------|------|
| TC 정의 | 24개 (A:5 · B:5 · C:8 · D:6) |
| 문서 경로 | `docs/TestCases.md` (v1.0) |
| 시나리오 레벨 커버 | L1(5개) · L2(6개) · L3(13개) |
| REQ 추적 | REQ-001~009 중 8개 직접 커버 (REQ-006 ⚠️) |
| ECB 레이어 커버 | Entity(18TC) · Boundary(6TC) |

### 11.2 핵심 설계 결정

1. **TC ID 체계** — `TC-MS-{그룹}-{번호}` 형식으로 기능 그룹을 명확히 분리
2. **입력 기준 행렬** — 뒤러 마방진 단일 기준점 사용 → 테스트 간 데이터 일관성 확보
3. **BDD 단계 구조** — Given/When/Then 으로 구현 시 `pytest` 코드로 직접 전환 가능
4. **경계값 별도 명시** — C-003(0개), C-004(MIN=1), C-005(MAX=16)를 ⭐ 표기로 강조

### 11.3 다음 단계

```
현재: docs/TestCases.md 정의 완료 (RED 브랜치)
  ↓
다음: TASK-001-1 [RED] test_domain_constants.py 작성
      → red/us-001-domain-init 브랜치에서 실패 테스트 구현
  ↓
이후: green/us-001-domain-init 브랜치에서 최소 구현 → 통과
  ↓
최종: 74개 전체 GREEN → pytest 커버리지 SC-01~SC-09 충족
```

---

*이 보고서는 `docs/TestCases.md` 작성 결과를 요약하며,  
실제 TC 상세 명세는 [`docs/TestCases.md`](../docs/TestCases.md)를 참조한다.*
