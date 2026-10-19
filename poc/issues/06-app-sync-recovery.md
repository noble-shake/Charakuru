# 앱 연결 오류 시 복구 방법

| 항목 | 값 |
| --- | --- |
| 報告の種類 / Type | 不具合・失敗した工程 / Bug or unsuccessful workflow |
| キットの版 / Kit version | 1.0.4 |
| OS・ブラウザ / OS and browser | Windows 10 / Chrome |
| エージェント・モデル・工程 / Agent, model and stage | Codex(모델 기입) / 단계 요청 begin |

## 行った操作・提案 / Steps or proposal
앱에서 요청문을 복사해 에이전트에 보냈다. 요청을 만든 탭과 실제 연결의 client id가 어긋난 상태였다.

## 期待した結果 / Expected result
begin이 성공하거나, 실패 시 복구 방법(새 요청 생성 등)을 안내한다.

## 実際の結果 / Actual result
「最新状態を取得できませんでした」로 실패. 새 요청을 만들고 로컬 checkpoint를 감시해 우회했다.

## 첨부 예정
- 전/후 렌더 (개인 경로·계정 정보 제거 후)
