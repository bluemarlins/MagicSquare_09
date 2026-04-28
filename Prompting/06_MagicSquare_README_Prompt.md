# TODO 리스트 작성 참고 문서
_Exported on 4/28/2026 at 10:44:57 GMT+9 from Cursor (3.2.11)_

---

**User**

TODO 리스트를 작성하고 싶습니다. 작성한 문서중 무엇을 참조하여 만들어야 할까요 ? 

---

**Cursor**

프로젝트 문서를 확인해 TODO 작성 시 참조할 자료를 정리합니다.



TODO를 만들 때는 **“무엇을 할지”는 PRD·설계**, **“어떻게 할지의 제약”은 `.cursorrules`**, **배경·근거는 Report**를 나누어 쓰는 편이 좋습니다.

## 1순위: `docs/PRD.md`

PRD 자체가 “참조 문서”를 표로 밝히고 있고, TODO의 **작업 단위·완료 조건**을 여기서 뽑는 것이 맞습니다.

- **§2 Epic** — 큰 덩어리(마일스톤) 단위 TODO
- **§3 도메인 불변조건 (INV-01~09)** — 도메인/테스트 항목으로 쪼개기
- **§4 입출력 계약** — Boundary·검증 순서 관련 TODO
- **§6 기능 요구사항 (Dual-Track)** — Track A(UI) / Track B(Logic) 병렬 작업
- **§9 Gherkin (L0~L3)** — 시나리오별 체크리스트·테스트 TODO
- **§10 테스트 계획** — 테스트 개수·종류 정렬
- **§12 성공 기준 (SC-01~ 등)** — “완료” 정의를 TODO 설명에 붙이기
- **§14 Traceability Matrix** — 요구 ↔ 테스트 ↔ 컴포넌트 매핑으로 빠진 항목 찾기

즉, **실제 TODO 문장의 본문은 PRD에서 가져오는 것**을 기준으로 두면 됩니다.

## 2순위: 설계 문서 (`Design/`)

구현 순서·화면/유스케이스 흐름을 TODO에 반영할 때 사용합니다.

- `Design/04_MagicSquare_Epic_UserJourney_Design.md` — 사용자 여정·Epic 단위 작업 순서
- `Design/02_MagicSquare_TDD_CleanArchitecture_Design.md` — 레이어·TDD 단계별 작업

PRD가 “무엇”이면, Design은 **“어떤 순서로 쌓을지”** 보조입니다.

## 코딩·리뷰 기준: `.cursorrules`

TODO에 “MagicSquareSolver에서 검증 금지”처럼 **아키텍처·스타일·금지 사항**을 짧게 붙일 때 참조합니다. 작업 목록의 내용보다는 **각 항목의 제약 메모**용입니다.

## 배경·근거가 필요할 때: `Report/`

PRD 표기대로 **01 문제 정의 · 02 TDD+Clean Architecture · 03 CursorRules · 04 Epic+User Journey**는, TODO를 쓸 때보다 **왜 그 작업이 있는지**를 적고 싶을 때·온보딩용으로 쓰면 됩니다. 일상적인 실행 TODO는 PRD+Design만으로도 충분한 경우가 많습니다.

---

**정리:** 실행 가능한 TODO 리스트의 **주 소스는 `docs/PRD.md`**이고, **순서·흐름은 `Design/04`·`Design/02`**, **구현 시 지켜야 할 규칙 메모는 `.cursorrules`**, **Report**는 필요할 때만 근거용으로 참조하면 됩니다.

---

**User**

