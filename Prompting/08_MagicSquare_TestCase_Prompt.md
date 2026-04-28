# Git branch strategy guidance
_Exported on 4/28/2026 at 13:43:30 GMT+9 from Cursor (3.2.11)_

---

**User**

@README.md 을 참조하여 작업을 하려는데, 깃 브랜치 전략을 어떻게 하면 좋을지 알려줘 

---

**Cursor**

README.md를 전체적으로 분석했습니다. 프로젝트 구조(ECB + Dual-Track TDD + 30 TASK / 9 US)에 최적화된 Git 브랜치 전략을 제안합니다.

---

## 추천 Git 브랜치 전략

### 브랜치 계층 구조

```
main
  └── develop
        ├── track-b/us-001-domain-init        ← Entity (TASK-001~003)
        ├── track-b/us-002-validator           ← Entity (TASK-004~006)
        ├── track-b/us-003-blank-finder        ← Entity (TASK-007~009)
        ├── track-b/us-004-missing-number      ← Entity (TASK-010~012)
        ├── track-b/us-005-solving-logic       ← Entity (TASK-013~015)
        ├── track-a/us-007-boundary            ← Boundary (TASK-019~022)
        ├── feat/us-006-control-solver         ← Control (TASK-016~018)
        ├── feat/us-008-integration-data       ← 통합+Data (TASK-023~026)
        └── feat/us-009-quality-gate           ← 품질 게이트 (TASK-027~030)
```

---

### 브랜치 설명

| 브랜치 | 역할 | 병합 조건 |
|--------|------|-----------|
| `main` | 최종 릴리즈 — SC-07 (74개 전체 GREEN) | `develop` → `main` PR, 74개 GREEN 확인 후 |
| `develop` | 통합 브랜치 — US 단위 병합 | 각 US 브랜치 완료 후 PR |
| `track-b/us-XXX-*` | **Track B** — 순수 Domain 로직 (Entity 레이어) | 해당 US의 모든 TASK RED→GREEN→REFACTOR 완료 |
| `track-a/us-007-boundary` | **Track A** — UI Boundary (Mock 기반 격리) | UI-T01~T19 전체 GREEN |
| `feat/us-006-*` | Control 레이어 — Solver 조율 | SV-T01~T03 GREEN |
| `feat/us-008-*` | 통합 + Data Layer | IT-S01~S04, DT-T01~T13 GREEN |
| `feat/us-009-*` | 커버리지·ECB 점검·품질 게이트 | SC-01~SC-09 전체 충족 |

---

### 커밋 컨벤션 (TDD 단계 반영)

```
[RED]    test: BF-T03 InvalidBlankCountError 실패 확인
[GREEN]  feat: blank_finder 빈칸 개수 검증 최소 구현
[REFACT] refactor: 예외 메시지 상수화 · 타입힌트 추가
```

TDD 단계 태그를 커밋 앞에 명시하면 `git log`에서 RED→GREEN→REFACTOR 흐름을 바로 추적할 수 있습니다.

---

### 작업 순서 및 의존성 (ECB 레이어 순서 준수)

```
1단계 (병렬 가능)
  track-b/us-001  →  track-b/us-002  →  track-b/us-003
  track-b/us-004  →  track-b/us-005
  track-a/us-007  ← Domain을 Mock으로 격리하므로 병렬 진행 가능

2단계 (Entity 완료 후)
  feat/us-006-control-solver  ← Track B US-001~005 develop 병합 후 진행

3단계 (Control 완료 후)
  feat/us-008-integration-data  ← 전 스택 연결

4단계 (통합 완료 후)
  feat/us-009-quality-gate  ← pytest 74개 GREEN + ECB 점검
```

> **Track A(Boundary)는 Domain을 Mock으로 격리**하므로, Track B와 병렬로 브랜치를 열어 독립 진행할 수 있습니다. README의 Dual-Track TDD 설계 의도와 정확히 일치합니다.

---

### 브랜치 생성 명령 (시작 시)

