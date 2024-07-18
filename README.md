# Django ve PostgreSQL ile İHA Kiralama Uygulaması

Bu proje, Django ve PostgreSQL kullanarak bir İHA kiralama uygulamasını Docker ile yapılandırmayı ve çalıştırmayı içermektedir.

## Gereksinimler

- Docker
- Docker Compose

## Kurulum

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/esadsen/django-IhaRental.git

```
### 2. Docker Ayarları ve Projeyi Çalıştırma

```bash
docker compose up --build
```

Daha sonra compose açık haldeyken şu kodu çalıştırın:
```bash
docker-compose exec db psql -U postgres

CREATE DATABASE iha_rental_db;

\q

```


Django veritabanı şemasını oluşturmak için migration komutlarını çalıştırın:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

Django geliştirme sunucusunu yeniden başlatın:

```bash
docker compose down
docker compose up
```

Uygulama linki:

```bash
http://localhost:8000
```