당신은 시니어 소프트웨어 아키텍트이자 TDD 코치입니다. 다음 방법론을 적용하여
"Magic Square 4x4 완성 시스템"의 구현용 To-Do 구조를 작성하세요.
적용 방법론:
Concept-to-Code Traceability
Dual-Track UI + Logic TDD
To-Do → Scenario → Test → Code 구조
ECB(Entity / Control / Boundary) 모델
RED → GREEN → REFACTOR
반드시 한국어로 작성하세요.
[시스템 목표]
부분적으로 비어 있는 4x4 Magic Square를 완성하는 시스템의 개발 To-Do를 작성합니다.
[도메인 규칙]
보드는 4x4이다.
숫자는 1~16만 사용한다.
0은 빈칸이다.
정확히 2칸이 비어 있다.
0을 제외한 중복 숫자는 허용되지 않는다.
모든 행, 열, 대각선의 합은 34여야 한다.
해결 가능한 경우 빈칸 값을 찾아 채운다.
유효하지 않은 보드는 거부한다.
[출력 형식]
다음 구조를 반드시 지켜서 작성하세요.
Epic
User Story
Phase별 Task 목록
각 Task에는 반드시 아래 정보를 포함하세요.
Task ID
RED / GREEN / REFACTOR 여부
작업 제목
Scenario Level (L0/L1/L2/L3)
연결되는 Test 이름
연결되는 Code 대상
ECB 스테레오타입 (Entity / Control / Boundary)
필요 시 체크포인트
[표현 스타일]
Markdown 사용
체크박스 형식 사용
실제 Cursor.AI 실습용 개발 보드처럼 작성
식별자는 Epic-001, US-001, TASK-001 형식 사용
유효한 케이스와 실패 케이스를 모두 포함
최소한 다음 작업을 포함
보드 생성
보드 유효성 검사
빈칸 탐지
후보값 필터링
완성 로직
잘못된 입력 처리
테스트 커버리지 체크포인트
[Scenario Level 정의]
L0: 기능 개요
L1: 정상 흐름
L2: 경계 상황
L3: 실패 상황
[추가 제약]
Logic 책임은 명확히 분리할 것
UI/Boundary에는 비즈니스 규칙을 넣지 말 것
Control은 검증과 해결 흐름을 조율할 것
Entity는 보드 상태를 표현할 것
모든 To-Do는 Scenario, Test, Code로 추적 가능해야 함
이제
"Magic Square 4x4 완성 시스템"의 To-Do 구조를 생성하세요.

---

**Cursor**

PRD의 시나리오·테스트·컴포넌트 명명을 확인해 To-Do 구조를 정확히 맞춥니다.



아래는 PRD·ECB·L0~L3 시나리오·테스트 ID 체계와 맞춘 **구현용 To-Do 구조**입니다. Cursor 실습 보드처럼 체크박스로 쓸 수 있게 정리했습니다.

---

# Magic Square 4×4 완성 시스템 — 구현 To-Do 구조

**추적 원칙:** 각 Task는 **Scenario(L0~L3) → Test → Code**로 역추적 가능. Logic(Entity/Control)과 UI/Boundary는 **Dual-Track**으로 분리.

---

## Epic-001 — Invariant 기반 4×4 마방진 두 빈칸 완성 시스템

| 항목 | 내용 |
|------|------|
| 목표 | 부분 채워진 4×4 보드에서 빈칸 2곳을 채워 Magic Constant 34를 만족시키고, `int[6]`(1-index)로 반환 |
| 방법론 | Concept-to-Code Traceability · Dual-Track UI+Logic TDD · ECB · RED→GREEN→REFACTOR |
| 제약 | Boundary/UI에 비즈니스 규칙 금지 · Control은 검증·해결 흐름 조율 · Entity는 보드·규칙 표현 |

---

## US-001 — 도메인 보드 표현 및 초기화 (보드 생성)

> **Concept:** 격자는 4×4, 값은 0(빈칸) 또는 1~16. **Track:** Logic(L0).

### Phase 1-A — 패키지·상수·보드 Entity

- [ ] **TASK-001** | **RED** | 도메인 상수 모듈 로드 검증  
  - **Scenario Level:** L0  
  - **연결 시나리오:** 도메인 상수 초기값 검증 (IT-L0-03)  
  - **연결 Test:** `test_magic_constant_is_34`, `test_grid_size_is_4`, `test_blank_count_is_2` (단위, `tests/entity/`)  
  - **연결 Code:** `magic_square/entity/constants.py` (또는 동등 모듈)  
  - **ECB:** Entity  
  - **체크포인트:** MAGIC_CONSTANT=34, GRID_SIZE=4, BLANK_COUNT=2, VALUE_RANGE 반영

