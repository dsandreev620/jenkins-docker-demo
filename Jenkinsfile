pipeline {
    agent any
    
    environment {
        REGISTRY = 'ghcr.io'
        GITHUB_USER = 'dsandreev620'
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

                    // Используем чистый PowerShell, так как он у вас уже работает вручную
                    withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GHCR_TOKEN')]) {
                        powershell """
                            # 1. Записываем токен в файл АБСОЛЮТНО чисто, без кавычек и переносов строки
                            [System.IO.File]::WriteAllText("\$PWD\\temp_token.txt", \$env:GHCR_TOKEN)
                            
                            # 2. Читаем файл как поток байтов и передаем в docker login (гарантирует отсутствие \r\n)
                            \$bytes = [System.Text.Encoding]::UTF8.GetBytes([System.IO.File]::ReadAllText("\$PWD\\temp_token.txt"))
                            \$stream = New-Object System.IO.MemoryStream(,\$bytes)
                            \$stream | docker login ghcr.io -u ${env.GITHUB_USER} --password-stdin
                            
                            # 3. Отправляем образы
                            docker push ${imageTag}
                            docker tag ${imageTag} ${latestTag}
                            docker push ${latestTag}
                            
                            # 4. Очистка
                            docker logout ghcr.io
                            Remove-Item "\$PWD\\temp_token.txt" -Force
                        """
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