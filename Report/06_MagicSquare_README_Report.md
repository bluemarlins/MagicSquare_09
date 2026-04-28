# 4×4 Magic Square — README 개선 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square — 두 빈칸 완성 시스템 |
| **보고서 유형** | `docs/README.md` 개선 보고서 (v1 → v2) |
| **최초 작성일** | 2026-04-28 |
| **개선 작업일** | 2026-04-28 |
| **단계 범위** | C2C Traceability 슬라이드 기준으로 README 전면 재구성 |
| **목적** | Requirements Traceability Matrix 신설, 체크박스 서브태스크 3단계화, ECB 어노테이션 및 진행 관문 마커 추가 |
| **산출물** | `docs/README.md` (v1 약 194줄 → v2 약 619줄) |

---

## 목차

1. [개선 배경 및 목적](#1-개선-배경-및-목적)
2. [v1 → v2 변경 요약](#2-v1--v2-변경-요약)
3. [개선 항목 상세](#3-개선-항목-상세)
4. [README v2 구성 요약](#4-readme-v2-구성-요약)
5. [C2C Traceability 구조 반영 방식](#5-c2c-traceability-구조-반영-방식)
6. [PRD·ECB·Dual-Track과의 일치성](#6-prdecbdual-track과의-일치성)
7. [의도적으로 남긴 제약·후속 작업](#7-의도적으로-남긴-제약후속-작업)
8. [산출물 및 링크](#8-산출물-및-링크)
9. [종합 결론](#9-종합-결론)

---

## 1. 개선 배경 및 목적

### 1.1 개선 배경

v1 README(194줄)는 저장소 진입점 역할을 하며 PRD·ECB·방법론을 요약했으나, 아래 두 가지 측면에서 **Concept-to-Code Traceability가 불완전**했다.

| 부족한 점 | 현상 |
|-----------|------|
| **TASK 단일 줄 압축** | 각 TASK가 한 줄 요약에 그쳐, RED→GREEN→REFACTOR 3단계 서브태스크가 없었다 |
| **Requirements Traceability Matrix 부재** | Task ID와 Invariant(REQ ID)·Scenario Level·Test ID를 한눈에 볼 수 있는 표가 없었다 |
| **ECB 레이어 어노테이션 미흡** | 각 TASK에서 어느 레이어(Entity/Control/Boundary)에 해당하는지 일관된 표기가 없었다 |
| **진행 관문(Checkpoint/Validate) 부재** | 다음 TASK로 넘어가기 전 반드시 통과해야 할 조건이 명시되지 않았다 |

### 1.2 개선 트리거

8교시 실습 슬라이드의 두 장이 개선 기준을 제시했다.

- **슬라이드 1.3** — 체크박스·단계별 번호 체계와 Requirements Traceability Matrix 병치 구조
- **슬라이드 1.5** — 완성 To-Do 구조 예시: `[RED]·[GREEN]·[REFACTOR]` 서브태스크, `(<<<layer>>>)` 어노테이션, `[Checkpoint]·[Validate]` 마커

### 1.3 개선 목적

| 목적 | 설명 |
|------|------|
| **C2C 수직 추적 완성** | Task → REQ(INV) → Scenario Level → Test ID → Code(ECB Layer) 5단 연결 |
| **구현 진행 관문 명시** | 각 TASK 완료 후 확인해야 할 조건을 `[Checkpoint]`·`[Validate]` 마커로 고정 |
| **TDD 3단계 가시화** | 서브태스크 `-1:[RED]` → `-2:[GREEN]` → `-3:[REFACTOR]` 구조로 단계 위반 방지 |
| **레이어 책임 명시** | `(<<<entity>>>)` · `(<<<control>>>)` · `(<<<boundary>>>)` · `(<<<data>>>)` 어노테이션 통일 |

---

## 2. v1 → v2 변경 요약

| 항목 | v1 (194줄) | v2 (619줄) |
|------|-----------|-----------|
| **문서 길이** | 194줄 | 619줄 |
| **목차** | 없음 | 11개 섹션 목차 |
| **메타 표** | 4행 | 6행 (테스트 수·방법론 추가) |
| **Requirements Traceability Matrix** | 없음 | 신설 (§5) — 30 TASK × 6열 |
| **REQ ID ↔ INV 매핑 표** | 없음 | 신설 (§5.1) — REQ-001~009 ↔ INV-01~09 |
| **To-Do TASK 구조** | 한 줄 요약 | 서브태스크 3단 (`-1:[RED]` / `-2:[GREEN]` / `-3:[REFACTOR]`) |
| **ECB 레이어 어노테이션** | 일부 문장에만 포함 | 전 TASK에 `(<<<layer>>>)` 통일 표기 |
| **진행 관문 마커** | 없음 | `> [Checkpoint]` · `> [Validate]` 전 US에 추가 |
| **ECB 다이어그램** | ASCII 한 줄 | 4-레이어 박스 다이어그램 + 의존성 방향 표 |
| **개발 환경** | pytest·black만 | 매직 넘버 스캔·ECB import 검사 명령 추가 |
| **성공 기준** | 별도 없음 | §10에 SC-01~SC-09 표 추가 |

---

## 3. 개선 항목 상세

### 3.1 Requirements Traceability Matrix 신설 (§5)

v1에는 `## Concept → Test → Code 빠른 참조` 표(3행 예시)만 있었다. v2는 이를 확장하여 전체 30개 TASK에 대한 완전한 추적 테이블을 제공한다.

**§5.1 REQ ID ↔ Invariant 매핑:**

```
REQ-001 ↔ INV-01 (Magic Constant = 34)
REQ-002 ↔ INV-02 (숫자 집합 완전성)
...
REQ-009 ↔ INV-09 (출력 숫자 범위·유일성)
```

PRD에서 INV 번호로만 언급되던 불변조건에 `REQ-xxx` 식별자를 부여하여, To-Do 헤더에서 `REQ: REQ-001 (INV-01 ...)` 형태로 US와 REQ를 직접 연결했다.

**§5.2 Requirements Traceability Matrix (30행 × 6열):**

| 열 | 내용 |
|----|------|
| Task ID | TASK-001~030 |
| REQ ID | REQ-001~009 (단일 또는 복합) |
| Scenario Level | L0·L1·L2·L3 |
| Test ID | PRD 테스트 ID 계열 + 함수명 |
| 컴포넌트 (ECB) | Entity · Control · Boundary · Data · 통합 · 품질 게이트 |
| 상태 | ⬜ TODO · 🔴 RED · 🟡 GREEN · ✅ PASS · ♻️ REFACTOR |

### 3.2 To-Do 서브태스크 3단계화 (§7)

**v1 방식 (한 줄):**
```markdown
- [ ] TASK-004 · RED · 완성 격자에서 행 합 실패 · L3 · Test: test_validator_rejects_invalid_row
```

**v2 방식 (3단계 서브태스크):**
```markdown
- [ ] TASK-004 · 행 합 실패 검증 · L3 · (<<<entity>>>)
  - [ ] TASK-004-1: [RED]  테스트 작성 — MV-T02 실패 확인
  - [ ] TASK-004-2: [GREEN] 최소 구현 — 행 합산만
  - [ ] TASK-004-3: [REFACTOR] 열·대각선 합산 추가
  > [Checkpoint] MV-T02 RED 확인 후 진행 · GREEN 후 MV-T01 자동 통과 확인
```

이 구조는 슬라이드 1.5의 완성 To-Do 예시를 그대로 따른 것으로, **GREEN 없이 RED→RED 연속 금지**, **GREEN 단계에서 리팩터링 금지** 규칙을 파일 구조로 강제한다.

### 3.3 ECB 레이어 어노테이션 통일 (§7)

모든 TASK 헤더에 다음 4종 중 하나를 표기한다.

| 어노테이션 | 적용 대상 |
|-----------|-----------|
| `(<<<entity>>>)` | US-001~005 — Domain 순수 로직 |
| `(<<<control>>>)` | US-006 — 비즈니스 흐름 조율 |
| `(<<<boundary>>>)` | US-007 — 입력 검증·응답 포맷 |
| `(<<<data>>>)` | US-008 저장소 관련 TASK |
| `(<<<통합>>>)` | US-008 통합 테스트 TASK |

v1에서는 일부 TASK에 `· Entity`, `· Boundary` 텍스트로 포함되어 있었으나, 형식이 일관되지 않았다.

### 3.4 진행 관문 마커 추가 (§7)

두 종류의 마커를 전 US에 걸쳐 추가했다.

| 마커 | 의미 | 예시 |
|------|------|------|
| `> [Checkpoint]` | 다음 TASK 진행 전 반드시 통과할 조건 | `MAGIC_CONSTANT=34, GRID_SIZE=4 전부 통과 확인 후 진행` |
| `> [Validate]` | 커버리지·계약·불변성 검증 조건 | `커버리지 ≥ 95% (entity/) 확인` |

### 3.5 ECB 다이어그램 개선 (§3)

v1의 한 줄 ASCII 표현을 4-레이어 박스 다이어그램으로 교체하고, 의존성 방향 표(허용/금지)를 별도 섹션으로 추가했다.

### 3.6 개발 환경 명령 보강 (§9)

v1의 `pytest`, `black` 외에 다음을 추가했다.

```bash
# 매직 넘버 스캔 (REFACTOR 단계 이후 0건 목표)
rg --type py "[^A-Z_\"'(]\b(34|16|4)\b[^)]" entity/ control/

# ECB 역방향 import 검사
rg --type py "from boundary|import boundary" entity/ control/
rg --type py "from control|import control" entity/
```

---

## 4. README v2 구성 요약

| 섹션 | 역할 | v1 대비 |
|------|------|---------|
| 메타 표 | 언어·아키텍처·방법론·테스트 수·문서 링크 | 테스트 수·방법론 추가 |
| **목차** | 11개 섹션 내비게이션 | 신규 |
| §1 프로젝트 개요 | Why 체인 + 훈련 목표 4가지 표 | 개선 (표 추가) |
| §2 도메인 규칙 요약 | INV-01~09 표 + 입출력 계약 (검증 순서·배치 우선순위) | 개선 (표 구조화) |
| §3 ECB 아키텍처 | 4-레이어 박스 다이어그램 + 의존성 방향 표 + 파일 구조 | 개선 (다이어그램 확장) |
| §4 방법론 | Track 구조·TDD 단계 기준·Scenario Level | 개선 (TDD 기준 표 추가) |
| **§5 C2C Traceability — RTM** | REQ↔INV 매핑 표 + 30행 Requirements Traceability Matrix | **신규** |
| §6 Epic & User Story | Epic-001 + US-001~009 표 (REQ 열 추가) | REQ 열 추가 |
| **§7 구현 To-Do 리스트** | 서브태스크 3단계 + `(<<<layer>>>)` + `[Checkpoint]`·`[Validate]` | **전면 재구성** |
| §8 에러 코드 7종 | errorCode·발생조건·메시지·레이어 표 | 별도 섹션 분리 |
| §9 개발 환경 | venv·pytest·black·rg 스캔 명령 | 스캔 명령 추가 |
| §10 성공 기준 | SC-01~SC-09 표 | 별도 섹션 분리 |
| §11 참고 문서 | PRD·Design·Report 링크 | 위치 이동 |

---

## 5. C2C Traceability 구조 반영 방식

### 5.1 슬라이드 → README 매핑

| 슬라이드 요소 | README 반영 위치 |
|--------------|----------------|
| 체크박스 + 단계별 번호 (`TASK-002-1`, `-2`, `-3`) | §7 서브태스크 구조 |
| Requirements Traceability Matrix (Task→Req→Scenario→Test→상태) | §5.2 |
| `(<<<entity>>>)`, `(<<<control>>>)` 어노테이션 | §7 전 TASK 헤더 |
| `> [Checkpoint]` 진행 관문 | §7 각 TASK 하단 |
| `* 선택:` 알고리즘 힌트 | 해당 TASK 설명에 선택 사항으로 포함 |
| `[Validate] 커버리지 80%+` | §7 `[Validate]` 마커 |

### 5.2 추적 체인 5단계

```
Concept (훈련 목표)
    ↓
REQ ID (INV-xx 불변조건) ── §5.1 매핑 표
    ↓
Scenario Level (L0~L3) ── §4.3 정의
    ↓
Test ID (BF-T01, MV-T02 ...) ── §5.2 RTM
    ↓
Code (ECB Layer + 파일 경로) ── §3.3 파일 구조 + §7 어노테이션
```

이 체인이 README 한 파일 안에서 완전히 순환 가능하다.

---

## 6. PRD·ECB·Dual-Track과의 일치성

| PRD 요소 | v2 README 반영 위치 |
|-----------|---------------------|
| ECB §8.1~8.3 의존성 방향 | §3.2 의존성 규칙 표 (허용/금지 6행) |
| ECB §8.4 파일 구조 | §3.3 코드 블록 (그대로 수록) |
| 입출력 계약 §4 (검증 순서, 배치 우선순위) | §2.2 |
| INV-01~09 | §2.1 + §5.1 REQ 매핑 |
| Gherkin L0~L3 §9 | §4.3 Scenario Level 표 + §7 각 US 헤더 REQ 블록 |
| Dual-Track Track A/B | §4.1 Track 구조 다이어그램 |
| TDD 단계별 진입·완료 기준 §10.3 | §4.2 + §7 서브태스크 `[RED]·[GREEN]·[REFACTOR]` |
| 금지 패턴 §11.2 | §9 개발 환경의 ECB import 검사 명령 |
| 성공 기준 §12 SC-01~09 | §10 성공 기준 표 |

불일치 발생 시 **PRD가 우선**임을 README 하단 푸터에 명시했다.

---

## 7. 의도적으로 남긴 제약·후속 작업

| 항목 | 내용 |
|------|------|
| **실행 명령 조정** | `pyproject.toml` 미생성 단계이므로 "구현 후 조정" 안내 유지 |
| **배지·CI 연동** | 커버리지·테스트 통과 배지 미부착 — 파이프라인 확정 후 §9에 추가 |
| **상태 열 갱신** | RTM의 상태 열은 현재 전부 ⬜ TODO — 구현 진행에 따라 수동 갱신 필요 |
| **영문 README** | 요청 범위에 없음 — 한국어 단일 |
| **To-Do 자동 동기화** | TASK-027 수동 대조 전제; 자동화 스크립트는 별도 과제 |
| **5×5 확장** | Out-of-Scope (PRD §13) — README에도 Phase 2로 명시 |

---

## 8. 산출물 및 링크

| 파일 | 설명 |
|------|------|
| [docs/README.md](../docs/README.md) | v2 — C2C Traceability 완성 README (619줄) |
| [docs/PRD.md](../docs/PRD.md) | 계약·시나리오·테스트 계획의 정본 (변경 없음) |
| [Report/05_MagicSquare_PRD_Report.md](./05_MagicSquare_PRD_Report.md) | PRD 작성 단계 보고 (선행 문서) |

---

## 9. 종합 결론

v1 README는 저장소 진입점·방법론 요약·To-Do 목록을 한 파일에 모으는 데 성공했으나, **C2C Traceability의 수직 연결이 불완전**했다. Task는 한 줄로 압축되어 있었고, Requirement와 Test의 연결 표가 없었으며, 구현 단계를 안내할 진행 관문도 부재했다.

v2 개선은 슬라이드의 완성 To-Do 구조 예시를 직접 반영하여 세 가지를 달성했다.

1. **Requirements Traceability Matrix (§5)** — 30개 TASK 전체에 걸친 Task→REQ→Scenario→Test→Code 5단 추적 테이블 완성
2. **서브태스크 3단계화 (§7)** — `[RED]→[GREEN]→[REFACTOR]` 서브태스크로 TDD 사이클 위반을 파일 구조로 방지
3. **`(<<<layer>>>)` + `[Checkpoint]·[Validate]` (§7)** — ECB 레이어 어노테이션과 진행 관문 마커로 구현 진입·완료 기준을 README 안에 고정

다음 구현 단계에서는 각 TASK 서브태스크를 순서대로 이행하며 상태 열을 갱신하고, TASK-027~030(품질 게이트)으로 전체 추적 체인의 완결성을 검증한다.

---

*본 보고서는 `docs/README.md` v2 개선 작업에 대한 기록이며, 제품 요구사항의 정본은 `docs/PRD.md`이다.*