- [ ] **TASK-002** | **GREEN** | `MagicSquare` Entity — 4×4 격자 보유  
  - **Scenario Level:** L0  
  - **연결 시나리오:** MagicSquare 객체 초기화 (IT-L0-01)  
  - **연결 Test:** `test_magic_square_initializes_with_4x4_grid`  
  - **연결 Code:** `magic_square/entity/magic_square.py`  
  - **ECB:** Entity  
  - **체크포인트:** 외부 I/O 없음, 격자 구조만 유지

- [ ] **TASK-003** | **REFACTOR** | Value Object `Cell`, `CellValue` 정리  
  - **Scenario Level:** L0  
  - **연결 시나리오:** (내부) 좌표·값 불변 표현  
  - **연결 Test:** `test_cell_coordinates_1_index`, `test_cell_value_bounds`  
  - **연결 Code:** `magic_square/entity/value_objects/cell.py`, `cell_value.py`  
  - **ECB:** Entity  

---

## US-002 — 보드 유효성 검사 (형식·마방진 합)

> **Concept:** INV-01~06. 검증 순서는 Boundary 4단계 vs Domain 완성 검증으로 분리.

### Phase 1-B — Domain: 완성 격자 검증 (Logic)

- [ ] **TASK-004** | **RED** | 완성 격자 10개 합산 = 34 실패 케이스  
  - **Scenario Level:** L3  
  - **연결 시나리오:** MagicSquareValidator — 행 합 ≠ 34 (MV-T02)  
  - **연결 Test:** `test_validator_rejects_row_sum_not_34`  
  - **연결 Code:** `magic_square/entity/services/magic_square_validator.py`  
  - **ECB:** Entity  
  - **체크포인트:** 0 포함 격자는 `IncompleteGridError` 등 PRD 예외 정책 준수

- [ ] **TASK-005** | **GREEN** | `MagicSquareValidator.is_valid` — 10조건 전부 True  
  - **Scenario Level:** L1  
  - **연결 시나리오:** MV-T01  
  - **연결 Test:** `test_validator_accepts_fully_valid_magic_square` (`MV-T01` 계열)  
  - **연결 Code:** `magic_square_validator.py`  
  - **ECB:** Entity  

- [ ] **TASK-006** | **REFACTOR** | 행/열/대각선 검증 중복 제거  
  - **Scenario Level:** L2  
  - **연결 Test:** `test_validator_column_and_diagonal_edge_cases` (`MV-T03~T07` 매핑)  
  - **연결 Code:** `magic_square_validator.py`  
  - **ECB:** Entity  

---

## US-003 — 빈칸 탐지 (row-major, 정확히 2개)

> **Concept:** INV-04, INV-08. **Track:** Logic.

- [ ] **TASK-007** | **RED** | 빈칸 3개 시 Domain 예외  
  - **Scenario Level:** L3  
  - **연결 시나리오:** BlankFinder — 빈칸 3개 (BF-T03)  
  - **연결 Test:** `test_blank_finder_raises_invalid_blank_count_three`  
  - **연결 Code:** `magic_square/entity/services/blank_finder.py`  
  - **ECB:** Entity  

- [ ] **TASK-008** | **GREEN** | `BlankFinder.find_blanks` → 2개 `Cell`, row-major  
  - **Scenario Level:** L1  
  - **연결 시나리오:** BF-T01  
  - **연결 Test:** `test_blank_finder_returns_two_cells_row_major` (`BF-T01~T02`)  
  - **연결 Code:** `blank_finder.py`  
  - **ECB:** Entity  
  - **체크포인트:** 첫 0 = (r1,c1) 정의와 출력 1-index 일관성

