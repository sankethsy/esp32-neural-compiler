class MemoryPlanner:
    def plan_memory(self, optimized_graph):
        print("--- Running Memory Planning Pass ---")
        # In a real compiler, you calculate input/output tensor sizes.
        # Here we simulate the max memory needed for the largest fused layer.
        
        # Assigning a flat 150KB for the Fused layer, 100KB for Dense
        for layer in optimized_graph:
            if layer["type"] == "Fused_Conv2D":
                layer["ram_needed"] = 150000 
            elif layer["type"] == "Dense":
                layer["ram_needed"] = 100000

        # Memory Reuse: We only need enough RAM for the largest single layer execution
        peak_ram = max(layer["ram_needed"] for layer in optimized_graph)
        
        print(f"Memory Planned! By reusing buffers, peak RAM dropped to: {peak_ram} bytes.")
        print("Memory planning complete.\n")
        return peak_ram