```bash
git checkout -b develop
git checkout -b track-b/us-001-domain-init develop
git checkout -b track-a/us-007-boundary develop   # 병렬 시작 가능
```

---

### 요약

- `track-b/*` — Entity 순수 로직 (외부 의존 없음, 독립 진행)
- `track-a/*` — Boundary, Mock 기반 격리 (**Track B와 병렬 가능**)
- `feat/*` — Control, 통합, 품질 게이트 (레이어 의존 순서 준수)
- 각 US 브랜치는 TASK 단위 RED→GREEN→REFACTOR 커밋 흐름 유지
- `develop` 병합 기준: 해당 US 체크포인트/Validate 조건 통과
- `main` 병합 기준: TASK-028 (`pytest` 74개 전체 GREEN) + SC-01~SC-09 충족

---

**User**

red/green/refactor를 분리하여 branch로 관리하려고 해 우선 red branch를 생성해줘 

---

**Cursor**

현재 `main` 브랜치만 있는 초기 상태입니다. 앞서 논의한 전략대로 `develop`을 먼저 만들고, 첫 작업인 US-001의 RED 브랜치를 생성합니다.

브랜치 생성이 완료됐습니다. 현재 상태는 아래와 같습니다.

---

### 현재 브랜치 구조

```
main
  └── develop
        └── red/us-001-domain-init  ← 현재 위치 (*)
```

---

### TDD 사이클별 브랜치 흐름 (US-001 기준)

| 단계 | 브랜치 | 작업 내용 | 병합 목적지 |
|------|--------|-----------|-------------|
| **RED** | `red/us-001-domain-init` | TASK-001~003 실패 테스트 작성 | → `green/us-001-domain-init` 생성 기점 |
| **GREEN** | `green/us-001-domain-init` | 최소 구현으로 테스트 통과 | → `refactor/us-001-domain-init` 생성 기점 |
| **REFACTOR** | `refactor/us-001-domain-init` | 타입힌트·독스트링·상수 정리 | → `develop` 병합 |

---

지금 `red/us-001-domain-init` 브랜치에서 다음 작업을 시작하면 됩니다.

**TASK-001-1 `[RED]`** — `tests/entity/test_domain_constants.py` 작성
- `MAGIC_CONSTANT`, `GRID_SIZE`, `BLANK_COUNT` 임포트 실패(`ImportError`) 확인

테스트 파일을 바로 작성할까요?

---

**User**

첨부된 Table은 Test Case List야,  이를 아래의 양식에 맞춰 작성해줘 

테스트 케이스	프로젝트명	
	대상 시스템	
단계		작성자		승인자		문서 상태	
작성일		버전		테스트 범위		테스트 조직	
테스트 ID			테스트 일자	
테스트 목적	
테스트 기능	
입력값	
테스트단계					
					
					
					
					
					
					
					
					
					
					
					
	
테스트환경	
전제 조건	
성공 /실패 기준	
특별하게 필요한 절차	




---

**Cursor**

이미지에서 테스트 케이스를 분석하고 문서를 작성하겠습니다.

`Report/08_MagicSquare_TestCase_Document.md` (44KB) 파일이 생성됐습니다.

---

## 작성 결과 요약

이미지에서 추출한 **총 24개 테스트 케이스**를 모두 양식에 맞춰 작성했습니다.

### 구성

| 그룹 | 기능 | 건수 |
|------|------|:----:|
| A | 빈칸 찾기 (`find_blank_coords`) | 5 |
| B | 마방진 검증 (`is_magic_square`) | 5 |
| C | 솔루션 / 경계값 (`solution()`) | 8 |
| D | 오류 예외 (Error Cases) | 6 |
| **합계** | | **24** |

### 각 테스트 케이스에 포함된 항목

