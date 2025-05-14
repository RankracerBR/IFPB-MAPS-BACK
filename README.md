## Documentação do Projeto

## Orientações

- Ambiente em Linux
- Instalação dos pacotes(libs)
- Como rodar o projeto

## Ambiente em Linux

- Primeiro de tudo, é importante baixar o WSL2 na sua máquina para rodar o projeto, e em seguida configurar uma chave SSH para fazer git clone do projeto e assim enviar alterações, aqui estão alguns tutoriais que podem ajudar você a fazer isso:

- https://documentation.ubuntu.com/wsl/en/latest/howto/install-ubuntu-wsl2/

- https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04-pt


## Instalação dos pacotes(libs)

- Antes de mais nada, é importante que você tenha duas coisas instaladas: Python e Docker
aqui estão alguns comandos para instalação de ambos:

- Docker
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

- Python

```bash
sudo apt install python3.12
```

## Como rodar o projeto