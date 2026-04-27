# 4×4 Magic Square — Epic · User Journey 설계 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square 프로그램 개발 |
| **보고서 유형** | 사용자 여정 설계 보고서 (Epic · User Journey Report) |
| **작성일** | 2026-04-27 |
| **단계 범위** | Level 1 (Epic) → Level 2 (User Journey 5단계) |
| **목적** | 비즈니스 목표(Epic)와 학습자 여정(User Journey)을 명문화하여 이후 User Story · Task 분해의 기준을 확립한다 |
| **설계 원문** | `Design/04_MagicSquare_Epic_UserJourney_Design.md` |

---

## 목차

1. [작업 배경 및 목적](#1-작업-배경-및-목적)
2. [Level 1 — Epic 설계 결정](#2-level-1--epic-설계-결정)
3. [Level 2 — User Journey 설계 결정](#3-level-2--user-journey-설계-결정)
4. [설계 결정 간 일관성 검토](#4-설계-결정-간-일관성-검토)
5. [산출물 전체 요약](#5-산출물-전체-요약)
6. [종합 결론 및 다음 단계](#6-종합-결론-및-다음-단계)

---

## 1. 작업 배경 및 목적

이전 단계(보고서 01·02·03)에서 확립된 결과물은 다음과 같다.

| 단계 | 결과물 | 핵심 확립 내용 |
|------|--------|---------------|
| 보고서 01 | 문제 정의 | 도메인 불변조건 INV-01~INV-09, 입출력 계약 `int[6]` |
| 보고서 02 | TDD + Clean Architecture 설계 | 71개 테스트 계획, ECB 레이어 분리, 에러 코드 7종 |
| 보고서 03 | `.cursorrules` | AI 행동 규칙 — 위 두 결과물을 AI 지침으로 변환 |
| **이 보고서** | **Epic + User Journey** | 비즈니스 목표와 학습자 여정을 구조화 |

### Epic · User Journey가 필요한 이유

> 설계 문서는 **"무엇을 만들어야 하는가"** 를 정의한다.  
> Epic · User Journey는 **"왜 만드는가, 누가 어떤 순서로 경험하는가"** 를 정의한다.

설계 문서와 `.cursorrules`가 완성되어도, 학습자가 어떤 순서로 어떤 사고를 해야 하는지 명시되지 않으면 실행 시 방향을 잃게 된다.  
Epic · User Journey는 이 간극을 메운다 — **훈련 목표와 실행 흐름을 하나의 문서로 통합**한다.

---

## 2. Level 1 — Epic 설계 결정

### 2.1 Epic 명칭 결정

| 후보 | 탈락 이유 |
|------|-----------|
| "마방진 풀이 프로그램 개발" | 결과물(구현)에 초점 → 훈련 목적 누락 |
| "TDD 실습 프로젝트" | 방법론만 언급 → 사고 훈련 목적 누락 |
| **"Invariant 기반 사고 훈련 시스템 구축"** | 불변조건 중심 사고라는 **본질적 목적** 명시 ✓ |

> Epic 명칭은 "무엇을 만드는가"가 아니라 **"무엇을 훈련하는가"** 로 결정하였다.

---

### 2.2 훈련 목표 4가지 설계

4가지 훈련 목표는 이 프로젝트를 통해 학습자가 체화해야 할 **사고 능력**을 중심으로 정의하였다.

| # | 훈련 목표 | 핵심 질문 | 연관 설계 결정 |
|---|-----------|-----------|----------------|
| ① | Invariant 중심 설계 사고 | "절대 위반할 수 없는 조건은?" | INV-01~INV-09 도출 |
| ② | Dual-Track TDD 적용 | "UI와 Domain을 병렬로 RED→GREEN→REFACTOR 할 수 있는가?" | Track A/B 분리 |
| ③ | 입력/출력 계약 명확화 | "계약은 코드에 어떻게 표현되는가?" | 에러 코드 7종, `int[6]` 출력 |
| ④ | 설계→테스트→구현→리팩토링 흐름 체화 | "각 단계 진입·완료 기준을 지키는가?" | TDD 단계별 규칙 |

---

### 2.3 성공 기준 (SC-01~SC-08) 설계 원칙

성공 기준은 **측정 가능성**과 **자동화 가능성**을 두 축으로 설계하였다.

| 설계 원칙 | 적용 내용 |
|-----------|-----------|
| 정량 목표 명시 | Domain ≥ 95%, Boundary ≥ 85%, Data ≥ 80% — 임의적 수치 배제 |
| 자동 측정 명령 | 각 기준마다 `pytest --cov`, `rg` 등 실행 가능한 명령을 병기 |
| 추적 가능성 보장 | SC-04: 테스트 주석의 `INV-xx` 태그로 Invariant → Test 연결 강제 |
| 구조적 제약 포함 | SC-08: ECB 의존성 방향 위반 0건 — 코드 품질 측면 기준 포함 |

**성공 기준 전체 목록:**

| 기준 ID | 항목 | 목표값 | 측정 방법 |
|---------|------|--------|-----------|
| SC-01 | Domain Logic 테스트 커버리지 | ≥ 95% | `pytest --cov=entity` |
| SC-02 | 입력 검증 계약 테스트 통과율 | 100% | `pytest tests/boundary/` |
| SC-03 | 하드코딩(매직 넘버) 잔존 여부 | 0건 | `rg` 패턴 스캔 |
| SC-04 | Invariant → Test 추적 가능성 | INV-01~INV-09 전체 | 테스트 주석 `INV-xx` 확인 |
| SC-05 | UI Boundary 테스트 커버리지 | ≥ 85% | `pytest --cov=boundary` |
| SC-06 | Data Layer 테스트 커버리지 | ≥ 80% | `pytest --cov=data` |
| SC-07 | 전체 테스트 케이스 통과 | 71개 전체 GREEN | `pytest tests/ -v` |
| SC-08 | ECB 레이어 의존성 방향 위반 | 0건 | import 방향 수동 검토 |

---

### 2.4 In-Scope / Out-of-Scope 경계 결정

Out-of-Scope를 명시적으로 선언한 이유:

> "무엇을 하지 않는가"를 정의하지 않으면, 학습자는 범위를 벗어난 작업에 시간을 소비하게 된다.

| Out-of-Scope 항목 | 배제 근거 |
|-------------------|-----------|
| GUI / Web UI | Boundary는 입출력 계약 경계 — 실제 화면은 이 훈련의 대상 외 |
| 데이터베이스 영속성 | Data Layer는 인터페이스(Protocol) 수준으로 충분 |
| 5×5 이상 마방진 | 격자 크기 확장은 INV-03 위반 — 별도 Epic으로 분리 필요 |
| 빈칸 수 변형 케이스 | INV-04(빈칸 = 정확히 2개) 위반 — 이 훈련 범위 외 |

---

## 3. Level 2 — User Journey 설계 결정

### 3.1 Persona 정의 결정

| 항목 | 설계 결정 | 이유 |
|------|-----------|------|
| 역할 | 소프트웨어 개발 학습자 | 전문 개발자가 아닌 TDD·Clean Architecture 훈련 중인 학습자 |
| 어려움 명시 | "구현부터 시작하는 관성" | 이 훈련이 극복하려는 핵심 습관을 명시 → Journey의 방향 설정 |
| 현재 상태 | TDD 훈련 중, Clean Architecture 이해 중 | 완전 초보도 전문가도 아닌 — 정확한 대상 독자 설정 |

---

### 3.2 5단계 Journey 구조 설계 결정

Journey를 5단계로 구성한 이유:

| 결정 | 근거 |
|------|------|
| 5단계 구조 | 보고서 01(문제 정의) → 보고서 02(설계) → 보고서 03(규칙) 흐름과 정합 |
| 단계별 체크포인트 | 각 단계가 "완료"임을 학습자가 스스로 확인할 수 있는 기준 제공 |
| Before/After 표 | Step 1에서 사고 전환을 가시화 — 관성적 접근과 Invariant 기반 접근의 차이 명시 |

**Journey 전체 구조:**

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4 ──→ Step 5
문제 인식   계약 정의   Domain 분리  Dual-Track  회귀 보호
(INV 도출)  (계약 문서화) (SRP 분리)  (TDD 진행)  (Edge Case)
```

---

### 3.3 각 Step별 설계 포인트

#### Step 1 — 문제 인식

> 핵심 설계 결정: Journey의 시작점을 **"구현"이 아닌 "Invariant 도출"** 로 설정

학습자가 가장 흔히 범하는 실수는 문제를 받자마자 코드를 작성하는 것이다.  
Step 1은 이 관성을 의도적으로 차단하고, **9가지 불변조건이 모두 명문화되기 전까지 Step 2로 진행할 수 없다**는 진입 조건을 설정하였다.

| 확립 대상 | 연관 Invariant |
|-----------|---------------|
| 마방진 수학적 속성 | INV-01, INV-02 |
| 문제 제약 조건 | INV-03, INV-04, INV-05, INV-06 |
| 해의 유일성 전제 | INV-07 |
| 출력 포맷 계약 | INV-08, INV-09 |

---

#### Step 2 — 계약 정의

> 핵심 설계 결정: 입력·출력·예외 세 가지 계약을 **별도 스키마**로 분리하여 명세

계약을 하나의 덩어리로 서술하지 않고 3개 섹션(입력 스키마 / 출력 스키마 / 예외 정책)으로 분리한 이유:

| 분리 이유 | 효과 |
|-----------|------|
| 입력 스키마 분리 | 입력 검증 4단계 순서(크기→값→빈칸→중복)를 강제할 수 있음 |
| 출력 스키마 분리 | `int[6]` 포맷과 1-index 좌표계를 독립적으로 계약 가능 |
| 예외 정책 분리 | 에러 코드 7종과 처리 레이어를 명확히 매핑 가능 |

**입력 검증 4단계 순서 (계약 고정):**

```
1단계: 크기 검증     → INVALID_GRID_SIZE
2단계: 값 범위 검증  → INVALID_CELL_VALUE
3단계: 빈칸 수 검증  → INVALID_BLANK_COUNT
4단계: 중복 검증     → DUPLICATE_VALUE
```

> 순서를 고정한 이유: **첫 번째 실패 즉시 반환** 정책 — 다중 오류를 동시에 반환하지 않음

---

#### Step 3 — Domain 분리

> 핵심 설계 결정: "이 책임을 다른 컴포넌트가 가지면 어떻게 되는가?" **역설계 검증** 도입

단순히 컴포넌트 목록을 나열하는 대신, **잘못된 설계의 문제점**을 함께 명시하여  
학습자가 SRP 위반 패턴을 스스로 식별할 수 있도록 설계하였다.

| 컴포넌트 | 책임 | 역설계 예방 |
|----------|------|-------------|
| `BlankFinder` | 빈칸 위치 탐색 | Solver가 빈칸을 직접 탐색하면 SRP 위반 |
| `MissingNumberFinder` | 누락 숫자 탐색 | Validator가 누락 숫자를 처리하면 SRP 위반 |
| `MagicSquareValidator` | 합산 조건 검증 | Controller가 검증을 수행하면 ECB 붕괴 |
| `SolvingStrategy` | 조합 선택 | InputValidator가 조합을 시도하면 레이어 경계 붕괴 |

---

#### Step 4 — Dual-Track 진행

> 핵심 설계 결정: Track A(UI Boundary)와 Track B(Domain Logic)를 **Mock 경계**로 완전히 격리

| Track | 대상 | 격리 방법 | 테스트 수 |
|-------|------|-----------|-----------|
| Track A (UI) | Boundary 계약 검증 | Domain을 `Mock`으로 대체 | 19개 (UI-T01~T19) |
| Track B (Domain) | Domain 로직 검증 | 순수 Python — 외부 의존 없음 | 29개 (BF/MF/MV/SS/SR) |
| Integration | 두 Track 통합 | 실제 컴포넌트 전체 연결 | 10개 (IT-S/F) |
| Data | Repository 계약 | InMemoryRepository | 13개 (DT-T01~T13) |

**RED → GREEN → REFACTOR 단계별 진입 조건:**

| 단계 | 진입 조건 | 완료 기준 |
|------|-----------|-----------|
| RED | 없음 (첫 단계) | 새 테스트가 `AssertionError` 또는 `ImportError`로 실패 |
| GREEN | RED 확인 완료 | 해당 테스트만 통과 + 기존 GREEN 유지 |
| REFACTOR | 모든 테스트 GREEN | 커버리지 목표 유지 + 회귀 없음 확인 |

---

#### Step 5 — 회귀 보호

> 핵심 설계 결정: 엣지 케이스를 **3개 카테고리**로 분류하여 누락 방지

| 카테고리 | 목적 | 대표 케이스 |
|----------|------|-------------|
| 엣지 케이스 | 경계값·특수 위치 검증 | 같은 행/열/대각선의 빈칸, 누락 숫자 1과 16 |
| 입력 오류 케이스 | 에러 코드 7종 완전 커버 | `None` 입력, 셀 값 17, 음수, 중복 |
| 조합 실패 케이스 | `NO_SOLUTION` 경로 검증 | 두 조합 모두 불만족 |

**회귀 보호 실행 체크리스트:**

```bash
# 전체 테스트 실행
pytest tests/ -v

# 커버리지 측정
pytest tests/ --cov=entity --cov=boundary --cov=data --cov-report=term-missing

# 매직 넘버 스캔
rg --type py '[^A-Z_"'"'"'(]\b(34|16|4)\b[^)]' entity/ control/
```

---

## 4. 설계 결정 간 일관성 검토

이 보고서에서 내린 설계 결정들이 이전 보고서와 일관성을 유지하는지 검증한다.

| 검토 항목 | 이전 결정 (보고서 01·02·03) | 이번 결정 (Epic · Journey) | 일관성 |
|-----------|----------------------------|--------------------------|--------|
| 불변조건 수 | INV-01~INV-09 (9개) | Epic 기반 + Journey 각 Step에 INV 매핑 | ✅ 일치 |
| 테스트 케이스 수 | 71개 | Journey Step 4에서 71개 전체 참조 | ✅ 일치 |
| 에러 코드 수 | 7종 | Step 2 예외 정책, Step 5 회귀 보호에 7종 전체 포함 | ✅ 일치 |
| 입력 검증 순서 | 크기→값→빈칸→중복 | Step 2 계약 정의에서 동일 순서 명세 | ✅ 일치 |
| ECB 레이어 | Boundary→Control→Entity | Step 3 의존성 방향 다이어그램 동일 | ✅ 일치 |
| 커버리지 목표 | Domain ≥ 95% / UI ≥ 85% / Data ≥ 80% | SC-01·SC-05·SC-06에 동일 수치 | ✅ 일치 |
| 출력 포맷 | `int[6]`, 1-index | Step 2 출력 스키마에서 동일 계약 | ✅ 일치 |

> **검토 결론:** 7개 검토 항목 모두 일관성 확인 — 불일치 0건.

---

## 5. 산출물 전체 요약

### 5.1 설계 문서 구조

```
Design/04_MagicSquare_Epic_UserJourney_Design.md  (353줄)
│
├── Level 1 — Epic
│   ├── 1.1 목적 (훈련 목표 4가지)
│   ├── 1.2 성공 기준 (SC-01~SC-08)
│   ├── 1.3 Epic 범위 (In/Out-of-Scope)
│   └── 1.4 도메인 불변조건 요약 (INV-01~INV-09)
│
└── Level 2 — User Journey
    ├── Persona 정의
    ├── Journey Map (5단계 흐름도)
    ├── Step 1 — 문제 인식 (Before/After + 체크포인트)
    ├── Step 2 — 계약 정의 (입력·출력·예외 스키마)
    ├── Step 3 — Domain 분리 (SRP + 의존성 방향)
    ├── Step 4 — Dual-Track 진행 (RED/GREEN/REFACTOR + 71개 배분)
    ├── Step 5 — 회귀 보호 (엣지·오류·실패 케이스)
    └── 여정 전체 요약 표
```

### 5.2 핵심 숫자 요약

| 항목 | 값 |
|------|----|
| 훈련 목표 수 | 4가지 |
| 성공 기준 수 | 8개 (SC-01~SC-08) |
| Invariant 수 | 9개 (INV-01~INV-09) |
| User Journey 단계 수 | 5단계 |
| 에러 코드 수 | 7종 |
| 전체 테스트 케이스 수 | 71개 |
| 각 Step 체크포인트 수 | 3~4개 |

### 5.3 보고서 간 연결 관계

```
보고서 01 (문제 정의)
  └── INV-01~INV-09 확립
       └── 보고서 02 (설계)
             └── ECB 레이어 + 71개 테스트 + 에러 코드 7종
                  └── 보고서 03 (.cursorrules)
                        └── AI 행동 규칙화
                             └── 보고서 04 ★ (이 문서)
                                   └── Epic + User Journey 구조화
                                        └── (다음) User Story + Task 분해
```

---

## 6. 종합 결론 및 다음 단계

### 이 보고서에서 확립한 것

| 확립 내용 | 활용처 |
|-----------|--------|
| Epic: "Invariant 기반 사고 훈련 시스템 구축" | 모든 User Story의 비즈니스 근거 |
| 성공 기준 SC-01~SC-08 | 프로젝트 완료 판단 기준 |
| 학습자 Persona + 어려움 명시 | User Story 작성 시 주어 설정 근거 |
| 5단계 Journey + 단계별 체크포인트 | 구현 순서 및 단계 완료 기준 |
| Journey ↔ Invariant 매핑 | 각 단계가 어떤 불변조건을 보호하는지 추적 가능 |

### 다음 단계 — Level 3: User Story

Epic과 User Journey가 확립되었으므로, 다음 단계는 **각 Journey Step을 User Story로 분해**하는 것이다.

| 목표 | 형식 |
|------|------|
| 각 Step → User Story | `As a [Persona], I want to [Goal], so that [Benefit]` |
| 각 User Story → Task | 구체적인 구현 단위로 분해 |
| 각 Task → 테스트 ID 매핑 | BF-T01, UI-T01 등과 직접 연결 |

**예상 User Story 분포:**

| Journey Step | 예상 User Story 수 |
|--------------|-------------------|
| Step 1 — 문제 인식 | 1~2개 |
| Step 2 — 계약 정의 | 2~3개 |
| Step 3 — Domain 분리 | 4~5개 (컴포넌트별) |
| Step 4 — Dual-Track | 2~3개 (Track A/B + REFACTOR) |
| Step 5 — 회귀 보호 | 1~2개 |

---

> **이전 단계 보고서:**  
> - `Report/01_MagicSquare_ProblemDefinition_Report.md` — 문제 정의  
> - `Report/02_MagicSquare_TDD_CleanArchitecture_Report.md` — TDD + Clean Architecture 설계  
> - `Report/03_MagicSquare_CursorRules_Report.md` — `.cursorrules` 설계
