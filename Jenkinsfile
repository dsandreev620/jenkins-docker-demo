pipeline {
    agent any
    
    environment {
        REGISTRY = 'ghcr.io'
        GITHUB_USER = 'dsandreev620'
        IMAGE_NAME = "${GITHUB_USER}/jenkins-docker-demo"
        // Переменная GITHUB_TOKEN удалена, так как мы используем withDockerRegistry
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

                    // ОФИЦИАЛЬНЫЙ метод Jenkins. Он сам безопасно управляет логином и логином.
                    withDockerRegistry([credentialsId: 'GHCR_CREDS', url: 'https://ghcr.io']) {
                        bat "docker push ${imageTag}"
                        bat "docker tag ${imageTag} ${latestTag}"
                        bat "docker push ${latestTag}"
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