- [ ] **TASK-009** | **REFACTOR** | 빈칸 0·1개 등 부가 실패 테스트 정리 (`BF-T04~T06`)  
  - **Scenario Level:** L2/L3  
  - **연결 Test:** `test_blank_finder_invalid_count_variants`  
  - **연결 Code:** `blank_finder.py`  
  - **ECB:** Entity  

---

## US-004 — 후보값(누락 숫자) 및 배치 필터링

> **Concept:** INV-02, INV-06, INV-09 — 1~16 중 없는 두 수 = 후보 풀.

- [ ] **TASK-010** | **RED** | 누락 2개를 `MissingPair(smaller, larger)`로 반환  
  - **Scenario Level:** L1  
  - **연결 시나리오:** MF-T01  
  - **연결 Test:** `test_missing_number_finder_returns_ordered_pair` (`MF-T01`)  
  - **연결 Code:** `magic_square/entity/services/missing_number_finder.py`, `missing_pair.py`  
  - **ECB:** Entity  

- [ ] **TASK-011** | **GREEN** | 누락 개수 ≠ 2 시 예외 (비정상 보드)  
  - **Scenario Level:** L3  
  - **연결 시나리오:** MF-T02 등  
  - **연결 Test:** `test_missing_number_finder_invalid_missing_count` (`MF-T02~T05`)  
  - **연결 Code:** `missing_number_finder.py`  
  - **ECB:** Entity  
  - **체크포인트:** Logic만 — Boundary의 “빈칸 2개”와 역할 중복 없게

- [ ] **TASK-012** | **REFACTOR** | 극단값 쌍 (1,16) L2 시나리오 반영  
  - **Scenario Level:** L2  
  - **연결 시나리오:** PRD 엣지 — 누락이 1과 16  
  - **연결 Test:** `test_missing_pair_extreme_values`  
  - **연결 Code:** `missing_pair.py`  
  - **ECB:** Entity  

---

## US-005 — 완성 로직 (시도 A→B, 결정론적 `int[6]`)

> **Concept:** INV-01, INV-07, INV-09. **Track:** Logic.

- [ ] **TASK-013** | **RED** | 시도 A/B 후 `SolveResult` 또는 `NoSolutionError`  
  - **Scenario Level:** L3  
  - **연결 시나리오:** SS-T03  
  - **연결 Test:** `test_solving_strategy_raises_no_solution_when_both_fail` (`SS-T03`)  
  - **연결 Code:** `magic_square/entity/services/solving_strategy.py`, `solve_result.py`  
  - **ECB:** Entity  

- [ ] **TASK-014** | **GREEN** | 조합 A 성공 시 n1 < n2, 조합 B 성공 시 n1 > n2  
  - **Scenario Level:** L1  
  - **연결 시나리오:** IT-S01, IT-S02  
  - **연결 Test:** `test_strategy_combination_a`, `test_strategy_combination_b` (`SS-T01~T02`)  
  - **연결 Code:** `solving_strategy.py`  
  - **ECB:** Entity  

- [ ] **TASK-015** | **REFACTOR** | `SolveResult` → `int[6]` 1-index 포맷 (`SR-T01~T06`)  
  - **Scenario Level:** L1  
  - **연결 Test:** `test_solve_result_to_int_six_tuple`  
  - **연결 Code:** `solve_result.py`  
  - **ECB:** Entity  

---

## US-006 — Control: 검증 위임 없이 흐름만 조율

> **Concept:** BlankFinder → MissingNumberFinder → SolvingStrategy 순서. 검증은 Boundary.

- [ ] **TASK-016** | **RED** | 유효 격자 입력 시 E2E와 동일한 `int[6]` (단위에서는 Mock 없이 진짜 조합)  
  - **Scenario Level:** L1  
  - **연결 시나리오:** IT-S01 (통합 전 Control 단독 호출 변형)  
  - **연결 Test:** `test_magic_square_solver_happy_path_combination_a`  
  - **연결 Code:** `magic_square/control/magic_square_solver.py`  
  - **ECB:** Control  
  - **체크포인트:** Control이 `InputValidator`를 호출하지 않음

