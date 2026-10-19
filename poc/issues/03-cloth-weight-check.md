# 웨이트 전송 후 옷 몸통 웨이트 점검

| 항목 | 값 |
| --- | --- |
| 報告の種類 / Type | 改善案 / Suggestion |
| キットの版 / Kit version | 1.0.4 |
| OS・ブラウザ / OS and browser | Windows 10 / Chrome |
| エージェント・モデル・工程 / Agent, model and stage | Codex(모델 기입) / 리깅·웨이트 전송 |

## 行った操作・提案 / Steps or proposal
Tripo 리깅 후 몸 웨이트를 옷(후디)에 전송했다. 제안: 전송 직후 높이별 우세 본을 검사해 몸통 정점이 다리 본에 묶였는지 경고한다.

## 期待した結果 / Expected result
후디 몸통은 spine/chest 계열 본을 따른다.

## 実際の結果 / Actual result
후디 옆구리 약 70%, 아랫단 100%가 upper_leg에 연결돼 걸을 때 상하체가 어긋났다.

## 첨부
- 걷기 자세 전/후: [`../images/03-hoodie-hem-weight.png`](../images/03-hoodie-hem-weight.png) — 전: 아랫단이 들린 다리를 따라 올라감, 후: 몸통 본으로 옮긴 뒤.
- 점검 예시: [`../tools/weight_check.py`](../tools/weight_check.py) — 엉덩이보다 위에 있는 상체 재질의 정점 중 다리 본이 우세한 비율을 본다.
  수정 전 파일 18%(z 0.7~0.8에 집중) → 경고, 수정 후 0% → 통과.
