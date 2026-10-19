# 치마 스프링 체인 수 기본값 상향

| 항목 | 값 |
| --- | --- |
| 報告の種類 / Type | 改善案 / Suggestion |
| キットの版 / Kit version | 1.0.4 |
| OS・ブラウザ / OS and browser | Windows 10 / Chrome |
| エージェント・モデル・工程 / Agent, model and stage | Codex(모델 기입) / 흔들리는 부위 |

## 行った操作・提案 / Steps or proposal
치마를 8줄 스프링 체인으로 설정했다. 제안: 기본 줄 수를 16 이상으로 하거나 다리 추종 웨이트와 혼합을 허용한다. 허벅지·어깨 캡슐 충돌체 템플릿도 함께 제공한다.

## 期待した結果 / Expected result
걷거나 앉을 때 치마 주름이 붙어서 움직인다.

## 実際の結果 / Actual result
줄끼리 독립이라 주름 사이가 벌어진다. 다리 추종만 쓰면 키트 검사가 거부한다(흔들림 본 연결 필수). 구 충돌체 하나로는 허벅지를 막지 못한다.

## 첨부
- 충돌체 템플릿 예시: [`../tools/collider_template.py`](../tools/collider_template.py) — 허벅지·목-어깨·윗팔 캡슐과 윗가슴 구를 hips 높이 비례로 만든다.
- 치마 전/후 렌더는 개선이 분명한 쌍이 없어 아직 넣지 않았다.
