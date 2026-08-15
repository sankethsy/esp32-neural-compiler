from parser import ModelParser
from optimizer import Quantizer, Optimizer
from memory_planner import MemoryPlanner
from code_generator import CodeGenerator

if __name__ == "__main__":
    print("Starting Hardware-Aware Neural Compiler...\n")
    
    # 1. Parse and Check
    parser = ModelParser()
    raw_graph = parser.parse_model()
    parser.check_fit(raw_graph)
    
    # 2. Quantize
    quantizer = Quantizer()
    quantized_graph = quantizer.run_pass(raw_graph)
    
    # 3. Fuse and Prune
    optimizer = Optimizer()
    optimized_graph = optimizer.run_pass(quantized_graph)
    
    # 4. Plan Memory
    planner = MemoryPlanner()
    planner.plan_memory(optimized_graph)
    
    # 5. Generate Code
    generator = CodeGenerator()
    generator.generate_c_header(optimized_graph)