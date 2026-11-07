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
                    
                    // Аутентификация
                    bat "docker login ${env.REGISTRY} -u ${env.GITHUB_USER} -p ${env.GITHUB_TOKEN}"
                    
                    // ДОБАВЛЕН ФЛАГ --max-concurrent-uploads=1
                    bat "docker push --max-concurrent-uploads=1 ${imageTag}"
                    
                    // Пометка и отправка latest
                    bat "docker tag ${imageTag} ${latestTag}"
                    bat "docker push --max-concurrent-uploads=1 ${latestTag}"
                    
                    bat "docker logout ${env.REGISTRY}"
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