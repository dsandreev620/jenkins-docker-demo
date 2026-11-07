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

                    // Безопасно внедряем токен как переменную окружения CMD
                    withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GHCR_TOKEN')]) {
                        
                        // 1. Записываем токен в файл. Синтаксис echo("...") защищает от спецсимволов в Windows
                        bat "echo(\"%GHCR_TOKEN%\" > temp_token.txt"
                        
                        // 2. Передаем содержимое файла в docker login
                        bat "docker login ${env.REGISTRY} -u ${env.GITHUB_USER} --password-stdin < temp_token.txt"
                        
                        // 3. Пушим образы (здесь нет секретов, поэтому обычная интерполяция ${env...} безопасна)
                        bat "docker push ${imageTag}"
                        bat "docker tag ${imageTag} ${latestTag}"
                        bat "docker push ${latestTag}"
                        
                        // 4. Очистка
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