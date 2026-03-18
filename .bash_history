git git config --global user.name "JorgeCaballeroHSU"
git config --global user.name "JorgeCaballeroHSU"
git config --global user.email "JorgeCaballeroHSU"
git config --global user.email "caballej@hsu-hh.de"
python3 - venv .venv
python3 -m  venv .venv
source .venv/bin/activate
clear
source .venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
 /usr/bin/env /home/computer_vision/.venv/bin/python /home/computer_vision/.vscode-server/extensions/ms-python.debugpy-2025.18.0-linux-x64/bundled/libs/debugpy/adapter/../../debugpy/launcher 57877 -- /home/computer_vision/main.py 
 cd /home/computer_vision ; /usr/bin/env /home/computer_vision/.venv/bin/python /home/computer_vision/.vscode-server/extensions/ms-python.debugpy-2025.18.0-linux-x64/bundled/libs/debugpy/adapter/../../debugpy/launcher 36873 -- /home/computer_vision/main.py 
pip install --upgrade keras
conda create -y -n keras-jax python=3.11
pip install -r requirements-jax-cuda.txt
python3 -m pip install tensorflow[and-cuda]
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
nvidia-smi
pip install --upgrade pip
# For GPU users
pip install tensorflow[and-cuda]
# For CPU users
pip install tensorflow
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
sudo apt update
sudo apt install nvidia-cuda-toolkit
# For GPU users
pip install tensorflow[and-cuda]
# For CPU users
pip install tensorflow
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
pip install tensorflow==2.14.1  # TensorFlow >=2.14 has GPU support in WSL
pip install tensorflow==2.14.1
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
 source /home/computer_vision/.venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
nvidia-smi
pip install --upgrade pip
pip install tensorflow[and-cuda]
python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
sudo apt update
sudo apt install nvidia-cuda-toolkit
pip install tensorflow==2.14.1
pip install tensorflow
python3 -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices('GPU'))"
sudo apt update
sudo apt install nvidia-cuda-toolkit
pip install tensorflow
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
pip unisntall tensorflow
pip uninstall tensorflow
pip uninstall keras
pip install tensorflow[and-cuda]
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
nvidia-smi
sudo apt update
sudo apt install -y build-essential
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"
sudo apt update
sudo apt install -y cuda-toolkit-13-0
source .venv/bin/activate
pip install --upgrade pip
pip install tensorflow
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python3 -c "import tensorflow as tf; print(tf.sysconfig.get_build_info())"
sudo apt remove --purge cuda-13-0
sudo apt autoremove
pip install --upgrade tf-nightly
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
apt list cuda-toolkit --all-versions
sudo apt-get install cuda-toolkit-12-5 -y
echo 'export PATH=/usr/local/cuda-12.5/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.5/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
nvcc --version
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
pip install keras
export TF_CPP_MIN_LOG_LEVEL=2
 source /home/computer_vision/.venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
git config pull.rebase false
 source /home/computer_vision/.venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
 source /home/computer_vision/.venv/bin/activate
