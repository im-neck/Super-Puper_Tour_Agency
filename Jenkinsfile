pipeline {
  agent any

  environment {
    IMAGE_NAME = "super-puper-tour-agency"
    CONTAINER_NAME = "spa"
    ENV_FILE = ".env"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

//     stage('Tests') {
//   steps {
//     sh '''
//       if [ -d "tests" ]; then
//         docker run --rm -v "$PWD":/app -w /app python:3.11-slim \
//           sh -c "pip install -r requirements.txt && pytest -q"
//       else
//         echo "No tests/ directory found; skipping tests."
//       fi
//     '''
//   }
// }


    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
      }
    }

    stage('Run Container') {
      steps {
        sh '''
          if [ ! -f "${ENV_FILE}" ]; then
            echo "Missing ${ENV_FILE}. Create it in repo root."
            exit 1
          fi
          docker stop ${CONTAINER_NAME} || true
          docker rm ${CONTAINER_NAME} || true
          docker run -d --name ${CONTAINER_NAME} -p 8000:8000 --env-file ${ENV_FILE} ${IMAGE_NAME}:latest
        '''
      }
    }
  }
}
