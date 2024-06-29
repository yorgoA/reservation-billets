# Système de Réservation de Billets

## Analyse des Défis Rencontrés

### Gestion des ressources distribuées
Le système doit coordonner plusieurs composants distribués :
- **MySQL**: Utilisé pour stocker les données principales des événements, des utilisateurs et des réservations.
- **Etcd**: Utilisé pour le verrouillage afin de gérer les réservations concurrentes.
- **Redis**: Utilisé pour le caching des données d'événements afin d'améliorer les performances en réduisant les requêtes à la base de données.

### Verrouillage des réservations concurrentes
L'un des défis majeurs était d'éviter les réservations concurrentes pour un même événement. Pour résoudre cela, le système utilise Etcd pour acquérir un verrou avant de traiter une réservation. Cela garantit qu'une seule réservation peut être traitée à la fois pour un événement spécifique, assurant la cohérence des données.

### Performances et Scalabilité
Pour améliorer les performances, le système utilise Redis pour le caching des données d'événements. Cela réduit la latence en permettant au système de récupérer rapidement les données d'événements fréquemment demandées sans interroger directement la base de données. De plus, le système est conçu pour être scalable en utilisant des conteneurs Docker et Docker Compose, permettant une gestion efficace des ressources et une évolutivité horizontale.

## Solutions Apportées

### Utilisation de Docker et Docker Compose
Pour simplifier le déploiement et la gestion des dépendances, le système est conteneurisé avec Docker. Docker Compose est utilisé pour orchestrer les conteneurs MySQL, Etcd, Redis et l'application Flask, assurant une configuration et une mise en réseau cohérentes.

### Verrouillage avec Etcd
Pour gérer les réservations concurrentes, le système utilise Etcd pour l'acquisition de verrous distribués. Avant de traiter une réservation, un verrou est placé sur l'événement concerné dans Etcd. Cela empêche plusieurs utilisateurs de réserver les mêmes billets simultanément.

### Caching avec Redis
Les données d'événements sont mises en cache dans Redis pour réduire la charge sur la base de données. Les informations sur les événements sont stockées en mémoire et mises à jour périodiquement pour refléter les changements dans la base de données.

## Performances du Système

Le système de réservation de billets a démontré les performances suivantes :
- **Latence réduite**: Grâce à l'utilisation de Redis pour le caching, les requêtes d'événements sont traitées plus rapidement.
- **Scalabilité**: Le système est capable de gérer un nombre croissant de réservations et d'utilisateurs grâce à son architecture basée sur des conteneurs et à l'utilisation de technologies distribuées comme Etcd et Redis.
- **Fiabilité**: Les tests automatisés avec pytest assurent que les fonctionnalités critiques comme la réservation de billets et la récupération de données fonctionnent correctement.

## Exemple d'Utilisation du Système

Pour utiliser le système de réservation de billets :
1. Assurez-vous que Docker et Docker Compose sont installés sur votre machine.
2. Clonez le dépôt GitHub du projet.
3. Naviguez vers le répertoire racine du projet et exécutez `docker-compose up --build` pour construire et démarrer les conteneurs.
4. Une fois les conteneurs démarrés, l'application est accessible à l'adresse http://localhost:8080.
5. Utilisez les endpoints HTTP définis (`/users`, `/events`, `/reserve`, `/reservations`, etc.) pour interagir avec le système de réservation de billets.

Ce projet a été développé par Yorgo Aoun et Bruno Megharba.


