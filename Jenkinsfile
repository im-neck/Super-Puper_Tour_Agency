pipeline {
  agent any

  environment {
    IMAGE_NAME = "super-puper-tour-agency"
    CONTAINER_NAME = "spa-${BUILD_NUMBER}"
    PYTHON_IMAGE = "python:3.11.8-slim"
    APP_NAME = "Super Puper Tour Agency"
    DEBUG = "false"
    JWT_SECRET = "change-me"
    JWT_ALGORITHM = "HS256"
    API_VERSION = "v1"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Tests') {
      steps {
        sh '''
          if [ -d "tests" ]; then
            docker run --rm -v "$PWD":/app -w /app ${PYTHON_IMAGE} \
              sh -c "pip install -r requirements.txt && pytest -q"
          else
            echo "No tests/ directory found; skipping tests."
          fi
        '''
      }
    }


    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
      }
    }

    stage('Run Container') {
      steps {
        sh '''
          docker rm -f ${CONTAINER_NAME} || true
          docker run -d --name ${CONTAINER_NAME} -P \
            -e APP_NAME="${APP_NAME}" \
            -e DEBUG="${DEBUG}" \
            -e JWT_SECRET="${JWT_SECRET}" \
            -e JWT_ALGORITHM="${JWT_ALGORITHM}" \
            -e API_VERSION="${API_VERSION}" \
            ${IMAGE_NAME}:${BUILD_NUMBER}
          echo "Container ${CONTAINER_NAME} ports:"
          docker port ${CONTAINER_NAME}
        '''
      }
    }
  }
}
