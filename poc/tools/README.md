# 보조 스크립트

키트 코드를 복사하거나 불러오지 않고 새로 쓴 Blender 스크립트다. Blender 5.2 + VRM Add-on에서 확인했다.
키트의 작업 파일(`character.blend`)을 직접 고치지 말고, 복사본에 쓰거나 `--out`으로 새 파일에 저장한다.

| 파일 | 하는 일 | 확인 결과 |
| --- | --- | --- |
| [`weight_check.py`](weight_check.py) | 웨이트 전송 후 상체 재질(정점 중앙값이 hips보다 위)의 정점 중 다리 본이 우세한 비율을 재고, `--limit`(기본 5%)을 넘으면 경고한다. 높이 0.1 단위로 어디에 몰렸는지 보여 준다. | 후디 아랫단이 다리에 묶인 파일: 18% → WARN, exit 1. 고친 파일: 0% → OK. |
| [`collider_template.py`](collider_template.py) | VRM 1.0 스프링 충돌체 템플릿. 허벅지 캡슐(`Tmpl_Legs` → 치마 체인), 목-어깨·윗팔 캡슐과 윗가슴 구(`Tmpl_Torso` → 머리카락 체인)를 humanoid 본 기준·hips 높이 비례로 만든다. | PoC에서 손으로 맞춘 값과 1cm 안쪽으로 일치. 목-어깨 캡슐 끝점만 약 3cm 낮다. 같은 파일에 두 번 실행하면 멈춘다. |

```text
blender -b character.blend --python weight_check.py -- --json weight.json
blender -b character.blend --python collider_template.py -- --out character_colliders.blend --radius 0.9
```

Blender MCP 등으로 열린 Blender 안에서 실행하면 인자 없이 현재 장면을 대상으로 한다(충돌체 템플릿은 저장하지 않음).

## 한계

- 상체·하체가 재질로 나뉜 Tripo 출력 기준이다. 상체 옷과 다리가 한 재질이면 `weight_check`가 상체 재질로 인식하지 못한다.
- 충돌체 크기는 넓은 후디로 맞춘 값이다. 몸에 붙는 옷이면 `--radius 0.8` 정도로 줄인다.
- 스프링 이름 접두사(`Skirt_`, `Hair_`)가 다르면 `--skirt-prefix`, `--hair-prefix`로 지정한다.
