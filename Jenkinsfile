pipeline {
    agent any
    
    environment {
        REGISTRY = 'ghcr.io'
        GITHUB_USER = 'dsandreev620'
        IMAGE_NAME = "${GITHUB_USER}/jenkins-docker-demo"
        DOCKER_HOST = 'npipe:////./pipe/docker_engine'
        CONTAINER_NAME = 'my-demo-app'
    }

    stages {
        stage('Lint (Проверка кода)') {
            steps {
                echo 'Запуск flake8 для проверки стиля кода внутри контейнера...'
                // Запускаем временный контейнер, монтируем текущую папку и выполняем проверку
                script {
                    bat "docker run --rm -v \"%cd%\":/app -w /app python:3.11-slim sh -c \"pip install flake8 && flake8 src/ app.py --count --select=E9,F63,F7,F82 --show-source --statistics\""
                }
            }
        }

        stage('Unit Tests (Юнит-тесты)') {
            steps {
                echo 'Запуск pytest внутри контейнера...'
                script {
                    bat "docker run --rm -v \"%cd%\":/app -w /app python:3.11-slim sh -c \"pip install -r requirements.txt && python -m pytest tests/ -v\""
                }
            }
        }

        stage('Build (Сборка образа)') {
            steps {
                echo 'Сборка Docker-образа...'
                script {
                    def imageTag = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_ID}"
                    bat "docker build -t ${imageTag} ."
                }
            }
        }

        stage('Publish (Публикация в реестр)') {
            steps {
                echo 'Публикация образа в ghcr.io...'
                script {
                    def imageTag = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_ID}"
                    def latestTag = "${env.REGISTRY}/${env.IMAGE_NAME}:latest"

                    withDockerRegistry([credentialsId: 'GHCR_CREDS', url: 'https://ghcr.io']) {
                        bat "docker push ${imageTag}"
                        bat "docker tag ${imageTag} ${latestTag}"
                        bat "docker push ${latestTag}"
                    }
                }
            }
        }

        stage('Deploy (Развертывание)') {
            steps {
                echo 'Развертывание приложения в контейнере...'
                script {
                    def imageTag = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_ID}"
                    
                    // Останавливаем и удаляем старый контейнер, если он был запущен
                    bat "docker rm -f ${env.CONTAINER_NAME} || exit 0"
                    
                    // Запускаем новый контейнер в фоновом режиме с пробросом порта 5000
                    bat "docker run -d --name ${env.CONTAINER_NAME} -p 5000:5000 ${imageTag}"
                    
                    echo "Приложение успешно развернуто на http://localhost:5000"
                }
            }
        }
    }

    post {
        always {
            echo 'Отправка уведомления...'
            script {
                def buildStatus = currentBuild.currentResult
                def subject = buildStatus == 'SUCCESS' 
                    ? "УСПЕХ: Сборка #${env.BUILD_NUMBER}" 
                    : "ОШИБКА: Сборка #${env.BUILD_NUMBER}"
                
                def body = buildStatus == 'SUCCESS'
                    ? "<h2>Сборка успешна!</h2><p>Приложение: http://localhost:5000</p><p><a href='${env.BUILD_URL}'>Детали</a></p>"
                    : "<h2>Ошибка!</h2><p>Статус: ${buildStatus}</p><p><a href='${env.BUILD_URL}console'>Логи</a></p>"

                withCredentials([string(credentialsId: 'RESEND_API_KEY', variable: 'RESEND_KEY')]) {
                    powershell """
                        \$headers = @{'Authorization'='Bearer \$env:RESEND_KEY'; 'Content-Type'='application/json'}
                        \$body = @{'from'='CI/CD <onboarding@resend.dev>'; 'to'=@('dmitry.andreev620@gmail.com'); 'subject'='${subject}'; 'html'='${body}'} | ConvertTo-Json
                        Invoke-RestMethod -Uri 'https://api.resend.com/emails' -Method Post -Headers \$headers -Body \$body
                    """
                }
            }
        }
    }
}