# 4×4 Magic Square — 구현 전 문서 일관성 점검 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square — 두 빈칸 완성 시스템 |
| **보고서 유형** | 구현 시작 전 문서 갭 분석 및 일관성 보정 보고서 |
| **작성일** | 2026-04-28 |
| **분석 대상** | `.cursorrules` · `README.md` · `docs/PRD.md` |
| **목적** | 세 문서 교차 분석으로 구현 전 누락·불일치 항목을 발견하고 수정 적용 |
| **산출물** | `.cursorrules` (v2) · `README.md` (v3) · `docs/PRD.md` (v1.2.0) |

---

## 목차

1. [분석 배경 및 목적](#1-분석-배경-및-목적)
2. [갭 분석 결과 — 14개 항목](#2-갭-분석-결과--14개-항목)
3. [해결 항목 ① SolvingStrategy 레이어 통일](#3-해결-항목--solvingstrategy-레이어-통일)
4. [해결 항목 ② Control 레이어 테스트 추가](#4-해결-항목--control-레이어-테스트-추가)
5. [해결 항목 ④ 도메인 예외 전체 목록 명세화](#5-해결-항목--도메인-예외-전체-목록-명세화)
6. [문서별 변경 요약](#6-문서별-변경-요약)
7. [미해결 항목 — 후속 처리 계획](#7-미해결-항목--후속-처리-계획)
8. [문서 일관성 체크리스트](#8-문서-일관성-체크리스트)
9. [종합 결론](#9-종합-결론)

---

## 1. 분석 배경 및 목적

### 1.1 분석 배경

코드 구현 시작 전 `.cursorrules` · `README.md` · `docs/PRD.md` 세 문서를 교차 분석한 결과, **구조적 모순, 누락 항목, 환경 설정 부재** 세 유형으로 분류되는 14개의 갭이 발견됐다.

구현을 먼저 시작했을 경우 발생하는 예상 피해:

| 갭 유형 | 구현 중 발생했을 문제 |
|---------|---------------------|
| `SolvingStrategy` 레이어 모순 | 파일 생성 시점에 `entity/` vs `control/` 결정 불가 → 레이어 위반 코드 생성 위험 |
| Control 테스트 누락 | `MagicSquareSolver` 단위 테스트가 74개 카운트에 미포함 → 품질 게이트 달성 불가 |
| 예외 목록 미완성 | `IncompleteGridError` 등 구현 중 참조 시 임시 정의 → 일관성 붕괴 |

### 1.2 분석 방법

세 문서를 **동일 키워드로 교차 검색**하여 문서 간 불일치를 탐지하는 방식을 사용했다. 발견된 항목은 우선순위에 따라 3개 카테고리로 분류했다.

---

## 2. 갭 분석 결과 — 14개 항목

### 2.1 카테고리별 분류

| 카테고리 | 항목 수 | 설명 |
|----------|---------|------|
| **구조적 모순** (구현 전 결정 필수) | 3개 | 문서 간 직접 충돌 — 방치 시 레이어 위반 코드 생성 |
| **문서 누락** (구현 중 혼란 유발) | 6개 | 구현 중 참조 시 판단 불가 항목 |
| **환경 설정 부재** | 2개 | `pyproject.toml` / `requirements.txt` 내용 미정의 |
| **보완 권장** | 3개 | 있으면 좋지만 즉시 필수 아님 |

### 2.2 14개 항목 전체 목록

| # | 항목 | 카테고리 | 해결 여부 |
|---|------|----------|-----------|
| ① | `SolvingStrategy` 레이어 위치 불일치 | 구조적 모순 | ✅ 해결 |
| ② | Control 레이어 단위 테스트 디렉터리 미정의 / 71개 카운트 오류 | 구조적 모순 | ✅ 해결 |
| ③ | `entity/constants.py` 파일 구조 미명시 | 문서 누락 | ⬜ 미처리 |
| ④ | 도메인 예외 전체 목록 미완성 | 구조적 모순 | ✅ 해결 |
| ⑤ | `IT-F01` 시나리오 ID 중복 (None 입력 / 크기 오류 동일 ID) | 문서 누락 | ⬜ 미처리 |
| ⑥ | `SS-T04`, `SS-T05` Gherkin 시나리오 미정의 | 문서 누락 | ⬜ 미처리 |
| ⑦ | `conftest.py` 공통 픽스처 내용 미정의 | 문서 누락 | ⬜ 미처리 |
| ⑧ | 응답 스키마 Python 타입 미정의 | 문서 누락 | ✅ ④에서 동시 해결 |
| ⑨ | `IT-F06` INTERNAL_ERROR 시나리오 미정의 | 문서 누락 | ⬜ 미처리 |
| ⑩ | `pyproject.toml` 내용 미정의 | 환경 설정 | ⬜ 미처리 |
| ⑪ | `requirements.txt` 내용 미정의 | 환경 설정 | ⬜ 미처리 |
| ⑫ | `__init__.py` 내보내기(export) 정의 없음 | 보완 권장 | ⬜ 미처리 |
| ⑬ | `MagicSquare` 엔티티의 구체적 역할 미명확 | 보완 권장 | ⬜ 미처리 |
| ⑭ | Git Flow 브랜치 전략 미적용 | 보완 권장 | ⬜ 미처리 |

> **이번 작업 범위:** 구현 시작 불가 수준인 ①②④ 3개 + ④에서 연쇄 해결된 ⑧ = 총 4개 완료.

---

## 3. 해결 항목 ① SolvingStrategy 레이어 통일

### 3.1 문제 상황

| 문서·위치 | 기술 내용 | 레이어 |
|-----------|-----------|--------|
| `.cursorrules` `architecture.control.components` | `["MagicSquareSolver", "SolvingStrategy"]` | Control |
| `.cursorrules` `file_structure` | `entity/services/solving_strategy.py` | Entity |
| `PRD §8.1` 레이어 구조 | Control Layer 하위에 `SolvingStrategy` 표기 | Control |
| `README §3.3` 파일 구조 | `entity/services/solving_strategy.py` | Entity |

동일 컴포넌트가 논리적 레이어(Control)와 물리적 위치(Entity)가 모순되어 있었다.

### 3.2 판단 근거 (Entity 레이어로 확정)

| 근거 | 내용 |
|------|------|
| **테스트 위치** | `tests/entity/test_solving_strategy.py` → SS-T01~T05는 Domain 29개 카운트에 포함 |
| **순수 의존성** | 입력: `Cell[2]`, `MissingPair` (entity VO) / 호출: `MagicSquareValidator` (entity service) / 반환: `SolveResult` (entity VO) — 외부 라이브러리 의존 **0건** |
| **INV-07 성격** | "시도 A → 시도 B" 배치 우선순위는 수학적 도메인 규칙(PRD 부록B 변경 금지 항목) |
| **파일 구조 합의** | `.cursorrules` 파일 구조와 `README §3.3` 모두 `entity/services/`로 일치 |
| **오류의 위치** | 모순은 `.cursorrules` `architecture.control.components` 한 곳에만 존재 |

### 3.3 수정 내용

| 파일 | 수정 전 | 수정 후 |
|------|---------|---------|
| `.cursorrules` `control.components` | `["MagicSquareSolver", "SolvingStrategy"]` | `["MagicSquareSolver"]` |
| `README §3.1` Control Layer 다이어그램 | `MagicSquareSolver · SolvingStrategy` | `MagicSquareSolver` 만 |
| `README §3.1` Entity Layer 다이어그램 | `SolvingStrategy` 언급 없음 | `SolvingStrategy` 명시 추가 |
| `PRD §8.1` Control Layer | `MagicSquareSolver` + `SolvingStrategy` | `MagicSquareSolver` 만 |
| `PRD §8.1` Entity Layer | 없음 | `SolvingStrategy (Domain Service)` 추가 |

> **유지한 부분:** `control.responsibilities`의 `"BlankFinder → MissingNumberFinder → SolvingStrategy 순서 조율"` 문구는 보존. Control이 SolvingStrategy를 **호출**하는 사실은 변하지 않으며, 이는 허용된 의존 방향(Control → Entity)이다.

---

## 4. 해결 항목 ② Control 레이어 테스트 추가

### 4.1 문제 상황

`README §7` TASK-016~018에 `MagicSquareSolver` 단위 테스트 3개가 명시되어 있으나:
- `tests/control/` 디렉터리가 파일 구조에 없음
- 3개 테스트가 기존 71개 카운트 어디에도 포함되지 않음

```
기존 합산: Domain 29 + UI 19 + Data 13 + Integration 10 = 71개
TASK-016 test_solver_happy_path            → 귀속처 없음
TASK-017 test_solver_propagates_no_solution → 귀속처 없음
TASK-018 test_solver_injected_strategy      → 귀속처 없음
```

### 4.2 처리 결정: `tests/control/` 추가 및 카운트 74로 변경

**결정 근거:**

| 근거 | 내용 |
|------|------|
| TASK-016~018 성격 | MagicSquareSolver를 Mock 주입으로 격리하는 Control **단위 테스트** — 통합 테스트(IT)와 목적이 다름 |
| 구조 대칭성 | ECB 4개 레이어 중 Control만 테스트 디렉터리가 없는 구조적 불균형 |
| 커버리지 | Control 레이어 커버리지 목표(≥ 85%) 달성을 위해 전용 테스트 필요 |

### 4.3 신규 테스트 ID 매핑

| 테스트 ID | TASK | 테스트 함수 | Mock 대상 |
|-----------|------|-------------|-----------|
| `SV-T01` | TASK-016 | `test_solver_happy_path` | `SolvingStrategy` (Mock) |
| `SV-T02` | TASK-017 | `test_solver_propagates_no_solution` | `SolvingStrategy` (Mock) |
| `SV-T03` | TASK-018 | `test_solver_injected_strategy` | `SolvingStrategy` (Protocol 주입) |

### 4.4 수정 내용 (변경 위치 전체)

| 파일 | 수정 내용 |
|------|-----------|
| `.cursorrules` `total_test_cases` | `71` → `74` |
| `.cursorrules` `test_distribution` | `Control — MagicSquareSolver: SV-T01~T03 (3개)` 추가 |
| `.cursorrules` 파일 구조 트리 | `tests/control/test_magic_square_solver.py ← SV-T01~T03` 추가 |
| `.cursorrules` `file_structure.layers` | `tests/control/` 추가 |
| `README.md` 상단 메타 테이블 | `71개 목표` → `74개 목표 (Domain 29 · Control 3 · UI 19 · Data 13 · Integration 10)` |
| `README.md` §4.1 Track 구조 | `Control Layer (SV-T01~T03, 3개)` 추가 |
| `README.md` §3.3 파일 구조 | `tests/control/` 추가 |
| `README.md` TASK-028 · SC-07 | `71개` → `74개` |
| `PRD.md` §1.4 측정 가능성 | `71개 GREEN` → `74개 GREEN` |
| `PRD.md` §10.1 테스트 분포 표 | Control 행 추가, 전체 합계 74 |
| `PRD.md` §10.4 Mock 정책 | Control 테스트 Mock 정책 추가 |
| `PRD.md` §12 SC-07 | `71개` → `74개` |
| `PRD.md` §13 In-Scope | `71개` → `74개` |
| `PRD.md` 부록 A Step 4 | `71개` → `74개` |
| `PRD.md` §6.1 Dual-Track 구조도 | `Control Layer (SV-T01~T03, 3개)` 추가 |
| `PRD.md` §8.4 파일 구조 | `tests/control/` 추가 |

---

## 5. 해결 항목 ④ 도메인 예외 전체 목록 명세화

### 5.1 문제 상황

PRD 본문 곳곳에서 5개의 예외 클래스가 참조되고 있었으나, 공식 클래스 정의와 파일 배치가 어디에도 없었다.

| 예외 클래스 | 참조 위치 | 문제 |
|-------------|-----------|------|
| `InvalidBlankCountError` | PRD §6.3, BF-T03 | 클래스 정의 없음 |
| `InvalidMissingCountError` | PRD §6.3, MF-T02~T05 | 클래스 정의 없음 |
| `IncompleteGridError` | PRD §6.3 FR-D03 | 클래스 정의 없음 |
| `NoSolutionError` | 전체 문서 | 언급만 있고 상속 관계 미정의 |
| `DuplicateIdError` | PRD §6.4 FR-R01 | 파일 위치 불명확 |
| `NotFoundError` | PRD §6.4 FR-R01 | 파일 위치 불명확 |

`DuplicateIdError`와 `NotFoundError`는 Data Layer 예외임에도 `domain_exceptions.py`에 넣을지 별도 파일로 분리할지 정의가 없었다.

### 5.2 처리 결정: 레이어별 3파일 구조

```
exceptions/
├── __init__.py
├── domain_exceptions.py   ← 도메인 순수 예외 (Entity 레이어에서 발생)
├── data_exceptions.py     ← Data Layer 전용 예외 (신규 추가)
└── boundary_exceptions.py ← 에러코드 상수 + 응답 스키마 TypedDict
```

**`domain_exceptions.py` — 5개 클래스**

| 클래스 | 상속 | 발생 위치 | 보호 Invariant |
|--------|------|-----------|----------------|
| `MagicSquareError` | `Exception` | — (기반 클래스) | — |
| `NoSolutionError` | `MagicSquareError` | `SolvingStrategy` | INV-07 |
| `InvalidBlankCountError` | `MagicSquareError` | `BlankFinder` | INV-04 |
| `InvalidMissingCountError` | `MagicSquareError` | `MissingNumberFinder` | INV-02 |
| `IncompleteGridError` | `MagicSquareError` | `MagicSquareValidator` | INV-01 |

**`data_exceptions.py` — 3개 클래스 (신규)**

| 클래스 | 상속 | 발생 위치 |
|--------|------|-----------|
| `DataLayerError` | `Exception` | — (기반 클래스) |
| `DuplicateIdError` | `DataLayerError` | `InMemoryRepository.save()` |
| `NotFoundError` | `DataLayerError` | `InMemoryRepository.load()` / `.delete()` |

**`boundary_exceptions.py` — 상수 + TypedDict**

| 이름 | 종류 | 내용 |
|------|------|------|
| `ErrorCode` | `str` 상수 7종 | `INVALID_INPUT`, `INVALID_GRID_SIZE`, `INVALID_CELL_VALUE`, `INVALID_BLANK_COUNT`, `DUPLICATE_VALUE`, `NO_SOLUTION`, `INTERNAL_ERROR` |
| `ErrorResponse` | `TypedDict` | `{"errorCode": str, "message": str}` |
| `SuccessResponse` | `TypedDict` | `{"result": list[int]}` (길이 항상 6) |

**예외 전파 규칙 (신규 명시):**
- Entity → Control: 도메인 예외 그대로 전파 (변환 금지)
- Control → Boundary: 도메인 예외 그대로 전파 (변환 금지)
- Boundary: 도메인 예외를 `ErrorResponse`로 변환, `DataLayerError` 계열은 `INTERNAL_ERROR`로 변환

### 5.3 연쇄 해결: ⑧ 응답 스키마 TypedDict 미정의

`boundary_exceptions.py`에 `SuccessResponse` / `ErrorResponse` TypedDict를 공식 명세함으로써 **⑧번 항목도 동시 해결**됐다.

### 5.4 수정 내용

| 파일 | 수정 내용 |
|------|-----------|
| `.cursorrules` 파일 구조 트리 | `exceptions/` 하위 3파일 + 각 클래스 주석 상세화 |
| `README.md` §3.3 파일 구조 | `data_exceptions.py` 추가, 각 파일별 클래스 목록 명시 |
| `PRD.md` §8.4 파일 구조 | `data_exceptions.py` 추가 |
| `PRD.md` **§6.5 신설** | 예외 클래스 명세 섹션 (변경 금지) — 3파일 × 클래스 표 + 전파 규칙 |
| `PRD.md` 목차 | §6.5~§6.7 순서 재정렬 |

---

## 6. 문서별 변경 요약

### 6.1 `.cursorrules`

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| `architecture.control.components` | `["MagicSquareSolver", "SolvingStrategy"]` | `["MagicSquareSolver"]` |
| `testing.total_test_cases` | `71` | `74` |
| `testing.test_distribution` | 9행 | 10행 (Control 행 추가) |
| `file_structure` 트리 (exceptions) | 2파일 | 3파일 + 클래스 주석 |
| `file_structure` 트리 (tests) | 4개 디렉터리 | 5개 디렉터리 (`control/` 추가) |
| `file_structure.layers` | 6항목 | 11항목 (tests 하위 디렉터리 명시) |

### 6.2 `README.md`

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 상단 메타 테이블 | `71개 목표 (Domain 29 · UI 19 · Data 13 · Integration 10)` | `74개 목표 (Domain 29 · Control 3 · UI 19 · Data 13 · Integration 10)` |
| §3.1 Control Layer 다이어그램 | `MagicSquareSolver · SolvingStrategy` | `MagicSquareSolver` |
| §3.1 Entity Layer 다이어그램 | `SolvingStrategy` 미언급 | `SolvingStrategy` 명시 |
| §3.3 파일 구조 (`exceptions/`) | 2파일 | 3파일 + 클래스 목록 |
| §3.3 파일 구조 (`tests/`) | 4디렉터리 | 5디렉터리 |
| §4.1 Track 구조도 | Control Layer 없음 | `Control Layer (SV-T01~T03, 3개)` 추가 |
| TASK-028 · SC-07 | `71개` | `74개` |

### 6.3 `docs/PRD.md`

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| §1.4 측정 가능성 | `71개 GREEN` | `74개 GREEN` |
| §6.1 Dual-Track 구조도 | Control Layer 없음 | `Control Layer (SV-T01~T03, 3개)` 추가 |
| **§6.5 신설** | 없음 | 예외 클래스 명세 (3파일 × 클래스 표 + 전파 규칙) |
| §6.6 (구 §6.5) | 핵심 유스케이스 흐름 | 번호 재정렬 (내용 유지) |
| §6.7 (구 §6.6) | Dual-Track 언어 체계 | 번호 재정렬 (내용 유지) |
| §8.1 Control Layer | `MagicSquareSolver` + `SolvingStrategy` | `MagicSquareSolver` 만 |
| §8.1 Entity Layer | `SolvingStrategy` 미언급 | `SolvingStrategy (Domain Service)` 추가 |
| §8.4 파일 구조 | `exceptions/` 2파일, `tests/` 4디렉터리 | `exceptions/` 3파일, `tests/` 5디렉터리 |
| §10.1 테스트 분포 | 71개, Control 행 없음 | 74개, Control 행 추가 |
| §10.4 Mock 정책 | UI/Domain/Data 3항목 | Control 항목 추가로 4항목 |
| §12 SC-07 | `71개 GREEN` | `74개 GREEN` |
| §13 In-Scope | `71개 테스트` | `74개 테스트` |
| 부록 A Step 4 | `71개 GREEN` | `74개 GREEN` |

---

## 7. 미해결 항목 — 후속 처리 계획

아래 항목들은 구현을 막지는 않으나, 구현 진행 중 또는 구현 완료 후 처리가 권장된다.

| # | 항목 | 권장 처리 시점 | 영향 범위 |
|---|------|----------------|-----------|
| ③ | `entity/constants.py` 파일 구조 미명시 | TASK-001 착수 전 | `.cursorrules`, `README`, `PRD` 파일 트리 |
| ⑤ | `IT-F01` 시나리오 ID 중복 | 통합 테스트 작성 전 | `PRD §9` Gherkin 시나리오, Traceability Matrix |
| ⑥ | `SS-T04`, `SS-T05` Gherkin 시나리오 미정의 | TASK-014 착수 전 | `PRD §9` Gherkin, `tests/entity/test_solving_strategy.py` |
| ⑦ | `conftest.py` 공통 픽스처 내용 미정의 | 테스트 작성 착수 전 | `tests/conftest.py` |
| ⑨ | `IT-F06` INTERNAL_ERROR 시나리오 미정의 | 통합 테스트 작성 전 | `PRD §9` Gherkin Group 2 |
| ⑩ | `pyproject.toml` 내용 미정의 | 환경 설정 단계 | 프로젝트 루트 |
| ⑪ | `requirements.txt` 내용 미정의 | 환경 설정 단계 | 프로젝트 루트 |
| ⑫ | `__init__.py` 내보내기 정의 없음 | 각 레이어 REFACTOR 단계 | 각 레이어 `__init__.py` |
| ⑬ | `MagicSquare` 엔티티 역할 미명확 | TASK-002 착수 전 | `entity/magic_square.py` |
| ⑭ | Git Flow 브랜치 전략 미적용 | 코드 구현 착수 전 | Git 저장소 |

---

## 8. 문서 일관성 체크리스트

구현 착수 전 최종 확인 기준:

| 체크 항목 | 확인 방법 | 상태 |
|-----------|-----------|------|
| `SolvingStrategy` → `entity/services/` 위치 | 세 문서 모두 Entity 레이어로 표기 | ✅ |
| `tests/control/test_magic_square_solver.py` 파일 구조 반영 | 세 문서 파일 트리 확인 | ✅ |
| 테스트 카운트 74 동기화 | 세 문서 모든 `71` 키워드 제거 확인 | ✅ |
| 도메인 예외 5개 클래스 정의 | `PRD §6.5` 확인 | ✅ |
| Data Layer 예외 3개 클래스 정의 | `PRD §6.5` 확인 | ✅ |
| `SuccessResponse` / `ErrorResponse` TypedDict 정의 | `PRD §6.5` 확인 | ✅ |
| `entity/constants.py` 파일 구조 반영 | 세 문서 파일 트리 확인 | ⬜ |
| `IT-F01` ID 중복 해소 | `PRD §9` 시나리오 ID 확인 | ⬜ |
| `SS-T04`, `SS-T05` 시나리오 정의 | `PRD §9` Gherkin 확인 | ⬜ |
| `pyproject.toml` / `requirements.txt` 작성 | 파일 존재 확인 | ⬜ |

---

## 9. 종합 결론

### 9.1 이번 작업의 의미

문서 작성 단계에서 발생한 모순·누락은 **코드 레벨에서 발견될 경우 수정 비용이 수배로 증가**한다. 이번 분석은 TDD 원칙의 "실패를 먼저 정의한다"는 철학을 문서 수준에서 실천한 사례다.

> "완성의 기준이 먼저 정의되어야 한다" (PRD §1.3 Why 체인)

이 원칙은 코드뿐 아니라 문서에도 적용된다. 구현 전 불일치를 제거하는 것이 곧 첫 번째 RED 단계다.

### 9.2 수정 후 문서 상태

| 문서 | 버전 변화 | 주요 변경 |
|------|-----------|-----------|
| `.cursorrules` | v1 → v2 | SolvingStrategy 위치 수정, 74개 카운트, 예외 구조 3파일 |
| `README.md` | v2 → v3 | SolvingStrategy 다이어그램, Control 테스트 추가, 파일 구조 갱신 |
| `docs/PRD.md` | v1.1.0 → v1.2.0 | §6.5 예외 명세 신설, 테스트 분포 갱신, 파일 구조 갱신 |

### 9.3 다음 단계

1. 나머지 미해결 항목(③⑤⑥⑦⑨~⑭) 처리 또는 구현 중 병행 처리
2. `pyproject.toml` · `requirements.txt` 작성으로 환경 설정
3. TASK-001 (도메인 상수 검증) 부터 TDD 사이클 시작

---

*이 보고서는 구현 시작 전 문서 일관성 점검 작업의 전체 과정을 기록한다.  
변경된 세 문서(`.cursorrules` v2 · `README.md` v3 · `PRD.md` v1.2.0)가 이후 구현의 단일 진실 공급원으로 기능한다.*