- [ ] **TASK-017** | **GREEN** | Domain 예외를 변환하지 않고 전파  
  - **Scenario Level:** L3  
  - **연결 시나리오:** NoSolutionError 경로  
  - **연결 Test:** `test_magic_square_solver_propagates_no_solution`  
  - **연결 Code:** `magic_square_solver.py`  
  - **ECB:** Control  

- [ ] **TASK-018** | **REFACTOR** | `SolvingStrategy` 주입 가능 구조 (테스트 용이성)  
  - **Scenario Level:** L2  
  - **연결 Test:** `test_solver_with_injected_strategy`  
  - **연결 Code:** `magic_square_solver.py`  
  - **ECB:** Control  

---

## US-007 — Boundary: 잘못된 입력 처리 (4단계, 첫 실패만)

> **Concept:** INV-03~06. **Track:** UI/API Contract + Logic 규칙의 경계.

- [ ] **TASK-019** | **RED** | `None` → `INVALID_INPUT` (IT-F01 변형)  
  - **Scenario Level:** L3  
  - **연결 시나리오:** None 입력  
  - **연결 Test:** `test_input_validator_rejects_none` (`UI-T01` 계열)  
  - **연결 Code:** `magic_square/boundary/input_validator.py`  
  - **ECB:** Boundary  
  - **체크포인트:** 마방진 합·빈칸 개수 등 **비즈니스 규칙 미포함** — 형식/순서만

- [ ] **TASK-020** | **GREEN** | 크기 → 값 범위 → 빈칸 수 → 중복 순서 (`UI-T02~T08`)  
  - **Scenario Level:** L3  
  - **연결 시나리오:** IT-F01~F04, 복합 순서 IT-F06류  
  - **연결 Test:** `test_validation_order_grid_size_first`, `test_validation_stops_at_first_failure`  
  - **연결 Code:** `input_validator.py`  
  - **ECB:** Boundary  

- [ ] **TASK-021** | **GREEN** | `ResponseFormatter` — Domain 예외 → `ErrorResponse` + 고정 errorCode  
  - **Scenario Level:** L3  
  - **연결 시나리오:** IT-F01~F05 UX Contract  
  - **연결 Test:** `test_response_formatter_maps_no_solution`, `test_maps_duplicate_value` (`UI-T09~T19` 매핑)  
  - **연결 Code:** `magic_square/boundary/response_formatter.py`  
  - **ECB:** Boundary  

- [ ] **TASK-022** | **REFACTOR** | `MagicSquareController` — validate → solve → format 성공/실패 단일 진입점  
  - **Scenario Level:** L1/L3  
  - **연결 시나리오:** IT-S01, IT-F01  
  - **연결 Test:** `test_controller_success_payload_has_result_key`, `test_controller_error_payload_has_error_code`  
  - **연결 Code:** `magic_square/boundary/magic_square_controller.py`  
  - **ECB:** Boundary  
  - **체크포인트:** Boundary가 Repository 직접 호출 금지 — Facade 경유만

---

## US-008 — Dual-Track 통합 및 Data (선택 심화)

> **Track A (UI):** 응답 JSON 키 `result` / `errorCode`. **Track B (Logic):** IT-S*, IT-F*, 도메인 단위 테스트.

- [ ] **TASK-023** | **RED** | 통합: 조합 A/B·같은 행 빈칸 (IT-S01~S03)  
  - **Scenario Level:** L1 / L2  
  - **연결 시나리오:** IT-S01, IT-S02, IT-S03  
  - **연결 Test:** `test_integration_solve_combination_a`, `test_integration_same_row_blanks` (`tests/integration/`)  
  - **연결 Code:** 전 스택 + 테스트 픽스처  
  - **ECB:** Boundary + Control + Entity  

- [ ] **TASK-024** | **GREEN** | 통합: 모든 L3 실패 코드 (IT-F01~F05, 복합 순서)  
  - **Scenario Level:** L3  
  - **연결 시나리오:** Scenario Group 2·3  
  - **연결 Test:** `test_integration_invalid_grid_size`, `test_integration_no_solution`, … (`IT-F01~F06`)  
  - **연결 Code:** `magic_square_controller.py`, `input_validator.py`  
  - **ECB:** Boundary (주), Entity 예외 소스  

