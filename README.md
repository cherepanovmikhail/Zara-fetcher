# zara-fetcher

## Запуск приложения локально

Для запуска приложения требуется установить и настроить:

- docker-desktop по [мануалу](https://docs.docker.com/desktop/install/mac-install/)
- включить в docker-desktop локальный кластер kubernetes и настроить kubectl дл работы с ним по [мануалу](https://docs.docker.com/desktop/kubernetes/)
- установить helm по [мануалу](https://helm.sh/docs/intro/install/)

Если все прошло успешно то можно попробовать установить приложение в кластере с помощью команды:
`make install` запущенной из корня репозитория. Эта команда установит pstgresql как зависимость и накатит миграции.

Помле успешного запуска, helm выведет подсказку о том как можно получить доступ до сервиса:
```
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=zara-fetcher,app.kubernetes.io/instance=zara-fetcher" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
```

ЕЕ же можно получить позже выполнив `helm status zara-fetcher`

Выполнив инструкции можно зайти на страницу документации сервиса http://127.0.0.1:8080/docs

После того как приложение будет запущено, в Базе данных будет пусто, чтобы наполнить БД в первый раз можно руками запустить job по шаблону кронджобы, которая будет отрабатывать каждые 2 часа:

```
kubectl create job --from=cronjob/zara-fetcher zara-fetcher-cron-manual-001
```