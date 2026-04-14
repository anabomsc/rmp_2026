# Robótica Movel Probabilística - UFMA
Introdução ao ROS 2 Humble, Gazebo Fortress e SLAM para a disciplina Robotótica Móvel Probabilística da Universidade Federal do Maranhão

Autora: Ana Beatriz O. M. S. Costa

Data: 12/04/2026

## Resumo dos Diretórios
* `config` - contém arquivos de configuração utilizados por pacotes e ferramentas
* `description` - contém arquivos de descrição utilizados para simulação de sistemas e outros
* `env-hooks` - contém arquivos de gancho necessários para definir variáveis do Gazebo
* `launch` - contém arquivos de launch do ROS
* `worlds` - contém arquivos de simulação de sistema do Gazebo

## Instalar Requisitos
### Instalação do ROS 2 Humble
Fonte: [ROS 2 Documentation - Installation](https://docs.ros.org/en/humble/Installation.html)

1. Configurar localidade (recomendado)

  ```shell
  locale  # check for UTF-8
  
  sudo apt update && sudo apt install locales
  sudo locale-gen en_US en_US.UTF-8
  sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
  export LANG=en_US.UTF-8
  
  locale  # verify settings
  ```

2. Configurar fontes

  - Habilitar repositório Ubuntu Universe
  ```shell
  sudo apt install software-properties-common
  sudo add-apt-repository universe
  ```
  
  - Instalar pacote ros2-apt-source
  ```shell
  sudo apt update && sudo apt install curl -y
  export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
  curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
  sudo dpkg -i /tmp/ros2-apt-source.deb
  ```

3. Instalar pacotes ROS 2

  - Atualizar sistema Ubuntu
  ```shell
  sudo apt update
  sudo apt upgrade
  ```
  > [!CAUTION]
  > Instalar as dependências de ROS 2 em um sistema recém-instalado sem realizar o upgrade pode causar a remoção de pacotes críticos do sistema  
  
  - Instalar ROS 2 para desktop
  ```shell
  sudo apt install ros-humble-desktop
  ```
  
  - Instalar ferramentas de desenvolvimento
  ```shell
  sudo apt install ros-dev-tools
  ```

4. Automatizar source setup.bash
  ```shell
  echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
  ```

### Instalação do Gazebo Fortress
Fonte: [Gazebo Fortress Docs - Installing Gazebo with ROS](https://gazebosim.org/docs/fortress/ros_installation/)

  - Instalar o par Gazebo/ROS recomendado para ROS 2 Humble
  ```shell
  sudo apt-get install ros-humble-ros-gz
  ```

### Instalação do pacote SLAM Toolbox
Fonte: [Slam Toolbox](https://github.com/SteveMacenski/slam_toolbox)

  - Instalar a versão do pacote para ROS 2 Humble
  ```shell
  sudo apt install ros-humble-slam-toolbox
  ```

### Instalação do pacote Nav2
Fonte: [NAV2 - Getting Started - Installation](https://docs.nav2.org/getting_started/index.html#installation)

  - Instalar a versão do pacote para ROS 2 Humble
  ```shell
  sudo apt install ros-humble-navigation2
  sudo apt install ros-humble-nav2-bringup
  ```

## Uso do Pacote

1. Crie um workspace
  ```shell
  mkdir -p ~/rmp_ws/src
  cd ~/rmp_ws/src
  ```

2. Clone o repositório
  ```shell
  git clone https://github.com/anabomsc/rmp_2026.git
  ```

3. Construa o pacote
  ```shell
  cd ~/rmp_ws
  colcon build --packages-select rmp_2026
  ```
4. Source o workspace
  - Abra um novo terminal
  ```shell
  source install/setup.bash
  ```
  > [!WARNING]
  > Antes de fazer o source do overlay criado (rmp_ws), é extremamente importante que um novo terminal seja aberto e que o comando de source seja executado nesse terminal separado. Realizar o source do overlay no mesmo terminal onde foi feita a construção pode causar problemas complexos. 

5. Launch!
  ```shell
  ros2 launch rmp_2026 ${LAUNCH_FILE}.launch.py
  ```
