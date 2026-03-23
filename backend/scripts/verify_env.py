import torch
import transformers
import peft
import bitsandbytes
import datasets
import accelerate
import sys

def check_env():
    print(f"Python Version: {sys.version}")
    print(f"PyTorch Version: {torch.__version__}")
    print(f"Transformers Version: {transformers.__version__}")
    print(f"PEFT Version: {peft.__version__}")
    print(f"BitsAndBytes Version: {bitsandbytes.__version__}")
    print(f"Datasets Version: {datasets.__version__}")
    print(f"Accelerate Version: {accelerate.__version__}")
    
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available: {cuda_available}")
    
    if cuda_available:
        print(f"CUDA Device Name: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Device Count: {torch.cuda.device_count()}")
        print(f"Current CUDA Device: {torch.cuda.current_device()}")
    else:
        print("WARNING: CUDA not found. QLoRA training will be extremely slow or impossible on CPU.")

    # Try a small bitsandbytes check if CUDA is available
    if cuda_available:
        try:
            import bitsandbytes.nn as bnb_nn
            print("BitsAndBytes for CUDA: SUCCESS")
        except Exception as e:
            print(f"BitsAndBytes for CUDA: FAILED - {e}")

if __name__ == "__main__":
    check_env()
