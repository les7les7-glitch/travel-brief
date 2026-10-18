# 여행 브리핑

항공·호텔 프로그램의 프로모션, 퍼스트·비즈니스 새 좌석, 럭셔리 호텔 소식을 골라 한국어로 요약하고, 오늘의 여행지와 예산별 여행지를 보여주는 페이지예요. GitHub Pages로 공개돼 있고, Claude가 매일 아침 데이터를 갱신해요.

## 구성

- `index.html`: 페이지 전체(HTML·CSS·JS 한 파일). `data/` 폴더의 JSON을 읽어 그려요.
- `data/items.json`: 프로모션·항공·호텔 소식
- `data/pick.json`: 오늘의 여행지와 지난 추천
- `data/budget.json`: 예산으로 찾기에 쓰는 여행지별 예상 비용(만원 단위)
- `data/digest.json`: 갱신 시각과 오늘의 한 줄 요약
- `scripts/export_public.py`: 비공개 대시보드 데이터에서 공개용 사본을 만드는 스크립트. 개인 일정 관련 소식과 문장은 빼고 내보내요.
- `manifest.webmanifest`, `icons/`: 휴대폰 홈 화면에 추가했을 때 앱처럼 열리게 하는 설정

## 갱신

```
python3 scripts/export_public.py <비공개 데이터 폴더> data
git add data && git commit -m "데이터 갱신" && git push
```

가격과 조건은 조사한 날 기준 예상치예요. 예약 전에 각 카드의 출처에서 꼭 다시 확인하세요.
