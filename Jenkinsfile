pipeline {
    agent any
    
    environment {
        REGISTRY = 'ghcr.io'
        GITHUB_USER = 'dsandreev620'
        IMAGE_NAME = "${GITHUB_USER}/jenkins-docker-demo"
        // Явно извлекаем секрет из хранилища Jenkins по его ID
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Скачивание кода из репозитория...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Сборка Docker-образа...'
                script {
                    def imageTag = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_ID}"
                    bat "docker build -t ${imageTag} ."
                }
            }
        }

        stage('Run Tests in Container') {
            steps {
                echo 'Запуск тестов внутри контейнера...'
                script {
                    def imageTag = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_ID}"
                    bat "docker run --rm ${imageTag}"
                }
            }
        }

        stage('Push to GitHub Container Registry') {
            steps {
                echo 'Публикация образа в ghcr.io...'
                script {
                    def imageTag = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_ID}"
                    def latestTag = "${env.REGISTRY}/${env.IMAGE_NAME}:latest"

                    // Безопасно внедряем токен как переменную окружения
                    withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GHCR_TOKEN')]) {
                        
                        // 1. Записываем токен в файл БЕЗ кавычек и БЕЗ символа новой строки (решение проблемы CMD)
                        powershell '[System.IO.File]::WriteAllText("temp_token.txt", $env:GHCR_TOKEN)'
                        
                        // 2. Передаем чистый токен из файла в docker login через конвейер PowerShell
                        powershell 'Get-Content temp_token.txt | docker login ghcr.io -u dsandreev620 --password-stdin'
                        
                        // 3. Отправляем образ (здесь нет секретов, поэтому используем обычный bat)
                        bat "docker push ${imageTag}"
                        bat "docker tag ${imageTag} ${latestTag}"
                        bat "docker push ${latestTag}"
                        
                        // 4. Очистка
                        bat "docker logout ghcr.io"
                        powershell 'Remove-Item temp_token.txt -Force'
                    }
                    echo "Образ успешно опубликован: ${imageTag}"
                }
            }
        }
    }

    post {
        always {
            echo 'Пайплайн завершен.'
        }
        success {
            echo 'Все этапы выполнены успешно!'
        }
        failure {
            echo 'Ошибка в пайплайне. Проверьте логи консоли.'
        }
    }
}