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

                    // Безопасная передача токена через переменную окружения, а не интерполяцию строки
                    withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GHCR_TOKEN')]) {
                        // Хитрый трюк для Windows: записываем токен в файл БЕЗ перевода строки в конце
                        bat script: 'echo | set /p="%GHCR_TOKEN%" > temp_token.txt'
                        
                        // Передаем токен из файла в docker login
                        bat 'docker login ${env.REGISTRY} -u ${env.GITHUB_USER} --password-stdin < temp_token.txt'
                        
                        // Пушим образ
                        bat "docker push ${imageTag}"
                        bat "docker tag ${imageTag} ${latestTag}"
                        bat "docker push ${latestTag}"
                        
                        bat "docker logout ${env.REGISTRY}"
                        bat "del temp_token.txt"
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