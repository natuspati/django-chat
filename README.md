<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<a name="readme-top"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/natuspati/django-chat">
    <img src=frontend/public/random_logo.png alt="Logo" width="200" >
  </a>

<h3 align="center">Django Chat App</h3>

  <p align="center">
    Simple chat app build with Django channels and React.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Game</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project

Simple chat room, where a user types a username and can chat in a room.

Django channels is used to send messages asynchronously. Channel redis is used to store messages circumventing
costly database I/O operations.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

Back-end is built with Django, Django Rest Framework and Django Channels. Dockerized PostgreSQL and Redis
are spun up.

Front-end is built with React.

* [![Django][django.com]][Django-url]
* [![Django Rest Framework][DjangoRestFrameWork.com]][DjangoRestFrameWork-url]
* [![React][React.js]][React-url]
* [![Docker][Docker.com]][Docker-url]
* [![PostgreSQL][PostgreSQL.com]][PostgreSQL-url]
* [![Redis][Redis.com]][Redis-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

Docker and docker-compose must be installed. See here installation
instructions: [Get Docker](https://docs.docker.com/get-docker/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/natuspati/django-chat.git
   ```
2. Spin up docker containers
   ```sh
   docker-compose up -d --build
   ```
3. Migrate tables
   ```sh
   docker-compose exec backend python manage.py createmigrations
   docker-compose exec backend python manage.py migrate
   ```
4. Visit http://localhost/
5. To stop the containers, run
   ```shell
   docker-compose -f docker-compose.dev.yml down -v
   ```
   Remove dangling images and volumes to reduce used storage
   ```sh
   docker image prune
   docker volume prune
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

User enters a username and is able to send texts in the room. You can test it by opening
[localhost](localhost) on another browser.

<p float="left">
  <img src=frontend/public/default.png alt="Default" width="800" >
</p>



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Write message and chat endpoints
- [x] Add django channels and daphne to run asynchronous application
- [x] Configure front-end pipeline
- [x] Add channel redis to hasten message I/O operations
- [ ] Add tests to cover chat endpoints
- [ ] Add authentication service

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE.txt`](LICENSE.txt) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

Nurlat Bekdullayev - [@natuspati](https://twitter.com/natuspati) - natuspati@gmail.com

Project Link: [https://github.com/natuspati/django-chat](https://github.com/natuspati/django-chat)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Thanks to these resources that helped me to build the game.

* [Matthew Freire: Build a Chat App with Django Channels](https://justdjango.com/blog/chat-app-django-channels)
* [Wynn Teo: Building a Real-Time Chat Application with Django, Channels and React](https://blog.devgenius.io/building-a-real-time-chat-application-with-django-channels-and-react-ee2d8fee7328)
* [Othneil Drew: Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/natuspati/country-guess-game.svg?style=for-the-badge

[contributors-url]: https://github.com/natuspati/country-guess-game/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/natuspati/country-guess-game.svg?style=for-the-badge

[forks-url]: https://github.com/natuspati/country-guess-game/network/members

[stars-shield]: https://img.shields.io/github/stars/natuspati/country-guess-game.svg?style=for-the-badge

[stars-url]: https://github.com/natuspati/country-guess-game/stargazers

[issues-shield]: https://img.shields.io/github/issues/natuspati/country-guess-game.svg?style=for-the-badge

[issues-url]: https://github.com/natuspati/country-guess-game/issues

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://www.linkedin.com/in/nurlat/

[license-shield]: https://img.shields.io/github/license/natuspati/country-guess-game.svg?style=for-the-badge

[license-url]: https://github.com/natuspati/country-guess-game/blob/main/LICENSE.txt

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB

[React-url]: https://reactjs.org/

[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white

[Bootstrap-url]: https://getbootstrap.com

[Django.com]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white

[Django-url]: https://www.djangoproject.com/

[DjangoRestFramework.com]: https://img.shields.io/badge/DjangoRestFramework-A30000?style=for-the-badge&logoColor=white

[DjangoRestFramework-url]: https://www.django-rest-framework.org/

[OpenAPIGenerator.com]: https://img.shields.io/badge/OpenAPI_Generator-6BA539?style=for-the-badge&logo=openapiinitiative&logoColor=white

[OpenAPIGenerator-url]: https://openapi-generator.tech/

[Docker.com]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white

[Docker-url]: https://www.docker.com/

[Redis.com]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white

[Redis-url]: https://redis.io/

[PostgreSQL.com]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white

[PostgreSQL-url]: https://www.postgresql.org/

[Webpack.com]: https://img.shields.io/badge/Webpack-8DD6F9?style=for-the-badge&logo=webpack&logoColor=white

[Webpack-url]: https://webpack.js.org/
