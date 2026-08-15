class Quantizer:
    def quantize_weights(self, weights):
        # Find the absolute maximum value to calculate the scale factor
        max_val = max(abs(min(weights)), abs(max(weights)))
        
        # int8 range is -128 to 127
        scale = max_val / 127.0 if max_val != 0 else 1.0
        
        quantized = []
        for w in weights:
            # Scale the float, round it, and cast to integer
            q_val = int(round(w / scale))
            # Clamp to int8 limits
            q_val = max(-128, min(127, q_val))
            quantized.append(q_val)
            
        return quantized, scale

    def run_pass(self, model_graph):
        print("--- Running Quantization Pass ---")
        for layer in model_graph:
            if "weights" in layer:
                q_weights, scale = self.quantize_weights(layer["weights"])
                layer["weights"] = q_weights
                layer["scale"] = scale
                print(f"Quantized {layer['type']} weights to: {q_weights}")
        print("Quantization complete.\n")
        return model_graph



class Optimizer:
    def run_pass(self, model_graph):
        print("--- Running Fusion & Pruning Pass ---")
        optimized_graph = []
        skip_next = 0
        
        for i in range(len(model_graph)):
            if skip_next > 0:
                skip_next -= 1
                continue
                
            current_layer = model_graph[i]
            
            # Pruning: Remove useless Multiply by 1
            if current_layer["type"] == "Multiply" and current_layer.get("value") == 1:
                print("Pruned: Useless Multiply by 1 removed.")
                continue
                
            # Layer Fusion: Look ahead for Conv2D -> BatchNorm -> ReLU
            if current_layer["type"] == "Conv2D" and i + 2 < len(model_graph):
                if model_graph[i+1]["type"] == "BatchNorm" and model_graph[i+2]["type"] == "ReLU":
                    print("Fused: Conv2D + BatchNorm + ReLU -> Fused_Conv2D")
                    # Create a new fused layer, keeping the weights
                    fused_layer = {
                        "type": "Fused_Conv2D",
                        "weights": current_layer["weights"],
                        "scale": current_layer.get("scale", 1.0)
                    }
                    optimized_graph.append(fused_layer)
                    skip_next = 2 # Skip the next two layers we just absorbed
                    continue
            
            optimized_graph.append(current_layer)
            
        print("Optimization complete.\n")
        return optimized_graph