# 발표 자료 웹 공개 (GitHub Pages)

이 저장소의 `.pptx` 발표 자료를 웹 슬라이드로 공개합니다.
**GitHub Actions가 슬라이드를 이미지로 변환해 그대로 Pages로 배포**합니다.
생성물(슬라이드 PNG)은 저장소에 커밋하지 않으므로 로컬 작업과 충돌이 없습니다.

- 랜딩(회차 목록): `docs/index.html`
- 프레젠테이션 뷰어: `docs/viewer.html?event=<id>` (화살표/클릭 넘김, 전체화면, PPTX 다운로드)
- 룰렛: `docs/roulette.html`
- 변환 스크립트: `build_site.py`  ·  회차 목록: `events.config.json`
- 빌드+배포 워크플로: `.github/workflows/build-pages.yml`
- 생성물은 `.gitignore` 처리: `docs/events/`, `docs/events.json`

공개 후 주소(프로젝트 페이지):
```
https://cloud-native-community-korea.github.io/kubeCommunityNight/
```

## 1. 최초 1회 설정

1. (원격이 앞서 있으면 먼저 동기화)
   ```bash
   git pull --rebase
   ```
2. 이미 커밋돼 있던 생성물을 추적 해제하고 변경분을 커밋·푸시합니다.
   ```bash
   git rm -r --cached docs/events docs/events.json 2>/dev/null
   git add -A
   git commit -m "ci: deploy site via GitHub Actions; stop committing generated slides"
   git push
   ```
3. GitHub 저장소 → **Settings → Pages → Build and deployment**
   - **Source**: `GitHub Actions` 선택

푸시되면 워크플로가 슬라이드를 만들어 배포합니다(1~2분). 위 주소에서 확인하세요.

> 더 이상 "Workflow permissions: Read and write"는 필요 없습니다(봇이 커밋하지 않음).

## 2. 다음 회차(2회·3회) 추가하기

새 발표 자료(`.pptx`)를 저장소에 올리고 `events.config.json`에 한 줄 추가한 뒤 push하면 끝입니다.
워크플로가 자동으로 슬라이드를 만들어 배포합니다.

```jsonc
[
  { "id": "2", "no": 2, "title": "CNCK Kube Community Night",
    "subtitle": "", "date": "2026-09-XX", "pptx": "2회-자료.pptx" },
  { "id": "1", "no": 1, "title": "CNCK Kube Community Night",
    "subtitle": "w/ Kubestronaut", "date": "2026-06-12",
    "pptx": "cnck-kube-community-night.pptx" }
]
```

- `id`: URL/폴더 식별자(고유값), `no`: 회차 번호(목록 정렬 기준)
- `pptx`: 저장소 안 `.pptx` 파일 경로

## 로컬에서 미리보기(선택)

LibreOffice + poppler + 한글 폰트가 있으면 로컬에서 생성·미리보기할 수 있습니다.
생성물은 `.gitignore` 대상이라 커밋되지 않습니다.
```bash
python3 build_site.py                    # docs/events/<id>/slides/*.png 생성(로컬 전용)
cd docs && python3 -m http.server 8000   # http://localhost:8000
```
