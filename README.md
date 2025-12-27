## Автоматизация сборки и деплоя Python Docker-приложений через Jenkins с интеграцией GitHub
### Ход работы
#### Шаг 1. Клонирование репозитория
Выгрузила репозиторий с исходным кодом в свой репозиторий 
<img width="1170" height="684" alt="image" src="https://github.com/user-attachments/assets/5f233323-da93-49f4-a62b-ed71f2333edf" />

#### Шаг 2. Создание и конфигурирование Jenkins Job
Авторизовалась на Jenkins-сервере по указанному IP и порту.

В верхнем меню выбрала кнопку New Item для создания нового проекта.

Задала уникальное имя проекта — Anastasia Sharipova.

В списке типов проектов выбрала Pipeline и тыкнула OK.

В открывшемся окне перешела к разделу Pipeline:

В поле Definition выбрала Pipeline script.
В поле ниже вставила заготовленный Pipeline скрипт (Jenkinsfile), предоставленный преподавателем.
В Jenkinsfile отдельно отредактировала параметры:

В поле STUDENT_NAME указал своё имя — NastyaSharipova
В поле PORT указал уникальный порт - 8006
Сохранилa конфигурацию проекта.

#### Шаг 3. Структура Jenkinsfile

```
pipeline {
    agent any
    
    parameters {
        string(name: 'STUDENT_NAME', defaultValue: 'Nastya', description: 'Имя студента')
        string(name: 'PORT', defaultValue: '8006', description: 'Порт')
    }
    
    stages {
        stage('Удаляем старые контейнеры и образы') {
            steps {
                script {
                    // Останавливаем и удаляем контейнер с нужным именем, если он есть
                    sh "docker ps -a -q --filter name= hello-sharipovanasytya-container | xargs -r docker rm -f"
                    // Удаляем образ с нужным именем, если он есть
                    sh "docker images -q student-sharipovanasytya-app | xargs -r docker rmi -f"
                }
            }
        }
        stage('Выгружаем код из репозитория') {
            steps {
                git 'https://github.com/avopani/laba2.git'
            }
        }
        stage('Собираем docker image') {
            steps {
                script {
                    dockerImage = docker.build("student-sharipovanasytya-app")
                }
            }
        }
        stage('Запускаем тесты в докере') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'python -m unittest test_app.py'
                    }
                }
            }
        }
        stage('Запускаем докер контейнер') {
            steps {
                script {
                    sh "docker run -d --name hello-sharipovanasytya-container -p ${params.PORT}:${params.PORT} -e STUDENT_NAME='${params.STUDENT_NAME}' -e PORT=${params.PORT} student-sharipovanasytya-app"
                }
            }
        }
    }
}
```

#### Шаг 4. Настройка GitHub webhook для автоматического запуска сборки
Перешела в репозиторий на GitHub.

Во вкладке Settings выбрала пункт Webhooks.

Нажала кнопку Add webhook.

В поле Payload URL ввела адрес Jenkins вебхука:
http://158.160.194.244:8080/github-webhook/

В поле Content type выбрала application/json.

В разделе Which events would you like to trigger this webhook? выбрала Just the push event.

Подтвердила добавление вебхука.

#### Шаг 5. Работа с Jenkins и проверка
В интерфейсе Jenkins открыла созданную job.

Нажала кнопку Build Now, чтобы инициировать первую сборку.

Проверила, что приложение собрано

Открыла приложение в браузере по адресу: http://158.160.194.244:8006

<img width="1919" height="972" alt="image" src="https://github.com/user-attachments/assets/4c8273c3-0351-41b1-8768-b7677b301fe5" />

Изменила в файле index.html цвет текста на красный. Снова инициировала сборку, появилось окошко.




