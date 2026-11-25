# Streamlit → GitHub → Google Cloud Run 실습

Python Streamlit으로 월 지출 대시보드를 만들고 Google Cloud Run에 배포합니다.

## 1. 파일 구조

```text
streamlit-cloudrun-lab/
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .dockerignore
└── README.md
```

## 2. 로컬 실행 (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

브라우저에서 http://localhost:8501 접속. 종료는 Ctrl+C.

Windows PowerShell에서는 가상환경 활성화: `.venv\Scripts\Activate.ps1`.

## 3. GitHub에 업로드

GitHub 웹사이트에서 `streamlit-cloudrun-lab` 이름의 빈 저장소를 먼저 만듭니다(README 자동 생성 해제).

```bash
git init
git add .
git commit -m "Initial Streamlit app"
git branch -M main
git remote add origin https://github.com/USERNAME/streamlit-cloudrun-lab.git
git push -u origin main
```

`USERNAME`을 GitHub 사용자명으로 바꾸세요. GitHub 인증은 브라우저/credential manager 또는 토큰 방식으로 수행합니다.

## 4. Google Cloud Run 배포

Google Cloud 프로젝트 생성, 결제 계정 연결 및 gcloud CLI 설치가 필요합니다. Cloud Shell을 사용하면 로컬 CLI 설치를 생략할 수 있습니다.

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

gcloud run deploy streamlit-expense-demo \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 1
```

`YOUR_PROJECT_ID`는 실제 GCP 프로젝트 ID로 바꾸세요. 필요하면 배포 과정에서 API/권한 승인 메시지가 표시됩니다. 배포 완료 후 출력된 Service URL에 접속합니다. 일부 조직 정책에서는 공개 접근이 제한될 수 있습니다.

## 5. 수정 후 재배포

```bash
git add .
git commit -m "Update dashboard"
git push

gcloud run deploy streamlit-expense-demo --source . --region asia-northeast3 --allow-unauthenticated --memory 512Mi --min-instances 0 --max-instances 1
```

**중요:** 위 방식에서 GitHub push는 자동으로 Cloud Run에 반영되지 않습니다. `gcloud run deploy`를 다시 실행해야 합니다. GitHub → Cloud Run 자동 배포는 별도 CI/CD 실습입니다.

## 6. 비용 주의 및 정리

Cloud Run 자체 외에 Cloud Build 및 Artifact Registry 비용이 발생할 수 있으며 무료 사용량은 계정과 사용량에 따라 달라집니다. 사용하지 않는 서비스는 삭제합니다.

```bash
gcloud run services delete streamlit-expense-demo --region asia-northeast3
```

Cloud Run 서비스 삭제와 별개로 Artifact Registry에 빌드 이미지가 남을 수 있으므로 추가로 확인하세요.
