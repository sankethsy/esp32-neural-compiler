class CodeGenerator:
    def generate_c_header(self, optimized_graph, filename="model_data.h"):
        print("--- Generating C Header ---")
        c_code = "#ifndef MODEL_DATA_H\n#define MODEL_DATA_H\n\n#include <stdint.h>\n\n"
        
        for i, layer in enumerate(optimized_graph):
            if "weights" in layer:
                weights = layer["weights"]
                # Format array for C
                array_str = ", ".join(map(str, weights))
                c_code += f"// {layer['type']} Weights\n"
                c_code += f"const int8_t layer_{i}_weights[{len(weights)}] = {{{array_str}}};\n\n"
                
        c_code += "#endif // MODEL_DATA_H\n"
        
        # In a real scenario, you would write this to a file:
        # with open(filename, "w") as f: f.write(c_code)
        
        print(f"Generated {filename}:\n")
        print(c_code)