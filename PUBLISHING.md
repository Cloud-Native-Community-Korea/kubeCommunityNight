# 발표 자료 웹 공개 (GitHub Pages)

이 저장소의 `.pptx` 발표 자료를 웹 슬라이드로 공개합니다.
슬라이드는 이미지로 변환되어 `docs/`에 담기고, GitHub Pages가 정적 사이트로 서빙합니다.

- 랜딩(회차 목록): `docs/index.html`
- 프레젠테이션 뷰어: `docs/viewer.html?event=<id>` (화살표/클릭 넘김, 전체화면, PPTX 다운로드)
- 변환 스크립트: `build_site.py`  ·  회차 목록: `events.config.json`
- 자동 변환: `.github/workflows/build-pages.yml`

공개 후 주소(프로젝트 페이지):
```
https://cloud-native-community-korea.github.io/kubeCommunityNight/
```

## 1. 최초 1회 설정

1. 변경사항을 커밋·푸시합니다.
   ```bash
   git add docs build_site.py events.config.json .github PUBLISHING.md
   git commit -m "feat: publish slides as a web site"
   git push
   ```
2. GitHub 저장소 → **Settings → Pages**
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` / 폴더 `/docs` → **Save**
3. GitHub 저장소 → **Settings → Actions → General → Workflow permissions**
   - **Read and write permissions** 선택 → Save
   - (자동 변환 워크플로가 갱신된 슬라이드를 커밋할 수 있도록)

1~2분 뒤 위 주소에서 확인할 수 있습니다.

## 2. 다음 회차(2회·3회) 추가하기

새 발표 자료(`.pptx`)를 저장소에 올리고, `events.config.json`에 한 줄 추가한 뒤 푸시하면 끝입니다.
GitHub Action이 자동으로 슬라이드를 만들어 `docs/`를 갱신합니다.

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

## 로컬에서 직접 빌드(선택)

LibreOffice + poppler + 한글 폰트가 있으면 직접 생성할 수 있습니다.
```bash
python3 build_site.py        # docs/events/<id>/slides/*.png 생성
# 미리보기
cd docs && python3 -m http.server 8000   # http://localhost:8000
```
