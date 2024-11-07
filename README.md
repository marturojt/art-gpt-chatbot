<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Telegram BOT demo</h3>

  <p align="center">
    Introducing your personalized AI-powered nutritional and health assistant! This virtual companion is here to support your wellness journey 24/7. Chat with her about your nutrition, fitness goals, and health concerns, and she'll provide expert advice and encouragement every step of the way. Rest assured, she prioritizes your privacy and security, ensuring your personal information remains confidential. Experience the incredible support she offers for your overall well-being today!
    <br />
    <br />
    <a href="https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot">View Demo</a>
    ·
    <a href="https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/issues">Report Bug</a>
    ·
    <a href="https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/issues">Request Feature</a>
  </p>
</div>

<div>
    <ul>
        <li><strong>AI-powered nutritional and health assistant:</strong> This bot harnesses the power of artificial intelligence, allowing it to continuously learn and evolve. By adapting to your preferences and behaviors over time, it becomes more adept at providing personalized nutritional and health guidance tailored to your needs.</li>
        <li><strong>Personalized and engaging:</strong> Designed to cater specifically to your wellness goals, this bot ensures every interaction is tailored to your unique requirements. It engages you with informative discussions on nutrition, exercise, and overall well-being, keeping you informed and motivated on your journey to better health.</li>
        <li><strong>Available 24/7:</strong> Whether it's early morning or late at night, this nutritional and health assistant is always at your service. Its round-the-clock availability ensures you have access to guidance and support whenever you need it, providing consistency in your pursuit of a healthier lifestyle</li>
        <li><strong>Secure and private:</strong> Your privacy and confidentiality are paramount. This bot operates within a secure environment, safeguarding your personal information as you engage in discussions about your health and wellness. Rest assured, your privacy is respected at all times, making it a trustworthy companion in your journey to improved health.</li>
    </ul>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Why the Project Exists:

We are developing an AI-powered companion focused on nutrition and health that is personalized, engaging, and available 24/7. Our aim is to create a supportive tool that can offer guidance, encouragement, and educational content to individuals seeking to improve their well-being.

The project is driven by the belief that everyone deserves access to reliable support and information regarding their health journey. Our nutritional and health assistant will be readily available to provide assistance whenever needed, offering valuable insights and practical advice.

Reasons for the Project:

- To provide guidance: Our nutritional and health assistant offers personalized guidance to individuals striving to make healthier choices. From meal planning to exercise routines, she provides tailored recommendations to support your wellness goals.
- To offer encouragement: Our nutritional and health assistant serves as a source of encouragement and motivation for those facing challenges on their wellness journey. Through positive reinforcement and empathy, she inspires individuals to stay committed to their health goals.
- To educate and inform: Our nutritional and health assistant delivers educational content and valuable insights on nutrition, fitness, and overall well-being. By sharing evidence-based information in an accessible manner, she empowers individuals to make informed decisions about their health.

We are confident that our nutritional and health assistant can make a meaningful difference in the lives of many individuals. We look forward to witnessing the positive impact she can have by fostering healthier habits and promoting well-being.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Python][Python.org]][Python-url]  
[![Love][LoveBadge]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get started with your Python Telegram bot project, you will need the following:

- A Telegram account
- A Telegram bot
- Knowledge in Python
- OpenAI API key
- MySQL server

There are a lot of examples and documentation about creating a bot using the bot father ([Botfather](https://t.me/botfather))

Once you have the telegram bot key and openai key, you need to copy the `config.ini.dist` file and fill the file with your API keys. The connection info for MySQL server needs to be in this file too.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot
   ```
2. Create a python virtual enviroment
   ```sh
   python -m venv .venv_bot
   ```
3. Activate the virtual env (command depents on OS)
   ```sh
   source .venv_bot/bin/activate
   ```
4. Install python packages
   ```sh
   pip install -r pip_install.txt
   ```
5. Copy `config.ini.dist` to `config.ini` and enter your api keys and the database credentials

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Create a basic bot
- [x] Set conversation history
- [x] Add the capability to send photos
- [ ] Add the capability to send audios
- [ ] Multi-language Support
    - [ ] English
    - [x] Spanish


See the [open issues](https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

- Arturo Jiménez - arturo.jimenez@grupocsi.com

GPTDemoChatbot: [https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot](https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Buzz-Word-Comunicacion/gpt-demo-chatbot?style=for-the-badge
[contributors-url]: https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Buzz-Word-Comunicacion/gpt-demo-chatbot?style=for-the-badge
[forks-url]: https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/network/members
[stars-shield]: https://img.shields.io/github/stars/Buzz-Word-Comunicacion/gpt-demo-chatbot?style=for-the-badge
[stars-url]: https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/stargazers
[issues-shield]: https://img.shields.io/github/issues/Buzz-Word-Comunicacion/gpt-demo-chatbot?style=for-the-badge
[issues-url]: https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/issues
[license-shield]: https://img.shields.io/github/license/Buzz-Word-Comunicacion/gpt-demo-chatbot?style=for-the-badge
[license-url]: https://github.com/Buzz-Word-Comunicacion/gpt-demo-chatbot/blob/dev/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/marturojt
[product-screenshot]: images/screenshot.jpg
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[LoveBadge]: https://img.shields.io/static/v1?label=❤️&message=Love&style=for-the-badge&color=red
[Love-url]: https://freejolitos.com