- [ ] **TASK-025** | **GREEN** | InMemoryRepository + 재솔빙 동일 결과 (IT-S04, DT-T*)  
  - **Scenario Level:** L2  
  - **연결 시나리오:** IT-S04  
  - **연결 Test:** `test_save_load_solve_idempotent`  
  - **연결 Code:** `magic_square/data/in_memory_repository.py`, Facade  
  - **ECB:** Data + Boundary(Facade)  

- [ ] **TASK-026** | **REFACTOR** | L2 엣지 — 동일 열·대각선 빈칸, 저장소 없이 순수 Solver만으로도 재현 가능한 단위 분리  
  - **Scenario Level:** L2  
  - **연결 시나리오:** Scenario Group 5  
  - **연결 Test:** `test_integration_same_column_blanks`, `test_integration_diagonal_blanks`  
  - **연결 Code:** 통합 테스트만 또는 경량 Fixture  
  - **ECB:** 통합  

---

## US-009 — 테스트 커버리지·품질 체크포인트 (마감 Definition of Done)

- [ ] **TASK-027** | **GREEN** (측정) | **테스트 커버리지 체크포인트 1 — Traceability**  
  - **Scenario Level:** L0~L3 전 범위  
  - **연결 시나리오:** §14 Traceability Matrix와 1:1 대조  
  - **연결 Test:** 체크리스트: INV-01~09 각각 ≥1 테스트, 에러 코드 7종 전부  
  - **연결 Code:** `docs/PRD.md` §14, `tests/**`  
  - **ECB:** 전 레이어  
  - **체크포인트:** BF/MF/MV/SS/SR/UI/IT/DT ID 누락 없음

- [ ] **TASK-028** | **GREEN** | **테스트 커버리지 체크포인트 2 — 수량·상태**  
  - **Scenario Level:** —  
  - **연결 시나리오:** PRD SC (테스트 71 GREEN 등)  
  - **연결 Test:** `pytest` 전체 GREEN, 실패 시 스킵 0  
  - **연결 Code:** CI 또는 로컬 `pytest`  
  - **ECB:** —  

- [ ] **TASK-029** | **REFACTOR** | **테스트 커버리지 체크포인트 3 — ECB 위반 스캔**  
  - **Scenario Level:** —  
  - **연결 시나리오:** 아키텍처 금지 의존성  
  - **연결 Test:** (선택) import-linter / 수동 리뷰 체크리스트  
  - **연결 Code:** `.cursorrules` architecture 섹션  
  - **ECB:** 전 레이어  
  - **체크포인트:** Entity에 Boundary import 없음, Control에 입력 검증 로직 없음

- [ ] **TASK-030** | **GREEN** | **Dual-Track 동기화** — 각 IT 시나리오에 UX Contract 단언 1개 이상 (Track A)  
  - **Scenario Level:** L1~L3  
  - **연결 시나리오:** PRD §6 Dual-Track 매핑 표  
  - **연결 Test:** Boundary/통합 테스트의 응답 스키마 단언  
  - **연결 Code:** `tests/boundary/`, `tests/integration/`  
  - **ECB:** Boundary  

---

## 요약: 최소 작업 묶음 ↔ 본 To-Do 매핑

| 요청 최소 항목 | 대표 Task ID |
|----------------|--------------|
| 보드 생성 | TASK-001~003 |
| 보드 유효성 검사 | TASK-004~006 (Domain), TASK-019~020 (Boundary 형식) |
| 빈칸 탐지 | TASK-007~009 |
| 후보값 필터링 | TASK-010~012 |
| 완성 로직 | TASK-013~015, TASK-016~018 |
| 잘못된 입력 처리 | TASK-019~022, TASK-024 |
| 테스트 커버리지 체크포인트 | TASK-027~030 |

---

## Concept-to-Code 한 줄 추적 예시

