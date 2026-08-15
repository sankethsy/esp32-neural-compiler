class ModelParser:
    def __init__(self, esp32_ram_kb=520):
        self.esp32_ram = esp32_ram_kb * 1024 # Convert to bytes
        
    def parse_model(self):
        # Simulated unoptimized input model graph
        return [
            {"type": "Conv2D", "weights": [0.154, -0.223, 0.981, 0.001], "ram_needed": 300000},
            {"type": "BatchNorm", "ram_needed": 100000},
            {"type": "ReLU", "ram_needed": 100000},
            {"type": "Multiply", "value": 1, "ram_needed": 50000}, # Useless operation
            {"type": "Dense", "weights": [0.55, -0.11], "ram_needed": 200000}
        ]

    def check_fit(self, model_graph):
        total_ram = sum(layer["ram_needed"] for layer in model_graph)
        print(f"Total RAM needed: {total_ram} bytes")
        
        if total_ram > self.esp32_ram:
            print(f"Warning: Model requires {total_ram} bytes, but ESP32 only has {self.esp32_ram} bytes!")
            print("Beginning optimization passes...\n")
        return total_ram