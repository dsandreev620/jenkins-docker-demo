pipeline {
    agent any
    
    environment {
        REGISTRY = 'ghcr.io'
        // ЗАМЕНИТЕ на ваш логин GitHub (строго в нижнем регистре!)
        GITHUB_USER = 'ваш_логин' 
        IMAGE_NAME = "${GITHUB_USER}/jenkins-docker-demo"
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
                    // Используем bat для гарантированной работы в Windows
                    bat "docker build -t ${imageTag} ."
                }
            }
        }

        stage('Run Tests in Container') {
            steps {
                echo 'Запуск тестов внутри контейнера...'
                script {
                    def imageTag = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_ID}"
                    // --rm удаляет контейнер после завершения
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
                    
                    // Аутентификация в ghcr.io
                    bat "docker login ${env.REGISTRY} -u ${env.GITHUB_USER} -p ${env.GITHUB_TOKEN}"
                    
                    // Отправка образа с номером сборки
                    bat "docker push ${imageTag}"
                    
                    // Пометка образа как latest и отправка
                    bat "docker tag ${imageTag} ${latestTag}"
                    bat "docker push ${latestTag}"
                    
                    // Завершение сессии
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
