Vagrant.configure("2") do |config|

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
  end
  config.vm.box = "ubuntu/bionic64"
  config.vm.synced_folder ".", "/app"
  config.vm.network "forwarded_port", guest: 4000, host:4000
  config.vm.network "forwarded_port", guest: 25565, host:25565
  config.vm.network "forwarded_port", guest: 25575, host:25575
  config.vm.provision "shell", run: "once", inline:<<-SCRIPT
    apt update
    apt install -y python3.8
    apt install -y python3-pip python3-dev build-essential python3-setuptools
    echo Installing venv...
    apt install -y python3.8-venv
    apt install -y openjdk-8-jre-headless
    python3.8 -m venv /app/.venv
    wget https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar
    cp /home/vagrant/server.jar /app
    echo Activating Virtual Environment
    source /app/.venv/bin/activate
    pip3 install flask
    pip3 install wheel
    pip3 install gunicorn
    pip3 install mcipc==2.3.1
    ufw allow 4000
    ufw allow 25565
    ufw allow 25575
    chmod +x /app/minecraft.sh
    chmod +x /app/flask.sh
    cp /app/minecraft.service /etc/systemd/system
    cp /app/flask.service /etc/systemd/system
    systemctl start minecraft
    systemctl enable minecraft
    systemctl start flask
    systemctl enable minecraft
    SCRIPT
end