| Concept (불변/규칙) | Scenario L | Test | Code |
|---------------------|------------|------|------|
| 빈칸 정확히 2개 (INV-04) | L3 | BF-T03, IT-F02 | `BlankFinder`, `InputValidator` |
| 첫 검증 실패만 반환 | L3 | UI 복합, IT-F06 | `InputValidator` |
| 해 없음 (INV-07) | L3 | IT-F05, SS-T03 | `SolvingStrategy`, `ResponseFormatter` |

이 보드를 그대로 이슈/PR 단위로 쪼개려면 **Phase 순서대로** (Entity 핵심 → Control → Boundary → Integration → 커버리지) 진행하면 RED→GREEN이 자연스럽게 쌓입니다.

---

**User**

이 분석 내용을 토대로 To-Do 리스트를 포함한 MagicSquare를 만들기 위한 `docs/README.md` 파일을 만들어줘.

---

**Cursor**

프로젝트 상태를 확인한 뒤 `docs/README.md`를 작성합니다.



코드 패키지는 아직 없습니다. 문서와 이전 분석을 반영해 `docs/README.md`를 작성합니다.



`docs/`에 `README.md` 작성 중입니다.



`c:\DEV\MagicSquare_09\docs\README.md`를 추가했습니다.

## 포함 내용

1. **프로젝트 소개** — 목적, Python 3.10+, PRD·`.cursorrules` 링크  
2. **참고 문서 표** — PRD, Design 02/04, Report  
3. **도메인 규칙 요약** — 4×4, 0·빈칸 2개, 합 34, `int[6]` 등  
4. **ECB 개요** — 레이어별 책임·금지 사항 한눈에  
5. **개발 환경** — 패키지가 생긴 뒤 쓸 **예상** 명령(`venv`, `pytest`, `black`)  
6. **방법론** — Concept-to-Code, Dual-Track, RED→GREEN→REFACTOR, L0~L3 표  
7. **Epic-001** + **User Story US-001~009** 표  
8. **구현 To-Do** — 이전에 정리한 **TASK-001~030**을 US별로 체크박스·RED/GREEN/REFACTOR·L 레벨·Test·Code·ECB·체크포인트 형태로 재구성  
9. **Concept → Test → Code** 요약 표  

코드·`pyproject.toml`이 아직 없어 실행 명령은 “구현 후 조정” 안내로 두었고, 상세 계약은 항상 PRD를 따르도록 마지막에 명시해 두었습니다.

---

**User**

ReadMe 생성에 대한 보고서 @Report/ 에 작성해줘

---

**Cursor**

기존 Report 문서 형식을 확인한 뒤 보고서를 작성합니다.



보고서 05와 동일한 톤·구조로 `Report/06_MagicSquare_README_Report.md` 작성합니다.



`Report/06_MagicSquare_README_Report.md`를 추가했습니다.

## 보고서 요약

| 섹션 | 내용 |
|------|------|
| **메타** | 산출물 `docs/README.md`(약 194줄), 작성일 2026-04-28 |
| **§1** | README가 없던 상황, 온보딩·To-Do·추적·PRD 우선 역할 |
| **§2** | 참조: PRD, `.cursorrules`, 대화 기반 To-Do / Design·Report는 링크 위주 |
| **§3** | README 섹션별 역할 표 |
| **§4** | Epic/US/Task 식별자, 한 줄 압축 이유, 테스트·경로 명명 원칙 |
| **§5** | PRD ECB·Dual-Track·Traceability와의 대응 |
| **§6** | pyproject 미반영, 배지·영문 README 미포함 등 의도적 제약 |
| **§7** | README·PRD·Report 05 링크 |
| **§8** | 결론 및 다음 단계(패키지 추가 후 개발 환경 절 갱신, TASK-027) |

형식은 `Report/05_MagicSquare_PRD_Report.md`와 같이 표·목차·섹션 번호를 맞춰 두었습니다. `docs/README.md`의 “Report/01~05” 안내를 06까지 포함하도록 바꾸고 싶으면 알려 주세요.

