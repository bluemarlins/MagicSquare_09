# 4×4 Magic Square — `.cursorrules` 설계 및 작성 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square 프로그램 개발 |
| **보고서 유형** | AI 행동 규칙 설계 보고서 (Cursor Rules Report) |
| **작성일** | 2026-04-27 |
| **단계 범위** | D1_5 — `.cursorrules` 뼈대 생성 → 섹션별 작성 → 검토 → 완성 |
| **목적** | Cursor AI가 MagicSquare 프로젝트 전반에서 일관된 TDD 사이클·ECB 아키텍처·코드 스타일을 자동으로 준수하도록 규칙 기반 컨텍스트를 확립한다 |
| **결과물** | `.cursorrules` (YAML, 344줄, 8개 섹션) |
ㅇㄹㄹ
---

## 목차

1. [작업 배경 및 목적](#1-작업-배경-및-목적)
2. [작업 방법론 — 4단계 프롬프트 체인](#2-작업-방법론--4단계-프롬프트-체인)
3. [섹션별 설계 결정](#3-섹션별-설계-결정)
4. [섹션 간 일관성 검토 결과](#4-섹션-간-일관성-검토-결과)
5. [`.cursorrules` 구조 전체 요약](#5-cursorrules-구조-전체-요약)
6. [설계 원칙 및 제약](#6-설계-원칙-및-제약)
7. [종합 결론 및 다음 단계](#7-종합-결론-및-다음-단계)

---

## 1. 작업 배경 및 목적

이전 단계(보고서 01·02)에서 확립된 결과물은 다음과 같다.

| 단계 | 결과물 | 핵심 확립 내용 |
|------|--------|---------------|
| 보고서 01 | 문제 정의 | 도메인 불변조건 INV-01~INV-09, 입출력 계약 `int[6]` |
| 보고서 02 | TDD + Clean Architecture 설계 | 71개 테스트 계획, ECB 레이어 분리, 에러 코드 7종 |
| **이 보고서** | `.cursorrules` | AI가 따를 규칙 — 위 두 결과물을 AI 행동 지침으로 변환 |

### `.cursorrules`가 필요한 이유

> 설계 문서는 **사람을 위한 계약**이다.  
> `.cursorrules`는 **AI를 위한 계약**이다.

설계 문서가 아무리 정밀해도, Cursor AI가 코드를 생성할 때 설계를 자동으로 참조하지 않으면 의미가 없다.  
`.cursorrules`는 이 간극을 메운다 — 설계 문서의 핵심 제약을 AI가 **세션마다** 자동으로 따르는 규칙으로 변환한다.

---

## 2. 작업 방법론 — 4단계 프롬프트 체인

`.cursorrules` 파일을 한 번에 작성하지 않고, **점진적 구체화** 방식으로 4단계에 걸쳐 작성하였다.

### 단계별 작업 내용

| 단계 | 프롬프트 목적 | 산출물 |
|------|-------------|--------|
| **1단계** | 뼈대 생성 | 8개 최상위 키 + 80자 구분선, 값 비움 |
| **2단계** | `tdd_rules` 먼저 채우기 | `red_phase` / `green_phase` / `refactor_phase` 초안 |
| **3단계** | 검토 요청 (수정 없이) | YAML 문법, 누락 섹션, 섹션 간 충돌, AI 실행 가능성 검토 |
| **4단계** | 전체 섹션 완성 | 8개 섹션 모두 채움, 검토에서 발견된 충돌 해소 포함 |

### 이 방법론의 의도

```
뼈대 먼저 합의 → 섹션 하나씩 검증 → 전체 일관성 검토 → 완성
```

- **뼈대 우선:** 섹션 이름을 먼저 고정함으로써 전체 구조에 대한 합의를 선행한다.
- **부분 작성 검토:** `tdd_rules` 하나만 완성한 뒤 나머지를 채우기 전에 문제점을 확인한다.
- **검토 단계 분리:** 수정 요청 없이 문제만 보고하도록 프롬프트를 설계하여, AI가 즉시 수정하는 것을 방지하고 설계자가 판단을 유보할 수 있게 한다.

---

## 3. 섹션별 설계 결정

### 3.1 `project` — 도메인 계약의 단일 진실 공급원

```
project.domain_constants  ← 매직 상수(34), 격자 크기(4), 값 범위(1~16) 등
project.output_contract   ← [r1, c1, n1, r2, c2, n2]
project.invariants        ← INV-01 ~ INV-09 전체 목록
```

**설계 의도:** 하위 섹션(code_style, tdd_rules, forbidden 등)에서 숫자나 조건을 참조할 때, 그 근거가 항상 `project` 섹션으로 역추적 가능하도록 단일 출처를 확립하였다.

---

### 3.2 `code_style` — Python 3.10+ 기준 코딩 표준

| 항목 | 결정 값 | 근거 |
|------|---------|------|
| 포매터 | Black (88자) | 팀 논쟁 제거, 자동 일관성 보장 |
| 타입힌트 | 모든 파라미터·반환값 필수 | Value Object 불변성 검증에 필수 |
| Docstring | Google 스타일, public 메서드 전수 | Args / Returns / Raises 구조로 계약 문서화 |
| Import | isort 기준 (stdlib → third-party → local) | 레이어 의존 방향을 import 순서에서도 반영 |

**코드 예시 포함 이유:** AI가 규칙을 텍스트로만 읽으면 생성 품질이 낮다. 올바른 타입힌트·docstring 예시를 직접 삽입하여 AI가 형식을 패턴으로 학습하도록 유도하였다.

---

### 3.3 `architecture` — ECB 3레이어 계약

ECB(Entity-Control-Boundary) 패턴을 레이어별로 명시하고, 각 레이어에 `must_not` 항목을 추가하여 **허용 범위가 아닌 금지 범위**로 경계를 정의하였다.

```
의존성 방향: Boundary → Control → Entity  (역방향 절대 금지)
```

| 레이어 | 핵심 컴포넌트 | 절대 금지 |
|--------|-------------|----------|
| Boundary | InputValidator, ResponseFormatter, Controller | Domain 객체 직접 생성 / Data Layer 직접 호출 |
| Control | MagicSquareSolver, SolvingStrategy | 입력 검증 수행 / 저장·로드 직접 수행 |
| Entity | MagicSquare, VO 4종, Domain Services 4종 | 저장소 의존 / UI 코드 포함 / 외부 라이브러리 |

**금지 의존성 4종 명시:**

```yaml
forbidden_dependencies:
  - "Entity → Control  (절대 금지)"
  - "Entity → Boundary (절대 금지)"
  - "Control → Boundary (절대 금지)"
  - "Boundary → Data 직접 호출 (Facade 경유 필수)"
```

---

### 3.4 `tdd_rules` — RED/GREEN/REFACTOR 사이클 강제

2단계에서 작성한 초안을 3단계 검토 결과를 반영하여 구조를 개선하였다.

| 변경 전 (2단계) | 변경 후 (4단계) |
|----------------|----------------|
| `rule` + `conditions` + `checklist` | `description` + `rules` + `must_not` |
| 단계 설명이 `rule` 한 줄 | `description`으로 분리하여 가독성 향상 |
| `checklist`는 사람용 체크리스트 | AI가 따를 수 없는 항목 제거, `must_not`으로 대체 |

**`green_phase`의 하드코딩 허용 명시:**

```yaml
green_phase:
  rules:
    - "하드코딩도 허용 — 일반화는 REFACTOR 단계에서 한다."
```

이 항목은 `forbidden` 섹션의 하드코딩 금지 규칙과 잠재 충돌이 있다. → `forbidden`에 `exception: GREEN 단계 허용` 명시로 해소.

---

### 3.5 `testing` — 71개 테스트 계획 내재화

| 항목 | 결정 |
|------|------|
| 프레임워크 | pytest |
| 패턴 | AAA (Arrange-Act-Assert) |
| 커버리지 목표 | Domain ≥ 95% / UI ≥ 85% / Data ≥ 80% |
| fixture scope | `function`만 기본 허용, `module`·`session`은 금지 |
| Mock 정책 | UI Boundary 테스트에서 Domain은 반드시 Mock 대체 |

**테스트 분포를 직접 기재한 이유:** AI가 새 테스트를 작성할 때 기존 71개의 ID 체계(BF-T01, UI-T01 등)와 충돌하지 않도록 전체 현황을 컨텍스트로 제공한다.

---

### 3.6 `forbidden` — 금지 패턴 7종

3단계 검토에서 식별한 `tdd_rules`와의 충돌을 해소하며, 각 항목을 `pattern / reason / alternative` 3-필드 구조로 통일하였다.

| # | 금지 패턴 | 핵심 이유 | 예외 |
|---|----------|----------|------|
| 1 | `print()` 직접 사용 | 테스트 결과 오염 | — |
| 2 | 하드코딩 상수 (REFACTOR 이후) | 도메인 상수 분산 방지 | GREEN 단계 허용 |
| 3 | `bare except` | 치명적 예외 무시 | — |
| 4 | Domain → Boundary import | ECB 의존 방향 위반 | — |
| 5 | `isinstance()` 레이어 간 분기 | 암묵적 결합 | — |
| 6 | 테스트 내 실제 I/O | 테스트 격리 위반 | — |
| 7 | `type: ignore` 남용 | 타입 안전성 훼손 | — |

---

### 3.7 `file_structure` — ECB 기준 패키지 트리

파일 구조를 YAML 값이 아닌 **YAML 주석 트리**로 표현하였다.

```
magic_square/
├── boundary/   ← 외부 입출력
├── control/    ← 비즈니스 흐름 조율
├── entity/     ← 도메인 순수 로직
│   ├── value_objects/
│   └── services/
├── data/       ← 저장소 추상화
├── exceptions/ ← 예외 클래스
└── tests/      ← 71개 테스트 (레이어 구조 미러링)
    ├── entity/
    ├── boundary/
    ├── data/
    └── integration/
```

**`tests/` 구조가 `entity/`, `boundary/`, `data/`를 미러링하는 이유:** 테스트 파일과 구현 파일의 1:1 대응을 강제하여 누락 테스트를 구조적으로 방지한다.

---

### 3.8 `ai_behavior` — 코드 생성 전·중·후 3구간 규칙

3단계 검토에서 확인된 원칙 — **AI가 텍스트를 생성하는 방식만 지정** — 을 준수하여, 빌드·실행·파일 시스템 상태 자동 확인 등 외부 환경 의존 조건은 포함하지 않았다.

| 구간 | 규칙 수 | 핵심 규칙 |
|------|---------|----------|
| `before_writing_code` | 3개 | 테스트 파일 먼저 확인 / TDD 단계 파악 / ECB 레이어 식별 |
| `while_writing_code` | 4개 | ECB 경계 위반 금지 / 타입힌트 필수 / docstring 필수 / TDD 위반 경고 |
| `after_writing_code` | 3개 | 테스트 ID 추적성 확인 / forbidden 자가 검토 / 한국어 응답 |

**TDD 위반 경고 형식 고정:**

```
[TDD 경고] {위반 내용}. tdd_rules.{phase}.must_not 참조.
```

---

## 4. 섹션 간 일관성 검토 결과

3단계에서 수정 없이 보고된 문제점과 4단계에서의 해소 방식을 정리한다.

| 문제 유형 | 발견 내용 | 해소 방식 |
|----------|----------|----------|
| YAML 문법 오류 | 없음 | — |
| 누락 섹션 | 5개 섹션 비어 있음 | 4단계에서 전체 채움 |
| `tdd_rules` ↔ `forbidden` 충돌 ① | `green_phase` 하드코딩 허용 vs 하드코딩 금지 | `forbidden` 항목에 `exception: GREEN 단계 허용` 추가 |
| `tdd_rules` ↔ `forbidden` 충돌 ② | `refactor_phase` 테스트 수정 금지 범위 불명확 | `"테스트를 수정하지 않는다"` → `"테스트 로직을 수정하지 않는다"`로 범위 한정 |
| AI 실행 불가 규칙 위험 | 커버리지 자동 측정, RED 자동 확인 등 | `ai_behavior`에서 해당 패턴 완전 배제 |

---

## 5. `.cursorrules` 구조 전체 요약

```
.cursorrules (YAML, 344줄)
│
├── project          ← 도메인 상수 + INV-01~09 (단일 진실 공급원)
├── code_style       ← Python 3.10+, Black/88, 타입힌트, Google docstring
├── architecture     ← ECB 3레이어 정의 + 금지 의존성 4종
├── tdd_rules        ← RED/GREEN/REFACTOR — description + rules + must_not
├── testing          ← pytest, AAA, 커버리지 목표, 71개 분포, fixture scope
├── forbidden        ← 금지 패턴 7종 — pattern + reason + alternative
├── file_structure   ← ECB 기준 패키지 트리 (주석 형태)
└── ai_behavior      ← before / while / after 3구간 AI 행동 규칙
```

### 섹션 간 참조 관계

```
project.invariants
    ↓ 참조
tdd_rules.red_phase.rules (테스트 ID + INV 번호 명시)
    ↓ 보호
testing.test_distribution (71개 테스트 ID 체계)

architecture.forbidden_dependencies
    ↓ 강제
forbidden[4] (Domain→Boundary import 금지)
    ↓ AI에 적용
ai_behavior.while_writing_code (ECB 경계 위반 금지)

tdd_rules.green_phase (하드코딩 허용)
    ↔ 조율
forbidden[2] (하드코딩 금지 + GREEN 단계 예외)
```

---

## 6. 설계 원칙 및 제약

### 이 `.cursorrules`에 부과된 3가지 설계 원칙

| # | 원칙 | 적용 방식 |
|---|------|----------|
| 1 | **AI 실행 가능성 우선** | `ai_behavior`에는 AI가 텍스트로 이행 가능한 규칙만 포함 |
| 2 | **섹션 간 충돌 금지** | 3단계 검토를 통해 충돌 지점을 식별하고 `exception` 또는 범위 한정으로 해소 |
| 3 | **단일 진실 공급원** | 도메인 상수·불변조건은 `project` 섹션 한 곳에만 정의하고 다른 섹션에서 중복 정의 금지 |

### 변경 금지 항목

| 항목 | 변경 금지 이유 |
|------|--------------|
| `project.output_contract` 형식 | 보고서 02의 입출력 계약과 직결 |
| `project.invariants` INV 번호 체계 | 71개 테스트 ID와 1:1 연결 |
| `tdd_rules.cycle` 순서 | RED → GREEN → REFACTOR 역전 금지 |
| `architecture.dependency_direction` | ECB 레이어 붕괴 방지 |
| `ai_behavior.while_writing_code` TDD 경고 형식 | 경고 파싱 일관성 |

---

## 7. 종합 결론 및 다음 단계

### 이 작업 단계에서 확립된 것

```
문제 정의 (보고서 01)
  → "조건이 성립할 때 성공"을 정의했다
        ↓
아키텍처 설계 (보고서 02)
  → 그 조건을 레이어별 계약과 테스트로 변환했다
        ↓
.cursorrules 작성 (이 보고서)
  → 그 계약을 AI가 자동으로 따르는 규칙으로 변환했다
        ↓
다음: TDD RED 단계
  → 규칙을 따르는 AI와 함께 테스트를 먼저 작성한다
```

### 이 설계가 해결한 4가지 문제

| 이전 문제 | 해결 방식 |
|-----------|----------|
| AI가 설계 문서를 참조하지 않고 코드 생성 | `project.invariants` + `architecture` 섹션으로 컨텍스트 자동 주입 |
| TDD 순서 위반 코드 생성 | `ai_behavior.while_writing_code` TDD 위반 경고 메커니즘 |
| 레이어 경계를 넘는 import 생성 | `forbidden[4]` + `architecture.forbidden_dependencies` 이중 방어 |
| 타입힌트·docstring 누락 코드 생성 | `code_style` 규칙 + `ai_behavior` 자가 검토 규칙 동시 적용 |

### 다음 단계

| 단계 | 내용 | 입력 |
|------|------|------|
| **STEP 6** | RED 단계 — Domain 테스트 29개 작성 (실패 상태) | `.cursorrules` + 보고서 02의 Domain API 계약 |
| **STEP 7** | GREEN 단계 — Domain 구현체 작성 | RED 단계 테스트 |
| **STEP 8** | RED 단계 — UI Boundary 테스트 19개 작성 | `.cursorrules` + 보고서 02의 UI 계약 |
| **STEP 9** | GREEN 단계 — UI 구현체 작성 | UI RED 단계 테스트 |
| **STEP 10** | Data Layer 테스트 + 구현 | `.cursorrules` + 보고서 02의 Data 계약 |
| **STEP 11** | 통합 테스트 10개 작성 + 통과 | 모든 하위 레이어 완료 후 |
| **STEP 12** | Refactor — 커버리지 목표 달성 검증 | 전체 71개 테스트 GREEN |