- 테스트 케이스 ID / 프로젝트명 / 대상 시스템
- 단계 / 작성자 / 승인자 / 문서 상태
- 작성일 / 버전 / 테스트 범위 / 테스트 조직
- 테스트 목적 / 테스트 기능 / 입력값 (Python 코드)
- **테스트 단계 표** (순번 · Given/When/Then · 예상결과 · 실제결과 · 합격여부)
- 테스트 환경 / 전제 조건 / 성공·실패 기준 / 특별 절차

---

> 이미지 해상도 한계로 일부 입력 매트릭스 세부값은 프로젝트 도메인(뒤러 4×4 마방진)을 기반으로 재구성했습니다. 수정이 필요한 값이 있으면 알려주세요.

---

**User**

@Report/08_MagicSquare_TestCase_Document.md 는 보고서라기 보다 Test Case 문서야 @docs/ 로 이동 시키고 파일 이름도 역할에 맞게 변경해줘

---

**Cursor**

완료됐습니다.

- **이동 전:** `Report/08_MagicSquare_TestCase_Document.md`
- **이동 후:** `docs/TestCases.md`

`docs/` 폴더에는 이제 PRD와 나란히 테스트 케이스 문서가 위치합니다.

```
docs/
├── PRD.md          ← 요구사항 / 불변조건 / Gherkin 시나리오
└── TestCases.md    ← 테스트 케이스 문서 (24개)
```

README.md의 `## 11. 참고 문서` 섹션에 `TestCases.md` 링크도 추가할까요?

---

**User**

작업내용을 https://github.com/bluemarlins/MagicSquare_09 에 push 해줘 

---

**Cursor**

현재 상태를 파악했습니다. `red` 브랜치에 `docs/TestCases.md`가 미커밋 상태입니다. 커밋 후 모든 브랜치를 push하겠습니다.

모든 push가 완료됐습니다.

---

### Push 결과

| 브랜치 | 상태 | GitHub |
|--------|------|--------|
| `main` | 이미 최신 (up-to-date) | ✅ |
| `develop` | 신규 push 완료 | ✅ |
| `red` | 신규 push 완료 (TestCases.md 포함) | ✅ |

### 최신 커밋

```
053d228  docs: add TestCases.md with 24 test cases   ← red 브랜치
07fb692  docs: extend PRD and add pre-implementation  ← main / develop
```

GitHub 저장소: [https://github.com/bluemarlins/MagicSquare_09](https://github.com/bluemarlins/MagicSquare_09)

---

**User**

@Report/ 에 보고서로 내보내줘 

---

**Cursor**

기존 보고서 형식을 파악하겠습니다.

기존 보고서 형식(헤더 메타, 목차, 섹션 구조)에 맞게 테스트 케이스 작성 결과를 보고서로 내보내겠습니다.

`Report/08_MagicSquare_TestCase_Report.md` (13KB) 생성이 완료됐습니다.

---

### 보고서 구성 (11개 섹션)

| 섹션 | 내용 |
|------|------|
| 1. 작성 배경 및 목적 | TDD RED 단계 진입을 위한 TC 선행 정의 필요성 |
| 2. 설계 원칙 | TC ID 체계, 시나리오 레벨, BDD 구조, 입력 기준 행렬 |
| 3. 그룹별 현황 | A·B·C·D 그룹 24개 TC 집계 (L1/L2/L3 분류) |
| 4~7. 그룹별 상세 | 각 TC 목록, 설계 포인트, 입력 조건, 예상 결과 |
| 8. REQ-TC Traceability | INV-01~09 ↔ TC 연결 (REQ-006 갭 식별) |
| 9. ECB 레이어 커버리지 | Entity(18)/Boundary(6) — Control·Data·통합 미작성 현황 |
| 10. 미정의 항목 | D-007(DUPLICATE_VALUE) 등 후속 과제 |
| 11. 종합 결론 | 완료 사항, 핵심 설계 결정, 다음 단계 |

### 파일 구조 정리

```
docs/
├── PRD.md             ← 요구사항 원본
└── TestCases.md       ← TC 상세 명세 (24개)

Report/
├── 01~07_...
└── 08_MagicSquare_TestCase_Report.md   ← 새 보고서
```

