# Magic Square training system user journey
_Exported on 4/27/2026 at 17:19:09 GMT+9 from Cursor (3.2.11)_

---

**User**

Level 1: Epic (비즈니스 목표): EPIC — Business Goal
```
Magic Square를 위한 사용자 여정 작성 (Epic → User Story → Task)을 하고자 합니다.
먼저, Level 1: Epic (비즈니스 목표): EPIC — Business Goal에 대한 내용을 다음처럼 작성해 주세요.
Epic: “Invariant(불변조건) 기반 사고 훈련 시스템 구축”
목적
4x4 Magic Square 문제를 활용하여:
Invariant 중심 설계 사고 훈련
Dual-Track TDD 적용 훈련
입력/출력 계약 명확화 훈련
설계 → 테스트 → 구현 → 리팩토링 흐름 체화

성공 기준
Domain Logic 95% 이상 테스트 커버리지
입력 검증 100% 계약 테스트 통과
하드코딩 없음
매직 넘버 없음
Invariant → Test 추적 가능
```
Level 2: User Journey (사용자 여정) 例1
```
Level 2: User Journey (사용자 여정)를 다음 내용처럼 작성해 주세요.
Persona
소프트웨어 개발 학습자
TDD 훈련 중
Clean Architecture 이해 중

Journey
Step 1 — 문제 인식
“마방진을 구현한다”가 아니라

Step 2 — 계약 정의
입력 스키마 정의
출력 스키마 정의
예외 정책 정의


Step 3 — Domain 분리
BlankFinder
MissingNumberFinder
MagicSquareValidator
Solver

Step 4 — Dual-Track 진행
UI RED / Logic RED 병렬
GREEN 최소 구현
REFACTOR 통합 정리

Step 5 — 회귀 보호
엣지 케이스 추가
입력 오류 케이스 추가
조합 실패 케이스 추가

```


---

**Cursor**

기존 문서 구조와 포맷을 먼저 확인하겠습니다.

기존 문서 포맷을 파악했습니다. 이제 새 문서를 작성하겠습니다.

이제 Epic + User Journey 문서를 작성하겠습니다.

문서가 생성되었습니다. 작성된 내용을 확인합니다.

353줄 분량의 문서가 완성되었습니다.

---

`c:\DEV\MagicSquare\Design\04_MagicSquare_Epic_UserJourney_Design.md` 파일이 생성되었습니다.

---

## 작성 내용 요약

### Level 1 — Epic: "Invariant 기반 사고 훈련 시스템 구축"

| 섹션 | 내용 |
|------|------|
| **1.1 목적** | 훈련 목표 4가지를 표로 정리 (핵심 질문 포함) |
| **1.2 성공 기준** | SC-01~SC-08, 각 기준마다 목표값 + 측정 방법 명시 |
| **1.3 Epic 범위** | In-Scope / Out-of-Scope 명확히 구분 |
| **1.4 Invariant 요약** | INV-01~INV-09 와 관련 레이어 매핑 |

### Level 2 — User Journey (5단계)

| Step | 이름 | 핵심 추가 내용 |
|------|------|----------------|
| **Step 1** | 문제 인식 | Before/After 사고 전환 표 + 체크포인트 |
| **Step 2** | 계약 정의 | 입력 스키마, 출력 스키마(`int[6]`), 예외 정책 7종을 표로 명세 |
| **Step 3** | Domain 분리 | ECB 의존성 방향 다이어그램 + "잘못된 설계" 역예시 |
| **Step 4** | Dual-Track 진행 | Track A(UI) / Track B(Domain) 병렬 구조, RED/GREEN/REFACTOR 규칙표, 71개 테스트 배분 |
| **Step 5** | 회귀 보호 | 엣지 케이스, 입력 오류 케이스, 조합 실패 케이스 + 실행 체크리스트 (`pytest`, `rg` 명령 포함) |

마지막에 **여정 전체 요약 표**와 **"다음 단계: Level 3 — User Story"** 안내를 추가하였습니다.

---

**User**

해당 작업에 대한 보고서를 @Report/ 에 작성해줘

---

**Cursor**

기존 보고서 포맷을 참고하겠습니다.

설계 문서와 기존 보고서 포맷을 모두 확인했습니다. 이제 보고서를 작성합니다.

`Report/04_MagicSquare_Epic_UserJourney_Report.md` (349줄)가 완성되었습니다.

---

## 보고서 작성 내용 요약

### 전체 구조 (6개 섹션)

| 섹션 | 내용 |
|------|------|
| **1. 작업 배경** | 보고서 01~03과의 연결 관계, Epic·Journey가 필요한 이유 |
| **2. Level 1 — Epic 설계 결정** | Epic 명칭 결정 근거, 훈련 목표 4가지, SC-01~SC-08 설계 원칙, In/Out-of-Scope 배제 근거 |
| **3. Level 2 — Journey 설계 결정** | Persona 정의 근거, 5단계 구조 결정 이유, 각 Step별 핵심 설계 포인트 |
| **4. 일관성 검토** | 7개 항목(Invariant·테스트 수·에러 코드·검증 순서·레이어·커버리지·출력 포맷) 전부 ✅ 일치 확인 |
| **5. 산출물 요약** | 설계 문서 트리 구조, 핵심 숫자 요약 표, 보고서 01→04 연결 관계 다이어그램 |
| **6. 결론 및 다음 단계** | 이번 보고서에서 확립한 것 정리, Level 3 User Story 분해 방향 및 예상 분포 제시 |

기존 보고서 포맷(헤더 메타 테이블 → 목차 → 섹션별 설계 결정 → 검토 → 결론)을 그대로 유지하면서, **"왜 이런 결정을 내렸는가"** 를 중심으로 서술하였습니다.

