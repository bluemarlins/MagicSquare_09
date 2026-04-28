# 4×4 Magic Square — RED 테스트 구현 보고서

---

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 Magic Square — 두 빈칸 완성 시스템 |
| **보고서 유형** | RED 테스트 스켈레톤 구현 및 실행 검증 보고서 |
| **작성일** | 2026-04-28 |
| **분석/작업 대상** | `docs/TestCases.md` · `Report/08_MagicSquare_TestCase_Report.md` · `tests/` |
| **목적** | 문서 기반 RED 원칙을 코드 테스트 스위트에 반영하고, 실패 상태를 실행으로 검증 |
| **산출물** | `tests/` 하위 RED 테스트 6개 파일(총 45 테스트) |

---

## 목차

1. [작업 배경](#1-작업-배경)
2. [적용한 RED 원칙](#2-적용한-red-원칙)
3. [문서 반영 내역](#3-문서-반영-내역)
4. [RED 테스트 구현 내역](#4-red-테스트-구현-내역)
5. [실행 검증 결과](#5-실행-검증-결과)
6. [사용자 실행 가이드 전달 내용](#6-사용자-실행-가이드-전달-내용)
7. [후속 단계 제안](#7-후속-단계-제안)

---

## 1. 작업 배경

이번 채팅에서는 사용자 요청에 따라 다음 흐름으로 작업을 진행했다.

1) 저장소의 테스트 프레임워크 확인  
2) 문서에 RED 스켈레톤 허용 규칙 반영  
3) 문서 기반 RED 테스트 케이스를 실제 `pytest` 코드로 생성  
4) `pytest` 실행으로 의도된 실패(RED) 상태 검증  
5) 사용자가 로컬에서 직접 실행할 수 있도록 환경 구성/실행 커맨드 안내

프레임워크는 문서 및 저장소 설정 기준으로 `pytest`를 사용했다.

---

## 2. 적용한 RED 원칙

다음 원칙을 기준으로 RED 테스트를 작성했다.

- 테스트 파일/클래스/함수 이름만 먼저 확정한 스켈레톤도 RED로 인정
- 테스트 본문은 구현 전 실패를 명시하기 위해 1줄 실패 단언 사용
  - `pytest.fail("RED: ... not implemented yet")`
  - (대안) `assert True is False`
- GREEN/REFACTOR 및 도메인 구현 본문은 본 단계 범위에서 제외

---

## 3. 문서 반영 내역

### 3.1 `docs/TestCases.md`

- 상단에 `문서 작성 원칙 (RED)` 섹션 추가
- `pytest` 기준 스켈레톤 RED 허용 규칙 명시
- 1줄 실패 단언 허용(`pytest.fail(...)` 또는 `assert True is False`) 명시

### 3.2 `Report/08_MagicSquare_TestCase_Report.md`

- §12.3(RED 단계 범위 명시) 표에 아래 허용 항목 추가
  - 파일/클래스(또는 함수) 이름 중심 최소 스켈레톤
  - 본문 1줄 실패 단언(`pytest.fail(...)` 또는 `assert True is False`)

---

## 4. RED 테스트 구현 내역

문서의 `TC-MS-*`, `UI-*`, `L-*`, `TASK-001-1`를 테스트 함수명에 직접 매핑해 스켈레톤을 생성했다.

### 4.1 생성 파일 목록

- `tests/entity/test_domain_constants.py`
- `tests/entity/test_blank_finder_red.py`
- `tests/entity/test_magic_square_validator_red.py`
- `tests/entity/test_solving_strategy_red.py`
- `tests/boundary/test_input_validator_red.py`
- `tests/boundary/test_solution_contract_red.py`

### 4.2 테스트 개수 집계

| 파일 | 테스트 수 |
|------|:---------:|
| `tests/entity/test_domain_constants.py` | 1 |
| `tests/entity/test_blank_finder_red.py` | 8 |
| `tests/entity/test_magic_square_validator_red.py` | 10 |
| `tests/entity/test_solving_strategy_red.py` | 14 |
| `tests/boundary/test_input_validator_red.py` | 10 |
| `tests/boundary/test_solution_contract_red.py` | 2 |
| **합계** | **45** |

### 4.3 범위 매핑 요약

- **TC 그룹 A**: `find_blank_coords` 관련 RED 5건 + L-01 시리즈
- **TC 그룹 B**: `is_magic_square` 관련 RED 5건 + L-03 시리즈
- **TC 그룹 C**: `solution`/경계값 RED 8건 + L-02, L-04 시리즈
- **TC 그룹 D**: `InputValidator` 오류 예외 RED 6건 + UI-01~04
- **UI 계약 RED**: UI-05~06 별도 파일로 분리
- **README TASK**: `TASK-001-1 test_domain_constants` RED 스켈레톤 추가

---

## 5. 실행 검증 결과

### 5.1 실행 명령

```bash
python -m pytest tests -q
```

### 5.2 결과 요약

- 실행 결과: **45 failed**
- 실패 유형: 모든 테스트가 의도된 `pytest.fail("RED: ...")`로 실패
- 해석: RED 단계 진입 조건(실패 테스트 선행) 충족
- 린트 상태: `tests/` 기준 linter 오류 없음

---

## 6. 사용자 실행 가이드 전달 내용

사용자가 로컬에서 직접 실행할 수 있도록 다음 절차를 안내했다.

- PowerShell에서 작업 경로 이동
- 가상환경 생성/활성화(`.venv`)
- `pytest`, `pytest-cov`, `pytest-mock`, `pytest-benchmark` 설치
- 전체/영역/개별 테스트 실행 명령
- (선택) 커버리지 실행 명령
- 활성화 해제(`deactivate`)

---

## 7. 후속 단계 제안

다음 GREEN 전환은 테스트 폭이 가장 작은 항목부터 진행하는 것이 안전하다.

1. `test_domain_constants` 단독 GREEN (`entity/constants.py` 최소 구현)  
2. `test_blank_finder_red.py`의 A-001/A-002 우선 GREEN  
3. `InputValidator`의 UI-01~04, D-001~D-006 순차 GREEN  
4. `is_magic_square`와 `solution` 계열 GREEN 확장  
5. 각 단계마다 `pytest -k <대상>`으로 국소 확인 후 전체 회귀 실행

---

*본 보고서는 본 채팅 세션에서 수행한 RED 테스트 준비/구현/검증 작업만 다룬다.*  
