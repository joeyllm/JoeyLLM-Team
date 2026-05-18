"""
JoeyLLM DDP Training Simulation Script
---------------------------------------
Launched by the notebook via:
    torchrun --nproc_per_node=<N> ddp_training_simulation.py

This script simulates the DDP training loop that will later be used for
full-scale JoeyLLM training on the 5B-token Australian dataset.
It uses a tiny toy language model and a randomly generated dataset so it
can be verified on any machine with or without multiple GPUs.
"""

import os
import time
import math
import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler


# ── Hyperparameters (toy scale) ──────────────────────────────────────────────

VOCAB_SIZE      = 1_000
EMBED_DIM       = 128
N_HEADS         = 4
N_LAYERS        = 2
SEQ_LEN         = 64
BATCH_SIZE      = 16          # per GPU
TRAINING_STEPS  = 20
LR              = 3e-4
CHECKPOINT_DIR  = "./checkpoints"


# ── Tiny toy dataset ─────────────────────────────────────────────────────────

class ToyTextDataset(Dataset):
    """
    Generates random token-ID sequences that mimic the shape of a real
    language-modelling dataset.  Each item is (input_ids, labels) where
    labels = input_ids shifted left by one (next-token prediction).
    """
    def __init__(self, n_samples: int = 2_000):
        torch.manual_seed(42)
        self.data = torch.randint(0, VOCAB_SIZE, (n_samples, SEQ_LEN + 1))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        tokens = self.data[idx]
        return tokens[:-1], tokens[1:]   # input_ids, labels


# ── Toy Transformer language model ───────────────────────────────────────────

class ToyLanguageModel(nn.Module):
    """
    Embedding + N × TransformerEncoderLayer + Linear LM head.
    Intentionally small so it fits on any GPU or even CPU.

    Later this will be replaced by the real JoeyLLM architecture
    (decoder-only Transformer, ~2B parameters).
    """
    def __init__(self):
        super().__init__()
        self.embed   = nn.Embedding(VOCAB_SIZE, EMBED_DIM)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=EMBED_DIM, nhead=N_HEADS,
            dim_feedforward=EMBED_DIM * 4,
            dropout=0.1, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=N_LAYERS)
        self.lm_head = nn.Linear(EMBED_DIM, VOCAB_SIZE, bias=False)
        # Weight tying: lm_head shares weights with embedding (standard LM practice)
        self.lm_head.weight = self.embed.weight

    def forward(self, x):
        # x: (batch, seq_len)
        h = self.embed(x)                          # (B, S, D)
        h = self.transformer(h)                    # (B, S, D)
        logits = self.lm_head(h)                   # (B, S, V)
        return logits


# ── Main training loop ────────────────────────────────────────────────────────

def main():
    # ── 1. Initialise the process group ──────────────────────────────────────
    dist.init_process_group(backend="nccl" if torch.cuda.is_available() else "gloo")

    rank       = dist.get_rank()
    world_size = dist.get_world_size()
    local_rank = int(os.environ.get("LOCAL_RANK", 0))

    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")

    if rank == 0:
        print(f"\n{'='*55}")
        print(f"  JoeyLLM DDP Training Simulation")
        print(f"{'='*55}")
        print(f"  PyTorch  : {torch.__version__}")
        print(f"  CUDA     : {torch.cuda.is_available()}")
        print(f"  GPUs     : {torch.cuda.device_count()}")
        print(f"  World    : {world_size} process(es)")
        print(f"{'='*55}\n")

    print(f"  [Rank {rank}/{world_size}] started on device {device}")
    dist.barrier()

    # ── 2. Dataset + DistributedSampler ──────────────────────────────────────
    dataset = ToyTextDataset(n_samples=2_000)
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank, shuffle=True)
    loader  = DataLoader(dataset, batch_size=BATCH_SIZE, sampler=sampler, pin_memory=True)

    # ── 3. Model + DDP wrapper ────────────────────────────────────────────────
    model = ToyLanguageModel().to(device)
    model = DDP(model, device_ids=[local_rank] if torch.cuda.is_available() else None)

    # ── 4. Optimiser + loss ───────────────────────────────────────────────────
    optimizer  = torch.optim.AdamW(model.parameters(), lr=LR)
    loss_fn    = nn.CrossEntropyLoss()

    # ── 5. Training loop ──────────────────────────────────────────────────────
    model.train()
    step       = 0
    epoch      = 0
    start_time = time.time()

    while step < TRAINING_STEPS:
        sampler.set_epoch(epoch)
        for input_ids, labels in loader:
            if step >= TRAINING_STEPS:
                break

            input_ids = input_ids.to(device)
            labels    = labels.to(device)

            optimizer.zero_grad()
            logits = model(input_ids)               # (B, S, V)
            # Reshape for cross-entropy: (B*S, V) vs (B*S,)
            loss = loss_fn(logits.reshape(-1, VOCAB_SIZE), labels.reshape(-1))
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            if rank == 0:
                perplexity = math.exp(min(loss.item(), 20))
                elapsed    = time.time() - start_time
                print(
                    f"  Step {step+1:>3}/{TRAINING_STEPS}"
                    f"  |  Loss: {loss.item():.4f}"
                    f"  |  PPL: {perplexity:.2f}"
                    f"  |  Elapsed: {elapsed:.1f}s"
                )

            step += 1

        epoch += 1

    dist.barrier()

    # ── 6. Save checkpoint (rank 0 only) ──────────────────────────────────────
    if rank == 0:
        os.makedirs(CHECKPOINT_DIR, exist_ok=True)
        ckpt_path = os.path.join(CHECKPOINT_DIR, "ddp_simulation.pt")
        torch.save({
            "step":        step,
            "world_size":  world_size,
            "model_state": model.module.state_dict(),   # unwrap DDP wrapper
            "optim_state": optimizer.state_dict(),
            "loss":        loss.item(),
        }, ckpt_path)
        print(f"\n  Checkpoint saved → {ckpt_path}")
        print(f"\n{'='*55}")
        print(f"  Simulation complete.  {step} steps in {time.time()-start_time:.1f}s")
        print(f"{'='*55}\n")

    dist.destroy_process_group()


if __name__ == "__main__":
    main()
