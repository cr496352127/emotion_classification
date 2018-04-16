from utils.config_utils import get_config_from_json
from torch.utils.data import DataLoader
from torch.nn import CrossEntropyLoss
from model import SimpleLSTM
from trainer import AudioTrainer
from logger import AudioLogger
from torch.optim import Adam
from data import AudioData

# This import must be maintained in order for script to work on paperspace
from os import path

# Any parameters that may change from run-to-run
RUN_CONFIG_FILE = "config_1.json"

# Run Configs
model_configs, _ = get_config_from_json(path.join('./configs', RUN_CONFIG_FILE))

# Data
audio_data = AudioData(configs=model_configs)
train_loader = DataLoader(dataset=audio_data, batch_size=model_configs.batch_size, shuffle=True, num_workers=4)

# Model
audio_model = SimpleLSTM(model_configs=model_configs)
audio_model.cuda()

# Training Params
loss_fn = CrossEntropyLoss()
optimizer = Adam(audio_model.parameters(), lr=model_configs.learning_rate)

# Logger
logger = AudioLogger("./run.json")

# Train Model
trainer = AudioTrainer(model_configs, audio_model, train_loader, loss_fn, optimizer, logger,
                       save_path="./models/new_model2.pt")
trainer.train()
